---
title: Group operations in R
date: 2016-03-27
comments: false
tags: R, programming tips
keywords: rlanguage, group operations, summary statistics, birthwt, plyr, doBy
---

One of the things I really missed when I moved from Stata to R was how easy it was to do group operations; that is, being able to apply summary statistics by levels of a variable or variables in a dataset. Fortunately for me, I just needed a bit of time exploring R's massive number of functions in order to find that not only does R have as good functionality for producing statistics by groups, it offers far more flexibility and customisation than Stata. In this week's blog post, I will describe 4 functions that have become my grouping workhorses in R.

## The data

For this post, I will use Hosmer and Lemeshow's `birthwt` dataset in the `MASS` package, which describes risk factors for low birthweight in 189 infants (see `help(birthwt)` for more details about these data). In order to make the categories clearer when performing the group operations, I'll convert all of the indicator variables into labelled factors.


```r
data(birthwt, package="MASS")

# Turn indicator variables into labelled factors
birthwt$low <- factor(birthwt$low, labels = c("Above 2.5kgs", "Below 2.5kgs"))
birthwt$race <- factor(birthwt$race, labels = c("White", "Black", "Other"))
birthwt$smoke <- factor(birthwt$smoke, labels = c("Non-smoker", "Smoker"))
birthwt$ht <- factor(birthwt$ht, labels = c("No HT", "HT"))
birthwt$ui <- factor(birthwt$ui, labels = c("No UI", "UI"))
```

Now we're ready to get started.

## table and prop.table

One of the most basic group operations are frequency tables, which give us the count of the number of observations in a group. This can be achieved using the `table` function, which we'll use to look at the frequency of `low` below.


```r
table(birthwt$low)
```

```
## 
## Above 2.5kgs Below 2.5kgs 
##          130           59
```

`table` also allows us to do a contingency table, which is the crosstab between two categorical variables. Let's have a look at the contingency table of `low` by `smoke`, or the number of babies with low birthweight by their mother's smoking status.


```r
table(birthwt$low, birthwt$smoke)
```

```
##               
##                Non-smoker Smoker
##   Above 2.5kgs         86     44
##   Below 2.5kgs         29     30
```

Often, the proportion of observations is more useful than the raw counts. We can easily convert the values in `table` to proportions by encasing it in the function `prop.table`. As a default, `prop.table` will give you the percentage of the total. However, by entering a second argument we can specify if we want the proportions calculated along the rows (`1`) or the columns (`2`) instead. Let's generate the row proportions for our `low` by `smoke` contingency table:


```r
prop.table(table(birthwt$low, birthwt$smoke), 1)
```

```
##               
##                Non-smoker    Smoker
##   Above 2.5kgs  0.6615385 0.3384615
##   Below 2.5kgs  0.4915254 0.5084746
```

We can also join tables with the raw count and the proportion using `cbind`. In the second example I have rounded off the results of `prop.table` using the `round` function to make the table a little neater.


```r
cbind(table(birthwt$low, birthwt$smoke), prop.table(table(birthwt$low, birthwt$smoke), 1))
```

```
##              Non-smoker Smoker Non-smoker    Smoker
## Above 2.5kgs         86     44  0.6615385 0.3384615
## Below 2.5kgs         29     30  0.4915254 0.5084746
```

```r
cbind(table(birthwt$low, birthwt$smoke), round(prop.table(table(birthwt$low, birthwt$smoke), 1), 2))
```

```
##              Non-smoker Smoker Non-smoker Smoker
## Above 2.5kgs         86     44       0.66   0.34
## Below 2.5kgs         29     30       0.49   0.51
```

## aggregate

`table` is great for counts, but what if you want to do something else? `aggregate` is a neat way of extending this functionality, allowing you apply a variety of different statistics by groups. Let's calculate the mean birthweight by smoking status.


```r
aggregate(bwt ~ smoke, data = birthwt, FUN = mean)
```

```
##        smoke      bwt
## 1 Non-smoker 3055.696
## 2     Smoker 2771.919
```

We can also group by multiple variables. Here I have added hypertension status (`ht`) as an additional grouping variable.


```r
aggregate(bwt ~ smoke + ht, data = birthwt, FUN = mean)
```

```
##        smoke    ht      bwt
## 1 Non-smoker No HT 3090.444
## 2     Smoker No HT 2787.203
## 3 Non-smoker    HT 2519.571
## 4     Smoker    HT 2561.000
```

