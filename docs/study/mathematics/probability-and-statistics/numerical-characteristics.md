---
description: 整理数学期望、方差、协方差、相关系数与矩的定义、性质和计算，刻画随机变量的分布特征。
---

# 随机变量的数字特征

分布函数完整描述随机变量，但在实际分析中，常用少量数字特征概括其位置、离散程度和变量间的关系。本章讨论数学期望、方差、矩、协方差与相关系数。

## 数学期望

数学期望（Expectation）刻画随机变量的平均位置。

离散型随机变量
: 若 $P(X=x_i)=p_i$ 且 $\sum_i |x_i|p_i<\infty$，则

    $$
    E(X)=\sum_i x_i p_i.
    $$

连续型随机变量
: 若 $X$ 的密度为 $f(x)$ 且 $\int_{-\infty}^{+\infty}|x|f(x)\,\mathrm dx<\infty$，则

    $$
    E(X)=\int_{-\infty}^{+\infty}xf(x)\,\mathrm dx.
    $$

数学期望是一个确定的数，不再是随机变量。

### 常见分布的期望

| 分布 | 记号 | 数学期望 |
| --- | --- | --- |
| 二项分布 | $X\sim B(n,p)$ | $E(X)=np$ |
| 泊松分布 | $X\sim P(\lambda)$ | $E(X)=\lambda$ |
| 正态分布 | $X\sim N(\mu,\sigma^2)$ | $E(X)=\mu$ |

???+ example "二项分布期望的直接推导"
    对 $X\sim B(n,p)$，

    $$
    \begin{aligned}
    E(X)
    &=\sum_{k=0}^{n}k\binom nkp^k(1-p)^{n-k}\\
    &=np\sum_{k=1}^{n}\binom{n-1}{k-1}p^{k-1}(1-p)^{n-k}\\
    &=np.
    \end{aligned}
    $$

??? example "正态分布期望"
    若 $X\sim N(\mu,\sigma^2)$，作代换 $u=(x-\mu)/\sigma$，则积分中的奇函数部分为零，故 $E(X)=\mu$。

### 随机变量函数的期望

若 $Y=g(X)$，不必先求 $Y$ 的分布。满足可积条件时，可以直接计算

$$
E[g(X)]=
\begin{cases}
\displaystyle\sum_i g(x_i)p_i, & X\text{ 为离散型},\\[8pt]
\displaystyle\int_{-\infty}^{+\infty}g(x)f(x)\,\mathrm dx, & X\text{ 为连续型}.
\end{cases}
$$

多维情形同理。例如 $(X,Y)$ 的联合密度为 $f(x,y)$ 时，

$$
E[g(X,Y)]
=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}
g(x,y)f(x,y)\,\mathrm dx\,\mathrm dy.
$$

### 数学期望的性质

对常数 $a_1,\ldots,a_n$，只要相应期望存在，就有线性性

$$
E\left(\sum_{i=1}^{n}a_iX_i\right)
=\sum_{i=1}^{n}a_iE(X_i).
$$

该结论不要求 $X_i$ 相互独立。

若 $X,Y$ 独立且期望存在，则

$$
E(XY)=E(X)E(Y).
$$

反过来，$E(XY)=E(X)E(Y)$ 通常不能推出 $X,Y$ 独立。

## 生成函数与矩母函数

### 概率生成函数

对取值为 $0,1,2,\ldots$ 的离散型随机变量，概率生成函数（Probability Generating Function）为

$$
G_X(t)=E(t^X)=\sum_{k=0}^{\infty}P(X=k)t^k.
$$

在可逐项求导的条件下，

$$
G_X'(1)=E(X),
$$

$$
G_X''(1)=E[X(X-1)].
$$

因此

$$
\operatorname{Var}(X)
=G_X''(1)+G_X'(1)-[G_X'(1)]^2.
$$

例如：

$$
X\sim B(n,p)
\quad\Longrightarrow\quad
G_X(t)=[pt+(1-p)]^n,
$$

$$
X\sim P(\lambda)
\quad\Longrightarrow\quad
G_X(t)=e^{\lambda(t-1)}.
$$

### 矩母函数

矩母函数（Moment Generating Function）定义为

$$
M_X(t)=E(e^{tX}).
$$

若它在 $t=0$ 的邻域内存在，则

$$
M_X^{(k)}(0)=E(X^k).
$$

特别地，

