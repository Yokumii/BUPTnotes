---
description: 介绍随机向量的联合、边缘与条件分布，随机变量独立性、函数分布及最大值和最小值的分布。
---

# 多维随机变量及其分布

多个随机变量同时出现时，研究重点从单个变量的取值规律转向变量之间的联合关系。本章依次介绍联合分布、边缘分布、条件分布、独立性以及随机向量函数的分布。

## 随机向量与联合分布

随机向量（Random Vector）
: 设 $X_1,X_2,\ldots,X_n$ 是同一样本空间上的随机变量，则

    $$
    \boldsymbol X=(X_1,X_2,\ldots,X_n)^{\mathrm T}
    $$

    称为 $n$ 维随机向量。

以下主要以二维随机向量 $(X,Y)$ 为例。

### 二维离散型随机变量

若 $(X,Y)$ 的全部可能取值至多可数，则它是二维离散型随机变量。其联合概率质量函数为

$$
p_{ij}=P(X=x_i,Y=y_j),\qquad i=1,2,\ldots,\quad j=1,2,\ldots
$$

并满足

$$
p_{ij}\ge 0,\qquad \sum_i\sum_j p_{ij}=1.
$$

联合概率也可以借助条件概率分解：

$$
P(X=x_i,Y=y_j)
=P(X=x_i)P(Y=y_j\mid X=x_i).
$$

### 联合分布函数

二维随机变量的联合分布函数定义为

$$
F(x,y)=P(X\le x,Y\le y).
$$

它具有以下性质：

1. 固定 $y$ 时，$F(x,y)$ 关于 $x$ 单调不减；固定 $x$ 时，$F(x,y)$ 关于 $y$ 单调不减；
2. $0\le F(x,y)\le 1$；
3. 当 $x\to-\infty$ 或 $y\to-\infty$ 时，$F(x,y)\to0$；当 $x,y\to+\infty$ 时，$F(x,y)\to1$；
4. $F(x,y)$ 分别关于 $x$、$y$ 右连续；
5. 任意矩形上的概率非负：

    $$
    \begin{aligned}
    P(a<X\le b,c<Y\le d)
    ={}&F(b,d)-F(a,d)\\
    &-F(b,c)+F(a,c)\ge0.
    \end{aligned}
    $$

!!! warning "二维分布函数的增量"
    二维情形不能只考察一条边上的差。矩形概率必须由四个角的分布函数值作“右上减左上、减右下、加左下”的运算。

### 二维连续型随机变量

若存在非负函数 $f(x,y)$，使任意 $(x,y)\in\mathbb R^2$ 都满足

$$
F(x,y)=\int_{-\infty}^{x}\int_{-\infty}^{y}f(u,v)\,\mathrm dv\,\mathrm du,
$$

则称 $(X,Y)$ 为二维连续型随机变量，$f(x,y)$ 为其联合概率密度函数。它满足

$$
f(x,y)\ge0,\qquad
\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(x,y)\,\mathrm dy\,\mathrm dx=1.
$$

若 $F$ 在相应点二阶可导，则

$$
f(x,y)=\frac{\partial^2 F(x,y)}{\partial x\,\partial y}.
$$

对平面区域 $D$，有

$$
P\bigl((X,Y)\in D\bigr)=\iint_D f(x,y)\,\mathrm dx\,\mathrm dy.
$$

### 二维正态分布

若 $|\rho|<1$，二维正态分布的联合密度为

$$
\begin{aligned}
f(x,y)=\frac{1}{2\pi\sigma_1\sigma_2\sqrt{1-\rho^2}}
\exp\Biggl\{-\frac{1}{2(1-\rho^2)}\Biggl[
&\frac{(x-\mu_1)^2}{\sigma_1^2}\\
&-\frac{2\rho(x-\mu_1)(y-\mu_2)}{\sigma_1\sigma_2}
+\frac{(y-\mu_2)^2}{\sigma_2^2}
\Biggr]\Biggr\}.
\end{aligned}
$$

记作

$$
(X,Y)\sim N(\mu_1,\mu_2;\sigma_1^2,\sigma_2^2;\rho).
$$

其中 $\rho$ 是 $X$ 与 $Y$ 的相关系数。其边缘分布仍为正态分布：

$$
X\sim N(\mu_1,\sigma_1^2),\qquad
Y\sim N(\mu_2,\sigma_2^2).
$$

## 边缘分布

从联合分布中只保留某一个随机变量的分布，得到边缘分布（Marginal Distribution）。

对分布函数，有

$$
F_X(x)=F(x,+\infty),\qquad
F_Y(y)=F(+\infty,y).
$$

离散型情形通过求和消去另一个变量：

$$
P(X=x_i)=\sum_j p_{ij},\qquad
P(Y=y_j)=\sum_i p_{ij}.
$$

连续型情形通过积分得到边缘密度：

$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,\mathrm dy,\qquad
f_Y(y)=\int_{-\infty}^{+\infty}f(x,y)\,\mathrm dx.
$$

!!! note "联合分布决定边缘分布，反之不成立"
    仅知道 $X$ 和 $Y$ 各自的分布，通常无法确定二者如何共同变化；还需要描述它们依赖关系的信息。

