---
title: Working with matrices: inversion   
date: 2020-06-15   
comments: false  
tags: maths, linear algebra, python  
keywords: python, data science, linear algebra, matrix inversion, identity matrix, numpy
---

Today we will continue our discussion of the basic operations you can do with matrices in linear algebra. In the [last post]({filename}2020-06-01-matrices-addition-subtraction-and-multiplication.md) we covered addition, subtraction, scalar multiplication and matrix multiplication. This week, we'll cover matrix inversion.

So far we've seen matrix addition, subtraction and multiplication, but what about matrix division? Well, technically there is no such thing! The closest thing we have is multiplying a matrix by its inverse. Before we get into what an inverse is, we need to pause to describe a special matrix called the **identity matrix**. 

### Identity matrix

The identity matrix is simply a square matrix which has 0 everywhere except along the diagonal, where it instead contains 1's. For example, a $2 \times 2$ identity matrix would be:

$$
I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
$$

The identity matrix can be thought of as the equivalent of 1 for matrices, in the sense that if you multiply any number by 1, the number will remain unchanged. Similarly, if you multiply any matrix by its identity matrix, that matrix will remain unchanged. Let's see this with a new matrix $A$:

$$
A = \begin{bmatrix} 4 & 3 \\ 6 & 5 \end{bmatrix}
$$

If we multiply $A$ by $I$, we get:
$$
\begin{aligned}
AI &= \begin{bmatrix} 4 & 3 \\ 6 & 5 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}\\
&= \begin{bmatrix} (4 \times 1 + 3 \times 0) & (4 \times 0 + 3 \times 1) \\ (6 \times 1 + 5 \times 0) & (6 \times 0 + 5 \times 1) \end{bmatrix}\\
&= \begin{bmatrix} 4 & 3 \\ 6 & 5 \end{bmatrix}
\end{aligned}
$$

In order to do this in Numpy, we can generate an identity matrix using the `identity` function, passing the number of rows (and columns) as the argument.


```python
import numpy as np

A = np.array([[4, 3], [6, 5]])
I = np.identity(2)
I
```




    array([[1., 0.],
           [0., 1.]])




```python
AI = A.dot(I)
AI
```




    array([[4., 3.],
           [6., 5.]])



Unlike most matrix multiplications, we get the same result if we multiply $AI$ or $IA$, as both results just simplify to $A$: $AI = IA = A$. This means that matrix multiplication by the identity is commutative.


```python
IA = I.dot(A)
IA
```




    array([[4., 3.],
           [6., 5.]])



### Inverse of a matrix

The inverse of a matrix is another matrix by which you multiply that matrix to get the identity matrix. This is comparable to the inverse with numbers, where the [inverse of a number is what you multiply that number by to get 1](https://www.mathsisfun.com/numbers/inverse.html). You may have noticed that I referred to **the** inverse of a matrix. This is because every matrix that can be inverted has only one unique inverse. The inverse of the matrix is indicated by writing the name of the original matrix with a little $-1$ superscript ([which is exactly the same notation as for the multiplicative inverse for numbers](https://www.mathsisfun.com/numbers/inverse.html)). For example, the matrix $Z$ would have the inverse $Z^{-1}$.

How do we find the inverse of a matrix? For $2 \times 2$ matrices it is straightforward. In order to do so, we transform our original matrix in the following way:
$$
M^{-1} = \frac{1}{m_{11}m_{22} - m_{12}m_{21}} \begin{bmatrix}m_{22} & -m_{12}\\-m_{21} & m_{11}\end{bmatrix}
$$

This looks a little complicated, but let's break it down. Have a look at the matrix component of this equation. You can see that we have swapped the positions of the first and last elements in the matrix, so that the element that was in $m_{11}$ is now in $m_{22}$, and vice versa. $m_{12}$ and $m_{21}$ stay in their original spots, but we multiply them by $-1$. We then calculate something called the determinant, which is basically a number we divide this reorganised matrix by to get the inverse. This is calculated by the formula $m_{11}m_{22} - m_{12}m_{21}$, and if we multiply our reorganised matrix by $1$ divided by this number, we get the inverse.

Let's try this with a concrete example, using our matrix $A$. In order to get the inverse of $A$, or $A^{-1}$, we do the following:
$$
\begin{aligned}
A^{-1} &= \frac{1}{4 \times 5 - 3 \times 6} \begin{bmatrix}5 & -3 \\ -6 & 4 \end{bmatrix}\\
&= \frac{1}{2} \begin{bmatrix} 5 & -3 \\ -6 & 4 \end{bmatrix}\\
&= \begin{bmatrix}(\frac{1}{2} \times 5) & (\frac{1}{2} \times -3) \\[4pt] (\frac{1}{2} \times -6) & (\frac{1}{2} \times 4) \end{bmatrix}\\
&= \begin{bmatrix} \frac{5}{2} & -\frac{3}{2} \\ -3 & 2 \end{bmatrix}
\end{aligned}
$$

And voilà, we have our matrix inversion! Let's just double check it worked by multiplying $A$ by it:
$$
\begin{aligned}
AA^{-1} &= \begin{bmatrix}(4 \times \frac{5}{2} + 3 \times -3) & (4\times-\frac{3}{2} + 3\times2)\\[4pt] (6\times\frac{5}{2} + -3 \times 5) & (6\times-\frac{3}{2} + 5\times2)\end{bmatrix}\\
&= \begin{bmatrix}(10-9) & (-6 + 6)\\(15-15) & (-9 + 10)\end{bmatrix}\\
&= \begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}
\end{aligned}
$$

