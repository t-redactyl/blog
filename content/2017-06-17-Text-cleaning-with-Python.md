---
title: Text cleaning in multiple languages
date: 2017-06-17
comments: false
tags: python, programming tips, text mining
keywords: python, data science, text mining, machine learning
---

One of the most basic (and most important) tasks when doing text mining is cleaning up your text. While this might seem a bit dull compared to sexy stuff like sentiment analysis and topic modelling, I hope to show you in this post that not only is this pretty straightforward with the right Python packages, it can also help you to get to know your data before you get stuck into modelling.

In this post, my ultimate aim of cleaning is to transform text from sentences into a standardised [bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model) for further analysis, but you can pick and choose from these methods to get your text into the format most suitable for you. To demonstrate the flexibility of these packages, I'll show you how we can process both English and Spanish texts (and by extension a few other common languages) using similar methods.

## Our example texts

For our example texts, let's use some famous opening lines from both English and Spanish novels. On the English side, we have 'Pride and Prejudice' by Jane Austen, 'The Making of Americans' by Gertrude Stein, 'The Old Man and the Sea' by Ernest Hemingway, and 'Adventures of Huckleberry Finn' by Mark Twain. On the Spanish side, we have 'Don Quixote' by Miguel de Cervantes, 'Cien años de soledad' ('One Hundred Years of Solitude') by Gabriel García Márquez, 'El túnel' ('The Tunnel') by Ernesto Sábato, and 'La familia de Pascual Duarte' ('The Family of Pascual Duarte') by Camilo José Cela.


```python
# English texts
engTexts = [u'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.',
            u'Once an angry man dragged his father along the ground through his own orchard. "Stop!" cried the groaning old man at last, "Stop! I did not drag my father beyond this tree."',
            u'He was an old man who fished alone in a skiff in the Gulf Stream and he had gone eighty-four days now without taking a fish.',
            u'You don\'t know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain\'t no matter.']
```


```python
# Spanish texts
espTexts = [u'En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no hace mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor.',
            u'Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo.',
            u'Bastará decir que soy Juan Pablo Castel, el pintor que mató a María Iribarne; supongo que el proceso está en el recuerdo de todos y que no se necesitan mayores explicaciones sobre mi persona.',
            u'Yo, señor, no soy malo, aunque no me faltarían motivos para serlo.']
```

## Expanding contractions

In English, it is pretty common for us to use contractions of words, such as isn't, you're and should've. However, these contractions cause all sorts of problems for normalisation and standardisation algorithms (which we'll speak about more later in this post). As such, it is best to get rid of them, and the easiest way to do so expand all of these contractions prior to further cleaning steps.