## 条件分布

### 离散型条件分布

当 $P(Y=y_j)>0$ 时，

$$
P(X=x_i\mid Y=y_j)
=\frac{P(X=x_i,Y=y_j)}{P(Y=y_j)}.
$$

### 连续型条件分布

当 $f_Y(y)>0$ 时，给定 $Y=y$ 条件下 $X$ 的条件密度为

$$
f_{X\mid Y}(x\mid y)=\frac{f(x,y)}{f_Y(y)}.
$$

因此联合密度可以分解为

$$
f(x,y)=f_{X\mid Y}(x\mid y)f_Y(y).
$$

条件分布函数为

$$
F_{X\mid Y}(x\mid y)
=\int_{-\infty}^{x}f_{X\mid Y}(u\mid y)\,\mathrm du.
$$

???+ example "先取上界，再在区间内均匀抽取"
    先从 $(0,1)$ 上均匀抽取 $X$，再在给定 $X=x$ 时从 $(0,x)$ 上均匀抽取 $Y$。于是

    $$
    f_X(x)=\mathbf 1_{(0,1)}(x),\qquad
    f_{Y\mid X}(y\mid x)=\frac1x\mathbf 1_{(0,x)}(y).
    $$

    联合密度为

    $$
    f(x,y)=\frac1x\mathbf 1_{\{0<y<x<1\}}.
    $$

    对 $0<y<1$ 积分可得

    $$
    f_Y(y)=\int_y^1\frac1x\,\mathrm dx=-\ln y.
    $$

## 相互独立

$X$ 与 $Y$ 相互独立，当且仅当对任意 $x,y$，

$$
F(x,y)=F_X(x)F_Y(y).
$$

若联合密度存在，则等价于几乎处处满足

$$
f(x,y)=f_X(x)f_Y(y).
$$

离散型情形对应为

$$
P(X=x_i,Y=y_j)=P(X=x_i)P(Y=y_j).
$$

!!! info "二维正态中的特殊结论"
    对联合正态的 $(X,Y)$，$X$ 与 $Y$ 独立当且仅当 $\rho=0$。该结论依赖“联合正态”条件；一般随机变量不相关并不能推出独立。

若 $X_1,\ldots,X_n$ 相互独立，则联合分布函数可分解为

$$
F(x_1,\ldots,x_n)=\prod_{i=1}^{n}F_i(x_i),
$$

密度存在时也有

$$
f(x_1,\ldots,x_n)=\prod_{i=1}^{n}f_i(x_i).
$$

若它们还具有相同的边缘分布，则称为独立同分布，记作 i.i.d.。

## 随机向量函数的分布

### 分布函数法

设 $Z=g(X,Y)$。先求

$$
F_Z(z)=P(g(X,Y)\le z)
=\iint_{g(x,y)\le z}f(x,y)\,\mathrm dx\,\mathrm dy,
$$

再在可导处计算 $f_Z(z)=F_Z'(z)$。该方法的关键是正确画出积分区域 $g(x,y)\le z$。

### 和的分布与卷积

令 $Z=X+Y$，则

$$
f_Z(z)=\int_{-\infty}^{+\infty}f(x,z-x)\,\mathrm dx.
$$

若 $X,Y$ 独立，便得到卷积公式

$$
f_{X+Y}(z)
=\int_{-\infty}^{+\infty}f_X(x)f_Y(z-x)\,\mathrm dx
=(f_X*f_Y)(z).
$$

### 二维变量变换

设

$$
U=g_1(X,Y),\qquad V=g_2(X,Y),
$$

并且反变换

$$
X=\varphi(U,V),\qquad Y=\psi(U,V)
$$

在考虑的区域上一一对应且可微，则

$$
f_{U,V}(u,v)
=f_{X,Y}\bigl(\varphi(u,v),\psi(u,v)\bigr)
\left|\frac{\partial(x,y)}{\partial(u,v)}\right|.
$$

其中

$$
\frac{\partial(x,y)}{\partial(u,v)}
=\begin{vmatrix}
\dfrac{\partial x}{\partial u} & \dfrac{\partial x}{\partial v}\\[6pt]
\dfrac{\partial y}{\partial u} & \dfrac{\partial y}{\partial v}
\end{vmatrix}
$$

是雅可比行列式（Jacobian Determinant）。

!!! warning "必须取雅可比行列式的绝对值"
    密度变换中的因子描述面积伸缩比例，应当非负，因此使用行列式的绝对值，而不是行列式本身。

## 最大值与最小值的分布

设 $X_1,\ldots,X_n$ 独立同分布，公共分布函数为 $F$。令

$$
M=\max(X_1,\ldots,X_n),\qquad
L=\min(X_1,\ldots,X_n).
$$

则

$$
F_M(x)=P(M\le x)=F(x)^n,
$$

$$
F_L(x)=P(L\le x)=1-[1-F(x)]^n.
$$

若公共密度 $f$ 存在，则

$$
f_M(x)=nF(x)^{n-1}f(x),
$$

$$
f_L(x)=n[1-F(x)]^{n-1}f(x).
$$

*[i.i.d.]: independent and identically distributed，独立同分布
