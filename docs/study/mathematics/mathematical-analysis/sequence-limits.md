---
description: 介绍数列极限定义、收敛数列性质与判据、典型极限、增长阶，以及 Stolz 定理和平均值极限。
---

# 数列极限

数列极限用“从某一项以后始终接近”刻画无限过程。本章从 $\varepsilon$–$N$ 定义出发，整理收敛判据、递推数列的常用证明框架与典型极限。

## 极限的定义

设数列 $\{a_n\}$ 与常数 $a\in\mathbb R$。若

$$
\forall\varepsilon>0,\ \exists N\in\mathbb N_+,
\quad n>N\Longrightarrow |a_n-a|<\varepsilon,
$$

则称 $\{a_n\}$ 收敛于 $a$，记作

$$
\lim_{n\to\infty}a_n=a.
$$

定义只约束充分靠后的项，前面有限项如何取值不影响极限。

### 常用等价表述

下列改变不会影响数列极限的定义：

1. 把 $n>N$ 改成 $n\ge N$；
2. 把 $|a_n-a|<\varepsilon$ 改成 $|a_n-a|\le\varepsilon$；
3. 只对 $\varepsilon=1/m$（$m\in\mathbb N_+$）验证；
4. 把整数门槛 $N$ 换成实数门槛 $X$；
5. 对某个固定 $M>0$，把误差界换成 $M\varepsilon$；
6. 只对 $0<\varepsilon<\varepsilon_0$ 验证，其中 $\varepsilon_0>0$ 固定。

???+ note "为什么只验证小的 $\varepsilon$ 就够了"
    若结论已经对 $0<\varepsilon<\varepsilon_0$ 成立，那么对任意 $\varepsilon\ge\varepsilon_0$，选取一个更小的 $\eta<\varepsilon_0$。由 $|a_n-a|<\eta$ 立即得到 $|a_n-a|<\varepsilon$。

### 用定义证明极限

证明 $a_n\to a$ 的核心是从

$$
|a_n-a|<\varepsilon
$$

反推出一个只依赖于 $\varepsilon$ 的门槛 $N$。

???+ example "证明 $\sqrt[n]{n+1}\to1$"
    令 $t=\sqrt[n]{n+1}-1>0$，则 $(1+t)^n=n+1$。由二项式展开，

    $$
    n+1=(1+t)^n
    \ge 1+nt+\frac{n(n-1)}2t^2,
    $$

    因而

    $$
    0<t\le\sqrt{\frac{2}{n-1}}.
    $$

    只要取 $N>2/\varepsilon^2+1$，当 $n>N$ 时便有

    $$
    \left|\sqrt[n]{n+1}-1\right|<\varepsilon.
    $$

## 收敛数列的性质

若 $a_n\to a$，则有：

- 唯一性：极限 $a$ 唯一；
- 有界性：$\{a_n\}$ 必有界；
- 保号性：若 $a>0$，则充分大的 $n$ 满足 $a_n>0$；若 $a<0$，结论相反；
- 子列收敛性：$\{a_n\}$ 的每个子列都收敛于 $a$。

反过来，若能找到两个收敛于不同极限的子列，则原数列发散。

### 保不等式性

若 $a_n\to a$、$b_n\to b$，且从某一项起 $a_n\ge b_n$，则

$$
a\ge b.
$$

若从某一项起 $a_n>b_n$，一般也只能推出 $a\ge b$，不能推出 $a>b$。例如 $1/n>0$，但 $1/n\to0$。

### 四则运算

设 $a_n\to a$、$b_n\to b$，则

$$
a_n\pm b_n\to a\pm b,\qquad
a_nb_n\to ab.
$$

若 $b\ne0$，则充分大的 $n$ 有 $b_n\ne0$，并且

$$
\frac{a_n}{b_n}\to\frac ab.
$$

### 夹逼准则

若从某一项起

$$
a_n\le b_n\le c_n,
$$

且 $a_n\to L$、$c_n\to L$，则 $b_n\to L$。

???+ example "夹逼含有 $n$ 项的和"
    对

    $$
    s_n=\frac1{n+\sqrt1}+\frac1{n+\sqrt2}+\cdots+
    \frac1{n+\sqrt n},
    $$

    每一项都介于 $1/(n+\sqrt n)$ 与 $1/(n+1)$ 之间，所以

    $$
    \frac{n}{n+\sqrt n}\le s_n\le\frac{n}{n+1}.
    $$

    两端都趋于 $1$，故 $s_n\to1$。