An easy way of doing this is to simply find the contractions and replace them with their full form. [This gist](https://gist.github.com/nealrs/96342d8231b75cf4bb82) has a nice little function, `expandContractions()`, that does just that. In the below code I am using an [updated function](https://gist.github.com/t-redactyl/aff518d750f47f0ef6c20f04ef6fb823) where I've included `text.lower()` (as suggested by a user on the original post) to make sure words at the start of a sentence are included. Let's try it on our fourth English sentence, which has a number of contractions:


```python
expandContractions(engTexts[3])
```




    u'you do not know about me without you have read a book by the name of the adventures of tom sawyer; but that am not no matter.'



It's a bit grammatically incorrect, but you'll see later in this post that this is not very important for what we're trying to do. Let's go ahead and replace this sentence:


```python
engTexts[3] = expandContractions(engTexts[3])

from pprint import pprint
pprint(engTexts)
```

    [u'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.',
     u'Once an angry man dragged his father along the ground through his own orchard. "Stop!" cried the groaning old man at last, "Stop! I did not drag my father beyond this tree."',
     u'He was an old man who fished alone in a skiff in the Gulf Stream and he had gone eighty-four days now without taking a fish.',
     u'you do not know about me without you have read a book by the name of the adventures of tom sawyer; but that am not no matter.']


## Standardising your signal words

Bag-of-words analyses rely on getting the frequency of all of the 'signal' words in a piece of text, or those that are likely to characterise what the piece of text is about. For example, in the opening lines to *Pride and Prejudice* words such as 'man', 'fortune' and 'wife' give a pretty good idea of what the sentence is about. As you might guess, these frequencies rely on these signal words being in the exact same format. However, the same word often has different representations depending on the context. The word 'camp', for example, can be 'camped', 'camps' and 'camping', but these words all ultimately mean the same thing and should be grouped together in a bag-of-words analysis.

One way of addressing this is [stemming](https://en.wikipedia.org/wiki/Stemming). Stemming is where you strip words back to a base form that is common to related words, even if that is not the actual grammatical root of the word. For example, 'judging' would be stripped back to 'judg', although the actual correct root is 'judge'.

As we're interested in processing both English and Spanish texts, we'll use the [Snowball stemmer](http://snowballstem.org/) from Python's NLTK. This stemmer has support for a [wide variety of languages](http://snowballstem.org/algorithms/), including French, Italian, German, Dutch, Swedish, Russian and Finnish.

Let's import the package, and assign the English and Spanish stemmers to different variables.


```python
from nltk.stem.snowball import SnowballStemmer

sbEng = SnowballStemmer('english')
sbEsp = SnowballStemmer('spanish')
```

To run the stemmers over our sentences, we need to split the sentences into a list of words and run the stemmer over each of the words. We still want to do some more processing, so we'll join them back into a sentence with the `join()` function for now, but we will eventually tokenise these when we're happy with our cleaning.


```python
' '.join([sbEng.stem(item) for item in (engTexts[0]).split(' ')])
```




    u'it is a truth univers acknowledged, that a singl man in possess of a good fortune, must be in want of a wife.'



This looks alright, but not completely accurate. We can see that 'universally' has been stemmed to 'univers' and 'possession' has been stemmed to 'possess', which could be useful in grouping related words, but other words, like 'is' and 'acknowledged' have not been touched.


```python
' '.join([sbEsp.stem(item) for item in (espTexts[0]).split(' ')])
```




    u'lug manch cuy nombr quer acord hac tiemp viv hidalg lanz astiller adarg antigu rocin flac galg corredor'



The Spanish text also has some problems. Nouns that don't need to be stemmed, such as 'lugar' (place) and 'tiempo' (time), have been reduced to unnecessary base forms. In addition, verbs that come from common roots are stemmed inconsistently. For example, the verb 'quiero' (I want) is reduced to 'quier', but you can see that another form of this verb, 'queremos' (we want) would be stemmed to 'quer' below.


```python
sbEsp.stem('queremos')
```




    u'quer'



In order to address this, there is a more sophisticated approach called [lemmatisation](https://en.wikipedia.org/wiki/Stemming#Lemmatisation_algorithms). Lemmatisation takes into account whether a word in a sentence is a noun, verb, adjective, etc., which is known as tagging a word's [part-of-speech](https://en.wikipedia.org/wiki/Part_of_speech). This means the algorithm can apply more appropriate rules about how to standardise words. For example, nouns can be singularised (and in Spanish, have their genders set to masculine).

We will use a package called [pattern](http://www.clips.ua.ac.be/pattern) which includes both English and Spanish lemmatisation (among many other functions). `pattern`, like `Snowball`, also supports lemmatisation in a small number of other languages. Let's install `pattern`, and then import the English and Spanish packages:


```python
!pip install pattern
```


```python
import pattern.en as lemEng
import pattern.es as lemEsp
```

Using this package, we can easily tag the part-of-speech of each word, and then run the lemmatisation algorithm over it. Have a look at this example:


```python
pprint(lemEng.parse('I ate many pizzas', lemmata=True).split(' '))
```

    [u'I/PRP/B-NP/O/i',
     u'ate/VBD/B-VP/O/eat',
     u'many/JJ/B-NP/O/many',
     u'pizzas/NNS/I-NP/O/pizza']


This output is a little confusing, but you can see that there are a few bits of information associated with each word. Let's just take the word 'pizzas', for example:


```python
lemEng.parse('I ate many pizzas', lemmata=True).split(' ')[3]
```




    u'pizzas/NNS/I-NP/O/pizza'



We can see that it is tagged as 'NNS', which indicates that it is a plural noun (information on all possible tags is [here](http://www.clips.ua.ac.be/pages/mbsp-tags)). More importantly for us, because the algorithm knows that it is a plural noun it can correctly lemmatise it to 'pizza'.

Now that we know what is going on under the hood, we can jump to pulling the lemmatised words out. Let's try again with the first sentence in our English set:


```python
' '.join(lemEng.Sentence(lemEng.parse(engTexts[0], lemmata=True)).lemmata)
```




    u'it be a truth universally acknowledge , that a single man in possession of a good fortune , must be in want of a wife .'



This looks a lot better - it has changed 'is' to 'be', and 'acknowledged' to 'acknowledge'. Now let's try our first Spanish sentence again.


```python
' '.join(lemEsp.Sentence(lemEsp.parse(espTexts[0], lemmata=True)).lemmata)
```




    u'en un lugar de el mancha , de cuyo nombre no querer acordarme , no hacer mucho tiempo que viv\xe3\xada un hidalgo de el de lanzar en astillero , adarga antiguo , roc\xe3\xadn flaco y galgo corredor .'



This is *much* better. It has left 'lugar' and 'tiempo' alone, and has changed 'quiero' to its correct root 'querer'. Given that this is the nicest possible result for standardising our words, let's do this for all of our sentences before moving onto the next step.


```python
engTexts = [' '.join(lemEng.Sentence(lemEng.parse(sentence, lemmata=True)).lemmata) for sentence in engTexts]
pprint(engTexts)
```

    [u'it be a truth universally acknowledge , that a single man in possession of a good fortune , must be in want of a wife .',
     u'once an angry man drag his father along the ground through his own orchard .\n" stop !\n" cry the groan old man at last , " stop !\nI do not drag my father beyond this tree .\n"',
     u'he be an old man who fish alone in a skiff in the gulf stream and he have go eighty-four day now without take a fish .',
     u'you do not know about me without you have read a book by the name of the adventure of tom sawyer ; but that be not no matter .']



```python
espTexts = [' '.join(lemEsp.Sentence(lemEsp.parse(sentence, lemmata=True)).lemmata) for sentence in espTexts]
pprint(espTexts)
```

    [u'lugar mancha cuyo nombre querer acordarme hacer tiempo vivir hidalgo lanzar astillero adarga antiguo roc\xedn flaco galgo corredor',
     u'a\xf1o despu\xe9s frente pelot\xf3n fusilamiento coronel aureliano buend\xeda haber recordar aquella tarde remoto padre llevar conocer hielo',
     u'bastar\xe1 decir ser juan pablo castel pintor matar mar\xeda iribarne suponer proceso recuerdo necesitar mayor explicaci\xf3n persona',
     u'se\xf1or ser malo aunque faltar\xedan motivo serlo']


## Dealing with numbers

The first line of the Old Man and the Sea has something kind of annoying - a number. Even worse, it's written out as a word. For my purposes, numbers are not very useful and should be stripped out, although, of course, you might need them left in for your analysis!

To do this, we can use this [function](https://gist.github.com/t-redactyl/4297c8e01e5b37e8a4fdb0fea2ed93dd) that I wrote, based on the [text2num](https://github.com/ghewgill/text2num) package. All this function does is strip out any words related to numbers in English, as well as numbers themselves, as part of this text cleaning process. Let's run it over our piece of text containing 'eighty-four':


```python
remove_numbers(engTexts[2])
```




    u'he be an old man who fish alone in a skiff in the gulf stream and he have go day now without take a fish .'



It's done the job! Let's now update that piece of text:


```python
engTexts[2] = remove_numbers(engTexts[2])
```

## Normalising our text

Obviously our text still contains a lot of rubbish that needs to be cleaned up. Some important things we need to get rid of prior to tokenising the sentences are the punctuation marks and all of that extra whitespace. Another thing we want to get rid of are non-signal, or [stop words](https://en.wikipedia.org/wiki/Stop_words), that are likely to be common across texts, such as 'a', 'the', and 'in'. These tasks fall into a process called [normalisation](https://en.wikipedia.org/wiki/Text_normalization), and surprise, surprise, there is another multi-language package called [cucco](https://github.com/davidmogar/cucco) that can do all of the most common normalisation tasks in English, Spanish and about 10 other languages. Please note that this blog post uses Cucco 1.0.0 - if you wish to use the package as I have in this post, download the tar.gz file from [here](https://pypi.python.org/pypi/cucco/1.0.0) and install as below:


```python
!pip install path/to/file/cucco-1.0.0.tar.gz
```

Let's now import `cucco` for both English and Spanish:


```python
from cucco import Cucco

normEng = Cucco(language='en')
normEsp = Cucco(language='es')
```

Cucco has a function called `normalize()` which, as a default, runs all of its normalisation procedures over a piece of text. While convenient, we don't want to do this as it gets rid of accent marks, and we want to keep these in our Spanish text (we'll talk about how to get our special characters back in the next section). Instead, we'll run three specific functions over our text: `remove_stop_words`, `replace_punctuation` and `remove_extra_whitespaces`. We can run these in order by putting them in a list and adding this as an argument to `normalize()`. Let's try it with our first lines from the English and Spanish texts.


```python
norms = ['remove_stop_words', 'replace_punctuation', 'remove_extra_whitespaces']
normEng.normalize(engTexts[0], norms)
```




    u'truth universally acknowledge single man possession good fortune must want wife'




```python
normEsp.normalize(espTexts[0], norms)
```




    u'lugar mancha cuyo nombre querer acordarme hacer tiempo vivir hidalgo lanzar astillero adarga antiguo roc\xedn flaco galgo corredor'



Looks great! Let's apply this over all of our texts.


```python
engTexts = [normEng.normalize(sentence, norms) for sentence in engTexts]
pprint(engTexts)
```

    [u'truth universally acknowledge single man possession good fortune must want wife',
     u'angry man drag father along ground orchard stop cry groan old man last stop I drag father beyond tree',
     u'old man fish alone skiff gulf stream go day now without take fish',
     u'know without read book name adventure tom sawyer matter']



```python
espTexts = [normEsp.normalize(sentence, norms) for sentence in espTexts]
pprint(espTexts)
```

    [u'lugar mancha cuyo nombre querer acordarme hacer tiempo vivir hidalgo lanzar astillero adarga antiguo roc\xedn flaco galgo corredor',
     u'a\xf1o despu\xe9s frente pelot\xf3n fusilamiento coronel aureliano buend\xeda haber recordar aquella tarde remoto padre llevar conocer hielo',
     u'bastar\xe1 decir ser juan pablo castel pintor matar mar\xeda iribarne suponer proceso recuerdo necesitar mayor explicaci\xf3n persona',
     u'se\xf1or ser malo aunque faltar\xedan motivo serlo']



## Dealing with mojibake

[Mojibake??](https://en.wikipedia.org/wiki/Mojibake) What the heck is that?? It is a very cute term for that very annoying thing that happens when your text gets changed from one form of encoding to another and your special characters and punctuation turn into that crazy character salad. (In fact, the German term for this, *Buchstabensalat* means 'letter salad'.) As we've already noticed, this has happened with all of the special characters (like á and ñ) in our Spanish sentences.

The good news is that it is pretty easy to reclaim our special characters. However, the bad news is that we need to jump over to Python 3 to do so. We can use a Python 3 package called [ftfy](https://github.com/LuminosoInsight/python-ftfy), or 'fixes text for you', which is designed to deal with these encoding issues. Let's go ahead and install it:


```python
!pip3 install ftfy
```

We can use the `fix_encoding()` function to get rid of all of that ugly mojibake. Let's see how it goes with our first line of Spanish text:


```python
import ftfy

print(ftfy.fix_encoding(espTexts[0]))
```

    lugar mancha cuyo nombre querer acordarme hacer tiempo vivir hidalgo lanzar astillero adarga antiguo rocín flaco galgo corredor


Nice! It has worked beautifully, with the 'í' put back into 'rocín'. Now we can fix up all of our text in preparation for the last step.


```python
espTexts = [ftfy.fix_encoding(sentence) for sentence in espTexts]
espTexts[1]
```




    'año después frente pelotón fusilamiento coronel aureliano buendía haber recordar aquella tarde remoto padre llevar conocer hielo'



## Tokenising the text and getting the frequencies

We have finally cleaned this text to a point where we can tokenise it and get the frequencies of all of the words. This is very straightforward in NLTK - we simply use the the `word_tokenize` function from the [tokenize package](http://www.nltk.org/api/nltk.tokenize.html). We'll import it below and run it over our lists of English and Spanish text separately.


```python
from nltk.tokenize import word_tokenize
```


```python
engTokens = [word_tokenize(text) for text in engTexts]
print(engTokens)
```

    [['truth', 'universally', 'acknowledge', 'single', 'man', 'possession', 'good', 'fortune', 'must', 'want', 'wife'], ['angry', 'man', 'drag', 'father', 'along', 'ground', 'orchard', 'stop', 'cry', 'groan', 'old', 'man', 'last', 'stop', 'I', 'drag', 'father', 'beyond', 'tree'], ['old', 'man', 'fish', 'alone', 'skiff', 'gulf', 'stream', 'go', 'day', 'now', 'without', 'take', 'fish'], ['know', 'without', 'read', 'book', 'name', 'adventure', 'tom', 'sawyer', 'matter']]



```python
espTokens = [word_tokenize(text) for text in espTexts]
espTokens
```




    [['lugar', 'mancha', 'cuyo', 'nombre', 'querer', 'acordarme', 'hacer', 'tiempo', 'vivir', 'hidalgo', 'lanzar', 'astillero', 'adarga', 'antiguo', 'rocín', 'flaco', 'galgo', 'corredor'], ['año', 'después', 'frente', 'pelotón', 'fusilamiento', 'coronel', 'aureliano', 'buendía', 'haber', 'recordar', 'aquella', 'tarde', 'remoto', 'padre', 'llevar', 'conocer', 'hielo'], ['bastará', 'decir', 'ser', 'juan', 'pablo', 'castel', 'pintor', 'matar', 'maría', 'iribarne', 'suponer', 'proceso', 'recuerdo', 'necesitar', 'mayor', 'explicación', 'persona'], ['señor', 'ser', 'malo', 'aunque', 'faltarían', 'motivo', 'serlo']]



We're now going to do a very simple frequency count of all of the words in each of the language's texts, using the `FreqDist` function from `nltk`. Let's import the package:


```python
from nltk import FreqDist
```

Before we can use the tokenised list of words, we need to flatten it. We can then run the `FreqDist` method over it and get the top 10 results for each language.


```python
flatList = [word for sentList in engTokens for word in sentList]
engFreq = FreqDist(word for word in flatList)

for word, frequency in engFreq.most_common(10):
print(u'{}: {}'.format(word, frequency))
```

    man: 4
    drag: 2
    father: 2
    stop: 2
    old: 2
    fish: 2
    without: 2
    truth: 1
    universally: 1
    acknowledge: 1



```python
flatList = [word for sentList in espTokens for word in sentList]
espFreq = FreqDist(word for word in flatList)

for word, frequency in espFreq.most_common(10):
print(u'{}: {}'.format(word, frequency))
```

    ser: 2
    lugar: 1
    mancha: 1
    cuyo: 1
    nombre: 1
    querer: 1
    acordarme: 1
    hacer: 1
    tiempo: 1
    vivir: 1


And that's it! This is obviously not the most useful metric (as we only have 4 sentences in each corpus), but you can see that we've arrived at something that, with more data, would form a solid foundation for a bag-of-words analysis. You can also see that while it is a bit of work to strip a text down to a useable form, there are plenty of Python packages to make this work pretty painless, even if you're working across a number of languages.
