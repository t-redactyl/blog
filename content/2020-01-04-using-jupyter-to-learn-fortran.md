---
title: Using Jupyter to learn Fortran
date: 2020-01-04  
comments: false  
tags: Fortran, Jupyter, programming tips
keywords: programming, fortran 95, bash, jupyter
---

Having heard people talk about the performance improvements that Fortran gives over R or Python, I got curious - how hard is it to learn? Turns out that more recent standards of Fortran, such as Fortran 95, are pretty easy to pick up, so I started working my way through [this excellent tutorial](http://www.fortrantutorial.com/). However, while I started out by writing separate scripts, I got really annoyed not being able to take notes alongside my scripts or keep related scripts together in the same document. As such, I started looking at my options for running my Fortran scripts within a Jupyter notebook.

## Option 1: Run your notebook from a Fortran kernel

The first option is to simply install a Fortran kernel for Jupyter, which means all of your cells will automatically run Fortran code. Peter Hill has written a very easy to use and install Fortran kernel, which you can find [here](https://github.com/ZedThree/jupyter-fortran-kernel) along with instructions on how to run it. Once you have installed it, you simply need to select `Fortran` as your kernel type when you create a new notebook, and you're good to go!

Let's see how it runs with a simple program that just prints some hardcoded text.


```python
program simple_print
    print *,'This Fortran program just prints a line.'
end program simple_print
```

     This Fortran program just prints a line.


Very nice! However, we run into problems when we try to run something that requires some user input. Let's have a look at a program that calculates people's ages based on their year of birth.


```python
program get_age
    real :: year, age
    print *, 'What year were you born?'
    read *, year
    age = 2020 - year
    print *, 'Your age is', age
end program get_age
```

     What year were you born?


    At line 5 of file /var/folders/jq/j1k41wzs0ddflbrr33twdnm00000gn/T/tmptil2332r.f90 (unit = 5, file = 'stdin')
    Fortran runtime error: End of file
    
    Error termination. Backtrace:
    #0  0x107c406a9
    #1  0x107c41365
    #2  0x107c41ac9
    #3  0x107d0914b
    #4  0x107d03b69
    #5  0x107c3ad30
    #6  0x107c3ae0e
    [Fortran kernel] Executable exited with code 2

You can see that because the Fortran kernel is trying to compile and execute the program in one go, it fails when it does not receive all of the expected inputs (in this case, a single number). Luckily, there is a pretty easy way to get around this using the pre-existing magics built into Jupyter.

## Option 2: Compile and execute Fortran scripts using Bash cells

A pretty simple workaround is to write the Fortran scripts to file within Jupyter and then execute using a Bash cell. We can do this using a couple of magics: `%%writefile` to create the scripts, and then `%%bash` to create our bash cell. Note that you need to do this within your Python kernel, as the Fortran kernel doesn't recognise the `%%bash` magic. Let's try our program to calculate age again.


```python
%%writefile get_age.f95

program get_age
    real :: year, age
    print *, 'What year were you born?'
    read *, year
    age = 2020 - year
    print *, 'Your age is', age
end program get_age
```

    Writing get_age.f95


So far, so good - it hasn't thrown an error like last time. Now we can compile our script using `gfortran -ffree-form <script name>`, and execute the resulting `a.out` file. We also need to include any required inputs at the end of the cell, each on a separate line. You can see we've put 1984 as our input for the year for our age program.


```bash
%%bash

gfortran -ffree-form get_age.f95
./a.out
1984
```

     What year were you born?
     Your age is   36.0000000    


While it might not be as nice as the interactive experience of executing this script at the command line, it is a great way to keep all of your work together while you are learning. I hope you've found this a useful guide to taking advantage of Jupyter while learning Fortran!