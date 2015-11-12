---
title: Object-oriented programming in Python for a non-object-oriented programmer 
date: 2015-11-11  
comments: false  
tags: Python, Programming tips  
keywords: python, programming, oop
---

When I first seriously decided to learn programming about three years ago, I picked up Python using Zed Shaw's [**Learn Python the Hard Way**](http://learnpythonthehardway.org/). While an excellent introduction to programming for someone who had previously only cobbled together [SPSS](https://en.wikipedia.org/wiki/SPSS) syntax, his explanation of [object-orientated programming (OOP)](https://en.wikipedia.org/wiki/Object-oriented_programming) went completely over my head. I confess, I had spent the entire time since convinced I was incapable of understanding OOP! 

When refreshing Python recently, I used the book [**Practical Programming: An Introduction to Computer Science Using Python**](http://www.amazon.com/Practical-Programming-Introduction-Pragmatic-Programmers/dp/1934356271). This book had such a nice explanation of OOP that it (well, the basics at least!) finally clicked for me. I'll therefore use this week's blog post to assist someone else to conquer OOP using Python. 

I used Python 2.7.10 for this post.

## Python uses types

You will remember that Python uses a number of [**types**](https://docs.python.org/2/library/stdtypes.html). A type takes the form of a value or collection of values, and each have specific **methods** you can call on them. 

For example, a major type is a **list**. Let's say we own a cattery and we want to keep track of the cats we have at the moment. We can store their names in a list:


```python
cats = ['Whiskers', 'Felix', 'Charley', 'Rosebud', 'Biddy']
print cats
```

    ['Whiskers', 'Felix', 'Charley', 'Rosebud', 'Biddy']


<img src="/figure/catsinboxes.png" title="cats in boxes" alt="plot of chunk interpretation" style="display: block; margin: auto;" />

However, today Whiskers is going home and we are also getting a new cat (Mr. Paws). We can update our list by calling the methods 'append' and 'remove':


```python
cats.remove('Whiskers')
cats.append('Mr. Paws')
print cats
```

    ['Felix', 'Charley', 'Rosebud', 'Biddy', 'Mr. Paws']


## Creating a class is creating a new type

You can see that the list type has a **general** form (immutable sequence of any length, containing any type of value, separated by commas and surrounded by square brackets). You can also see that we created a **specific** list **object** which contained a sequence of strings to represent our cat names.

We can extend the functionality of Python by creating our own types. The general forms of each of these types are called **classes**, and  we can create a specific object which is an **instance** of this class. We can also define the methods we want our class to have.

## Class Cat

Let's say that we want to make a general form to describe the cats we are looking after. We will do this by defining a new type we'll call Cat. This Cat will have a name, a temperament, and a weight (in kgs). In this first step, you can see that we are are using the keyword `class` to indicate to Python that we want to create a type, and the `object` argument indicates that this is an object. For now, this class is empty as shown by the `pass` argument.


```python
class Cat(object):
    '''A Cat with name, temperament and weight components.'''
    
    pass
```

If we want to create a new Cat, we simply assign it to a new variable like below:


```python
felix = Cat()
```

This is the equivalent of creating an empty list for a list type.

The first thing we want our Cat type to do is print the name of the cat. A (bad) way to do this is to attach a name value to the Cat object like below. This Cat now has an **instance variable** called `name`.


```python
felix.name = "Felix"
print felix.name
```

    Felix


We could then use this `name` variable in a function:


```python
def name_print(cat):
    '''Print the name of the cat.'''
    print "The cat is called %s." % cat.name

name_print(felix)
```

    The cat is called Felix.


We can make this function a method of the Cat type by moving it into the class. Note that an important change to the code is that the `cat` parameter has been replaced with `self`. This indicates that the class refers to the specific instance to supply it with the parameter for the function, which in this case is `felix`.


```python
class Cat(object):
    '''A Cat with name, temperament and weight components.'''
    
    def name_print(self):
        '''Print the name of the cat.'''
        print "The cat is called %s." % self.name
    
felix = Cat()
felix.name = "Felix"
felix.name_print()
```

    The cat is called Felix.


Obviously defining the instance variables outside the class is undesirable - it is inefficient and prone to mistakes. Instead, it would be better if we could just include the variables at the same time as creating a new Cat. The way we do this is to add a **constructor** method, which in Python is called using `__init__`. This is one of Python's **special methods** that can be used within classes. You can see how we've included this below:


```python
class Cat(object):
    '''A Cat with name, temperament and weight components.'''
    
    def __init__(self, name):
        '''A new cat with name value name.'''
        self.name = name
    
    def name_print(self):
        '''Print the name of the cat.'''
        print "The cat is called %s." % self.name
    
felix = Cat("Felix")
felix.name_print()
```

    The cat is called Felix.


You can see that, just like a function, the `__init__` method allows you to pass the `name` parameter to a new Cat when it is being created. You can also see that the class is again passing a reference to the instance being created using the `self` parameter. As such, the `__init__` method also requires that you attach each instance variable to the instance. You can see we did this by defining the `name` parameter as `self.name` within the class.

You may also have noticed that I changed my `name_print` method into a method called `__str__`. This is another special method. The `__str__` method returns a string representation of the object when it is printed. As the only instance variable we have input so far is the cat's name, that is all that string returns. `__init__` and `__str__` are just two of the many special methods Python has.


```python
class Cat(object):
    '''A Cat with name, temperament and weight components.'''
    
    def __init__(self, name):
        '''A new Cat with a name (string).'''
        self.name = name
    
    def __str__(self):
        '''Print the name of the cat.'''
        return "The cat is called %s." % self.name
    
felix = Cat("Felix")
print felix
```

    The cat is called Felix.


The final step is adding in the temperament and weight instance variables and methods to use them. We do this by simply adding them to the list of parameters within the `__init__` method, and then writing functions that define what the new methods do. In this case, a method I have included to use temperament is `is_friendly`, which returns True when the cat is friendly and False otherwise. Additionally I have included an `if_weighs_more` method for weight, which takes a second "threshold" weight as an argument and returns True if the cat weighs more and False otherwise. Finally, you may have noticed that I changed the `__str__` method. As it is supposed to be a full representation of the object, I have expanded it to include all of the instance variables.


```python
class Cat(object):
    '''A Cat with name, temperament and weight components.'''
    
    def __init__(self, name, temperament, weight):
        '''A new Cat with a name (string), temperament (string) 
        and weight (float).'''
        self.name = name
        self.temperament = temperament
        self.weight = weight
    
    def __str__(self):
        '''Print the Cat object.'''
        return "The cat is called %s. Its temperament is %s. It weighs %s kgs." \
        % (self.name, self.temperament, self.weight)
    
    def is_friendly(self):
        '''Prints the temperament of the cat.'''
        return self.temperament == "friendly"
    
    def if_weighs_more(self, cutoff_weight):
        '''Returns if cat weighs more than a specified value.'''
        return self.weight > cutoff_weight
```


```python
felix = Cat("Felix", "friendly", 6)
print felix
```

    The cat is called Felix. Its temperament is friendly. It weighs 6 kgs.



```python
felix.is_friendly()
```




    True




```python
felix.if_weighs_more(5)
```




    True



## Inheritance

Ok, so imagine that we have cats with special needs in our cattery. One such type of cat is older cats. Let's pretend that older cats have some property that younger cats don't have, which is that they get illnesses that require specific care plans. We could write an entire new Older_Cat class from scratch. However, this will create redundancy as we will be repeating all of the instance variables and methods as in the Cat class.

We can get around this using something called **inheritance**. Inheritance is where a class (called the **child**) can inherit the properties of another class (called the **parent**). In our case, the Cat class is the parent, and the Older_Cat class is, ironically, the child. Below is how we would begin an inherited class. You can see that instead of passing the argument object, we pass the object Cat to this class.


```python
class Older_Cat(Cat):
    '''A Cat aged over 8 years with name, temperament and weight components.'''
    
    pass
```

We add in the `__init__` method to this child class. You can see it works a little differently than in the parent. Instead of adding each of the Cat instance variables one-by-one to the Older_Cat class, we instead call the `__init__` method from Cat within the class.


```python
class Older_Cat(Cat):
    '''A Cat aged over 8 years with name, temperament and weight components.'''
    
    def __init__(self, name, temperament, weight):
        '''A new Older_Cat with a name (string), temperament (string) and weight (float).'''
        
        Cat.__init__(self, name, temperament, weight)

rosebud = Older_Cat("Rosebud", "cranky", 4)
print rosebud
```

    The cat is called Rosebud. Its temperament is cranky. It weighs 4 kgs.



```python
rosebud.is_friendly()
```




    False




```python
rosebud.if_weighs_more(5)
```




    False



Ok, so the reason we have created this child class is to add in additional instance variables and methods. Below you can see that I have added the additional instance variable illness into the `__init__` method in the exact same way we added them to the parent class orginally. You can also see I have created a new method specific to Older_Cat that uses illness, called `has_illness`. This method returns a description of whether the Older_Cat has an illness, and if so, what it is and to consult the care plan.


```python
class Older_Cat(Cat):
    '''A Cat aged over 8 years with name, temperament and weight components.'''
    
    def __init__(self, name, temperament, weight, illness):
        '''A new Older_Cat with a name (string), temperament (string) and weight (float).'''
        
        Cat.__init__(self, name, temperament, weight)
        self.illness = illness
        
    def has_illness(self):
        '''Describes if the Older_Cat has any health conditions.'''
        if self.illness != "none":
            print "%s has %s. Please consult care plan." \
            % (self.name, self.illness)
        else:
            print "%s has no health conditions." % self.name

rosebud = Older_Cat("Rosebud", "cranky", 4, "arthritis")
print rosebud
```

    The cat is called Rosebud. Its temperament is cranky. It weighs 4 kgs.



```python
rosebud.has_illness()
```

    Rosebud has arthritis. Please consult care plan.


I hope this has been a helpful overview of OOP and has helped you understand this really useful concept in programming. As I said at the beginning of this article, I relied heavily on the wonderful [**Practical Programming: An Introduction to Computer Science Using Python**](http://www.amazon.com/Practical-Programming-Introduction-Pragmatic-Programmers/dp/1934356271), which gives a much more comprehensive coverage of this topic.

Finally, the full code used to create the figures in this post is located in this [gist on my Github page](https://gist.github.com/t-redactyl/d9c906e11391d0885978).
