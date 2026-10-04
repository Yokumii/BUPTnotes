---
description: 讲解依概率收敛、弱大数定律和中心极限定理，并说明其在样本均值近似与概率计算中的应用。
---

# 大数定律与中心极限定理

大数定律解释样本均值为什么会稳定在总体均值附近；中心极限定理进一步给出样本和或样本均值的近似分布。二者共同构成统计推断的理论基础。

## 弱大数定律

设 $X_1,X_2,\ldots$ 独立同分布，并且

$$
E(X_i)=\mu,\qquad \operatorname{Var}(X_i)=\sigma^2<\infty.
$$

记样本均值为

$$
\overline X_n=\frac1n\sum_{i=1}^{n}X_i.
$$

则对任意 $\varepsilon>0$，

$$
P(|\overline X_n-\mu|>\varepsilon)\to0,\qquad n\to\infty.
$$

即

$$
\overline X_n\xrightarrow{P}\mu.
$$

这说明当样本量增大时，样本均值偏离总体均值一个固定距离的概率趋于零。

???+ note "利用 Chebyshev 不等式证明"
    由独立同分布条件，

    $$
    E(\overline X_n)=\mu,\qquad
    \operatorname{Var}(\overline X_n)
    =\frac{1}{n^2}\sum_{i=1}^{n}\operatorname{Var}(X_i)
    =\frac{\sigma^2}{n}.
    $$

    因此由 Chebyshev 不等式，

    $$
    P(|\overline X_n-\mu|>\varepsilon)
    \le\frac{\sigma^2}{n\varepsilon^2}\to0.
    $$

!!! info "大数定律回答的问题"
    大数定律描述的是“是否收敛”：$\overline X_n$ 依概率收敛到 $\mu$。它不直接给出有限样本下误差的精确分布。

## 中心极限定理

设 $X_1,X_2,\ldots$ 独立同分布，且

$$
E(X_i)=\mu,\qquad 0<\operatorname{Var}(X_i)=\sigma^2<\infty.
$$

记

$$
S_n=\sum_{i=1}^{n}X_i.
$$

则对任意实数 $x$，

$$
P\left(
\frac{S_n-n\mu}{\sigma\sqrt n}\le x
\right)
\to\Phi(x),\qquad n\to\infty,
$$

其中 $\Phi$ 是标准正态分布函数。等价地，

$$
\frac{\sqrt n(\overline X_n-\mu)}{\sigma}
\xrightarrow{d}N(0,1).
$$

当 $n$ 足够大时，可以近似写成

$$
S_n\approx N(n\mu,n\sigma^2),
$$

或

$$
\overline X_n\approx N\left(\mu,\frac{\sigma^2}{n}\right).
$$

!!! info "中心极限定理回答的问题"
    中心极限定理描述的是“怎样波动”：样本均值与总体均值之差的典型量级为 $\sigma/\sqrt n$，标准化后近似服从标准正态分布。

!!! note "适用范围"
    - $X_i$ 本身不必服从正态分布，可以是离散型或连续型；
    - 独立同分布条件存在更一般的放宽形式，但必须配套相应的正则条件；
    - 近似效果取决于原分布形状与样本量，不能只凭“样本量较大”机械套用。

## 二项分布的正态近似

若 $X_i\sim B(1,p)$ 相互独立，则

$$
S_n=\sum_{i=1}^{n}X_i\sim B(n,p),\qquad
\mu=p,\quad \sigma^2=p(1-p).
$$

由中心极限定理，

$$
\frac{S_n-np}{\sqrt{np(1-p)}}
\xrightarrow{d}N(0,1).
$$

因此当 $n$ 较大且 $p$ 不过分接近 $0$ 或 $1$ 时，可以用

$$
S_n\approx N\bigl(np,np(1-p)\bigr)
$$

近似二项分布。

### 连续性修正

二项分布是离散分布，而正态分布是连续分布。计算点概率或整数区间概率时，应把每个整数 $k$ 对应到区间 $[k-0.5,k+0.5]$：

$$
P(S_n=k)
\approx
P\left(k-\frac12<Y<k+\frac12\right),
$$

其中 $Y\sim N(np,np(1-p))$。

例如，

$$
P(a\le S_n\le b)
\approx
P\left(a-\frac12<Y<b+\frac12\right).
$$

!!! warning "不要遗漏标准化"
    使用标准正态分布表或 $\Phi$ 函数前，还需将 $Y$ 标准化：

    $$
    Z=\frac{Y-np}{\sqrt{np(1-p)}}.
    $$