## 收敛判据

### 单调有界定理

单调递增且有上界的数列必收敛，其极限为该数列值域的上确界；单调递减且有下界的数列必收敛，其极限为值域的下确界。

对递推数列，常用流程是：

```mermaid
flowchart LR
    A[找不变区间] --> B[证明有界]
    B --> C[比较相邻两项]
    C --> D[得到单调性]
    D --> E[由单调有界得收敛]
    E --> F[代入递推式求极限]
```

!!! warning "先证明收敛，再令 $n\to\infty$"
    把递推式两边直接取极限，只能得到“若极限存在，它应满足什么方程”，不能证明极限确实存在。还必须先用单调有界定理或其他判据建立收敛性。

???+ example "算术—调和平均型递推"
    设 $a>0$，并令

    $$
    a_{n+1}=\frac12\left(a_n+\frac{a}{a_n}\right),\qquad a_1>0.
    $$

    由均值不等式 $a_{n+1}\ge\sqrt a$。当 $a_n\ge\sqrt a$ 时，

    $$
    a_{n+1}-a_n
    =\frac{a-a_n^2}{2a_n}\le0.
    $$

    因此从进入区间 $[\sqrt a,+\infty)$ 起，数列单调递减且有下界，故收敛。设极限为 $L>0$，则

    $$
    L=\frac12\left(L+\frac aL\right),
    $$

    从而 $L=\sqrt a$。

### Cauchy 收敛准则

数列 $\{a_n\}$ 收敛，当且仅当

$$
\forall\varepsilon>0,\ \exists N\in\mathbb N_+,
\quad m,n>N\Longrightarrow |a_n-a_m|<\varepsilon.
$$

它不需要预先知道极限值，适合处理部分和、函数逼近等问题。其否定形式为：存在 $\varepsilon_0>0$，使得对任意 $N$，总能找到 $m,n>N$ 满足

$$
|a_n-a_m|\ge\varepsilon_0.
$$

## 典型极限与增长阶

常见极限包括

$$
\lim_{n\to\infty}\sqrt[n]{a}=1\quad(a>0),
$$

$$
\lim_{n\to\infty}\sqrt[n]{n}=1,
\qquad
\lim_{n\to\infty}\left(1+\frac1n\right)^n=e.
$$

当 $a>1$ 且 $k>0$ 时，常用增长阶为

$$
\log_a n\ll n^k\ll a^n\ll n!\ll n^n.
$$

这里 $u_n\ll v_n$ 表示 $u_n/v_n\to0$。

若 $a_n>0$，并且

$$
\lim_{n\to\infty}\frac{a_n}{a_{n+1}}=L>1,
$$

则 $a_n\to0$。事实上可取 $1<q<L$，使充分大的 $n$ 满足 $a_n/a_{n+1}>q$，从而 $a_n$ 被一个公比小于 $1$ 的几何数列控制。

## Stolz 定理与平均值极限

### Stolz–Cesàro 定理

设 $y_n$ 严格递增且 $y_n\to+\infty$。若

$$
\lim_{n\to\infty}\frac{x_{n+1}-x_n}{y_{n+1}-y_n}=L,
$$

则在相应条件下

$$
\lim_{n\to\infty}\frac{x_n}{y_n}=L.
$$

它是离散形式的 L'Hôpital 法则，尤其适合处理 $\infty/\infty$ 型数列极限。另有 $0/0$ 型版本：若 $x_n\to0$、$y_n\to0$，$y_n$ 严格单调，且相邻差商极限存在，也可得到同样结论。

### Cesàro 平均

若 $a_n\to a$，则

$$
\frac{a_1+a_2+\cdots+a_n}{n}\to a.
$$

当 $a_n>0$ 且 $a_n\to a>0$ 时，还有几何平均结论

$$
\sqrt[n]{a_1a_2\cdots a_n}\to a.
$$

!!! note "逆命题通常不成立"
    平均值收敛并不能保证原数列收敛。例如 $a_n=(-1)^n$ 不收敛，但其 Cesàro 平均趋于 $0$。
