# 函数极限与连续性

函数极限研究自变量接近某点或趋于无穷时函数值的变化；连续性则把极限与函数在该点的取值连接起来。本章同时整理极限的判定、等价无穷小、间断点和一致连续性。

## 函数极限

### 自变量趋于有限点

设 $f$ 在点 $x_0$ 的某个去心邻域内有定义。若

$$
\forall\varepsilon>0,\ \exists\delta>0,
\quad 0<|x-x_0|<\delta
\Longrightarrow |f(x)-A|<\varepsilon,
$$

则称 $x\to x_0$ 时 $f(x)$ 的极限为 $A$，记作

$$
\lim_{x\to x_0}f(x)=A.
$$

极限只考察 $x_0$ 附近但不等于 $x_0$ 的点，因此 $f(x_0)$ 可以不存在，也可以不等于 $A$。

### 自变量趋于无穷

若

$$
\forall\varepsilon>0,\ \exists M>0,
\quad x>M\Longrightarrow |f(x)-A|<\varepsilon,
$$

则记 $\lim_{x\to+\infty}f(x)=A$。对于 $x\to-\infty$，把条件改为 $x<-M$；对于 $x\to\infty$，则使用 $|x|>M$。

### 无穷极限

例如，$x\to x_0$ 时 $f(x)\to+\infty$ 的含义是

$$
\forall G>0,\ \exists\delta>0,
\quad 0<|x-x_0|<\delta\Longrightarrow f(x)>G.
$$

这里的 $+\infty$ 描述函数值可以超过任意给定界限，不是一个实数。

## 单侧极限与极限存在

右极限与左极限分别记为

$$
f(x_0+0)=\lim_{x\to x_0^+}f(x),\qquad
f(x_0-0)=\lim_{x\to x_0^-}f(x).
$$

双侧极限存在的充要条件是左右极限都存在且相等：

$$
\lim_{x\to x_0}f(x)=A
\iff
f(x_0-0)=f(x_0+0)=A.
$$

!!! warning "定义域边界只考察可达方向"
    若 $f$ 只在 $[a,b]$ 上定义，讨论 $x\to a$ 时实际使用右极限，讨论 $x\to b$ 时使用左极限。

## 极限的性质与判据

若 $\lim_{x\to x_0}f(x)=A$，则有：

- 唯一性；
- 局部有界性：在 $x_0$ 的某个去心邻域中，$f$ 有界；
- 局部保号性：若 $A>0$，则在充分小的去心邻域中 $f(x)>0$；
- 局部保不等式性：若附近始终有 $f(x)\le g(x)$，且二者极限存在，则 $\lim f\le\lim g$；
- 四则运算和夹逼准则。

### Heine 归结原理

设 $f$ 在 $x_0$ 的某个去心邻域中有定义，则

$$
\lim_{x\to x_0}f(x)=A
$$

当且仅当对任意满足 $x_n\ne x_0$ 且 $x_n\to x_0$ 的数列，都有

$$
f(x_n)\to A.
$$

要证明极限不存在，只需构造两条趋于 $x_0$ 的路径，使函数值趋向不同的极限，或构造一条路径使函数值不收敛。

### Cauchy 准则

有限极限 $\lim_{x\to x_0}f(x)$ 存在，当且仅当