Unfortunately, finding the inverse of matrices that are bigger than $2 \times 2$ is less straightforward. There are a few methods to do it, but they are beyond the scope of this blog post. A couple of nice (and gentle) introductions to these can be found [here](https://www.mathsisfun.com/algebra/matrix-inverse-row-operations-gauss-jordan.html) and [here](https://www.mathsisfun.com/algebra/matrix-inverse-minors-cofactors-adjugate.html).

In order to calculate the inverse of a matrix in Numpy, we can use the `inv` function from the `linalg` subpackage.


```python
from numpy.linalg import inv

Ainv = inv(A)
Ainv
```




    array([[ 2.5, -1.5],
           [-3. ,  2. ]])



Let's check it is the correct inverse by multiplying it by $A$:


```python
np.round(A.dot(Ainv))
```




    array([[1., 0.],
           [0., 1.]])



Like with multiplication by the identity matrix, multiplication by the inverse is also commutative. This is because, as we just saw above, multiplying $A$ by its inverse simplifies to $I$, so $AA^{-1} = A^{-1}A = I$. Let's confirm this is true using Numpy:


```python
np.round(Ainv.dot(A))
```




    array([[1., 0.],
           [0., 1.]])



You've probably guessed from what I said earlier that not all matrices are invertible. Firstly, only square matrices are invertible. In addition, if any of the columns are a combination of any of the other columns in the matrix, then you cannot invert the matrix (in other words, when any of the columns are a linear combination of any of the other columns). Let's see why this is the case. Let's say we have a matrix $B$, where the second column is a multiple of the first column:

$$
B = \begin{bmatrix}1 & 2\\3 & 6\end{bmatrix}
$$

Let's now try to calculate the inverse, $B^{-1}$:

$$
\begin{aligned}
B^{-1} &= \frac{1}{(1 \times 6) - (2 \times 3)}\begin{bmatrix}6 & -2\\-3 & 1\end{bmatrix}\\ 
&= \frac{1}{6 - 6}\begin{bmatrix}6 & -2\\-3 & 1\end{bmatrix}\\ 
&= \frac{1}{0}\begin{bmatrix}6 & -2\\-3 & 1\end{bmatrix}
\end{aligned}
$$

But wait! Our determinant is $\frac{1}{0}$, which is undefined. This means we can't go any further in solving this equation, making our matrix uninvertible. Such non-invertible matrices are called "singular" or "degenerate" matrices.

Let's see what happens when we try to pass our matrix $B$ to Numpy's `inv` function:


```python
B = np.array([[1, 2], [3, 6]])
inv(B)
```


    ---------------------------------------------------------------------------

    LinAlgError                               Traceback (most recent call last)

    <ipython-input-18-ae75e56b5e72> in <module>
          1 B = np.array([[1, 2], [3, 6]])
    ----> 2 inv(B)
    

    <__array_function__ internals> in inv(*args, **kwargs)


    ~/Documents/Blog-posts/.maths_venv/lib/python3.7/site-packages/numpy/linalg/linalg.py in inv(a)
        545     signature = 'D->D' if isComplexType(t) else 'd->d'
        546     extobj = get_linalg_error_extobj(_raise_linalgerror_singular)
    --> 547     ainv = _umath_linalg.inv(a, signature=signature, extobj=extobj)
        548     return wrap(ainv.astype(result_t, copy=False))
        549 


    ~/Documents/Blog-posts/.maths_venv/lib/python3.7/site-packages/numpy/linalg/linalg.py in _raise_linalgerror_singular(err, flag)
         95 
         96 def _raise_linalgerror_singular(err, flag):
    ---> 97     raise LinAlgError("Singular matrix")
         98 
         99 def _raise_linalgerror_nonposdef(err, flag):


    LinAlgError: Singular matrix


Numpy tells us clearly that this matrix is non-invertible, exactly for the reasons we talked about above.

That caps off our discussion of matrix inversion. In the next post, we'll finish up this series on matrix operations by talking about powers of a matrix and matrix transposition.