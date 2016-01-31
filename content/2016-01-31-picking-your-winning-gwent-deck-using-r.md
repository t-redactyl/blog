---
title: Picking your winning gwent deck using R
date: 2016-01-31
comments: false
tags: R, public data
keywords: rlanguage, ggplot2, data visualisation, gwent
---

My apologies for the two week hiatus from posting - I have been flat out job hunting so the blog has moved down the list of priorities a little. Happily I will be starting a new job next week so I will have more time to get back into my routine!

This week I want to talk about a topic near and dear to my heart - winning [gwent](http://witcher.wikia.com/wiki/Gwent). What is gwent, you ask? Gwent is a card game within the incredible video game, the [Witcher 3](http://thewitcher.com/witcher3). Those of you who are also gwent fans can benefit from my obsession with this game by using this data-driven guide to playing strategies. I've come up with five single approach strategies to win the game, and I will evaluate the decks on their various merits in each. Let's get started!

<img src="/figure/gwent1.jpeg" title="Gwent 1" alt="Gwent 1" style="display: block; margin: auto;" />

## Read in and clean the data

To get started, we'll use this spreadsheet containing the core (non-DLC) gwent cards from [this site](http://gwentcards.com/).


```r
require(XLConnect)
wb = loadWorkbook("Gwent.xlsx")
df = readWorksheet(wb, sheet = "Sheet1", header = TRUE)
```

We have a little bit of cleaning to do. Firstly, to help group repeated cards, I'll get rid of the numbers attached to these cards (e.g., 1 of 3) using a simple regex.


```r
df$Card <- gsub(" \\(.*", "", df$Card)
```

The other thing I need to do is fix up the labels of the [Nilfgaardian](http://witcher.wikia.com/wiki/Nilfgaardian_Empire) and [Northern Realms](http://witcher.wikia.com/wiki/Northern_Kingdoms) decks, which are mislabelled in the original data.


```r
df$Deck[df$Deck == "Nilfgaard"] <- "Nilfgaardian"
df$Deck[df$Deck == "Norther Realms"] <- "Northern Realms"
```

Ok, the data are now ready, so let's get started!

## Strategy 1: Win on strength alone

<img src="/figure/gwent2.png" title="Gwent 2" alt="Gwent 2" style="display: block; margin: auto;" />

The most obvious and blunt strategy is to try and win on strength alone. To see which deck is best suited to this, let's have a look at the overall attack strength of each deck. I've removed the spies for reasons I will explain in the next strategy.


```r
aggregate(ATK ~ Deck, df[!grepl("spy", df$Card.Abilities, ignore.case = TRUE) & 
                         df$Deck != "Neutral", ], sum)
```

```
##              Deck ATK
## 1        Monsters 175
## 2    Nilfgaardian 161
## 3 Northern Realms 150
## 4      Scoia'tael 177
```

We can see that the [Scoia'tael](http://witcher.wikia.com/wiki/Scoia%27tael) deck wins when we consider the total strength of the deck. However, the total strength is not the best measure of how strong a deck is as you will only be using a limited number of cards in each game. What we need to work out is whether a deck has a lot of high-powered cards. Let's first have a look at the distribution of attack strengths per deck.

<img src="/figure/unnamed-chunk-5-1.png" title="plot of chunk unnamed-chunk-5" alt="plot of chunk unnamed-chunk-5" style="display: block; margin: auto;" />

The graph shows that the Scoia'tael and Nilfgaardian decks have the highest amount of cards at the top of the strength range. Let's now have a look at the average strength of cards in the deck.


```r
aggregate(ATK ~ Deck, df[!grepl("spy", df$Card.Abilities, ignore.case = TRUE) &
                         df$Deck != "Neutral", ], median)
```

```
##              Deck ATK
## 1        Monsters 4.0
## 2    Nilfgaardian 3.0
## 3 Northern Realms 4.5
## 4      Scoia'tael 5.0
```

Again, Scoia'tael has the highest attack strength, with a median score of 5 per card. Finally, let's check which deck has the highest number of cards at attack strength 6 or above.


```r
aggregate(ATK ~ Deck, df[!grepl("spy", df$Card.Abilities, ignore.case = TRUE) &
                         df$Deck != "Neutral" & df$ATK >= 6, ], length)
```

```
##              Deck ATK
## 1        Monsters  11
## 2    Nilfgaardian  11
## 3 Northern Realms  10
## 4      Scoia'tael  13
```

Again, Scoia'tael wins out on pure strength, having 13 cards scoring at 6 or above. Therefore, **if you want to try and win using strength alone, Scoia'tael is the best choice of deck.**

## Strategy 2: Use spies to build number of cards

<img src="/figure/gwent3.jpeg" title="Gwent 3" alt="Gwent 3" style="display: block; margin: auto;" />

Of course, given the many special abilities of cards in gwent you're likely going to want to use a more subtle strategy. My boyfriend and I play with a very hero-heavy Northern Realms deck, so one of our favourite strategies is to build up a huge hand using the spy cards. For those new to gwent, spy cards allow you to draw two new cards from your deck, but have the disadvantage of contributing to your opponent's score.

Let's look at the distribution of spy cards in the decks.


```r
aggregate(Card ~ Deck, df[grepl("spy", df$Card.Abilities, ignore.case = TRUE), ], length)
```

```
##              Deck Card
## 1         Neutral    1
## 2    Nilfgaardian    3
## 3 Northern Realms    3
```

The only decks that have spy cards are Northern Realms and Nilfgaardian, with an additional spy (the Avallac'h hero card) in the neutral deck. As such, if you want to use spies you cannot get away with supplementing your deck from the neutral deck - you will have to commit to either Northern Realms or Nilfgaardian. However, while these decks have the same number of spies, they are not quite created equal. Let's have a look at the total value of the spy cards in each deck.


```r
aggregate(ATK ~ Deck, df[grepl("spy", df$Card.Abilities, ignore.case = TRUE), ], 
          sum)
```

```
##              Deck ATK
## 1         Neutral   0
## 2    Nilfgaardian  20
## 3 Northern Realms  10
```

You can see that the Nilfgaardian spy cards are worth **double** those of the Northern Realms, contributing a hefty 20 points to your opponent's score. As such, **if you want to rely on using spies the Northern Realms deck is the best choice.**

## Strategy 3: Use medics to recoup used cards

<img src="/figure/gwent4.jpeg" title="Gwent 4" alt="Gwent 4" style="display: block; margin: auto;" />

Another favourite strategy of ours is to use the medic cards. These cards recover one card of your choice from your discard pile, allowing you to play it multiple times during the game. Coupled with the decoy cards (which allow you to remove one of your cards in play and put it in your discard pile), these cards can be a powerful way to increase the value of your deck. Let's have a look where the medics are in the game.


```r
aggregate(Card ~ Deck, df[grepl("medic", df$Card.Abilities, ignore.case = TRUE), ], length)
```

```
##              Deck Card
## 1        Monsters    1
## 2         Neutral    1
## 3    Nilfgaardian    3
## 4 Northern Realms    1
## 5      Scoia'tael    3
```

Each deck has at least one medic, but the Nilfgaardian and Scoia'tael decks have three each. Again, there is only one neutral medic (the Yennefer of Vengerberg hero card), so you'll need to commit to one of these decks to fully exploit the medic strategy. Let's again have a look at the value of these medics:


```r
aggregate(ATK ~ Deck, df[grepl("medic", df$Card.Abilities, ignore.case = TRUE), ], 
          sum)
```

```
##              Deck ATK
## 1        Monsters   0
## 2         Neutral   7
## 3    Nilfgaardian   2
## 4 Northern Realms   5
## 5      Scoia'tael   0
```

```r
df[grepl("medic", df$Card.Abilities, ignore.case = TRUE), c("Deck", "Card", "ATK")]
```

```
##                Deck                       Card ATK
## 43         Monsters Eredin Destroyer of Worlds   0
## 59          Neutral     Yennefer of Vengerberg   7
## 78     Nilfgaardian  Etolian Auxiliary Archers   1
## 79     Nilfgaardian  Etolian Auxiliary Archers   1
## 109    Nilfgaardian           Siege Technician   0
## 135 Northern Realms           Dun Banner Medic   5
## 166      Scoia'tael             Havekar Healer   0
## 180      Scoia'tael             Havekar Healer   0
## 185      Scoia'tael             Havekar Healer   0
```

You can see that both the Nilfgaardian and Scoia'tael medics are extremely low valued cards, with all of the Scoia'tael medics worth 0, and the Nilfgaardian medics worth either 1 or 0. As such, using the medics is pretty much equivalent between the two decks - you gain the advantage of reusing high value cards at the expense of filling your hand with zero-value cards. **If you want to rely on the medics, either the Nilfgaardian and Scoia'tael decks are the best option.**

## Strategy 4: Use muster cards to overwhelm your opponent

<img src="/figure/gwent5.jpeg" title="Gwent 5" alt="Gwent 5" style="display: block; margin: auto;" />

The signature ability of the [Monsters](http://witcher.wikia.com/wiki/Monsters) and Scoia'tael decks is the muster ability. This means that every card with the same name will be pulled out of the deck and into play when one of them is played. Let's have a look at the number of muster cards in each of these decks.


```r
aggregate(Card ~ Deck, df[grepl("muster", df$Card.Abilities, ignore.case = TRUE), ], length)
```

```
##         Deck Card
## 1   Monsters   18
## 2 Scoia'tael    9
```

It looks like the Monsters deck has far more muster cards than the Scoia'tael deck. Let's have a look at the value of the muster cards in each deck.


```r
aggregate(ATK ~ Deck, df[grepl("muster", df$Card.Abilities, ignore.case = TRUE), ], sum)
```

```
##         Deck ATK
## 1   Monsters  66
## 2 Scoia'tael  30
```

Unsurprisingly, the Monster muster cards also have a higher value than the Scoia'tael ones, summing to more than double. So what are the best value muster cards in each deck? Firstly, we'll change the name of the muster cards to make sure that all of the ones in the same muster group have the same name.


```r
df$Muster.Combos <- df$Card
df$Muster.Combos[grep("arachas", df$Card, ignore.case = TRUE)] <- "Arachas"
df$Muster.Combos[grep("crone", df$Card, ignore.case = TRUE)] <- "Crone"
df$Muster.Combos[grep("vampire", df$Card, ignore.case = TRUE)] <- "Vampire"
```

The graph below shows the total attack strength of each of the muster groups, with lines within each bar showing the value of individual cards.

<img src="/figure/unnamed-chunk-15-1.png" title="plot of chunk unnamed-chunk-15" alt="plot of chunk unnamed-chunk-15" style="display: block; margin: auto;" />

You can see that the top **three** Monster muster groups (Arachas, Crone and Vampire) all score higher than the highest Scoia'tael muster group (Havekar Smuggler). The only issue is that the top Monster muster groups are comprised of more cards on average than the Scoia'tael ones, meaning that more of your deck will be taken up by the muster cards when using Monsters. That said, **the Monsters deck clearly outperforms the Scoia'tael deck for the muster strategy.** 

## Strategy 5: Use tight bond cards to multiply card strength

<img src="/figure/gwent6.png" title="Gwent 6" alt="Gwent 6" style="display: block; margin: auto;" />

The final strategy is tight bond, the signature strategy for the Nilfgaardian and Northern Realms decks. In this strategy, the value of all cards in the group will be multiplied by the total number of cards in that group in play. For example, if I have two cards from a group in play, the value of each will be doubled. Let's have a look at the number of tight bond cards in each deck. 


```r
aggregate(Card ~ Deck, df[grepl("bond", df$Card.Abilities, ignore.case = TRUE), ], length)
```

```
##              Deck Card
## 1    Nilfgaardian    9
## 2 Northern Realms   11
```

The number is pretty even between the decks, but obviously what matters is the (potential) value of the tight bond groups. Let's have a graph to look at the maximum value of each of the tight bond groups. We'll first shorten the two longest names to make sure the axis labels don't overlap.


```r
df$Card[df$Card == "Crinfrid Reavers Dragon Hunter"] <- "Crinfrid Reavers"
df$Card[df$Card == "Poor Fucking Infantry"] <- "Poor Infantry"
```

<img src="/figure/unnamed-chunk-18-1.png" title="plot of chunk unnamed-chunk-18" alt="plot of chunk unnamed-chunk-18" style="display: block; margin: auto;" />

You can see that the strongest tight bond group is the Nilgaardian Impera Brigade Guard, with a maximum value for the group of 48. However, the Northern Realms deck has more high scoring tight bond groups, with the Blue Stripes Commando, Crinfrid Reavers Dragon Hunter and (my favourite) Catapult groups all scoring above 30 when all are in play. In addition, each of these groups require you to use 3 or less cards to reach this maximum. As such, **you should use the Northern Realms deck to best exploit the tight bond strategy.**

## Picking your strategy

Gwent can be really overwhelming for beginners, and you can see that the game has a lot subtleties. I hope this data-driven guide has helped you weigh up the relative merits of each deck and given you some ideas about where to start when playing the game. Happy gwenting! 
