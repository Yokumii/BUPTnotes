---
description: 讲解二次型的合同变换与标准形、正定性判别、约束极值，以及 Hessian 矩阵在极值问题中的应用。
---

# 二次型与正定矩阵

二次型把对称矩阵变成一个实值函数。通过合同变换，它可以化为平方和之差；其正负号结构决定曲面的类型、约束极值和多元函数的局部形态。

## 二次型与合同变换

$n$ 元二次型可写为

$$
f(x)=x^{\mathrm T}Ax,
$$

其中总可以取 $A$ 为实对称矩阵。若原式中的交叉项为 $c_{ij}x_ix_j$，则

$$
a_{ij}=a_{ji}=\frac{c_{ij}}2.
$$

作可逆线性替换 $x=Cy$，有

$$
f(x)=y^{\mathrm T}(C^{\mathrm T}AC)y.
$$

若

$$
B=C^{\mathrm T}AC,
$$

则称 $A$ 与 $B$ 合同。合同变换保持二次型的秩与定性。

## 标准形与规范形

把实二次型化为

$$
f=d_1y_1^2+\cdots+d_ry_r^2,
\qquad d_i\ne0,
$$

称为标准形。进一步缩放变量，可得规范形

$$
f=z_1^2+\cdots+z_p^2
-z_{p+1}^2-\cdots-z_{p+q}^2,
$$

其中 $p+q=r=\operatorname{rank}(A)$。

正平方项个数 $p$ 称为正惯性指数，负平方项个数 $q$ 称为负惯性指数，$p-q$ 称为符号差。

!!! info "Sylvester 惯性定律"
    实二次型经过任意可逆线性替换后，正惯性指数和负惯性指数都不变。因此规范形中正、负平方项的个数是二次型本身的性质，而不是化简方法的偶然结果。

常用化简方法有：

1. 对实对称矩阵作正交对角化；
2. 配方法；
3. 对矩阵同时作同类型的行、列初等变换。

正交对角化给出

$$
A=Q\Lambda Q^{\mathrm T},
\qquad x=Qy,
$$

从而

$$
f=\lambda_1y_1^2+\cdots+\lambda_ny_n^2.
$$

## 几何意义与约束极值

正交变换保持长度和夹角，因此把对称矩阵对角化，在几何上相当于旋转或反射坐标系，使坐标轴对准曲面的主轴。

对单位球面 $\|x\|=1$，Rayleigh 商为

$$
R_A(x)=\frac{x^{\mathrm T}Ax}{x^{\mathrm T}x}.
$$

若实对称矩阵 $A$ 的特征值按

$$
\lambda_1\le\cdots\le\lambda_n
$$

排列，则

$$
\lambda_1\le R_A(x)\le\lambda_n.
$$

上下界分别在最小、最大特征值对应的单位特征向量处取得。因此

$$
\min_{\|x\|=1}x^{\mathrm T}Ax=\lambda_1,
\qquad
\max_{\|x\|=1}x^{\mathrm T}Ax=\lambda_n.
$$

这也是用 Lagrange 乘子求约束极值时出现特征值方程的原因：

$$
\nabla(x^{\mathrm T}Ax)=2Ax=2\lambda x.
$$

## 正定性

实对称矩阵 $A$ 称为正定矩阵，若对任意 $x\ne0$，

$$
x^{\mathrm T}Ax>0.
$$

相应地：

- $x^{\mathrm T}Ax\ge0$：半正定；
- $x^{\mathrm T}Ax<0$：负定；
- $x^{\mathrm T}Ax\le0$：半负定；
- 既能取正值又能取负值：不定。

对实对称矩阵，下列条件等价：

1. $A$ 正定；
2. $A$ 的全部特征值为正；
3. $A$ 合同于 $I$；
4. 存在可逆矩阵 $C$，使 $A=C^{\mathrm T}C$；
5. $A$ 的全部顺序主子式为正；
6. $A$ 的全部主子式为正。

其中顺序主子式为

$$
\Delta_k=\det A_{1:k,1:k},
\qquad k=1,\ldots,n.
$$

判据 $\Delta_1>0,\ldots,\Delta_n>0$ 称为 Sylvester 判据。

???+ note "Sylvester 判据的归纳思路"
    把矩阵写成

    $$
    A=\begin{pmatrix}A_{n-1}&a\\a^{\mathrm T}&a_{nn}\end{pmatrix}.
    $$

    由前 $n-1$ 个顺序主子式为正，归纳得到 $A_{n-1}$ 正定。再用合同消元把 $A$ 化为

    $$
    \begin{pmatrix}
    A_{n-1}&0\\
    0&a_{nn}-a^{\mathrm T}A_{n-1}^{-1}a
    \end{pmatrix}.
    $$

    最后一个 Schur 补的正性由 $\det A>0$ 得到。

负定矩阵可转化为 $-A$ 正定。等价地，其顺序主子式满足

$$
(-1)^k\Delta_k>0,
\qquad k=1,\ldots,n.
$$

!!! warning "半正定不能只看顺序主子式"
    对半正定矩阵，仅有所有顺序主子式非负并不充分。实对称矩阵半正定，当且仅当所有特征值非负，也当且仅当所有主子式非负；还等价于存在矩阵 $C$ 使 $A=C^{\mathrm T}C$，此时 $C$ 不必可逆。

## 常用构造与判定

### 分块对角矩阵

若 $A$、$B$ 都正定，则

$$
C=\begin{pmatrix}A&0\\0&B\end{pmatrix}
$$

也正定，因为

$$
\begin{pmatrix}x^{\mathrm T}&y^{\mathrm T}\end{pmatrix}
C
\begin{pmatrix}x\\y\end{pmatrix}
=x^{\mathrm T}Ax+y^{\mathrm T}By>0
$$

对任意非零 $(x,y)$ 成立。

### 对角占优

若实对称矩阵满足

$$
a_{ii}\ge\sum_{j\ne i}|a_{ij}|
$$

且 $a_{ii}\ge0$，则由 Gershgorin 圆盘定理可知其特征值非负，故 $A$ 半正定。若严格对角占优且 $a_{ii}>0$，则所有特征值为正，故 $A$ 正定。

## Hessian 矩阵与多元函数极值

对二阶可微函数 $F:\mathbb R^n\to\mathbb R$，Hessian 矩阵为

$$
H_F(x)=\left(\frac{\partial^2F}
{\partial x_i\partial x_j}\right)_{n\times n}.
$$

在驻点 $x_0$ 附近，二阶 Taylor 主项为

$$
\frac12h^{\mathrm T}H_F(x_0)h.
$$

因此：

- $H_F(x_0)$ 正定时，$x_0$ 是严格局部极小点；
- $H_F(x_0)$ 负定时，$x_0$ 是严格局部极大点；
- $H_F(x_0)$ 不定时，$x_0$ 是鞍点；
- 半正定或半负定时，二阶信息通常不足以判定。

特别地，若

$$
F(x)=\frac12x^{\mathrm T}Ax+b^{\mathrm T}x+c
$$

且 $A$ 正定，则 $F$ 严格凸，唯一全局极小点满足

$$
Ax+b=0.
$$
