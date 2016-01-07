---
title: Basic web scraping in Python  
date: 2016-01-06  
comments: false  
tags: Python, web scraping, programming tips    
keywords: python, programming, web scraping, movielens, christmas
---

If you followed along with [my analysis of the top Christmas movies according to the MovieLens 10M dataset]({filename}2015-12-23-christmas-movies-ratings.md), you would remember I obtained the list of Christmas movies by scraping [this page](http://www.timeout.com/london/film/the-50-best-christmas-movies). I am fairly new to [web scraping](https://en.wikipedia.org/wiki/Web_scraping) and this is one of my first serious attempts to get data in this manner. However, you can see that even with a basic understanding of how to find information in webpages it is relatively easy to extract the information you need. Let's get started!

## Setting up your virtualenv

The first step as always with Python analyses is to set up a virtualenv. If you're unfamiliar with how to do this, [this blog post]({filename}2015-11-18-reddit-api-part-1.md) explains how (and I promise you will never want to go back to system-installing packages!). Once you're in your virtualenv, install the following packages:


```python
!pip install lxml
!pip install cssselect
!pip install requests
!pip install jupyter
```

We then enter `!ipython notebook` into the command line and start a new notebook (alternatively you can use your preferred Python [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment)). 

## Scraping the movie titles

Once we're ready to go, we first import our newly installed packages.


```python
import lxml.html
from lxml.cssselect import CSSSelector
import requests
```

The next thing we need to do is find out where our titles are in the page. This is pretty straightforward in a browser that supports developer tools, like [Chrome](https://www.google.com/chrome/). With Chrome, we simply need to go to our list of top 50 movies, right click, and select "Inspect". This brings up the developer tools for the page.

<img src="/figure/web_scraping_inspect_element.png" title="Inspect element button" alt="Finding elements on page in Chrome." style="display: block; margin: auto;" />

Once you've done that the developer tools will open on the right of the screen. In the image above, I have highlighted a button that allows you to view the tags associated with any element of the page. If you click on this and select one of the movie titles, it will take you to the title tag, like so:

<img src="/figure/web_scraping_title_element.png" title="Inspect title" alt="Finding 'The Santa Clause' title in the page." style="display: block; margin: auto;" />

Ah ha! We can see that the first title, 'The Santa Clause', is tagged as `div.feature-item__text h3 a`. However, looking through the rest of the movies (for example, 'Joyeux Noël') are tagged only as `div.feature-item__text h3`. Huh, that creates some problems. To get around this, the function below checks whether the title tag contains an `a` (anchor) element, and if so, looks in there for the title. Otherwise, it looks in the `h3` element for the title.


```python
def get_title(node):
    '''
    Extracts the movie title from the URL http://www.timeout.com/london/film/the-50-best-christmas-movies
    taking into account that some titles are tagged as h3, and some as h3 a.
    '''
    h3_elem = node.cssselect('div.feature-item__text h3')[0]
    anchor_elem = h3_elem.cssselect('a')
    if len(anchor_elem) == 0:
        return h3_elem.text_content()
    else:
        return anchor_elem[0].text_content()
```

Now that we've set up where to look for the titles, we can extract the data from the website. The `requests.get()` function pulls the data from the website, and the `lxml.html.fromstring(r.text)` command parses the html into the `tree` variable.


```python
# Get data and transform to text
r = requests.get("http://www.timeout.com/london/film/the-50-best-christmas-movies")
tree = lxml.html.fromstring(r.text)
```

We can now select the parts of the html we want. We can see in the screenshot above that the titles are contained within the `article.feature-item` tag, therefore we select all data under this tag.


```python
items_selector = CSSSelector('article.feature-item')
all_items = items_selector(tree)
```

We can now apply our `get_title` function to the items we pulled out using list comprehension. Let's have a look at what we got:


```python
h3_titles = [get_title(item) for item in all_items[0:50]]
h3_titles
```




    ['The Santa Clause (1994)',
     'Reindeer Games (2000)',
     'The Family Stone (2005)',
     'Love Actually (2003)',
     'Merry Christmas Mr Lawrence (1983)',
     u'\n                                            Joyeux No\xebl (2005)\n                                        ',
     '\n                                            Christmas in Connecticut (1945)\n                                        ',
     'The Polar Express (2004)',
     'A Christmas Story (1983)',
     'The Holiday (2006)',
     'Planes, Trains and Automobiles (1987)',
     'Lethal Weapon (1987)',
     'Ghostbusters II (1989)',
     '\n                                            Prancer (1989)\n                                        ',
     'Holiday Inn (1942)',
     'White Christmas (1954)',
     u'\n                                            Mickey\u2019s Christmas Carol (1983)\n                                        ',
     u'National Lampoon\u2019s Christmas Vacation (1989)',
     '\n                                            Babes In Toyland (1934)\n                                        ',
     u'\n                                            \u2019R-Xmas (2001)\n                                        ',
     'Meet Me In St Louis (1944)',
     'About a Boy (2002)',
     'Christmas Evil (1980)',
     'Die Hard (1988)',
     'Die Hard 2 (1990)',
     '\n                                            A Christmas Carol (1938)\n                                        ',
     'While You Were Sleeping (1995)',
     'Arthur Christmas (2011)',
     'Trading Places (1983)',
     'Brazil (1985)',
     u'Bridget Jones\u2019 Diary (2001) ',
     'The Nightmare Before Christmas (1993)',
     'The Muppet Christmas Carol (1992)',
     'How The Grinch Stole Christmas (2000)',
     'The Long Kiss Goodnight (1996)',
     'In Bruges (2008)',
     'Miracle on 34th Street (1947)',
     'The Chronicles Of Narnia: The Lion, The Witch and the Wardrobe (2005)',
     '8 Women (2001)',
     'Scrooged (1988)',
     'Batman Returns (1992)',
     'A Charlie Brown Christmas (1965)',
     'Kiss Kiss Bang Bang (2005)',
     'The Snowman (1982)',
     'Edward Scissorhands (1990)',
     'Home Alone (1990)',
     'Gremlins (1984)',
     'Bad Santa (2003)',
     'Elf (2003)',
     u'It\u2019s a Wonderful Life (1946)']



Ok, this is a bit of a mess. To use it we need to clean it up using a bit of string manipulation.

## Cleaning up the list of titles

The first major issue you can see is that a number of titles contain whitespace and newline escape characters (`\n`). We'll get rid of the newlines by calling the `replace` method, and the whitespace by calling the `strip` method.


```python
# Strip newline and whitespace from titles
titles = [t.replace('\n', '').strip() for t in h3_titles]
```

As we don't need to preserve the unicode formatting, we'll use a lazy method to get our apostrophes back. We first call the `encode('utf8')` method, which converts the text into UTF-8 characters. We then call the `replace` method again to change the UTF-8 string for apostrophes into an actual apostrophe.


```python
# Convert from unicode and replace apostraphes
titles = [t.encode('utf8').replace('\xe2\x80\x99', '\'') for t in titles]
```

If you followed my previous post on the Christmas analyses, you would have seen that titles that start with "The" or "A" have this leading article moved to the end of the title. For example, "The Santa Clause (1994)" is represented as "Santa Clause, The (1994)" in the MovieLens 10M dataset. To change all of these, I wrote two small loops, which first use a regex to check if the title starts with "The" or "A", removes this word from the beginning of the sentence, and uses indexing to place it at the end of the title. The loop relies on the `enumerate` function to get both the index and content of each item in the list.


```python
# Replace titles in the form "The [title]" to "[title], The"
import re
for i, t in enumerate(titles):
    if re.match("^The", t):
        t = re.sub(r'^The ', '', t)
        titles[i] = t[:-7] + ", The" + t[-7:]
 
# Replace titles in the form "A [title]" to "[title], A"       
for i, t in enumerate(titles):
    if re.match("^A", t):
        t = re.sub(r'^A ', '', t)
        titles[i] = t[:-7] + ", A" + t[-7:]
```

Finally, I haven't yet replaced the UTF-8 character for 'ö' in 'Joyeux Noël'. However, as I know there are issues with the 'ö' character in the MovieLens 10M dataset as well, I'll just truncate the whole title to 'Joyeux' which is sufficient to get an exact match between the two movie lists.


```python
# Change "Joyeux Noël" to just "Joyeux" due to special character matching issues        
titles[5] = titles[5].replace('Joyeux No\xc3\xabl (2005)', 
                              'Joyeux')
```

We now have a complete list! Let's have a look at how it's turned out:


```python
titles
```




    ['Santa Clause, The (1994)',
     'Reindeer Games (2000)',
     'Family Stone, The (2005)',
     'Love Actually (2003)',
     'Merry Christmas Mr Lawrence (1983)',
     'Joyeux',
     'Christmas in Connecticut (1945)',
     'Polar Express, The (2004)',
     'Christmas Story, A (1983)',
     'Holiday, The (2006)',
     'Planes, Trains and Automobiles (1987)',
     'Lethal Weapon (1987)',
     'Ghostbusters II (1989)',
     'Prancer (1989)',
     'Holiday Inn (1942)',
     'White Christmas (1954)',
     "Mickey's Christmas Carol (1983)",
     "National Lampoon's Christmas Vacation (1989)",
     'Babes In Toyland (1934)',
     "'R-Xmas (2001)",
     'Meet Me In St Louis (1944)',
     'About a Boy, A (2002)',
     'Christmas Evil (1980)',
     'Die Hard (1988)',
     'Die Hard 2 (1990)',
     'Christmas Carol, A (1938)',
     'While You Were Sleeping (1995)',
     'Arthur Christmas, A (2011)',
     'Trading Places (1983)',
     'Brazil (1985)',
     "Bridget Jones' Diary (2001)",
     'Nightmare Before Christmas, The (1993)',
     'Muppet Christmas Carol, The (1992)',
     'How The Grinch Stole Christmas (2000)',
     'Long Kiss Goodnight, The (1996)',
     'In Bruges (2008)',
     'Miracle on 34th Street (1947)',
     'Chronicles Of Narnia: The Lion, The Witch and the Wardrobe, The (2005)',
     '8 Women (2001)',
     'Scrooged (1988)',
     'Batman Returns (1992)',
     'Charlie Brown Christmas, A (1965)',
     'Kiss Kiss Bang Bang (2005)',
     'Snowman, The (1982)',
     'Edward Scissorhands (1990)',
     'Home Alone (1990)',
     'Gremlins (1984)',
     'Bad Santa (2003)',
     'Elf (2003)',
     "It's a Wonderful Life (1946)"]



The last thing left to do is to export the whole thing to a text file. In the case of my analysis, I then imported this into an SQL database with the MovieLens 10M dataset, and I will describe how I used it in my next blog post.


```python
# Export to text file                              
f = open("christmas_movies.txt", "w")
f.write("\n".join(map(lambda x: str(x), titles)))
f.close()
```

I hope this was a useful introduction which demystifies the basics of web scraping. You can see how using your browser's developer tools to find the specific tags and the `lxml` package to select the information you need makes it relatively straightforward to get the information you need. It is then a matter of using some pretty simple string manipulation to clean up the data, and voila! You have successfully scraped the data you need from a web page! 
