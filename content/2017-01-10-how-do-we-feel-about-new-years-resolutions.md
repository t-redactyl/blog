---
title: How do we feel about New Year's resolutions (according to sentiment analysis)?
date: 2017-01-10
comments: false
tags: python, programming tips, public data, twitter api, pandas
keywords: python, data science, new years, twitter, vader, sentiment analysis
---

Happy New Year everyone! And given that it's a new year, it's the season for New Year's resolutions (I myself have been sadly off cake for the last week).

Why do we love making New Year's resolutions so much? Well, change is hard - so hard, in fact, that there is [a form of therapy](https://en.wikipedia.org/wiki/Motivational_interviewing) devoted to helping people commit to it. New Year's resolutions feel like change on easy mode: you can leave behind the old you with your bad habits in the previous year!

But do we love **all** New Year's resolutions equally? After all, it's far more exciting to commit to travelling overseas this year than giving up sugar. So how do people feel about their resolutions when they set them?

<img src="/figure/new_years_resolution.png" title="Change and life are both hard" style="display: block; margin: auto;" />

## The analysis

I looked at this by extracting 20,000 tweets (excluding retweets) through the [Twitter search API](https://dev.twitter.com/rest/public/search) that contained the phrase "new years resolution", as well as information about the number of favourites each tweet received. I was then able to classify 5,125 of these tweets into [six of the most popular](https://en.wikipedia.org/wiki/New_Year's_resolution#Popular_goals) types of New Year's resolutions using string matching.

I then performed a sentiment analysis on these tweets using the [Python package VADER](https://github.com/cjhutto/vaderSentiment). VADER gives positive, neutral and negative scores to pieces of text, which range from 0 to 1 (where higher numbers indicate a higher degree of that sentiment). These are then combined to form a weighted compound sentiment score ranging from -1 to 1, with -1 indicating absolutely negative and 1 indicating absolutely positive.

I'll pop up a detailed guide on my methods in a future blog post - for now, let's have a look at the results!

## What are the most popular resolutions?

The first interesting thing we can look at as part of this analysis is what the most common and rare types of resolution are. The types of resolutions in this analysis are:  
**Physical Health**: includes being healthy, exercising and getting fit, and giving up smoking or alcohol.  
**Learning and Career**: includes learning a new skill, starting a formal course of education, getting better grades, and advancing in a current job or getting a better one.  
**Mental Wellbeing**: includes getting more organised, managing stress, anxiety and depression, getting more sleep, and enjoying life more.  
**Finances**: includes getting out of debt, investing money, and building savings.  
**Relationships**: includes building better relationships with others, getting engaged or married, and planning to have kids.  
**Travel and Holidays**: includes planning for a trip, domestic or overseas.  

Let's have a look at how frequent they are:

<img src="/figure/new_years_frequency-1.png" title="plot of chunk new_years_frequency" alt="plot of chunk new_years_frequency" style="display: block; margin: auto;" />

Unsurprisingly, by far and away the most common tweets about New Year's resolutions are about Physical Health, with Relationships a distant second. The least frequent resolutions were about Finances and Travel and Holidays. However, the fact that over three times as many people tweeted about getting their finances in order compared to travelling suggests that most Twitter users are just trying to get their basics covered before thinking about splurging on a trip.

## How do people feel about their resolutions?

Ok, so now we know what people are making resolutions about, let's have a look at how they feel about them.

<img src="/figure/new_years_sentiment-1.png" title="plot of chunk new_years_sentiment" alt="plot of chunk new_years_sentiment" style="display: block; margin: auto;" />

In order to make it a bit easier to interpret these results, I got rid of tweets that had a compound sentiment score of 0 (as they could not be assigned a sentiment). Keeping in mind that negative scores indicate that the tweet was negative, and vice versa for positive scores, we can see that Mental Wellbeing and Travel and Holiday resolutions tend to be pretty positively toned. In contrast, people are generally pretty split about their Physical Health resolutions, with a pretty equal number of people feeling positive and negative about them. This is reflected in the median sentiment score for each of the tweets:

<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th>Resolution</th>
      <th>Sentiment Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Finances</th>
      <td>0.273</td>
    </tr>
    <tr>
      <th>Learning and Career</th>
      <td>0.361</td>
    </tr>
    <tr>
      <th>Mental Wellbeing</th>
      <td>0.572</td>
    </tr>
    <tr>
      <th>Physical Health</th>
      <td>0.202</td>
    </tr>
    <tr>
      <th>Relationships</th>
      <td>0.399</td>
    </tr>
    <tr>
      <th>Travel and Holidays</th>
      <td>0.494</td>
    </tr>
  </tbody>
</table>
</div>


We can see that, on average, people feel strongly positive about Travel and Holiday and Mental Wellbeing resolutions. In contrast, people only feel weakly positive about Physical Health resolutions.

One of the reasons that physical health resolutions may not be scoring very positively is partially because people seem to be motivated by how much they currently hate their bodies or health states:

> I hate that I've gained weight over the past 3 months. New years resolution is to lose what I dont need.

However, on a somewhat funny note, something that is also bringing the sentiment score down is all of the people hating on people at the gym because of New Year's resolutions:

> Imma need all you New Years resolution people to stop clogging up the gym already, you're about one cookie away from giving up anyways.

Ouch. Keep this in mind as a limitation of the analysis - that it's difficult to get a true read on how people feel about Physical Health resolutions because of all of these passengers.

Speaking of how other people feel about resolution tweets...

## How do people's friends feel about their resolutions?

In order to get a gauge of how much people's followers on Twitter liked their resolutions, I looked at the proportion of tweets that got at least five favourites and mapped this against the compound sentiment score:

<img src="/figure/new_years_favourites-1.png" title="plot of chunk new_years_favourites" alt="plot of chunk new_years_favourites" style="display: block; margin: auto;" />

The first thing to note is that there is not that much variance in the proportion of tweets getting at least 5 favourites, ranging from 17% to 22%. This suggests that the type of resolution doesn't have that much of an effect on how much followers like them. However, there are some interesting patterns when comparing the proportion of favourites against the sentiment score.

In most cases, the number of favourites follows how the person making the tweet felt about the resolution. Physical Health resolutions tend to be more negative, and also seem to be less likely to attract many favourites, and the more positively-toned Relationships and Finances tweets are more likely to attract favourites.

However, Mental Wellbeing and Travel and Holiday tweets break this pattern. While these types of resolutions make the person making them really happy, they are some of the least likely to get five or more favourites. It's hard to say why these resolution topics don't get much love from followers. My best guess about the Mental Health resolutions is that a lot of them are pretty vague, for example this:

> new years resolution: breathe in happiness and positives, breath out toxic things, people, and activities. 2017 will be my year. watch.

It's kind of hard to get behind your friends if you don't really know what they're trying to achieve.

As for the Travel and Holiday tweets - my best guess is that no one really loves hearing about other people's travel plans!

And there you have it! Best of luck with your New Year's resolution if you made one, and hopefully your sentiment about it was nothing but positive!
