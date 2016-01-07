---
title: Creating plots in R using ggplot2 - part 3: bar plots
date: 2016-01-07
comments: false
tags: R, ggplot2, R graphing tutorials
keywords: rlanguage, ggplot2, data visualisation
---



In this third tutorial I am doing with [Mauricio Vargas Sepúlveda](http://pachamaltese.github.io/), we will demonstrate some of the many options the `ggplot2` package has for creating and customising bar plots. We will use the same [dataset](http://pachamaltese.github.io/stats/trade-chile-china/copper-data-for-tutorial.csv) from the [first](http://t-redactyl.github.io/blog/2015/12/creating-plots-in-r-using-ggplot2-part-1-line-plots.html) post.

The first thing to do is load in the data and libraries, as below:


```r
library(ggplot2)
library(ggthemes)
library(extrafont)
library(plyr)
library(scales)
charts.data <- read.csv("copper-data-for-tutorial.csv")
```

In this tutorial, we will work towards creating the area plot below. We will take you from a basic bar plot and explain all the customisations we add to the code step-by-step.

<img src="/figure/barfinalresult-1.png" title="plot of chunk finalresult" alt="plot of chunk finalresult" style="display: block; margin: auto;" />

### Basic graph
In order to initialise a plot we tell ggplot that `charts.data` is our data, and specify the variables on each axis. We then instruct ggplot to render this as an bar plot by adding the `geom_bar` command.


```r
p1 <- ggplot() + geom_bar(aes(y = export, x = year, fill = product), data = charts.data, 
                          stat="identity")
p1
```

<img src="/figure/bar1-1.png" title="plot of chunk bar1" alt="plot of chunk bar1" style="display: block; margin: auto;" />

### Adding data labels

To label the bars according to some variable in the data, we add the `label` argument to the `ggplot(aes())` option. In this case, we have labelled the bars with numbers from the `export` variable.


```r
p1 <- p1 + geom_text(data=charts.data, aes(x = year, y = export, label = export), size=4)
p1
```

<img src="/figure/bar2-1.png" title="plot of chunk bar2" alt="plot of chunk bar2" style="display: block; margin: auto;" />

### Adjusting data labels position

To adjust the position of the data labels from the default placement, we use the `ddply` function on the data, and create a new variable called `pos`. This variable is at the centre of each bar and can be used to specify the position of the labels by assigning it to the `y` argument in `geom_text(aes())`.


```r
charts.data <- ddply(charts.data, .(year), transform, pos = cumsum(export) - (0.5 * export))

p1 <- ggplot() + geom_bar(aes(y = export, x = year, fill = product), data = charts.data, 
                          stat="identity") 
p1 <- p1 + geom_text(data=charts.data, aes(x = year, y = pos, label = export), size=4)
p1
```

<img src="/figure/bar3-1.png" title="plot of chunk bar3" alt="plot of chunk bar3" style="display: block; margin: auto;" />

### Adjusting legend position

To adjust the position of the legend from the default spot of right of the graph, we add the `theme` option and specify the `legend.position="bottom"` argument. We can also change the title to blank using the ` legend.title = element_blank()` argument and change the legend shape using the `legend.direction="horizontal"` argument.


```r
charts.data <- ddply(charts.data, .(year), transform, pos = cumsum(export) - (0.5 * export))

p1 <- p1 + theme(legend.position="bottom", legend.direction="horizontal", 
                 legend.title = element_blank())
p1
```

<img src="/figure/bar4-1.png" title="plot of chunk bar4" alt="plot of chunk bar4" style="display: block; margin: auto;" />

### Changing variables display

To change the variables' displayed name, we need to re-factor our data labels in `charts.data` data frame.


```r
charts.data <- as.data.frame(charts.data)
charts.data$product <- factor(charts.data$product, levels = c("copper","others"), 
                              labels = c("Copper","Pulp wood, Fruit, Salmon & Others"))

p1 <- ggplot() + geom_bar(aes(y = export, x = year, fill = product), data = charts.data, 
                          stat="identity") 
p1 <- p1 + geom_text(data=charts.data, aes(x = year, y = pos, label = export, size=4), 
                     show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", legend.title = element_blank())
p1
```

<img src="/figure/bar5-1.png" title="plot of chunk bar5" alt="plot of chunk bar5" style="display: block; margin: auto;" />

### Adjusting x-axis scale

To change the axis tick marks, we use the `scale_x_continuous` and/or `scale_y_continuous` commands.


```r
p1 <- p1 + scale_x_continuous(breaks=seq(2006,2014,1))
p1
```

<img src="/figure/bar6-1.png" title="plot of chunk bar6" alt="plot of chunk bar6" style="display: block; margin: auto;" />

### Adjusting axis labels & adding title

To add a title, we include the option `ggtitle` and include the name of the graph as a string argument, and to change the axis names we use the `labs` command.


```r
p1 <- p1 + ggtitle("Composition of Exports to China ($)") + labs(x="Year", y="USD million") 
p1
```

<img src="/figure/bar7-1.png" title="plot of chunk bar7" alt="plot of chunk bar7" style="display: block; margin: auto;" />

### Adjusting color palette

To change the colours, we use the `scale_colour_manual` command. Note that you can reference the specific colours you'd like to use with specific HEX codes. You can also reference colours by name, with the full list of colours recognised by R [here](http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf).


```r
fill <- c("#5F9EA0", "#E1B378")
p1 <- p1 + scale_fill_manual(values=fill)
p1
```

<img src="/figure/bar8-1.png" title="plot of chunk bar8" alt="plot of chunk bar8" style="display: block; margin: auto;" />

### Using the white theme

As explained in the previous posts, we can also change the overall look of the graph using themes. We'll start using a simple theme customisation by adding `theme_bw() ` after `ggplot()`. As you can see, we can further tweak the graph using the `theme` option, which we've used so far to change the legend.


```r
p1 <- ggplot() + theme_bw() +
  geom_bar(aes(y = export, x = year, fill = product), data = charts.data, stat="identity") + 
  geom_text(data=charts.data, aes(x = year, y = pos, label = export, size=4), show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", 
        legend.title = element_blank()) + 
  scale_x_continuous(breaks=seq(2006,2014,1)) + 
  labs(x="Year", y="USD million") + 
  ggtitle("Composition of Exports to China ($)") + 
  scale_fill_manual(values=fill)
p1
```

<img src="/figure/bar9-1.png" title="plot of chunk bar9" alt="plot of chunk bar9" style="display: block; margin: auto;" />

### Creating an XKCD style chart

Of course, you may want to create your own themes as well. `ggplot2` allows for a very high degree of customisation, including allowing you to use imported fonts. Below is an example of a theme Mauricio was able to create which mimics the visual style of [XKCD](http://xkcd.com/). In order to create this chart, you first need to import the XKCD font, install it on your machine and load it into R using the `extrafont` package.
These instructions are taken from [here](https://www.google.com.au/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwiWzafchdPJAhVBpJQKHe_LDT8QFggbMAA&url=https%3A%2F%2Fcran.r-project.org%2Fweb%2Fpackages%2Fxkcd%2Fvignettes%2Fxkcd-intro.pdf&usg=AFQjCNE-KciGY14e-Q1buYIVmTFC0ht__Q&sig2=DZUwkvIHwfNWtTtkcz94jg):


```r
library(extrafont)

download.file("http://simonsoftware.se/other/xkcd.ttf", 
              dest="xkcd.ttf", mode="wb")
system("mkdir ~/.fonts")
system("cp xkcd.ttf  ~/.fonts")
font_import(paths = "~/.fonts", pattern="[X/x]kcd")
fonts()
loadfonts()
```

You can then create your graph:


```r
#font_import(pattern="[X/x]kcd")
#fonts()

fill <- c("#56B4E9", "#F0E442")

p1 <- ggplot() + 
  geom_bar(aes(y = export, x = year, fill = product), data = charts.data, stat="identity") + 
  geom_text(data=charts.data, aes(x = year, y = pos, label = export), colour="black", 
            family="xkcd-Regular", size = 4, show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", 
        legend.title = element_blank()) + 
  scale_x_continuous(breaks=seq(2006,2014,1)) + 
  labs(x="Year", y="USD million") + 
  ggtitle("Composition of Exports to China ($)") + 
  scale_fill_manual(values=fill) + 
  theme(axis.line = element_line(size=1, colour = "black"), 
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
        panel.border = element_blank(), panel.background = element_blank()) + 
  theme(plot.title=element_text(family="xkcd-Regular"), text=element_text(family="xkcd-Regular"), 
        axis.text.x=element_text(colour="black", size = 10), 
        axis.text.y=element_text(colour="black", size = 10)) 
p1
```

<img src="/figure/bar12-1.png" title="plot of chunk bar12" alt="plot of chunk bar12" style="display: block; margin: auto;" />

### Using 'The Economist' theme 

There are a wider range of pre-built themes available as part of the `ggthemes` package (more information on these [here](https://cran.r-project.org/web/packages/ggthemes/vignettes/ggthemes.html)). Below we've applied `theme_economist()`, which approximates graphs in the Economist magazine. It is also important that the font change argument inside `theme` is optional and it's only to obtain a more similar result compared to the original. For an exact result you need 'Officina Sans' which is a commercial font and is available [here](http://www.myfonts.com/fonts/itc/officina-sans/).


```r
p1 <- ggplot() + theme_economist() + scale_fill_economist() +
  theme(plot.title=element_text(family="OfficinaSanITC-Book"), 
        text=element_text(family="OfficinaSanITC-Book")) +
  geom_bar(aes(y = export, x = year, fill = product), data = charts.data, 
           stat="identity") + 
  geom_text(data=charts.data, aes(x = year, y = pos, label = export), colour="white", size = 4,
            family = "OfficinaSanITC-Book", show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", 
        legend.title = element_blank()) + 
  scale_x_continuous(breaks=seq(2006,2014,1)) + 
  labs(x="Year", y="USD million") + 
  ggtitle("Composition of Exports to China ($)")
p1
```

<img src="/figure/bar10-1.png" title="plot of chunk bar1" alt="plot of chunk bar1" style="display: block; margin: auto;" />

### Using 'Five Thirty Eight' theme 

Below we've applied `theme_fivethirtyeight()`, which approximates graphs in the nice [FiveThirtyEight](http://fivethirtyeight.com/) website. Again, it is also important that the font change is optional and it's only to obtain a more similar result compared to the original. For an exact result you need 'Atlas Grotesk' which is a commercial font and is available [here](https://commercialtype.com/catalog/atlas).


```r
p1 <- ggplot() + theme_fivethirtyeight() + scale_fill_fivethirtyeight() + 
  theme(plot.title=element_text(family="Atlas Grotesk Medium"), 
        text=element_text(family="Atlas Grotesk Light")) +
  geom_bar(aes(y = export, x = year, fill = product), data = charts.data, 
           stat="identity") + 
  geom_text(data=charts.data, aes(x = year, y = pos, label = export), colour="white", size = 3.5,
            family = "Atlas Grotesk Medium", show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", 
        legend.title = element_blank()) + 
  scale_x_continuous(breaks=seq(2006,2014,1)) + 
  labs(x="Year", y="USD million") + 
  ggtitle("Composition of Exports to China ($)")
p1
```

<img src="/figure/bar11-1.png" title="plot of chunk bar1" alt="plot of chunk bar1" style="display: block; margin: auto;" />

### Creating your own theme

As before, you can modify your plots a lot as `ggplot2` allows many customisations. Here we present our original result shown at the top of page.


```r
fill <- c("#40b8d0", "#b2d183")

p1 <- ggplot() + 
  geom_bar(aes(y = export, x = year, fill = product), data = charts.data, stat="identity") + 
  geom_text(data=charts.data, aes(x = year, y = pos, label = export), colour="black", 
            family="Tahoma", size = 4, show_guide = F) + 
  theme(legend.position="bottom", legend.direction="horizontal", 
        legend.title = element_blank()) + 
  scale_x_continuous(breaks=seq(2006,2014,1)) + 
  labs(x="Year", y="USD million") + 
  ggtitle("Composition of Exports to China ($)") + 
  scale_fill_manual(values=fill) + 
  theme(axis.line = element_line(size=1, colour = "black"), 
        panel.grid.major = element_line(colour = "#d3d3d3"), panel.grid.minor = element_blank(), 
        panel.border = element_blank(), panel.background = element_blank()) + 
  theme(plot.title = element_text(size = 14, family = "Tahoma", face = "bold"), 
        text=element_text(family="Tahoma"),
        axis.text.x=element_text(colour="black", size = 10), 
        axis.text.y=element_text(colour="black", size = 10)) 
p1
```

<img src="/figure/bar13-1.png" title="plot of chunk bar13" alt="plot of chunk bar13" style="display: block; margin: auto;" />