By using [anonymous functions](https://en.wikipedia.org/wiki/Anonymous_function), you can also generate the exact statistic you apply to your data. Anonymous functions are functions that are executed "on the fly" within R, and don't need the formal set up of being named and called separately. Here I have used an anonymous function to generate the 25th, 50th and 75th percentiles of birthweight by smoking status.


```r
aggregate(bwt ~ smoke, data = birthwt, FUN = function(x) quantile(x, c(.25, .5, .75)))
```

```
##        smoke bwt.25% bwt.50% bwt.75%
## 1 Non-smoker 2509.00 3100.00 3621.50
## 2     Smoker 2370.50 2775.50 3245.75
```

If you want to get fancy, you can also nest `aggregate` functions within each other, similar to the way you'd use nested [SQL queries](https://en.wikipedia.org/wiki/SQL). Let's first try getting the mean birthweight by maternal age (`age`) and smoking status, and then calculating the minimum of these birthweights by smoking status.


```r
aggregate(bwt ~ smoke, 
          data = aggregate(bwt ~ age + smoke, data = birthwt, FUN = mean),
          FUN = min)
```

```
##        smoke    bwt
## 1 Non-smoker 1887.5
## 2     Smoker 1135.0
```

You can see I've replaced the `data` argument with an aggregate function which calculates the sample I want to run the second aggregate function over.

## summaryBy

A couple of limitations of `aggregate` are that 1) it cannot do group operations over multiple variables, and 2) it cannot calculate multiple summary statistics unless they can be included in the same anonymous function.

An alternative function that can do both of these things is `summaryBy` in the `doBy` package. For Stata users, this is pretty much the R equivalent of `tabstat` but with a little more flexibility. Let's load in the package, and then calculate the mean of birthweight and maternal age by smoking status:


```r
library(doBy)
summaryBy(bwt + age ~ smoke, data = birthwt, FUN = mean)
```

```
##        smoke bwt.mean age.mean
## 1 Non-smoker 3055.696 23.42609
## 2     Smoker 2771.919 22.94595
```

We can also calculate a range of statistics using `summaryBy`. Let's calculate the minimum, maximum and median of birthweight by smoking status:


```r
summaryBy(bwt ~ smoke, data = birthwt, FUN = c(min, max, median))
```

```
##        smoke bwt.min bwt.max bwt.median
## 1 Non-smoker    1021    4990     3100.0
## 2     Smoker     709    4238     2775.5
```

Finally, we can combine anonymous functions with regular functions in `summaryBy`, which gives you a lot of power to get the custom summary statistics you want. Here we'll combine min, max, median and the 25th and 75th percentiles:


```r
summaryBy(bwt ~ smoke, data = birthwt,
          FUN = c(min, max, median, function(x) quantile(x, c(.25, .75))))
```

```
##        smoke bwt.FUN1 bwt.FUN2 bwt.FUN3 bwt.FUN4 bwt.FUN5
## 1 Non-smoker     1021     4990   3100.0   2509.0  3621.50
## 2     Smoker      709     4238   2775.5   2370.5  3245.75
```

You can see that an unfortunate side-effect of introducing anonymous functions into `summaryBy` is that you lose the meaningful column headings you get when using built-in functions. However, you can easily correct this by adding the names of each of the functions to the argument `fun.names`.


```r
summaryBy(bwt ~ smoke, data = birthwt,
          FUN = c(min, max, median, function(x) quantile(x, c(.25, .75))),
          fun.names = c("min", "max", "median", "25%", "75%"))
```

```
##        smoke bwt.min bwt.max bwt.median bwt.25% bwt.75%
## 1 Non-smoker    1021    4990     3100.0  2509.0 3621.50
## 2     Smoker     709    4238     2775.5  2370.5 3245.75
```

## ddply

The final function for performing group operations is the `ddply` command from the `plyr` package. `plyr` became well known a few years ago as a package that simplified data wrangling in R, and this reputation is definitely well-deserved.

Let's start by running our usual mean birthweight by smoking status operation in `ddply`. The first argument indicates the data to be used, the second is the grouping variable(s), the third tells ddply we are going to run a summary operation, and the final assigns the mean birthweight to a variable.


```r
library(plyr)
ddply(birthwt, "smoke", summarise,
      mean.bwt = mean(bwt))
```

```
##        smoke mean.bwt
## 1 Non-smoker 3055.696
## 2     Smoker 2771.919
```

You can see we get the exact same results as when using `aggregate` and `summaryBy` above. 

