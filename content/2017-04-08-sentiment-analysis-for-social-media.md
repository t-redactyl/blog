---
title: Using VADER to handle sentiment analysis with social media text
date: 2017-04-08
comments: false
tags: python, programming tips, text mining
keywords: python, data science, text mining, machine learning
---

A few months ago at work, I was fortunate enough to see some excellent presentations by a group of data scientists at [Experian](http://www.experian.com.au/) regarding the analytics work they do. One of the presenters gave a demonstration of some work they were doing with sentiment analysis using a Python package called [VADER, or the Valence Aware Dictionary and sEntiment Reasoner](https://github.com/cjhutto/vaderSentiment). After playing with it I realised how easy-to-use and powerful this package is, so let me talk you through how it works and how you can get up and running with it in this post!

<img src="/figure/Vader_1.jpg" title="Today I feel..." style="display: block; margin: auto;" />


## To start, what is sentiment analysis?

[Sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) is simply the process of working out (statistically) whether a piece of text is positive, negative or neutral. The majority of sentiment analysis approaches take one of two forms: **polarity-based**, where pieces of texts are classified as either positive or negative, or **valence-based**, where the intensity of the sentiment is taken into account. For example, the words 'good' and 'excellent' would be treated the same in a polarity-based approach, whereas 'excellent' would be treated as more positive than 'good' in a valence-based approach.

Sentiment analysis has applications across a range of industries - it's great for anything where you can get unstructured opinion data about a service or product. One application of sentiment analysis is for companies that have Twitter or other social media accounts to receive feedback. Obviously it's bad business for these companies to leave negative feedback unanswered too long, and sentiment analysis can give them a quick way to find and prioritise these unhappy customers.


## How does VADER work?

VADER belongs to a type of sentiment analysis that is based on lexicons of sentiment-related words. In this approach, each of the words in the lexicon is rated as to whether it is positive or negative, and in many cases, **how** positive or negative. Below you can see an excerpt from VADER's lexicon, where more positive words have higher positive ratings and more negative words have lower negative ratings.

<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th style="text-align:left">Word</th>
      <th style="text-align:center">Sentiment rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>tragedy</th>
      <td style="text-align:center">-3.4</td>
    </tr>
    <tr>
      <th>rejoiced</th>
      <td style="text-align:center">2.0</td>
    </tr>
    <tr>
      <th>insane</th>
      <td style="text-align:center">-1.7</td>
    </tr>
    <tr>
      <th>disaster</th>
      <td style="text-align:center">-3.1</td>
    </tr>
    <tr>
      <th>great</th>
      <td style="text-align:center">3.1</td>
    </tr>
  </tbody>
</table>
</div>

To work out whether these words are positive or negative (and optionally, to what degree), the developers of these approaches need to get a bunch of people to manually rate them, which is obviously pretty expensive and time-consuming. In addition, the lexicon needs to have good coverage of the words in your text of interest, otherwise it won't be very accurate. On the flipside, when there is a good fit between the lexicon and the text, this approach is accurate, and additionally quickly returns results even on large amounts of text. Incidentally, the developers of VADER used Amazon's Mechanical Turk to get most of their ratings, which is a very quick and cheap way to get their ratings!

As you might have guessed, when VADER analyses a piece of text it checks to see if any of the words in the text are present in the lexicon. For example, the sentence "The food is good and the atmosphere is nice" has two words in the lexicon (good and nice) with ratings of 1.9 and 1.8 respectively.

VADER produces four sentiment metrics from these word ratings, which you can see below. The first three, positive, neutral and negative, represent the proportion of the text that falls into those categories. As you can see, our example sentence was rated as 45% positive, 55% neutral and 0% negative. The final metric, the compound score, is the sum of all of the lexicon ratings (1.9 and 1.8 in this case) which have been standardised to range between -1 and 1. In this case, our example sentence has a rating of 0.69, which is pretty strongly positive.

<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th style="text-align:left">Sentiment metric</th>
      <th style="text-align:center">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Positive</th>
      <td style="text-align:center">0.45</td>
    </tr>
    <tr>
      <th>Neutral</th>
      <td style="text-align:center">0.55</td>
    </tr>
    <tr>
      <th>Negative</th>
      <td style="text-align:center">0.00</td>
    </tr>
    <tr>
      <th>Compound</th>
      <td style="text-align:center">0.69</td>
    </tr>
  </tbody>
</table>
</div>

## What makes VADER great for social media text?

As you might have guessed, the fact that lexicons are expensive and time-consuming to produce means they are not updated all that often. This means they lack a lot of current slang that may be used to express how a person is feeling. Take the below tweet to Optus' customer support account, for example. You can see that all of the elements of this text that indicate that the writer is unhappy (in the blue boxes) are actually informal writing - multiple punctuation marks, acronyms and an emoticon. If you didn't take this information into account, this tweet would actually look neutral to a sentiment analysis algorithm!

<img src="/figure/Vader_2.png" title="Twitter users don't write like NY Times columnists!" style="display: block; margin: auto;" />

VADER handles this by including these sorts of terms in its lexicon. Let's have a look at how this works. We'll start by installing the vaderSentiment package using pip:


```python
!pip install vaderSentiment
```

I'll now repeat here the method used by the package authors in their [github documentation](https://github.com/cjhutto/vaderSentiment) to show you how VADER outputs sentiment scores for a piece of text. We need to load the `SentimentIntensityAnalyser` object in from the VADER package and as it's a bit long, we'll assign it to another name, `analyser`, to make it a bit easier to use.


```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()
```

Finally, we'll use the `polarity_scores()` method to get the sentiment metrics for a piece of text. You can see the authors have included it in a function with some print formatting to make it a bit easier to read.


```python
def print_sentiment_scores(sentence):
    snt = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(snt)))
```

Alright, now that we have our sentiment analyser set up, let's start looking at how it handles some social media-specific terms. We'll start with a base sentence:


```python
print_sentiment_scores("I just got a call from my boss - does he realise it's Saturday?")
```

    I just got a call from my boss - does he realise it's Saturday? {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}


You can see that VADER rates this sentence as neutral. What about if we add an emoticon?


```python
print_sentiment_scores("I just got a call from my boss - does he realise it's Saturday? :(")
```

    I just got a call from my boss - does he realise it's Saturday? :( {'neg': 0.209, 'neu': 0.791, 'pos': 0.0, 'compound': -0.4404}


Now VADER is rating it as negative, picking up the sad face as useful sentiment-related information. Let's now add the acronym 'smh' (shaking my head):


```python
print_sentiment_scores("I just got a call from my boss - does he realise it's Saturday? smh :(")
```

    I just got a call from my boss - does he realise it's Saturday? smh :( {'neg': 0.321, 'neu': 0.679, 'pos': 0.0, 'compound': -0.6369}


VADER also picks this up and rates the sentence as even more intensely negative.

## Ok, but what about the word context?

VADER doesn't just do simple matching between the words in the text and in its lexicon. It also considers certain things about the way the words are written as well as their context. Let's explore this with another sentence:


```python
print_sentiment_scores("The food is good.")
```

    The food is good.----------------------- {'neg': 0.0, 'neu': 0.508, 'pos': 0.492, 'compound': 0.4404}


One of the things that VADER recognises is capitalisation, which increases the intensity of both positive and negative words. You can see below that capitalising 'good' increases the positive intensity of the whole sentence.


```python
print_sentiment_scores("The food is GOOD.")
```

    The food is GOOD.----------------------- {'neg': 0.0, 'neu': 0.452, 'pos': 0.548, 'compound': 0.5622}


Another factor that increases the intensity of sentence sentiment is exclamation marks, with up to 3 exclamation marks adding additional positive or negative intensity:


```python
print_sentiment_scores("The food is GOOD!")
```

    The food is GOOD!----------------------- {'neg': 0.0, 'neu': 0.433, 'pos': 0.567, 'compound': 0.6027}


VADER also takes into account what happens when modifying words are present in front of a sentiment term. For example, "**extremely** bad" would increase the negative intensity of a sentence, but "**kinda** bad" would decrease it. Let's see what happens if we add 'really' in front of 'good':


```python
print_sentiment_scores("The food is really GOOD!")
```

    The food is really GOOD!---------------- {'neg': 0.0, 'neu': 0.487, 'pos': 0.513, 'compound': 0.6391}


Finally, VADER also handles changes in a sentence's sentiment intensity when it contains 'but'. Essentially, the rule is that the sentiments expressed both before and after the 'but' are taken into consideration, but the sentiment afterwards is weighted more heavily than that before. Let's see how this looks:


```python
print_sentiment_scores("The food is really GOOD! But the service is dreadful.")
```

    The food is really GOOD! But the service is dreadful. {'neg': 0.192, 'neu': 0.529, 'pos': 0.279, 'compound': 0.3222}


You can see that our score has dropped from 0.64 to 0.32, as VADER has taken that 'dreadful' far more into account than the 'really GOOD!'.

I hope this has been a useful introduction to a very powerful and easy to use sentiment analysis package in Python - as you can see the implementation is very straightforward and it can be applied to quite a wide range of contexts. In the next post, I'll be detailing how I carried out [this analysis]({filename}2017-01-10-how-do-we-feel-about-new-years-resolutions.md) using VADER, and show some traps that come with doing text analysis without a very careful data cleaning strategy.

Finally, most of the information from this post comes from the very readable [paper](http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf) by the authors of the VADER package.
