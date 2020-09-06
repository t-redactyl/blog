---
title: Working with matrices: powers and transposition   
date: 2020-06-29   
comments: false  
tags: maths, linear algebra, python  
keywords: python, data science, linear algebra, matrix transposition, powers of a matrix, numpy
---

Today, we'll complete our series on basic matrix operations by covering powers of a matrix and matrix transposition. In the previous posts, we covered [matrix addition, subtraction and multiplication]({filename}2020-06-01-matrices-addition-subtraction-and-multiplication.md) and [matrix inversion]({filename}2020-06-15-matrix-inversion.md).

## Powers of a matrix

Say we have a number $a$, and we're asked to solve $a^2$. Well, this is easy: we just multiply $a$ by itself to get $a \times a$. Powers of matrices work in exactly the same way. If we take a matrix $A$, we can get $A^2$ by multiplying $A$ by itself:

$$
A^2 = AA = \begin{bmatrix}4 & 3\\6 & 5\end{bmatrix}\begin{bmatrix}4 & 3\\6 & 5\end{bmatrix} = \begin{bmatrix}34 & 27\\54 & 43\end{bmatrix}
$$

You can probably guess that, because of the way that matrix multiplication works, we can only raise square matrices to a power. We can raise square matrices to any (positive) power in the same way: if we want to get the cube of $A$, or $A^3$, we multiply the matrix by itself 3 times, if we want $A^4$, we multiply it by itself 4 times, and so on.

In Numpy, we can use the `matrix_power` function from the `linalg` subpackage to calculate the power of a matrix. The first argument is the matrix, and the second is the power you'd like to raise the matrix to.


```python
import numpy as np
from numpy.linalg import matrix_power

A = np.array([[4, 3], [6, 5]])
matrix_power(A, 2)
```




    array([[34, 27],
           [54, 43]])



Powers of matrices follow the [same rules as do powers of a number](https://www.mathplanet.com/education/algebra-1/exponents-and-exponential-functions/properties-of-exponents). Let's have a look at a couple of examples of these. Say we have two [integers](https://www.mathsisfun.com/definitions/integer.html), $m$ and $n$. If we have two matrices, $A^m$ and $A^n$ and we multiply them, we get $A^mA^n = A^{m+n}$. Similarly, if we have the matrix $A^m$ and we raise it to $n$, then we get $(A^m)^n = A^{mn}$.

Let's try this out in Numpy, by comparing the results of $A^5$ to $A^2A^3$:


```python
A_5 = matrix_power(A, 5)
A_5
```




    array([[22930, 18237],
           [36474, 29009]])




```python
A_2 = matrix_power(A, 2)
A_3 = matrix_power(A, 3)

A_2.dot(A_3)
```




    array([[22930, 18237],
           [36474, 29009]])



We can also raise matrices to negative powers. We've already seen an example of this with the inverse of a matrix, which is written as $A^{-1}$. In order to raise a matrix to the power of $-2$, we simply need to multiply the inverse by itself. This logic can then be extended in the same way as we did for raising the matrix to a positive power. 

Let's see this in Numpy by comparing the function to calculate the inverse to raising our matrix to the power of `-1`. As we can see, they are exactly the same.


```python
from numpy.linalg import inv

inv(A)
```




    array([[ 2.5, -1.5],
           [-3. ,  2. ]])




```python
matrix_power(A, -1)
```




    array([[ 2.5, -1.5],
           [-3. ,  2. ]])



## Matrix transposition and symmetrical matrices

The final thing we will cover is matrix transposition. This is simply what happens if you flip the rows and columns of a matrix. Let's have a look at this with matrix $B$:

$$
B = \begin{bmatrix}1 & 2\\3 & 4\\5 & 6\end{bmatrix}
$$

What would the transpose of $B$ (denoted by $B^T$) look like? Well, it is simple as taking the rows of $B$ and turning them into the columns of $B^T$ (or vice versa):

$$
B^T = \begin{bmatrix}1 & 3 & 5\\2 & 4 & 6\end{bmatrix}
$$

And what would the transpose of $B^T$ look like (in other words, what is $(B^T)^T)$? Well, if we flip the rows and columns again, we just end up back at our original matrix! In other words, $(B^T)^T = B$.

In order to transpose a matrix using Numpy, we use the `transpose` function on that matrix:


```python
B = np.array([[1, 2], [3, 4], [5, 6]])
B_T = B.transpose()
B_T
```




    array([[1, 3, 5],
           [2, 4, 6]])



We can also reverse the transposition by calling `transpose` on our new transposed matrix, `B_T`:


```python
B_T.transpose()
```




    array([[1, 2],
           [3, 4],
           [5, 6]])



As usual, square matrices behave a little differently to non-square matrices, in that the diagonal values of the matrix don't move when you take the transpose of the matrix. If we go back to our square matrix $A$, and take the transpose, we end up with:

$$
A^T = \begin{bmatrix}4 & 6\\3 & 5\end{bmatrix}
$$

You can see that the values in $a_{12}$ and $a_{21}$ have moved, but the values on the diagonals ($a_{11}$ and $a_{22}$) haven't. This means that if values that are diagonally opposite to each other in a square matrix are equal (say, if $a_{12} = a_{21}$ in the example above), then the transpose of the matrix would be identical to the matrix. Such matrices are called **symmetrical matrices**. Let's have a look at an example. Let's say we have a $3 \times 3$ matrix, $C$, which is symmetrical. Because of this:

$$
C = C^T = \begin{bmatrix}1 & 4 & 5\\4 & 2 & 6\\5 & 6 & 3\end{bmatrix}
$$

This matrix might not look symmetrical at a first glance. However, one way to see that it is really symmetrical is to compare the first row and the first column (and the second row and second column, and the third row and third column). You can see that they are identical, which means that it doesn't matter whether these elements function as a row or a column: the result will be the same. Another way to see this a bit more explicitly is to compare those elements are diagonal to each other in the matrix, as we spoke about above. We can see that $c_{12} = c_{21} = 4$, $c_{13} = c_{31} = 5$ and $c_{23} = c_{32} = 6$.

I hope these posts have given you a solid overview of the ways you can work with matrices. In the next post, we'll build on this by looking at the linear algebra approach to solving linear regression problems.