$$
E(X)=M_X'(0),\qquad
\operatorname{Var}(X)=M_X''(0)-[M_X'(0)]^2.
$$

## 条件数学期望

设 $(X,Y)$ 的联合密度为 $f(x,y)$。在 $f_Y(y)>0$ 时，给定 $Y=y$ 条件下 $X$ 的条件期望为

$$
E(X\mid Y=y)
=\int_{-\infty}^{+\infty}x f_{X\mid Y}(x\mid y)\,\mathrm dx.
$$

当不指定具体 $y$ 时，$E(X\mid Y)$ 是 $Y$ 的函数，因此本身也是随机变量。

全期望公式（塔式法则）为

$$
E(X)=E\bigl[E(X\mid Y)\bigr].
$$

???+ note "全期望公式的积分形式"
    令 $\varphi(y)=E(X\mid Y=y)$，则

    $$
    \begin{aligned}
    E[\varphi(Y)]
    &=\int\left[\int x f_{X\mid Y}(x\mid y)\,\mathrm dx\right]f_Y(y)\,\mathrm dy\\
    &=\iint x f(x,y)\,\mathrm dx\,\mathrm dy\\
    &=E(X).
    \end{aligned}
    $$

## 方差与标准差

方差（Variance）刻画随机变量围绕其均值的离散程度：

$$
\operatorname{Var}(X)=E\left[(X-E X)^2\right].
$$

标准差为

$$
\sigma_X=\sqrt{\operatorname{Var}(X)}.
$$

常用计算式为

$$
\operatorname{Var}(X)=E(X^2)-[E(X)]^2.
$$

由方差非负立刻得到

$$
E(X^2)\ge [E(X)]^2.
$$

### 常见分布的方差

| 分布 | 方差 |
| --- | --- |
| $X\sim B(n,p)$ | $np(1-p)$ |
| $X\sim P(\lambda)$ | $\lambda$ |
| $X\sim N(\mu,\sigma^2)$ | $\sigma^2$ |

### 方差的性质

$$
\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X).
$$

一般地，

$$
\operatorname{Var}(X+Y)
=\operatorname{Var}(X)+\operatorname{Var}(Y)
+2\operatorname{Cov}(X,Y).
$$

当 $X,Y$ 独立时，协方差为零，从而

$$
\operatorname{Var}(X+Y)
=\operatorname{Var}(X)+\operatorname{Var}(Y).
$$

标准化变量

$$
Z=\frac{X-E(X)}{\sigma_X}
$$

满足 $E(Z)=0$、$\operatorname{Var}(Z)=1$。

## Markov 不等式与 Chebyshev 不等式

若 $Y\ge0$，则对任意 $\varepsilon>0$，Markov 不等式给出

$$
P(Y\ge\varepsilon)\le\frac{E(Y)}{\varepsilon}.
$$

取 $Y=(X-E X)^2$、阈值取 $\varepsilon^2$，得到 Chebyshev 不等式：

$$
P(|X-E X|\ge\varepsilon)
\le\frac{\operatorname{Var}(X)}{\varepsilon^2}.
$$

???+ note "Markov 不等式的证明"
    对非负连续型随机变量 $Y$，

    $$
    \begin{aligned}
    E(Y)
    &=\int_0^{\infty}y f_Y(y)\,\mathrm dy\\
    &\ge\int_{\varepsilon}^{\infty}y f_Y(y)\,\mathrm dy\\
    &\ge\varepsilon\int_{\varepsilon}^{\infty}f_Y(y)\,\mathrm dy\\
    &=\varepsilon P(Y\ge\varepsilon).
    \end{aligned}
    $$

## 矩、偏度与峰度

$k$ 阶原点矩
: $E(X^k)$。

$k$ 阶中心矩
: $\mu_k=E[(X-E X)^k]$。

偏度系数
: $\gamma_1=\mu_3/\sigma^3$，描述分布的不对称程度。

峰度系数
: $\beta_2=\mu_4/\sigma^4$，描述分布尾部与峰部的集中程度。

!!! note "峰度与超额峰度"
    此处定义的是峰度 $\beta_2$。有些教材使用超额峰度 $\gamma_2=\beta_2-3$，二者不要混淆。

## 协方差与相关系数

协方差定义为

$$
\operatorname{Cov}(X,Y)
=E[(X-E X)(Y-E Y)]
=E(XY)-E(X)E(Y).
$$

特别地，

$$
\operatorname{Cov}(X,X)=\operatorname{Var}(X).
$$

相关系数定义为

$$
\rho_{XY}
=\frac{\operatorname{Cov}(X,Y)}
{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}.
$$

协方差在线性变换下满足

$$
\operatorname{Cov}(aX+b,cY+d)
=ac\operatorname{Cov}(X,Y).
$$

两个线性组合的协方差为

$$
\begin{aligned}
\operatorname{Cov}(aX+bY,cX+dY)
={}&ac\operatorname{Var}(X)+bd\operatorname{Var}(Y)\\
&+(ad+bc)\operatorname{Cov}(X,Y).
\end{aligned}
$$

!!! warning "独立、不相关与相关系数为零"
    - $X,Y$ 独立 $\Rightarrow \operatorname{Cov}(X,Y)=0$；
    - $\operatorname{Cov}(X,Y)=0$ 只表示不相关，通常不能推出独立；
    - 对联合正态随机变量，不相关与独立等价。

由 Cauchy–Schwarz 不等式可得

$$
\operatorname{Cov}(X,Y)^2
\le\operatorname{Var}(X)\operatorname{Var}(Y),
$$

因此 $|\rho_{XY}|\le1$。

???+ note "协方差不等式的二次函数证明"
    对任意实数 $t$，

    $$
    E\left[t(X-E X)+(Y-E Y)\right]^2\ge0.
    $$

    展开得到关于 $t$ 的二次式

    $$
    \operatorname{Var}(X)t^2
    +2\operatorname{Cov}(X,Y)t
    +\operatorname{Var}(Y)\ge0.
    $$

    该二次式对所有 $t$ 非负，所以判别式不大于零，从而得到所需不等式。

*[PGF]: Probability Generating Function，概率生成函数
*[MGF]: Moment Generating Function，矩母函数
