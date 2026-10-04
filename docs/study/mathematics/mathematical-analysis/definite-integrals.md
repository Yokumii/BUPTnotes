# 定积分

定积分把区间分割后的局部贡献求和，并取分割无限细时的极限。它既是面积与总量的统一模型，也是连接导数和原函数的桥梁。

## Riemann 积分的定义

设 $f$ 定义在 $[a,b]$ 上。取分割

$$
T:\quad a=x_0<x_1<\cdots<x_n=b,
$$

记

$$
\Delta x_i=x_i-x_{i-1},
\qquad
\lambda(T)=\max_{1\le i\le n}\Delta x_i.
$$

在每个小区间 $[x_{i-1},x_i]$ 中任取一点 $\xi_i$。若存在实数 $I$，使得无论怎样选取分割与取样点，只要 $\lambda(T)\to0$，都有

$$
\sum_{i=1}^{n}f(\xi_i)\Delta x_i\to I,
$$

则称 $f$ 在 $[a,b]$ 上 Riemann 可积，并记

$$
I=\int_a^b f(x)\,\mathrm dx.
$$

!!! note "极限必须与取样方式无关"
    只对某一种特殊分割或某一组取样点得到极限，还不足以说明函数可积。Riemann 可积要求所有足够细的分割与任意取样点都趋向同一个值。

## Newton–Leibniz 公式

若 $f$ 在 $[a,b]$ 上连续，且 $F$ 是 $f$ 的一个原函数，即 $F'=f$，则

$$
\int_a^b f(x)\,\mathrm dx=F(b)-F(a).
$$

更一般地，只要 $f$ 可积，$F$ 在 $[a,b]$ 上连续、在 $(a,b)$ 上可导且 $F'=f$，公式仍成立。

该公式把“和式极限”转化为“原函数端点之差”，是定积分计算的基本工具。

## 可积条件

以下条件都能保证 $f$ 在 $[a,b]$ 上 Riemann 可积：

- $f$ 在 $[a,b]$ 上连续；
- $f$ 在 $[a,b]$ 上有界，并且只有有限个间断点；
- $f$ 在 $[a,b]$ 上单调。

Riemann 可积必然推出有界，但有界不一定可积。

## 定积分的基本性质

若 $f,g$ 在 $[a,b]$ 上可积，则：

### 线性性

$$
\int_a^b\bigl(\alpha f(x)+\beta g(x)\bigr)\,\mathrm dx
=\alpha\int_a^bf(x)\,\mathrm dx
+\beta\int_a^bg(x)\,\mathrm dx.
$$

### 区间可加性

对任意 $c\in[a,b]$，

$$
\int_a^b f(x)\,\mathrm dx
=\int_a^c f(x)\,\mathrm dx
+\int_c^b f(x)\,\mathrm dx.
$$

### 保序性

若 $f(x)\le g(x)$，则

$$
\int_a^b f(x)\,\mathrm dx
\le\int_a^b g(x)\,\mathrm dx.
$$

特别地，若 $f(x)\ge0$，则 $\int_a^bf(x)\,\mathrm dx\ge0$。

若 $f$ 连续、$f\ge0$，并且 $f$ 不恒为零，则

$$
\int_a^bf(x)\,\mathrm dx>0.
$$

### 绝对值不等式

$$
\left|\int_a^bf(x)\,\mathrm dx\right|
\le\int_a^b|f(x)|\,\mathrm dx.
$$

!!! warning "一般不能拆成积分的乘积"
    通常

    $$
    \int_a^bf(x)g(x)\,\mathrm dx
    \ne
    \left(\int_a^bf(x)\,\mathrm dx\right)
    \left(\int_a^bg(x)\,\mathrm dx\right).
    $$

## 积分中值定理

### 第一积分中值定理

若 $f\in C[a,b]$，则存在 $\xi\in[a,b]$，使

$$
\int_a^bf(x)\,\mathrm dx=f(\xi)(b-a).
$$

这表明连续函数的平均值

$$
\frac1{b-a}\int_a^bf(x)\,\mathrm dx
$$

能在区间中某点取到。

若 $f,g\in C[a,b]$ 且 $g$ 不变号，则存在 $\xi\in[a,b]$，使

$$
\int_a^bf(x)g(x)\,\mathrm dx
=f(\xi)\int_a^bg(x)\,\mathrm dx.
$$