$$
\forall\varepsilon>0,\ \exists\delta>0,
\quad x',x''\in\mathring U(x_0,\delta)
\Longrightarrow |f(x')-f(x'')|<\varepsilon.
$$

这个判据不需要提前猜测极限值。

## 无穷小与等价无穷小

若 $x\to x_0$ 时 $f(x)\to0$，则称 $f$ 是无穷小量。

若

$$
\lim_{x\to x_0}\frac{f(x)}{g(x)}=0,
$$

则记 $f(x)=o(g(x))$，称 $f$ 是 $g$ 的高阶无穷小。

若存在 $L>0$，使得在某个去心邻域内

$$
\left|\frac{f(x)}{g(x)}\right|\le L,
$$

则记 $f(x)=O(g(x))$，表示 $f$ 至多与 $g$ 同阶。

若

$$
\lim_{x\to x_0}\frac{f(x)}{g(x)}=1,
$$

则称 $f$ 与 $g$ 是等价无穷小，记作 $f(x)\sim g(x)$。

当 $x\to0$ 时，常用等价关系有

$$
\sin x\sim x,
\qquad \tan x\sim x,
\qquad \arcsin x\sim x,
\qquad \arctan x\sim x,
$$

$$
1-\cos x\sim\frac{x^2}{2},
\qquad \ln(1+x)\sim x,
\qquad e^x-1\sim x,
$$

$$
(1+x)^\alpha-1\sim\alpha x.
$$

!!! warning "等价替换主要用于乘除结构"
    在乘积或商中可用等价无穷小替换因子；在加减式中直接逐项替换可能破坏低阶项抵消后的主部，应先通分、因式分解或使用 Taylor 展开。

## 极限计算方法

常用策略包括：

1. 因式分解与约分；
2. 根式有理化；
3. 等价无穷小替换；
4. 夹逼准则；
5. 把幂指型改写成指数形式；
6. Taylor 展开或 L'Hôpital 法则。

### 幂指型极限

处理 $1^\infty$ 型时，令

$$
y=u(x)^{v(x)},
$$

则

$$
\ln y=v(x)\ln u(x).
$$

若右端极限为 $L$，则原极限为 $e^L$。特别地，

$$
\lim_{x\to0}(1+x)^{1/x}=e.
$$

### 渐近线

若 $x\to\infty$ 时

$$
k=\lim_{x\to\infty}\frac{f(x)}x,
\qquad
b=\lim_{x\to\infty}\bigl(f(x)-kx\bigr)
$$

都存在且有限，则直线 $y=kx+b$ 是曲线 $y=f(x)$ 的一条斜渐近线。

## 连续性

设 $f$ 在 $x_0$ 的某个邻域内有定义。若

$$
\lim_{x\to x_0}f(x)=f(x_0),
$$

则称 $f$ 在 $x_0$ 连续。用 $\varepsilon$–$\delta$ 语言表述为

$$
\forall\varepsilon>0,\ \exists\delta>0,
\quad |x-x_0|<\delta
\Longrightarrow |f(x)-f(x_0)|<\varepsilon.
$$

若 $g(x)\to x_0$ 且 $f$ 在 $x_0$ 连续，则

$$
\lim f(g(x))=f\!\left(\lim g(x)\right)=f(x_0).
$$

连续函数的和、差、积仍连续；在分母非零处，商也连续。若 $f$ 在 $x_0$ 连续且 $f(x_0)\ne0$，则 $1/f$ 在 $x_0$ 连续。

## 间断点分类

若 $f$ 在 $x_0$ 不连续，则 $x_0$ 是间断点。

第一类间断点
: 左右极限都存在且有限。若两者相等但不等于 $f(x_0)$，称为可去间断点；若两者不相等，称为跳跃间断点。

第二类间断点
: 至少有一个单侧极限不存在或不是有限值。无穷间断点与振荡间断点都属于这一类。

!!! note "单调函数的间断结构"
    单调函数的间断点只能是跳跃间断点；它不会出现可去间断、无穷振荡等情形。

## 闭区间上的连续函数

若 $f\in C[a,b]$，则有以下重要性质：

- 有界性：$f$ 在 $[a,b]$ 上有界；
- 最值定理：$f$ 在 $[a,b]$ 上能取到最大值与最小值；
- 介值定理：若 $\mu$ 介于 $f(a)$ 与 $f(b)$ 之间，则存在 $\xi\in[a,b]$ 使 $f(\xi)=\mu$；
- 零点定理：若 $f(a)f(b)<0$，则存在 $\xi\in(a,b)$ 使 $f(\xi)=0$；
- 一致连续性：$f$ 在 $[a,b]$ 上一致连续。

## 一致连续

函数 $f$ 在区间 $I$ 上一致连续，是指

$$
\forall\varepsilon>0,\ \exists\delta>0,
\quad \forall x',x''\in I,
\quad |x'-x''|<\delta
\Longrightarrow |f(x')-f(x'')|<\varepsilon.
$$

这里的 $\delta$ 只依赖于 $\varepsilon$，不能随考察点变化。

一致连续也可用数列刻画：对任意 $x_n,y_n\in I$，若 $x_n-y_n\to0$，则

$$
f(x_n)-f(y_n)\to0.
$$

???+ example "$1/x$ 在 $(0,1)$ 上不一致连续"
    取

    $$
    x_n=\frac1n,
    \qquad
    y_n=\frac1{n+1}.
    $$

    则 $x_n-y_n\to0$，但

    $$
    \frac1{x_n}-\frac1{y_n}=n-(n+1)=-1
    $$

    不趋于 $0$，故 $1/x$ 在 $(0,1)$ 上不一致连续。

!!! info "点态连续与一致连续的差别"
    点态连续允许在不同位置选取不同的 $\delta$；一致连续要求同一个 $\delta$ 对整个区间中的所有点对同时有效。闭区间上的连续函数自动满足后一条件。
