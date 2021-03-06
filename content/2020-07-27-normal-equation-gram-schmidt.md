---
title: Simplifying the normal equation with Gram-Schmidt  
date: 2020-07-27   
comments: false  
tags: maths, linear algebra, python  
keywords: python, data science, linear algebra, linear regression, normal equation, least squares, numpy
---

In the [last post]({filename}2020-07-13-linear-algebra-ols-regression.md) I talked about how to find the coefficients that give us the line of best fit for a OLS regression problem using the normal solution. The core of this approach is the equation:

$$
X^TXb = X^Ty
$$

The way we solved this in the previous post was to pull out the system of simultaneous equations and solve these for $b$. However, a more straightforward way is to rewrite the equation by "dividing" both sides by $X^TX$, so that we are directly solving for $b$. If you remember back to [this post]({filename}2020-06-15-matrix-inversion.md), we need to multiply both sides of the equation by the inverse of $X^TX$ in order to do this:

$$
\begin{aligned}
(X^TX)^{-1}(X^TX)b &= (X^TX)^{-1}X^Ty \\
Ib &= (X^TX)^{-1}X^Ty \\
b &= (X^TX)^{-1}X^Ty
\end{aligned}
$$

The issue is that this equation now involves taking the inverse of a matrix, which is computationally expensive. However, there is a way of getting rid of this whole inversion step by using a special type of matrix called an [orthonormal matrix](https://en.wikipedia.org/wiki/Orthogonal_matrix), which we can calculate using the [Gram–Schmidt process](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process).

## The advantage of orthonormal matrices

An orthonormal matrix is one where every column vector is an orthogonal unit vector. We have seen orthogonal vectors before: this simply means that the dot product of every pair of vectors in the matrix is 0. Unit vectors are similarly straightforward - they are just vectors with a length of 1. Putting this together, an orthonormal matrix is thus one where every column vector has a length of one and is orthogonal with every other column vector in the matrix.

Why are orthonormal matrices so great for helping us find $b$? When we multiply an orthonormal matrix $Q$ by its transpose $Q^T$, we get the identity matrix; in other words, $Q^TQ = I$. Does the lefthand side of this equation look familiar? It's the exact part of $X^TXb = X^Ty$ that we tried to get rid of earlier by multiplying by the inverse. If we were able to use the orthonormal form of $X$, we could isolate $b$ without having to calculate the inverse at all, by simply calculating $b = Q^Ty$!

Before we get into how to convert our matrix $X$ into $Q$, let's have a look at why $Q^TQ = 0$. Let's take an example orthonormal vector:

$$
Q = \begin{bmatrix} \frac{4}{5} & \frac{1}{5} \\[4pt] \frac{2}{5} & -\frac{2}{5} \\[4pt] \frac{1}{5} & \frac{4}{5} \\[4pt] \frac{2}{5} & -\frac{2}{5} \end{bmatrix}
$$

Calculating $Q^TQ$ will give us a $2 \times 2$ matrix, with the following components:

$$
Q^TQ = \begin{bmatrix} q_1^Tq_1 & q_1^Tq_2 \\[4pt] q_2^Tq_1 & q_2^Tq_2 \end{bmatrix}
$$

Any vector multiplied by itself will give the squared [length of that vector](https://onlinemschool.com/math/library/vector/length/). In the case of a unit vector, the squared length is 1, as seen by the result of calculating $q_1^Tq_1$:

$$
\begin{aligned}
q_1^Tq_1 &= \begin{bmatrix} \frac{4}{5} \\[4pt] \frac{2}{5} \\[4pt] \frac{1}{5} \\[4pt] \frac{2}{5} \end{bmatrix} \cdotp \begin{bmatrix} \frac{4}{5} & \frac{2}{5} & \frac{1}{5} & \frac{2}{5} \end{bmatrix} \\
&= (\frac{4}{5})^2 + (\frac{2}{5})^2 + (\frac{1}{5})^2 + (\frac{2}{5})^2 \\
&= \frac{16}{25} + \frac{4}{25} + \frac{1}{25} + \frac{4}{25} \\
&= \frac{25}{25} = 1
\end{aligned}
$$

This means we will always get 1's in this matrix whenever we take the dot product of one of the columns of $Q$ with itself; that is, along the diagonals of the matrix. For the other components of the matrix, we are now taking the dot product of two orthogonal vectors, meaning the result will be 0.

$$
\begin{aligned}
q_1^Tq_1 &= \begin{bmatrix} \frac{4}{5} \\[4pt] \frac{2}{5} \\[4pt] \frac{1}{5} \\[4pt] \frac{2}{5} \end{bmatrix} \cdotp \begin{bmatrix} \frac{1}{5} & -\frac{2}{5} & \frac{4}{5} & -\frac{2}{5} \end{bmatrix} \\
&= \frac{4}{25} - \frac{4}{5} + \frac{4}{5} - \frac{4}{5} = 0
\end{aligned}
$$

Combining this, we get:

$$
\begin{aligned}
Q^TQ &= \begin{bmatrix} \frac{4}{5} & \frac{2}{5} & \frac{1}{5} & \frac{2}{5} \\[4pt] \frac{1}{5} & -\frac{2}{5} & \frac{4}{5} & -\frac{2}{5} \end{bmatrix} \begin{bmatrix} \frac{4}{5} & \frac{1}{5} \\[4pt] \frac{2}{5} & -\frac{2}{5} \\[4pt] \frac{1}{5} & \frac{4}{5} \\[4pt] \frac{2}{5} & -\frac{2}{5} \end{bmatrix} \\
&= \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I
\end{aligned}
$$

## Turning $X$ into an orthonormal matrix

So how do we convert $X$ into an orthonormal matrix $Q$? The first step of the Gram–Schmidt process is to find **orthogonal** vectors, and the method we use is an extension of how we found $\hat y$ and $e$ when trying to solve least squares for regression in the previous post. Those calculations essentially split $y$ into two orthogonal vectors: $\hat y$ which lay on the plane of the column space $C(X)$, and $e$, the vector orthogonal to $C(X)$.

We can think of the relationship between the first and second columns of $X$ as equivalent to the relationship between $C(X)$ and $y$. Let's call these columns $f$ and $g$, and their orthogonal versions $F$ and $G$. Essentially, we keep $f$ as is, so $f = F$. We then try to find the part of $g$ that lies on $F$ and the part that is orthogonal to it, $G$. 

In least squares, we would calculate $\hat y$ using:

$$
\hat y = X(X^TX)^{-1}X^Ty
$$

Similarly we can calculate the part of $g$ that lies on $F$ using:

$$
F(F^TF)^{-1}F^Tg
$$

We can then subtract this from $g$ to get $G$:

$$
G = g - F(F^TF)^{-1}F^Tg
$$

<img src="/figure/linear-algebra-5.png" title="Creating orthogonal vectors" style="display: block; margin: auto;" />

For this reason, we can obviously only find orthogonal vectors when the vectors of $X$ are independent: if they are not, then _all_ of $g$ lies on the line described by $F$, and there would be no orthogonal part left behind.

Finally, as we're now dealing entirely with vectors instead of a matrix, the terms $(F^TF)$ and $(F^Tg)$ simplify to scalars:

$$
\begin{aligned}
G &= g - F\frac{1}{F^TF}F^Tg \\
&= g - \frac{F^Tg}{F^TF}F
\end{aligned}
$$

Let's try this out with a matrix $X$:

$$
X = \begin{bmatrix} 1 & 2 \\ 1 & 0 \\ 1 & 2 \\ 1 & 0 \end{bmatrix}
$$

$f = F = (1, 1, 1, 1)$ and $g = (2, 0, 2, 0)$. We can now use our above formula to calculate $G$:

$$
G = \begin{bmatrix} 2 \\ 0 \\ 2 \\ 0 \end{bmatrix} - \frac{4}{4}\begin{bmatrix} 1 \\ 1 \\ 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \\ -1 \\ 1 \\ -1 \end{bmatrix}
$$

And voilà! We now have two orthogonal vectors, $(1, 1, 1, 1)$ and $(1, -1, 1, -1)$. The final step is taking these from orthogonal to orthonormal. To do this, we simply divide each vector by its length:

$$
F = \frac{1}{2}\begin{bmatrix} 1 \\ 1 \\ 1 \\ 1 \end{bmatrix} \quad\quad 
G = \frac{1}{2}\begin{bmatrix} 1 \\ -1 \\ 1 \\ -1 \end{bmatrix} \quad\quad 
Q = \begin{bmatrix} \frac{1}{2} & \frac{1}{2} \\[4pt] \frac{1}{2} & -\frac{1}{2} \\[4pt] \frac{1}{2} & \frac{1}{2} \\[4pt] \frac{1}{2} & -\frac{1}{2}\end{bmatrix}
$$

Let's complete the calculation by checking that $Q^TQ$ indeed equals $I$:

$$
Q^TQ = \begin{bmatrix} \frac{1}{2} & \frac{1}{2} & \frac{1}{2} & \frac{1}{2} \\[4pt] \frac{1}{2} & -\frac{1}{2} & \frac{1}{2} & -\frac{1}{2}\end{bmatrix} \begin{bmatrix} \frac{1}{2} & \frac{1}{2} \\[4pt] \frac{1}{2} & -\frac{1}{2} \\[4pt] \frac{1}{2} & \frac{1}{2} \\[4pt] \frac{1}{2} & -\frac{1}{2}\end{bmatrix}
= \begin{bmatrix} 4(\frac{1}{4}) & 2(\frac{1}{4}) - 2(\frac{1}{4}) \\[4pt] 2(\frac{1}{4}) - 2(\frac{1}{4}) & 4(\frac{1}{4}) \end{bmatrix} 
= \begin{bmatrix} 1 & 0 \\[4pt] 0 & 1 \end{bmatrix}
$$

## What happens if you have more than two vectors?

This method generalises out to whatever number of independent columns your matrix has. For each additional vector, we just need to subtract the parts of this vector that lie on $F$ and $G$ (and $H$ and $J$ and ...). Extending the formula is very easy. Let's say we're trying to solve for a third vector $H$, after solving for $F$ and $G$ as above:

$$
H = h - \frac{F^Th}{F^TF}F - \frac{G^Th}{G^TG}G
$$

You can easily see the pattern. In getting rid of the part of $g$ that lay on $F$, we subtracted $\frac{F^Tg}{F^TF}F$. Here we subtract $\frac{F^Th}{F^TF}F$. This idea transfers directly to subtracting the component that lies on $G$. For each additional vector, we just extend this pattern, making sure to subtract the part that lies on _each_ previous vector.

## Using $Q$ to solve linear regression

Now we know how to calculate our orthonormal vector $Q$, we can finally use it to obtain our regression coefficients $b$ and our predicted values $\hat y$. In the last post, we used a small dataset to demonstrate the normal equation, and showed how to get the $b$'s and $\hat y$ using this method. We'll use this same example to demonstrate how to do the same using an orthonormal matrix.

Firstly, let's load in the required packages, and create our dataset matrix $X$ and outcome vector $y$.


```python
import math
import numpy as np
from numpy.linalg import qr, inv, norm

X = np.array([[1, 1], [1, 2], [1, 3]])
y = np.array([[3], [6], [7]])
```

In order to calculate our orthonormal matrix, we can use the `qr` method from `numpy.linalg`.


```python
Q, R = qr(X)
Q
```




    array([[-5.77350269e-01,  7.07106781e-01],
           [-5.77350269e-01,  5.55111512e-17],
           [-5.77350269e-01, -7.07106781e-01]])



Let's confirm that `numpy` is giving us the same values that we would using the equations we defined above:


```python
# Calculate G
F_T_g = X[:, 0].transpose().dot(X[:, 1])
F_T_F = X[:, 0].transpose().dot(X[:, 0])
G = X[:, 1] - (F_T_g/F_T_F)*X[:, 0]

# Turn F and G into unit vectors
F = X[:, 0] / norm(X[:, 0])
G = G / norm(G)

np.column_stack((F, G))
```




    array([[ 0.57735027, -0.70710678],
           [ 0.57735027,  0.        ],
           [ 0.57735027,  0.70710678]])



We can see we have the same values, albeit with the signs reversed.

We can now calculate our $b$'s by using our simplified equation, $b = Q^Ty$:


```python
b = Q.transpose().dot(y)
b
```




    array([[-9.23760431],
           [-2.82842712]])



As you can see, these are a different set of coefficients from what you would get using $X$. However, we can get the same $\hat y$ by calculating $Qb$:


```python
y_hat = Q.dot(b)
y_hat
```




    array([[3.33333333],
           [5.33333333],
           [7.33333333]])



As you can see, these are the exact same $\hat y$ values that we obtained using the normal equation with $X$, and what `sklearn` produced for us in the last post.