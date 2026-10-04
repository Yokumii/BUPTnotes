# 函数列与函数项级数

函数列的每一项都是函数，因此“对每个点分别收敛”和“在整个区域以同一速度收敛”是两种不同概念。只有一致收敛足够强，才能稳定地传递连续性和积分等性质。

## 函数列的逐点收敛

设函数列 $\{f_n\}$ 定义在集合 $D$ 上。若对某个 $x_0\in D$，数列 $\{f_n(x_0)\}$ 收敛，则称函数列在 $x_0$ 收敛。

所有收敛点组成的集合称为收敛域。若对每个 $x\in E\subseteq D$ 都有

$$
\lim_{n\to\infty}f_n(x)=f(x),
$$

则称 $f_n$ 在 $E$ 上逐点收敛于极限函数 $f$。

逐点收敛的量词顺序是

$$
\forall x\in E,\ \forall\varepsilon>0,
\ \exists N=N(x,\varepsilon),
\quad n>N\Longrightarrow |f_n(x)-f(x)|<\varepsilon.
$$

门槛 $N$ 可以随考察点 $x$ 改变。

## 一致收敛

若

$$
\forall\varepsilon>0,\ \exists N=N(\varepsilon),
\quad \forall x\in E,\ n>N
\Longrightarrow |f_n(x)-f(x)|<\varepsilon,
$$

则称 $f_n$ 在 $E$ 上一致收敛于 $f$，记作 $f_n\rightrightarrows f$。

等价地，

$$
\sup_{x\in E}|f_n(x)-f(x)|\to0.
$$

一致收敛要求同一个 $N$ 同时控制集合中的所有点。

???+ example "$x^n$ 在 $[0,1]$ 上逐点收敛但不一致收敛"
    对 $f_n(x)=x^n$，逐点极限为

    $$
    f(x)=
    \begin{cases}
    0,&0\le x<1,\\
    1,&x=1.
    \end{cases}
    $$

    每个 $f_n$ 都连续，但极限函数在 $x=1$ 不连续，因此不可能一致收敛。也可以直接看到

    $$
    \sup_{0\le x<1}x^n=1,
    $$

    误差上确界并不趋于零。

### 一致 Cauchy 准则

函数列 $f_n$ 在 $E$ 上一致收敛，当且仅当

$$
\forall\varepsilon>0,\ \exists N,
\quad m,n>N,\ \forall x\in E
\Longrightarrow |f_n(x)-f_m(x)|<\varepsilon.
$$

这个判据不需要预先知道极限函数。

## 一致收敛保留的性质

### 连续性

若每个 $f_n$ 都在 $E$ 上连续，并且 $f_n\rightrightarrows f$，则 $f$ 连续。

该结论也解释了为什么“连续函数列的逐点极限仍连续”是错误的：缺少的是一致收敛。

### 逐项积分

若 $f_n\in C[a,b]$，且 $f_n\rightrightarrows f$，则

$$
\int_a^bf(x)\,\mathrm dx
=\lim_{n\to\infty}\int_a^bf_n(x)\,\mathrm dx.
$$

对函数项级数，如果 $\sum u_n(x)$ 在 $[a,b]$ 上一致收敛且各项连续，则

$$
\int_a^b\sum_{n=1}^{\infty}u_n(x)\,\mathrm dx
=\sum_{n=1}^{\infty}\int_a^bu_n(x)\,\mathrm dx.
$$

!!! warning "逐项求导需要更强条件"
    一致收敛本身不能保证极限可导。常用充分条件是：各 $f_n$ 可导、导函数列 $f_n'$ 一致收敛，并且 $f_n$ 在某一点收敛。此时 $f_n$ 一致收敛到某个 $f$，且 $f'=\lim f_n'$。

## 函数项级数

设 $u_n$ 定义在 $D$ 上，函数项级数为

$$
\sum_{n=1}^{\infty}u_n(x).
$$

其部分和函数为

$$
S_n(x)=\sum_{k=1}^{n}u_k(x).
$$

若对每个 $x\in E$，$S_n(x)$ 收敛到 $S(x)$，则称级数在 $E$ 上逐点收敛；若 $S_n\rightrightarrows S$，则称级数一致收敛。

函数项级数的一致 Cauchy 准则为

$$
\forall\varepsilon>0,\ \exists N,
\quad n>N,\ p\in\mathbb N_+,\ \forall x\in E,
\quad
\left|\sum_{k=n+1}^{n+p}u_k(x)\right|<\varepsilon.
$$

## Weierstrass 优级数判别法

若对所有 $x\in E$ 都有

$$
|u_n(x)|\le M_n,
$$

并且常数项级数 $\sum M_n$ 收敛，则 $\sum u_n(x)$ 在 $E$ 上一致且绝对收敛。

该方法把函数项级数的一致收敛转化为一个普通正项级数的收敛性判断。

???+ example "求一个函数项级数的收敛域"
    考察

    $$
    \sum_{n=1}^{\infty}
    \frac{(x^2+x+1)^n}{n(n+1)}.
    $$

    记 $q=x^2+x+1>0$。当 $q<1$ 时由几何衰减收敛；当 $q=1$ 时化为 $\sum1/[n(n+1)]$，仍收敛；当 $q>1$ 时通项不趋于零。因此

    $$
    q\le1
    \iff x^2+x\le0
    \iff -1\le x\le0.
    $$

    收敛域为 $[-1,0]$。并且在该区间上

    $$
    \left|\frac{(x^2+x+1)^n}{n(n+1)}\right|
    \le\frac1{n(n+1)},
    $$

    所以由 Weierstrass 判别法，该级数在整个 $[-1,0]$ 上一致收敛。