### 第二积分中值定理

若 $f$ 在 $[a,b]$ 上可积，$g$ 在 $[a,b]$ 上单调，则存在 $\xi\in[a,b]$，使

$$
\int_a^bf(x)g(x)\,\mathrm dx
=g(a)\int_a^\xi f(x)\,\mathrm dx
+g(b)\int_\xi^b f(x)\,\mathrm dx.
$$

当 $g$ 单调且非负时，还可写出相应的 Bonnet 形式，以一个端点值乘某段积分。

## 变上限积分

若 $f$ 在 $[a,b]$ 上连续，定义

$$
\Phi(x)=\int_a^x f(t)\,\mathrm dt,
$$

则 $\Phi$ 在 $[a,b]$ 上连续、在 $(a,b)$ 上可导，并且

$$
\Phi'(x)=f(x).
$$

更一般地，若积分上下限也是函数，则 Leibniz 公式为

$$
\frac{\mathrm d}{\mathrm dx}
\int_{h(x)}^{g(x)}f(t)\,\mathrm dt
=g'(x)f(g(x))-h'(x)f(h(x)).
$$

若被积函数还显含 $x$，则

$$
\frac{\mathrm d}{\mathrm dx}
\int_{h(x)}^{g(x)}F(x,t)\,\mathrm dt
=F(x,g(x))g'(x)-F(x,h(x))h'(x)
+\int_{h(x)}^{g(x)}\frac{\partial F}{\partial x}(x,t)\,\mathrm dt.
$$

???+ example "求变限积分的导数"
    设

    $$
    H(x)=\int_{x^2}^{0}t\cos(t^2)\,\mathrm dt.
    $$

    则

    $$
    H'(x)
    =-2x\cdot\bigl[x^2\cos(x^4)\bigr]
    =-2x^3\cos(x^4).
    $$

## 用定积分计算数列极限

若 $f$ 在 $[a,b]$ 上连续，则等距分割给出的 Riemann 和满足

$$
\lim_{n\to\infty}
\frac{b-a}{n}
\sum_{i=1}^{n}
f\left(a+\frac{i(b-a)}n\right)
=\int_a^bf(x)\,\mathrm dx.
$$

???+ example "正弦 Riemann 和"
    对

    $$
    \frac1n\sum_{i=1}^{n}\sin\frac{i\pi}{n},
    $$

    补上网格宽度 $\pi/n$：

    $$
    \frac1n\sum_{i=1}^{n}\sin\frac{i\pi}{n}
    =\frac1\pi\sum_{i=1}^{n}
    \sin\frac{i\pi}{n}\frac\pi n.
    $$

    因此极限为

    $$
    \frac1\pi\int_0^\pi\sin x\,\mathrm dx=\frac2\pi.
    $$

## 对称性与周期性

若 $f$ 为奇函数，则

$$
\int_{-a}^{a}f(x)\,\mathrm dx=0.
$$

若 $f$ 为偶函数，则

$$
\int_{-a}^{a}f(x)\,\mathrm dx
=2\int_0^af(x)\,\mathrm dx.
$$

若 $f$ 是以 $p>0$ 为周期的连续函数，则对任意实数 $a$，

$$
\int_a^{a+p}f(x)\,\mathrm dx
=\int_0^pf(x)\,\mathrm dx.
$$

## Wallis 公式

记

$$
I_n=\int_0^{\pi/2}\sin^n x\,\mathrm dx
=\int_0^{\pi/2}\cos^n x\,\mathrm dx.
$$

分部积分得到递推式

$$
I_n=\frac{n-1}{n}I_{n-2}.
$$

因此

$$
I_{2m}
=\frac{(2m-1)!!}{(2m)!!}\cdot\frac\pi2,
$$

$$
I_{2m+1}
=\frac{(2m)!!}{(2m+1)!!}.
$$

## 凸函数的积分不等式

若 $f$ 在 $[a,b]$ 上为凸函数，则有 Hermite–Hadamard 不等式：

$$
f\left(\frac{a+b}{2}\right)
\le
\frac1{b-a}\int_a^bf(x)\,\mathrm dx
\le
\frac{f(a)+f(b)}2.
$$

左侧来自凸函数图像位于切线上方，右侧来自图像位于端点弦的下方。对凹函数，不等号方向全部反向。
