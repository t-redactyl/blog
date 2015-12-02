---
title: Analysing reddit data - part 3: cleaning and describing the data  
date: 2015-12-02  
comments: false  
tags: Python, Programming tips, Public Data, Reddit API, pandas  
keywords: python, programming, reproducible research, reddit api, json, pandas, regex, numpy  
---

Over the past two weeks ([here]({filename}2015-11-18-reddit-api-part-1.md) and [here]({filename}2015-11-25-reddit-api-part-2.md)) we have been discussing how to use JSON-encoded data from reddit. So far we have set up our environment and extracted the top 1,000 posts of all time from the subreddit [/r/relationships](https://www.reddit.com/r/relationships#hme) into a `pandas Dataframe`. This week, we will work on cleaning the data, extracting further data from our existing variables and describing these variables. We'll end this series next week by doing some basic inferential analyses.

## Picking up where we left off

Last week, we ended up with a `pandas Dataframe` called `rel_df` with five variables: `Date`, `Title`, `Flair`, `Comments` and `Score`. If you don't have this Dataframe prepared, you'll need to go back to the previous posts and set this up to continue with the tutorial. Here is the first 5 results from this Dataframe.


```python
rel_df[:5]
```




<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Title</th>
      <th>Flair</th>
      <th>Comments</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1440187622</td>
      <td>[UPDATE]My [26 F] with my husband [29 M] 1 yea...</td>
      <td>Updates</td>
      <td>908</td>
      <td>7843</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1438962646</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>◉ Locked Post ◉</td>
      <td>631</td>
      <td>6038</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1435026034</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5548</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1438393090</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>◉ Locked Post ◉</td>
      <td>970</td>
      <td>5301</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1440543117</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>767</td>
      <td>5195</td>
    </tr>
  </tbody>
</table>
</div>



## Cleaning the data

As I pointed out in the last blog post, there are two immediately obvious issues with these data. The first is that the date is in [Unix or Epoch time](https://en.wikipedia.org/wiki/Unix_time), which represents the number of seconds that have passed since 1 January 1970. In order to convert this into a datetime format, we run the following:


```python
rel_df['Date'] = pd.to_datetime((rel_df['Date'].values*1e9).astype(int))
rel_df[:5]
```




<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Title</th>
      <th>Flair</th>
      <th>Comments</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-08-21 20:07:02</td>
      <td>[UPDATE]My [26 F] with my husband [29 M] 1 yea...</td>
      <td>Updates</td>
      <td>908</td>
      <td>7843</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-08-07 15:50:46</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>◉ Locked Post ◉</td>
      <td>631</td>
      <td>6038</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-06-23 02:20:34</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5548</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-08-01 01:38:10</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>◉ Locked Post ◉</td>
      <td>970</td>
      <td>5301</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-08-25 22:51:57</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>767</td>
      <td>5195</td>
    </tr>
  </tbody>
</table>
</div>



The other issue is that when posts become locked by the subreddit moderators, the original flair is replaced with "Locked Post". This is not really the most useful label as it doesn't give us any information about the topic. Let's replace all of the "Locked Post" flairs with missing values (NaN) and have a look at how many there are.


```python
import re

replace_value = rel_df['Flair'][1]
rel_df['Flair'] = rel_df['Flair'].replace(replace_value, np.nan)

rel_df['Flair'].isnull().sum()
```




    155



You can see a substantial number (16%) of flairs were replaced with "Locked Post", which means we have a large amount of [missing data](https://en.wikipedia.org/wiki/Missing_data) in this variable. However, we can recover some information by exploiting the fact that update posts usually have the word "Update" in the title. We can use a [regex](https://en.wikipedia.org/wiki/Regular_expression) to check for whether "Update" is in the title, and if so, replace the flair with "Updates".


```python
cond1 = rel_df['Title'].str.contains(
    '^\[?[a-z!?A-Z ]*UPDATE\]?:?', flags = re.IGNORECASE)
cond2 = rel_df['Flair'].isnull()

rel_df.loc[(cond1 & cond2), 'Flair'] = rel_df.loc[(cond1 & cond2), 'Flair'].replace(np.nan, 'Updates')
rel_df[:5]
```




<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Title</th>
      <th>Flair</th>
      <th>Comments</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-08-21 20:07:02</td>
      <td>[UPDATE]My [26 F] with my husband [29 M] 1 yea...</td>
      <td>Updates</td>
      <td>908</td>
      <td>7843</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-08-07 15:50:46</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>Updates</td>
      <td>631</td>
      <td>6038</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-06-23 02:20:34</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5548</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-08-01 01:38:10</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>NaN</td>
      <td>970</td>
      <td>5301</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-08-25 22:51:57</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>767</td>
      <td>5195</td>
    </tr>
  </tbody>
</table>
</div>




```python
rel_df['Flair'].isnull().sum()
```




    96



You can see that we still have 10% of missing data in this variable, which is quite high. However, we have replaced some of the missing data in a robust manner. This should be bookmarked as a possible source of [bias](https://en.wikipedia.org/wiki/Bias_(statistics)) in our data when we try and interpret our analyses.

## Extracting extra variables

You might have gotten the idea from how I replaced the missing flairs that we could extract further information from the `Title` variable, and indeed we can. Another convention that we can exploit is that posters to /r/relationships are asked to include their age and sex in the title. For example, you can see in the first post that the poster has included their age and sex as "[26F]", indicating they are a 26 year old woman. You can probably also see a pattern in how the posters information is nested in the title as well. Looking through the data, I picked out four words that precede the posters' information: "My", "I", "I'm" and "Me". We can use a (pretty complicated) regex to extract this portion of the title:


```python
poster_age_sex = rel_df['Title'].str.extract(
    "((i\'m|i|my|me)\s?(\[|\()(m|f)?(\s|/)?[0-9]{1,2}(\s|/)?([m,f]|male|female)?(\]|\)))", 
        flags = re.IGNORECASE)[0]
poster_age_sex[:5]
```




    0    My [26 F]
    1     I [30 F]
    2      I (25m)
    3     My [42M]
    4     My [26F]
    Name: 0, dtype: object



Let's now clean this up by getting rid of the starting word, then pulling the age and sex out into separate variables and adding them to the DataFrame.


```python
poster_age_sex = poster_age_sex.str.replace("((i\'m|i|my|me))\s?", "", flags = re.IGNORECASE)
poster_age = poster_age_sex.str.extract('([0-9]{1,2})')
poster_sex = poster_age_sex.str.extract('([m,f])', flags = re.IGNORECASE)

rel_df['PosterAge'] = pd.to_numeric(poster_age)
rel_df['PosterSex'] = poster_sex.str.upper()

rel_df[:5]
```




<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Title</th>
      <th>Flair</th>
      <th>Comments</th>
      <th>Score</th>
      <th>PosterAge</th>
      <th>PosterSex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-08-21 20:07:02</td>
      <td>[UPDATE]My [26 F] with my husband [29 M] 1 yea...</td>
      <td>Updates</td>
      <td>908</td>
      <td>7843</td>
      <td>26</td>
      <td>F</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-08-07 15:50:46</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>Updates</td>
      <td>631</td>
      <td>6038</td>
      <td>30</td>
      <td>F</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-06-23 02:20:34</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5548</td>
      <td>25</td>
      <td>M</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-08-01 01:38:10</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>NaN</td>
      <td>970</td>
      <td>5301</td>
      <td>42</td>
      <td>M</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-08-25 22:51:57</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>767</td>
      <td>5195</td>
      <td>26</td>
      <td>F</td>
    </tr>
  </tbody>
</table>
</div>



Let's now check for missing values in our new PosterAge and PosterSex variables:


```python
rel_df['PosterAge'].isnull().sum()
```




    91




```python
rel_df['PosterSex'].isnull().sum()
```




    103



Again, these variables have fairly high amounts of missing data (9% for age 10% for sex). This is another possible source of bias to keep in mind. I'll discuss how these possible biases might affect how we interpret our analyses at the end of next week's post.

Finally, we can use the date variable to obtain the day of the week that the post was created:


```python
rel_df['DayOfWeek'] = rel_df['Date'].dt.dayofweek
days = {0: 'Mon', 1: 'Tues', 2: 'Weds', 3: 'Thurs', 4: 'Fri',
        5: 'Sat', 6: 'Sun'}
rel_df['DayOfWeek'] = rel_df['DayOfWeek'].apply(lambda x: days[x])

rel_df[:5]
```




<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Title</th>
      <th>Flair</th>
      <th>Comments</th>
      <th>Score</th>
      <th>PosterAge</th>
      <th>PosterSex</th>
      <th>DayOfWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-08-21 20:07:02</td>
      <td>[UPDATE]My [26 F] with my husband [29 M] 1 yea...</td>
      <td>Updates</td>
      <td>908</td>
      <td>7843</td>
      <td>26</td>
      <td>F</td>
      <td>Fri</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-08-07 15:50:46</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>Updates</td>
      <td>631</td>
      <td>6038</td>
      <td>30</td>
      <td>F</td>
      <td>Fri</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-06-23 02:20:34</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5548</td>
      <td>25</td>
      <td>M</td>
      <td>Tues</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-08-01 01:38:10</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>NaN</td>
      <td>970</td>
      <td>5301</td>
      <td>42</td>
      <td>M</td>
      <td>Sat</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-08-25 22:51:57</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>767</td>
      <td>5195</td>
      <td>26</td>
      <td>F</td>
      <td>Tues</td>
    </tr>
  </tbody>
</table>
</div>



Checking for missing data, we find that this time no values are missing (due to the fact that every date is present).


```python
rel_df['DayOfWeek'].isnull().sum()
```




    0



## Descriptives

Now that we have finished cleaning, we are now ready to get acquainted with our data using some [descriptives](https://en.wikipedia.org/wiki/Descriptive_statistics). For the sake of brevity I will skip screening for [normality](https://en.wikipedia.org/wiki/Normal_distribution) and assume all of the continuous variables are non-normal, but obviously in a real analysis it would be necessary to explore this further. As such, I will use the [median](https://en.wikipedia.org/wiki/Median) and [interquartile range (IQR)](https://en.wikipedia.org/wiki/Interquartile_range) for continuous variables, and frequencies and percentages for categorical variables.

### Poster age
Let's start with `PosterAge`. We can see we have 909 data points for this variable, and that posters are a median of 26 years old (IQR: 23, 29).


```python
rel_df['PosterAge'].describe()
```




    count    909.000000
    mean      26.698570
    std        6.323285
    min       13.000000
    25%       23.000000
    50%       26.000000
    75%       29.000000
    max       57.000000
    Name: PosterAge, dtype: float64



### Poster sex

Looking at `PosterSex`, we can see that we have 897 data points for this variable. 542 of the posters are female (60% of non-missing values), and 355 are male (40%).


```python
rel_df['PosterSex'].notnull().sum()
```




    897




```python
rel_df['PosterSex'].value_counts()
```




    F    542
    M    355
    Name: PosterSex, dtype: int64




```python
100 * rel_df['PosterSex'].value_counts() / rel_df['PosterSex'].notnull().sum()
```




    F    60.423634
    M    39.576366
    Name: PosterSex, dtype: float64



### Flairs

In `Flairs`, we have 904 complete data points. The most common flair is "Updates" (516 posts, or 57%), and the least common is "Dating" (3, > 1%). The bottom three categories are concerningly small and are therefore unlikely to be suitable for further analysis, especially when we get to doing subgroup analyses next week (see this [previous blog post]({filename}2015-09-15-representative-sampling.md) for a discussion on the importance of sufficiently large samples).


```python
rel_df['Flair'].notnull().sum()
```




    904




```python
rel_df['Flair'].value_counts()
```




    Updates            516
    Relationships      161
    Non-Romantic       158
    Infidelity          38
    Breakups            15
    Personal issues     13
    Dating               3
    Name: Flair, dtype: int64




```python
100 * rel_df['Flair'].value_counts() / rel_df['Flair'].notnull().sum()
```




    Updates            57.079646
    Relationships      17.809735
    Non-Romantic       17.477876
    Infidelity          4.203540
    Breakups            1.659292
    Personal issues     1.438053
    Dating              0.331858
    Name: Flair, dtype: float64



### Score

Examining the `Score` variable we can see that it has all 1,000 data points, and the median score per post is 1,225 (IQR: 961, 1,761).


```python
rel_df['Score'].describe()
```




    count    1000.00000
    mean     1511.58000
    std       822.78436
    min       792.00000
    25%       963.00000
    50%      1224.50000
    75%      1762.00000
    max      7843.00000
    Name: Score, dtype: float64



### Comments

Similarly, the `Comments` variable has all 1,000 data points. The median number of comments per post is 269 (IQR: 161, 421).


```python
rel_df['Comments'].describe()
```




    count    1000.000000
    mean      318.964000
    std       219.461632
    min        15.000000
    25%       161.000000
    50%       269.000000
    75%       421.250000
    max      1693.000000
    Name: Comments, dtype: float64



### Day of week

Finally, let's have a look at `DayOfWeek`. We already know it has all 1,000 data points, so we don't have to check that again. We can see that the highest number of posts were created during the week, with around 15% of posts on each of the weekdays. In contrast, Sunday was the quietest day for popular posts.


```python
rel_df['DayOfWeek'].value_counts()
```




    Tues     156
    Weds     155
    Mon      155
    Thurs    154
    Fri      148
    Sun      121
    Sat      111
    Name: DayOfWeek, dtype: int64




```python
100 * rel_df['DayOfWeek'].value_counts() / rel_df['DayOfWeek'].notnull().sum()
```




    Tues     15.6
    Weds     15.5
    Mon      15.5
    Thurs    15.4
    Fri      14.8
    Sun      12.1
    Sat      11.1
    Name: DayOfWeek, dtype: float64



We now have a cleaned dataset and have inspected each of the variables (although be aware I took some shortcuts with my screening and didn't inspect things like normality). We are now ready to run some analyses next week.

For those who have followed this tutorial so far, or have been reading my blog more generally, a huge thank you! Today marks just past 3 months of blogging for me, and it has been wonderful to have an excuse to constantly learn new data science skills and to share them with others. I hope my posts have helped you to learn something just as I have learned, and continue to learn from all of the wonderful data science and programming bloggers out there in turn.
