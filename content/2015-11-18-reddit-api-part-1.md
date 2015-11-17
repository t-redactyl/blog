---
title: Analysing reddit data - part 1: setting up the environment 
date: 2015-11-18  
comments: false  
tags: Python, Programming tips, Public Data
keywords: python, programming, virtualenv, virtualfish, reproducible research  
---

Early in my career (before I discovered all I wanted to do was work with data) I thought I wanted to be a relationships psychologist. I actually wrote my Ph.D. thesis on hurtful events in relationships, and my Honours thesis on romantic jealousy, so you get the point! I still have a bit of a fascination with people's relationship problems, so a guilty pleasure of mine is reading the subreddit [/r/relationships](https://www.reddit.com/r/relationships#hme). Given how much time I spend on this subreddit, it seemed like a good place for a first attempt at extracting JSON-encoded data from the web.

This post is the first of a 3-part tutorial on extracting and analysing data from reddit. It is aimed at people completely new to working with JSON-encoded data. The parts are:   
1. **Setting up the environment.** This week's post will explain how to set up your environment with all the required packages in a way that lends itself to completely reproducible research.   
2. **Extracting the data.** Next week, I will cover how to pull JSON-encoded data from reddit (using /r/relationships as my example) and put in into a `pandas DataFrame` for analysis.   
3. **Cleaning and analysing the data.** I will end in two weeks by demonstrating some further data cleaning and basic analysis in `pandas` and plotting in `matplotlib`.   

Enough with the introduction, let's move onto setting up our environment!

## First steps

The very first step is making sure that you are working with the correct version of Python. I will be working with Python 2.7 in this tutorial; if you are currently working with Python 3 my code may not work for you. In order to check your version of Python, run the below in the command line (note that the `!` in front of the below code should not be typed; it is an indication that this code should be entered into the command line):


```python
!python -V
```

    Python 2.7.10