You might have noticed that allowing us to create a specific variable for the mean of birthweight gives us a lot more flexibility when using `aggregate` or `summaryBy`: instead of running every statistic for every variable we aggregate, we can apply specific statistics to specific variables. Let's have a further look at this, by calculating the the mean of birthweight and the median of age by smoking status:


```r
ddply(birthwt, "smoke", summarise,
      mean.bwt = mean(bwt),
      median.age = median(age))
```

```
##        smoke mean.bwt median.age
## 1 Non-smoker 3055.696         23
## 2     Smoker 2771.919         22
```

This also gives us the even more flexibility to calculate custom functions that we have when using anonymous functions in `aggregate` and `summaryBy`. This time we will count the number of observations with a low birthweight using subsetting:


```r
ddply(birthwt, "smoke", summarise,
      sum.low = length(low[low == "Below 2.5kgs"]),
      mean.bwt = mean(bwt),
      median.age = median(age))
```

```
##        smoke sum.low mean.bwt median.age
## 1 Non-smoker      29 3055.696         23
## 2     Smoker      30 2771.919         22
```

`ddply` can also group by multiple variables. Here we will group by both `smoke` and `ht`:


```r
ddply(birthwt, c("smoke", "ht"), summarise,
      sum.low = length(low[low == "Below 2.5kgs"]),
      mean.bwt = mean(bwt),
      median.age = median(age))
```

```
##        smoke    ht sum.low mean.bwt median.age
## 1 Non-smoker No HT      25 3090.444         23
## 2 Non-smoker    HT       4 2519.571         24
## 3     Smoker No HT      27 2787.203         22
## 4     Smoker    HT       3 2561.000         21
```

## Using grouping results with data.frames

In order to extend the utility of group operations even further, you can assign each of these outputs to a new data.frame and merge it with other data.frames. Let's say we want to merge the mean of birthweight by smoking status into the original `birthwt` data. For each of the three functions (`aggregate`, `summaryBy` and `ddply`), we need to assign the output to a new object. Then (as it is already a data.frame), we simply use the `merge` function to join them together.

Let's try this out using `ddply`. You can see that we merge the two data.frames on the grouping variable (`smoke`) as it is the constant between the two data.frames.


```r
agg.birthwt <- ddply(birthwt, "smoke", summarise,
                     mean.bwt = mean(bwt))
birthwt <- merge(birthwt, agg.birthwt, by = "smoke")
```

Let's have a look to see if it worked:


```r
head(birthwt[birthwt$smoke == "Non-smoker",])
```

```
##        smoke          low age lwt  race ptl    ht    ui ftv  bwt mean.bwt
## 1 Non-smoker Above 2.5kgs  19 182 Black   0 No HT    UI   0 2523 3055.696
## 2 Non-smoker Above 2.5kgs  33 155 Other   0 No HT No UI   3 2551 3055.696
## 3 Non-smoker Above 2.5kgs  23 130 Black   0 No HT No UI   1 3062 3055.696
## 4 Non-smoker Above 2.5kgs  21 160 White   0 No HT No UI   0 3062 3055.696
## 5 Non-smoker Above 2.5kgs  23 123 Other   0 No HT No UI   0 3544 3055.696
## 6 Non-smoker Above 2.5kgs  21 124 Other   0 No HT No UI   0 2622 3055.696
```

```r
head(birthwt[birthwt$smoke == "Smoker",])
```

```
##      smoke          low age lwt  race ptl    ht    ui ftv  bwt mean.bwt
## 116 Smoker Above 2.5kgs  22 130 White   0 No HT No UI   0 3132 2771.919
## 117 Smoker Above 2.5kgs  23 115 Other   0 No HT No UI   1 3331 2771.919
## 118 Smoker Above 2.5kgs  29 130 White   0 No HT No UI   2 3884 2771.919
## 119 Smoker Above 2.5kgs  26 133 Other   2 No HT No UI   0 3260 2771.919
## 120 Smoker Above 2.5kgs  18  90 White   0 No HT    UI   0 3062 2771.919
## 121 Smoker Above 2.5kgs  27 124 White   0 No HT No UI   0 2922 2771.919
```

And that's it! You can see that each of these group operations have their own strengths and benefits, ranging from when you need a quick and easy overview of one summary statistic by one variable (`table`, `aggregate`) to more complex and tailored aggregation of the data (`summaryBy`, `ddply`). I also hope this has helped demystify data screening and wrangling, which has a reputation for being a bit of a pain in R.
