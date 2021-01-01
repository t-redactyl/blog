---
title: Finding your new favourite Christmas recipe using NLP  
date: 2020-12-24  
comments: false  
tags: nlp, machine learning  
keywords: python, data science, aws, sagemaker, s3, pyspark, blazingtext, word2vec, w2v, nlp
---

With a full coronavirus shutdown in Germany, Christmas this year in Berlin will be very quiet. I have been keeping myself entertained for the last couple of weeks by watching old seasons of [The Great British Bakeoff](https://thegreatbritishbakeoff.co.uk/), so between that and the mountain of Christmas baking I've been doing, I felt rather inspired revisit my old tradition of making a Christmas-themed blog post. 

In this post, I will build a simple word2vec model from a dataset of BBC Good Food Christmas recipes, kindly scraped and posted to Kaggle by [Gary Broughton](https://www.kaggle.com/gjbroughton/christmas-recipes). We will then use this model to find the most similar recipes to one we might like to cook from the dataset, in order to recommend other things we could cook.

## Reading in and cleaning the data

Let's first load in the dataset, as well as import our dependencies.


```python
import ujson as json
import pandas as pd
from nltk import tokenize
import csv
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

records = map(json.loads, open('christmas_and_ny_2020/christmas_data/recipes.json'))
df = pd.DataFrame.from_records(records)
```

I want to train this dataset in such a way that I link the semantic information contained in recipes and the recipe titles together. As such, we're going to include each recipe name in the training dataset. However, we want to make sure that our recipe names are different to the rest of the model vocabulary. The easiest way to do so is to use an ID label that is distinct from anything in the vocabulary, instead of using the title itself. In this case, we're going to convert the rest of the training data to lowercase, so we can use the word "recipe" in uppercase, plus a number (e.g., `RECIPE1`).


```python
# Create unique recipe marker
df["recipe_tag"] = [f"RECIPE{i}" for i in range(len(df))]
```

We now need to decide which text we're going to use to train our model. I decided that the ingredients and methods columns contain the most relevant information. However, as the sentences from the ingredients section and those from the methods sections are such different lengths, this might cause some issues when setting the word2vec window size. For example, a sentence in the ingredients section might be "2kg turkey", compared to "Thoroughly wash the carrots and then cut them into small pieces." in the methods section. As such, I decided to combine all of the ingredients for a recipe into one sentence. 

I felt that the measurements in the ingredients column just added noise to this model, so I compiled a manual list of all of the measurement terms I could see and cleansed them out of the ingredients list. I also removed all of the numbers, converted all characters to lowercase, and removed any extra whitespace.

Once the cleaning was done, I merged the `recipe_tag` column created above with the cleaned ingredients sentences, making it the first "word" in each training sentence we will feed to our word2vec model.


```python
# Create sentences with ingredients
measurements = ["g", "tbsp", "tsp", "cup", "cups", "knob", "ml", "pack", "oz", "fl oz", "bunch", 
                "bag", "sprigs", "l", "pinch", "box", "kg", ]

df["ingredients_joined"] = df["Ingredients"].map(lambda x: " ".join(x))
df["ingredients_joined"] = (df["ingredients_joined"]
                            .str.lower()
                            .str.replace('[^a-zA-Z]', ' ')
                            .str.replace(r"\b({})\b".format("|".join(measurements)), " ")
                            .str.replace("\s+", " ")
                            .str.strip()
                           )

# # Create final column for output
df["training_sentences"] = df["recipe_tag"] + " " + df["ingredients_joined"]
ingredient_df = df[["training_sentences"]]
```

For the methods section, I first exploded out each list into a separate row. I then checked if there were still multiple sentences per row, and if so, used `nltk`'s `sent_tokenize` to split them. I then exploded these split paragraphs one last time, so every sentence was in its own row.

I then applied the same cleaning and normalisation steps to the methods data as I had for the ingredients data above, as well as merging the sentences with the `recipe_tag`.


```python
# Create sentences with methods
method_df = df[["recipe_tag", "Method"]]
method_df = method_df.explode("Method")
method_df["Method"] = method_df["Method"].map(lambda p: tokenize.sent_tokenize(str(p)))
method_df = method_df.explode("Method")

method_df["Method"] = (
    method_df["Method"]
    .str.lower()
    .str.replace("[^a-zA-Z]", " ")
    .str.replace("\s+", " ")
    .str.strip()
)

# Create final column for output
method_df["training_sentences"] = method_df["recipe_tag"] + " " + method_df["Method"]
method_df = method_df[["training_sentences"]]
```

Let's check how long each sentence is in the ingredients and methods datasets.


```python
print("Average number of tokens in a sentence (ingredients): {}".format(
    ingredient_df["training_sentences"].map(lambda s: len(str(s).split(" "))).median()
))

print("Average number of tokens in a sentence (methods): {}".format(
    method_df["training_sentences"].map(lambda s: len(str(s).split(" "))).median()
))
```

    Average number of tokens in a sentence (ingredients): 32.0
    Average number of tokens in a sentence (methods): 15.0


We can see that the sentences in the ingredients dataset are around twice as long as those in the methods dataset, so we haven't quite resolved our sentence length issue, but we can play with this by testing different window size parameters.

Let's combine our two datasets and have a look at how big our final dataset is.


```python
all_sentences = ingredient_df.append(method_df)

print(f"Number of sentences (ingredients only): {len(ingredient_df)}") 
print(f"Number of sentences (methods only): {len(method_df)}")
print(f"Number of sentences (ingredients and methods): {len(all_sentences)}") 
```

    Number of sentences (ingredients only): 1617
    Number of sentences (methods only): 20036
    Number of sentences (ingredients and methods): 21653


We can see our training data is a tiny 21,653 sentences, which is definitely not enough data to train a good-quality word2vec model. Short of sourcing another model with publically available weights for transfer learning, or sourcing more data, we could try `gensim`'s `intersect_word2vec_format` method. [This method](https://tedboy.github.io/nlps/generated/generated/gensim.models.Word2Vec.intersect_word2vec_format.html) allows us to load in a pretrained model that has been trained on a much larger corpus, and replace our weaker vectors with those from the pretrained model when the vocabularies overlap. Let's see how we go.

We first prepare our data for training. We need to convert the rows of our `training_sentences` column into a list of lists. The data also contained a number of `nan`s, so I removed them by keeping only rows which were of type `list`.


```python
# Convert sentences into list of lists for training
all_sentences_training = all_sentences["training_sentences"].str.split("\s").to_list()

# Remove nans
all_sentences_training = [s for s in all_sentences_training if type(s) is list]
```

## Training the model

Let's now train a model on our data. I didn't do any formal hyperparameter tuning, but from eyeballing the results I seemed to get the best neighbours with a window size of 20 and a minimum vocabulary count of 5 (which is quite high in this small dataset). As the pretrained model that I want to inject into my model has 300 dimensions, I have to use the same number in order for them to merge correctly.


```python
all_sentences_model = Word2Vec(sentences=all_sentences_training, size=300, window=20, 
                               min_count=5, workers=4)
```

Now let's load and inject in our pretrained model. We'll use the [Google News model](https://code.google.com/archive/p/word2vec/).


```python
filename = 'christmas_and_ny_2020/christmas_data/GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)

all_sentences_model.intersect_word2vec_format(filename, binary=True)
```

And that's it! As usual, the data cleaning and preparation took up most of our time, with just a few lines to train the models themselves.

## Testing the model out

Let's test out the model with a few recipes. We'll first create a function to restrict the list of neighbours to just recipes, and then merge these recipe IDs with their titles and descriptions.


```python
def retrieve_top_recipes(recipe_id: str, topn: int) -> None:
    """
    Gets the top 50 neighbours for a query, filters the neighbours list to only recipe IDs
    and merges the IDs with their name and description.
    """

    nbrs = all_sentences_model.wv.most_similar(recipe_id, topn = 50)
    recipe_nbrs = pd.DataFrame([r for r in nbrs if r[0].startswith("R")], 
                               columns = ["recipe_tag", "cs"])
    desc_nbrs = pd.merge(recipe_nbrs[recipe_nbrs["cs"] >= 0.7], 
                         df[["Name", "Description", "recipe_tag"]], 
                         on = "recipe_tag")


    name = df.loc[df["recipe_tag"] == recipe_id, "Name"].values[0]
    description = df.loc[df["recipe_tag"] == recipe_id, "Description"].values[0]
    print(f"REFERENCE RECIPE:\n{name}\n{description}")
    
    print("\nCLOSELY RELATED RECIPES:")
    for index, row in desc_nbrs[:topn].iterrows():
        print(f"{row['Name']}\n{row['Description']}\n" )
```

Let's first consider what we can make for our main meal at Christmas. Let's see what is similar to `RECIPE1613`, "Crispy Roast Duck":


```python
retrieve_top_recipes("RECIPE1613", 5)
```

    REFERENCE RECIPE:
    Crispy Roast Duck
    Duck basted to perfection, ideal for a Sunday lunch or special occasion
    
    CLOSELY RELATED RECIPES:
    Marmalade glazed roast duck
    it's Areet looking actually just doesn't taste very good.
    
    Chestnut & wild mushroom stuffed three-bird roast
    You'll need a little skill and patience to pull off this elegant multi-bird roast of chicken, pheasant and duck, but there's no other main course quite like it
    
    Easy coq au vin
    Didn't look like the picture at all but it was delicious!
    
    Game terrine
    John Torode shows how to prepare classic coarse set terrine with duck and mixed game of your choice
    
    Sticky treacle-glazed ham
    James uses the steam-roast method to cook his Christmas ham, so you don't need an enormous pan to boil it in
    


Not bad! We have a number of other poultry and then meat dishes recommended.

What about dessert? What else could we have other than `RECIPE25`, "Classic Christmas pudding"?


```python
retrieve_top_recipes("RECIPE21", 5)
```

    REFERENCE RECIPE:
    Easy Christmas pudding
    So are all the cups the same size as the butter cup? Specifying cup size would be helpful. Thanks
    
    CLOSELY RELATED RECIPES:
    Honey saffron Christmas cake
    Has all the flavours of Christmas without being too heavy and can be made at the last minute too
    
    Christmas morning spiced bread
    This festive bread can be made ahead and frozen and makes a lovely treat for breakfast on Christmas morning
    
    Gingery Christmas cake
    A good glug of ginger wine makes this cake a little different from the norm. It's also lighter than its predecessors, so you can have two pieces!
    
    Christmas pudding with citrus & spice
    A fruity pud, served with orange custard cream, makes the perfect end to the traditional Christmas meal
    
    Granny Cook's Christmas pud
    If you prefer a lighter, fruity Christmas pudding, share Sarah Cook's family recipe, which makes three sizes of pud
    


We're getting some interesting recommendations, including some alternative Christmas pudding ideas, as well as other desserts.

What about snacks? Let's see what is similar to `RECIPE11`, Mary Berry's Christmas chutney.


```python
retrieve_top_recipes("RECIPE11", 5)
```

    REFERENCE RECIPE:
    Mary Berry's Christmas chutney
    A perfect match for cheese and cold meats, and delicious in turkey sandwiches
    
    CLOSELY RELATED RECIPES:
    Courgette & tomato chutney
    A chunky and vibrant homemade pickle flavoured with yellow mustard seeds- keep as an accompaniment or present as a gift
    
    Granny Cook's Christmas pud
    If you prefer a lighter, fruity Christmas pudding, share Sarah Cook's family recipe, which makes three sizes of pud
    
    Christmas spiced red cabbage
    This classic side can be made up to two days in advance. For maximum flavour, cook the cabbage down really well over a low heat until it's really sticky
    
    Best ever roast potatoes
    This recipe is very similar to the way I've been roasting potatoes for some years. I don't place them in the fridge once boiled but return them to the empty pan over a low heat and steam them off for a few minutes whilst moving them around with a wooden spatula. This in an effort to remove as much water as possible. It seems to me that water is the sworn enemy of crusty roast potatoes. Then roast for perhaps just under the hour but take a look after 35 minutes. I agree on the Maris Pipers....
    


We can see the results here are (mostly) in some way related to the original chutney we were searching for, but are much less focused than what we were getting for the duck and pudding recipes. Due to the small size of the model, even with the enrichment from the Google pretrained model there were still issues with quality.

So that's it! I hope you enjoyed this little exercise in using NLP to get some ideas for Christmas cooking. Have a great Christmas, stay safe, and eat well!