Following this, make sure that `pip` is installed. [pip (Pip Installs Packages)](https://pip.pypa.io/en/stable/) is the recommended install tool for Python packages, and having it is going to make your life much easier going forward. To check if you have pip installed, run `pip help` in the command line. You should get something like the following:


```python
!pip help
```

    
    Usage:   
      pip <command> [options]
    
    Commands:
      install                     Install packages.
      uninstall                   Uninstall packages.
      freeze                      Output installed packages in requirements format.
      list                        List installed packages.
      show                        Show information about installed packages.
      search                      Search PyPI for packages.
      wheel                       Build wheels from your requirements.
      help                        Show help for commands.



If `pip` is not installed, [here](http://jamie.curle.io/posts/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x/) is a tutorial for installing it in OSX and [here](http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/) is another for installing it in Windows.

## Setting up a virtualenv

Now that we have Python and `pip` installed, it is best practice to create a virtual environment (or [**virtualenv**](http://docs.python-guide.org/en/latest/dev/virtualenvs/)) to contain all of the Python packages we need to use. I know what you're thinking - man, this seems so tedious and overly-complicated! Why can't I just install all of these packages straight onto my system? Just hear me out - once you see the benefits of using a virtualenv, you won't want to go back to installing your packages system-wide, I promise!

So what makes a virtualenv so great? If you've been programming for a while you will have encountered problems where you try to run someone else's code (or even your own old scripts) and it throws an error as the version of the package has changed. Obviously this is a problem in any setting, but it is a particular challenge for data scientists trying to conduct [**reproducible research**](https://en.wikipedia.org/wiki/Reproducibility#Reproducible_research). In a best case scenario, an analysis you have conducted with older versions of your dependencies may fail to work; in a worst case scenario, the analysis may yield a different answer without you realising. The situation gets even more complicated when you think that you'll likely have projects which rely on different versions of packages, or have a mixture of projects in Python 2 and Python 3.

Virtualenvs solve this issue by allowing you to create a number of self-contained environments with all of the dependencies required for a project. If you install your packages within a virtualenv, it doesn't matter if you have multiple versions of a package contained on your computer; because the virtualenvs can't 'see' each other, you can safely have all of these versions installed simultaneously. It also doesn't matter if you use both Python 2 and Python 3, as you can specify which version of Python you want your virtualenv to use.

The easiest way to use virtualenvs is through a wrapper specific to your [shell interpreter](https://en.wikipedia.org/wiki/Unix_shell). For example, an option for both [Bash in OSX](http://jamie.curle.io/posts/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x/) and [CMD.exe in Windows](http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/) is [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). In my case I use [Fish](http://fishshell.com/) in OSX, so I will carry out the rest of this tutorial using it and its associated wrapper [virtualfish](http://virtualfish.readthedocs.org/en/latest/index.html).

To start a new virtualenv with virtualfish, we simply go into the shell and type `vf new <envname>`. I'll call this virtualenv `reddit_api`.


```python
!vf new reddit_api
```

You should find that you automatically enter the new virtualenv after you create it. If not, type:


```python
!vf activate reddit_api
```

Subsequently, you can exit the virtualenv using:


```python
!vf deactivate
```

A full set of virtualfish commands are [here](http://virtualfish.readthedocs.org/en/latest/usage.html).

Now that we are in the virtualenv, let's check that we have a nice clean environment. The only things that should be installed are pip, setuptools and wheel.


```python
!pip list
```

    pip (7.1.2)
    setuptools (18.2)
    wheel (0.24.0)


## Installing the required packages

Let's now install all of the packages we need into our virtualenv. For this project, we will need `urllib2` and `json` to collect the JSON data from Reddit. We will also need [`numpy`](http://www.numpy.org/), [`pandas`](http://pandas.pydata.org/) and [`matplotlib`](http://matplotlib.org/) to run the analysis, and [`jupyter`](http://jupyter.org/) to create a reproducible notebook.


```python
!pip install urllib2
!pip install json
!pip install numpy
!pip install pandas
!pip install matplotlib
!pip install jupyter
```


```python
!pip list
```

    appnope (0.1.0)
    backports-abc (0.4)
    backports.ssl-match-hostname (3.4.0.2)
    certifi (2015.9.6.2)
    cycler (0.9.0)
    decorator (4.0.4)
    functools32 (3.2.3.post2)
    gnureadline (6.3.3)
    ipykernel (4.1.1)
    ipython (4.0.0)
    ipython-genutils (0.1.0)
    ...
    pyzmq (15.0.0)
    qtconsole (4.1.0)
    setuptools (18.2)
    simplegeneric (0.8.1)
    singledispatch (3.4.0.3)
    six (1.10.0)
    terminado (0.5)
    tornado (4.3)
    traitlets (4.0.0)
    urllib2 (0.1.13)
    wheel (0.24.0)


You can see that pip now has installed all of the required packages and their dependencies.

## Saving the best for last: freezing your virtualenv

Now remember how I was talking about how great virtualenvs were for reproducible research? An obvious problem you probably saw is that it is all well and good when you're running the analysis on the computer the virtualenv was created on. But how do you get access to someone else's virtualenv?

Luckily, there is a super easy way to do this called **freezing**. This is simply where the full list of packages and their versions are exported as a .txt file. Freezing is executed like so:


```python
!pip freeze > stable_requirements.txt
```

In order to access this list of packages, you simply load the .txt file into a new virtualenv like so:


```python
!vf new reddit_api_2
!pip install -r stable_requirements.txt
```

This allows you to completely replicate the original virtualenv that the project was created in. The beauty of this method is that this .txt file can easily be stored with your script (in my case, a Jupyter notebook). For example, the script and list of dependencies can be in the same Github repo for you or others to download and install. In addition, any changes to the list of dependencies can be tracked using source control methods such as Git. This makes complete replication of your analysis seamless and fuss-free!

And we're done setting up! We now have a virtualenv with all of our required packages and a way of exporting those packages and their versions to keep with our script for replication purposes. We are now ready to start extracting and processing our data, which we will get to next week.