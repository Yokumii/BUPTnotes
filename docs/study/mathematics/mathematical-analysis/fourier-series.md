---
description: 讲解 Fourier 系数、Dirichlet 收敛定理、奇偶函数展开、典型级数与半区间展开的计算流程。
---

# Fourier 级数

Fourier 级数用不同频率的正弦、余弦表示周期函数。与 Taylor 级数围绕一点展开不同，Fourier 系数由函数在整个周期上的积分决定。

## 三角级数与 Fourier 系数

设 $f$ 的周期为 $2l$。其 Fourier 级数形式为

$$
\frac{a_0}{2}
+\sum_{n=1}^{\infty}
\left(
a_n\cos\frac{n\pi x}{l}
+b_n\sin\frac{n\pi x}{l}
\right),
$$

其中

$$
a_0=\frac1l\int_{-l}^{l}f(x)\,\mathrm dx,
$$

$$
a_n=\frac1l\int_{-l}^{l}
f(x)\cos\frac{n\pi x}{l}\,\mathrm dx,
$$

$$
b_n=\frac1l\int_{-l}^{l}
f(x)\sin\frac{n\pi x}{l}\,\mathrm dx.
$$

这些公式来自三角函数系在 $[-l,l]$ 上的正交性。

当周期为 $2\pi$ 时，取 $l=\pi$，公式化为

$$
a_n=\frac1\pi\int_{-\pi}^{\pi}f(x)\cos nx\,\mathrm dx,
\qquad
b_n=\frac1\pi\int_{-\pi}^{\pi}f(x)\sin nx\,\mathrm dx.
$$

## Dirichlet 收敛定理

若 $f$ 在一个周期内分段连续，并且只有有限个极值点和第一类间断点，则其 Fourier 级数在每个点 $x$ 收敛到

$$
\frac{f(x-0)+f(x+0)}2.
$$

因此：

- 在连续点，Fourier 级数收敛到 $f(x)$；
- 在跳跃间断点，收敛到左右极限的平均值；
- 周期端点应按周期延拓后的左右极限计算。

!!! warning "写出系数不等于处处恢复原函数"
    在间断点，级数一般不等于人为指定的 $f(x)$，而等于跳跃两侧极限的平均值。必须区分“原函数在该点的取值”和“Fourier 级数的收敛值”。

## 利用奇偶性简化系数

若 $f$ 是偶函数，则 $b_n=0$，并且

$$
a_n=\frac2l\int_0^lf(x)
\cos\frac{n\pi x}{l}\,\mathrm dx.
$$

若 $f$ 是奇函数，则 $a_0=a_n=0$，并且

$$
b_n=\frac2l\int_0^lf(x)
\sin\frac{n\pi x}{l}\,\mathrm dx.
$$

因此计算前应先检查函数或其周期延拓的对称性。

## 典型展开

### 锯齿波 $f(x)=x$

在 $(-\pi,\pi)$ 上令 $f(x)=x$，并作 $2\pi$ 周期延拓。由于 $f$ 为奇函数，只有正弦项。分部积分得到

$$
b_n=\frac1\pi\int_{-\pi}^{\pi}x\sin nx\,\mathrm dx
=\frac{2(-1)^{n+1}}n.
$$

所以

$$
x=2\sum_{n=1}^{\infty}
\frac{(-1)^{n+1}}n\sin nx,
\qquad -\pi<x<\pi.
$$

在 $x=\pm\pi$ 处，周期延拓发生跳跃，级数收敛到 $0$。

### 方波

令

$$
f(x)=
\begin{cases}
-1,&-\pi<x<0,\\
1,&0<x<\pi,
\end{cases}
$$

并作 $2\pi$ 周期延拓。它是奇函数，并且

$$
b_n=
\begin{cases}
\dfrac4{n\pi},&n\text{ 为奇数},\\[2mm]
0,&n\text{ 为偶数}.
\end{cases}
$$

因此

$$
f(x)\sim\frac4\pi
\left(
\sin x+\frac{\sin3x}{3}+\frac{\sin5x}{5}+\cdots
\right).
$$

在跳跃点 $x=k\pi$，级数收敛到 $0$。

## 半区间展开

只给出 $[0,l]$ 上的函数时，可以先选择一种延拓：

- 作偶延拓，得到 Fourier 余弦级数；
- 作奇延拓，得到 Fourier 正弦级数；
- 直接指定 $[-l,0)$ 上的另一段函数，再作周期延拓，得到一般 Fourier 级数。

!!! note "不同延拓产生不同级数"
    半区间上的原函数相同，并不意味着展开唯一。余弦级数和正弦级数分别对应不同的周期延拓，但在 Dirichlet 条件成立时，它们都能在原开区间内表示原函数。

## 计算流程

```mermaid
flowchart LR
    A[确定基本周期] --> B[写出一个周期的分段函数]
    B --> C[检查奇偶性与对称性]
    C --> D[计算 Fourier 系数]
    D --> E[写出三角级数]
    E --> F[按左右极限确定各点收敛值]
```

最常见的错误是周期参数 $l$、归一化系数 $1/l$ 和三角函数中的频率 $n\pi/l$ 不配套。计算前先固定使用 $[-l,l]$ 还是 $[-\pi,\pi]$，可以避免混用公式。
