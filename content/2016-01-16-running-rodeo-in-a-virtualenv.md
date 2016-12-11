---
title: Running Rodeo within a virtualenv
date: 2016-01-16  
comments: false  
tags: Python, Rodeo, virtualenvs
keywords: python, programming, web scraping, movielens, christmas
---

**Note:** This post was updated on 11/12/2016 to reflect changes in how you change your PYTHONPATH in Rodeo.

I recently discovered the lovely [Rodeo by yhat](http://blog.yhat.com/posts/rodeo-native.html), an IDE for Python that is focused on data science. It was originally released as an in-browser web application, but the development team released it as an application in October last year. I am a **huge** fan of [RStudio](https://www.rstudio.com/), and by early looks Rodeo may fill this role for me on the Python side of things.

However, there was a small hiccup when it came to setting up Rodeo. As you might know, I am a devotee of virtual environments (or [virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/)) in Python. However, it is not immediately obvious how to run Rodeo within one. I therefore thought I would write this quick tutorial on how to set up Rodeo using a virtualenv.

## Creating the virtualenv (Python 2.7 version)

Let's first create our Python 2.7 virtualenv. I use [Fish](http://fishshell.com/) as my shell interpreter and its associated wrapper [virtualfish](http://virtualfish.readthedocs.org/en/latest/index.html), so I set up my new virtualenv like so:

```bash
vf new rodeo
```

(See this [blog post]({filename}2015-11-18-reddit-api-part-1.md) for more information about setting up virtualenvs.) Now that we're in our new virtualenv called "Rodeo", we can install the required packages. Rodeo requires [Jupyter](http://jupyter.readthedocs.org/en/latest/) and [matplotlib](http://matplotlib.org/) as a minimum to run, so let's install them using pip.

```bash
!pip install jupyter
!pip install matplotlib
```

We will also need [numpy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/) to complete the example I will show, so let's also install them:

```bash
!pip install numpy
!pip install pandas
```

Now we're ready to open Rodeo!

## Setting up Rodeo

The first step to setting up Rodeo with a virtualenv is to get the PYTHONPATH of the virtualenv. This is very straightforward: all you need to do is type `which python` at the command line **while you are in your virtualenv.** You should get something that looks like the below:

```bash
/Users/<your username>/.virtualenvs/rodeo/bin/python
```

(Note that this path will be a bit different if you are not working in Mac OSX.)

Now let's get Rodeo to use our virtualenv. If you haven't yet installed Rodeo, it can be downloaded from [here](https://www.yhat.com/products/rodeo). Once that is done, we can get on with changing its PYTHONPATH. To do so, we first need to go to Rodeo > Preferences in the Rodeo menu. Under the 'Python' tab, you will find an option called 'Python Command'. This is where we change the PYTHONPATH. Simply paste the path to your virtualenv in this space, click 'OK', and you're good to go!

You can check your code has worked by running this example I got from Wes McKinney's excellent [Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do).

```py
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

df = DataFrame(np.random.randn(10, 4).cumsum(0),
               columns=['A', 'B', 'C', 'D'],
               index=np.arange(0, 100, 10))

df.plot()
```

You should get something like the screenshot below:

<img src="/figure/Rodeo_example_small.png" title="Rodeo screenshot" alt="Example of Rodeo working correctly" style="display: block; margin: auto;" />

## What about Python 3?

You can easily switch Rodeo over to using Python 3 by creating a new virtualenv. In order to tell virtualfish that you want it to use Python 3, you simply use:

```bash
vf new -p python3 rodeo
```

We then install all of the required packages as above, and get our PYTHONPATH using `which python`. In order to switch Rodeo's PYTHONPATH over from our old virtualenv, simply replace the path in 'Python Command' as detailed above.

Now you're ready to go! Happy analysing :)
