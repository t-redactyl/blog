---
title: Analysing reddit data - part 2: extracting the data  
date: 2015-11-25  
comments: false  
tags: Python, Programming tips, Public Data, Reddit API, pandas  
keywords: python, programming, reproducible research  
---

In [last week's post]({filename}2015-11-18-reddit-api-part-1.md), we covered the basics of setting up our environment so we can extract data from reddit. Now it's time to start on the meat of this topic. This week I will show you how to use the reddit public API to retrieve JSON-encoded data from the subreddit /r/relationships, although this technique will translate to both the reddit mainpage and other subreddits. As I mentioned last week, this is aimed at people who are completely new to working with JSON data, so we will go through everything step-by-step.

## Setting up

To start, let's set up our environment and start a new Jupyter notebook. Last week, I described how to set up a virtualenv for this project using [Fish](http://fishshell.com/) and [virtualfish](http://virtualfish.readthedocs.org/en/latest/index.html) in OSX. With this set up, we start by navigating to the folder we have created for this project (I recommend a local Git repo) and entering our virtualenv:


```python
!cd ~/Documents/reddit_api
!vf activate reddit_api
```

Now that we are in the virtualenv, we launch Jupyter:


```python
!ipython notebook
```

Jupyter will then open in your default browser. If you have an empty working directory, you will get something like this:

<img src="/figure/Jupyter_screenshot_1.png" title="Jupyter home screen" alt="This is the blank Jupyter notebook homepage" style="display: block; margin: auto;" />

To start a new notebook, simply click on 'New' and select 'Python 2' under 'Notebooks' in the resultant dropdown menu, as below:

<img src="/figure/Jupyter_screenshot_2.png" title="Starting new Jupyter notebook" alt="This is how to start a new Jupyter notebook" style="display: block; margin: auto;" />

To get out of Jupyter when you are finished, close the browser window and enter control-c at the command line.

## How to retrieve JSON-encoded data from reddit

Accessing the (publically-available) data from reddit is done using the [Reddit API](https://www.reddit.com/dev/api). 
In this post, we will be looking at the most popular posts of all time on /r/relationships. We can access these using the GET request [https://www.reddit.com/r/relationships/top/](https://www.reddit.com/r/relationships/top/). Below is a sample of this page at the time I accessed it: 

<img src="/figure/rrel_top_normal.png" title="rrelationships top posts" alt="Capture of the first page of the top posts from subreddit relationships" style="display: block; margin: auto;" />

To retrieve the data in a JSON-encoded format, we simply add .json to the end of this request (i.e., [https://www.reddit.com/r/relationships/top/.json](https://www.reddit.com/r/relationships/top/.json)). However, there is an issue with this request - by default, it is only giving us the top posts from the last 24 hours. You can see from the API documentation that this request is a listing, therefore it takes the parameters `after`, `before`, `limit`, `count` and `show`. There is also an additional parameter `t` not mentioned on this page, which limits the time period of the posts to show. So in order to get the top posts of all time, we need to change our request to [https://www.reddit.com/r/relationships/top/.json?sort=top&t=all](https://www.reddit.com/r/relationships/top/.json?sort=top&t=all). Additionally, if we want a specific number of posts (let's start with one), we add the limit parameter to get [https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=1](https://www.reddit.com/r/relationships/top/.json?sort=top&t=all). If we put this into our browser, we end up with the following:

<img src="/figure/rrel_top_json.png" title="rrelationships top post json" alt="JSON-encoded data from the top post on subreddit relationships" style="display: block; margin: auto;" />

Gahh, what happened here?! I am sure you can see snippets of the data you want in there but it's a mess. In order to start decoding this, let's move over to reading the data in with Python. We first need to load in the required modules:


```python
import urllib2
import json
```

We next need to send a request for the data we want. Before we can do this, we need have a look at the [rules](https://github.com/reddit/reddit/wiki/API) that reddit has set up for accessing their site. The two most important rules for our current exercise is a) that we need to create a unique [UserAgent](https://en.wikipedia.org/wiki/User_agent) string, and b) that we need to limit the number of requests we send to less than 30 a minute (i.e., one every two seconds). reddit requires that the UserAgent string contains your username, so if you don't have a reddit account you will need to [sign up](https://www.reddit.com/register) so you can get one.

We are now ready to send our request:


```python
hdr = {'User-Agent': 'osx:r/relationships.single.result:v1.0 (by /u/<PutYourUserNameHere>)'}
url = 'https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=1'
req = urllib2.Request(url, headers=hdr)
text_data = urllib2.urlopen(req).read()
```

In order to convert this into JSON-encoded data, we need to run the loads method from the json module on it:


```python
data = json.loads(text_data)
```

If we call `dir` on the `data` object we just created, we can see that there is a method called `values`. If we call the values method on `data`, we can see that the contents of the post are contained in a series of nested dictionaries and lists.


```python
data.values()
```




    [u'Listing',
     {u'after': u't3_3hw1jh',
      u'before': None,
      u'children': [{u'data': {u'approved_by': None,
         u'archived': False,
         u'author': u'whenlifegivesyoushit',
         u'author_flair_css_class': None,
         u'author_flair_text': None,
         u'banned_by': None,
         u'clicked': False,
         u'created': 1440191222.0,
         u'created_utc': 1440187622.0,
         u'distinguished': None,
         u'domain': u'self.relationships',
         u'downs': 0,
         u'edited': 1443809894.0,
         u'from': None,
         u'from_id': None,
         u'from_kind': None,
         u'gilded': 11,
         u'hidden': False,
         u'hide_score': False,
         u'id': u'3hw1jh',
         u'is_self': True,
         u'likes': None,
         u'link_flair_css_class': u'm-it updates',
         u'link_flair_text': u'Updates',
         u'locked': False,
         u'media': None,
         u'media_embed': {},
         u'mod_reports': [],
         u'name': u't3_3hw1jh',
         u'num_comments': 903,
         u'num_reports': None,
         u'over_18': False,
         u'permalink': u'/r/relationships/comments/3hw1jh/updatemy_26_f_with_my_husband_29_m_1_year_he_has/',
         u'quarantine': False,
         u'removal_reason': None,
         u'report_reasons': None,
         u'saved': False,
         u'score': 7751,
         u'secure_media': None,
         u'secure_media_embed': {},
         u'selftext': [truncated],
         u'selftext_html': [truncated],
         u'stickied': False,
         u'subreddit': u'relationships',
         u'subreddit_id': u't5_2qjvn',
         u'suggested_sort': None,
         u'thumbnail': u'',
         u'title': u'[UPDATE]My [26 F] with my husband [29 M] 1 year, he has been diagnosed with terminal cancer, how to make it count?',
         u'ups': 7751,
         u'url': u'https://www.reddit.com/r/relationships/comments/3hw1jh/updatemy_26_f_with_my_husband_29_m_1_year_he_has/',
         u'user_reports': [],
         u'visited': False},
        u'kind': u't3'}],
      u'modhash': u''}]



If, for example, we wanted to access the title of the post, it is nested within the following structure: ['Listing', {'children': [{'data': {'title':}}]}]. In other words, the nesting structure goes as follows: list -> dictionary -> list -> dictionary -> dictionary. We can therefore access it using a combination of list and dictionary indexing:


```python
data.values()[1]['children'][0]['data']['title']
```




    u'[UPDATE]My [26 F] with my husband [29 M] 1 year, he has been diagnosed with terminal cancer, how to make it count?'



As all of the other data we want is in the same dictionary as `title`, we simply need to exchange the `title` key for the relevant key. For example, the total post score is under the `score` key. Getting the specific data you might want from reddit is a matter of going through and matching the information in the dictionary to data in the post to figure out what is what.

We now know how to extract information from a single post. Let's move up to extracting information from a larger number of posts.

## Getting and storing larger quantities of data

The methods above can be easily generalised in order to obtain larger quantities of data from reddit. However, there is one further hurdle to overcome. As you can see from the documentation, reddit only allows you to pull 100 posts at a time from the top board of a subreddit. We need some way of tracking the last post we get from each request and then starting the next request after this post. Luckily, each post has a unique identifier which is stored in the `name` key:


```python
data.values()[1]['children'][0]['data']['name']
```




    u't3_3hw1jh'



We simply couple this with the `after` parameter in a loop in order to get the number of posts we want. In other words, we will send a request for the first 100 posts, obtain the identifier of the final post in that request, and ask that the next request of 100 start at the first post after this post. In our case, let's extract the first 1000 posts. As part of extracting the data, we will keep only the content assigned to the `children` key in the first dictionary. This makes it possible to put all of the separate requests together in a collection (in this case, a list). In order to make sure we don't accidentally exceed reddit's request limit of 30 requests per minute, we'll use the `sleep` method from the `time` module to place a pause of 2 seconds in between each iteration of the loop.


```python
import time

hdr = {'User-Agent': 'osx:r/relationships.multiple.results:v1.0 (by /u/<PutYourUserNameHere>)'}
url = 'https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=100'
req = urllib2.Request(url, headers=hdr)
text_data = urllib2.urlopen(req).read()
data = json.loads(text_data)
data_all = data.values()[1]['children']

while (len(data_all) <= 1000):
    time.sleep(2)
    last = data_all[-1]['data']['name']
    url = 'https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=100&after=%s' % last
    req = urllib2.Request(url, headers=hdr)
    text_data = urllib2.urlopen(req).read()
    data = json.loads(text_data)
    data_all += data.values()[1]['children']
```

Let's check that we have retrieved the correct number of posts by checking the length of our list:


```python
len(data_all)
```




    1000



Now that we have our data in raw JSON format, we can simply use another loop to extract the desired information from each post. In this case, I have decided to get the date of posting, title, flair, number of comments and total score.


```python
article_title = []
article_flairs = []
article_date = []
article_comments = []
article_score = []

for i in range(0, len(data_all)):
    article_title.append(data_all[i]['data']['title'])
    article_flairs.append(data_all[i]['data']['link_flair_text'])
    article_date.append(data_all[i]['data']['created_utc'])
    article_comments.append(data_all[i]['data']['num_comments'])
    article_score.append(data_all[i]['data']['score'])
```

Now we're pretty much there! The final step is creating a `pandas DataFrame` using these lists of results.


```python
import numpy as np
from pandas import Series, DataFrame
import pandas as pd

rel_df = DataFrame({'Date': article_date,
                    'Title': article_title,
                    'Flair': article_flairs,
                    'Comments': article_comments,
                    'Score': article_score})
rel_df = rel_df[['Date', 'Title', 'Flair', 'Comments', 'Score']]
```


```python
rel_df[:5]
```




<div>
<table border="1" class="dataframe">
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
      <td>903</td>
      <td>7755</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1438962646</td>
      <td>Update: I [30 F] am sitting in the back of my ...</td>
      <td>◉ Locked Post ◉</td>
      <td>631</td>
      <td>6013</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1435026034</td>
      <td>UPDATE: My fiancee (24F) has no bridesmaids an...</td>
      <td>Updates</td>
      <td>623</td>
      <td>5519</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1438393090</td>
      <td>My [42M] daughter [17F] has been bullying a gi...</td>
      <td>◉ Locked Post ◉</td>
      <td>972</td>
      <td>5295</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1440543117</td>
      <td>[Update] My [26F] fiance's [28M] ex-wife [28F]...</td>
      <td>Updates</td>
      <td>768</td>
      <td>5181</td>
    </tr>
  </tbody>
</table>
</div>



We now have a `pandas DataFrame` that is ready for cleaning and analysis. Next week I will start with both cleaning problematic variables (e.g., converting `Date` into a datetime format and dealing with the "Locked Post" flairs) and extracting further data from these variables. I will finish this series doing some analyses and plotting with these data.
