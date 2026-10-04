# 不定积分

不定积分是求导的逆运算。实际计算的关键不在于孤立地记忆公式，而在于识别复合结构、选择换元或分部积分，并把有理式系统地化成基本积分。

## 原函数与不定积分

若函数 $F$ 在区间 $I$ 上可导，且

$$
F'(x)=f(x),\qquad x\in I,
$$

则称 $F$ 是 $f$ 在 $I$ 上的一个原函数。$f$ 的全体原函数称为不定积分，记作

$$
\int f(x)\,\mathrm dx=F(x)+C.
$$

同一区间上任意两个原函数只相差一个常数。

### 原函数的存在性

若 $f$ 在区间 $I$ 上连续，则它在 $I$ 上存在原函数。固定 $a\in I$，可取

$$
F(x)=\int_a^x f(t)\,\mathrm dt,
$$

由微积分基本定理有 $F'(x)=f(x)$。

连续只是充分条件，不是必要条件。但导数具有 Darboux 性质，因此具有跳跃间断点的函数不可能是某个函数的导数，也就不可能在跨越该点的区间上存在原函数。

## 基本积分表

$$
\int 0\,\mathrm dx=C,
\qquad
\int x^\alpha\,\mathrm dx
=\frac{x^{\alpha+1}}{\alpha+1}+C\quad(\alpha\ne-1),
$$

$$
\int\frac{\mathrm dx}{x}=\ln|x|+C,
\qquad
\int a^x\,\mathrm dx=\frac{a^x}{\ln a}+C,
$$

$$
\int\sec^2x\,\mathrm dx=\tan x+C,
\qquad
\int\sec x\tan x\,\mathrm dx=\sec x+C,
$$

$$
\int\csc^2x\,\mathrm dx=-\cot x+C,
$$

$$
\int\frac{\mathrm dx}{a^2+x^2}
=\frac1a\arctan\frac xa+C\quad(a>0),
$$

$$
\int\frac{\mathrm dx}{\sqrt{a^2-x^2}}
=\arcsin\frac xa+C,
$$

$$
\int\frac{\mathrm dx}{x^2-a^2}
=\frac1{2a}\ln\left|\frac{x-a}{x+a}\right|+C,
$$

$$
\int\frac{\mathrm dx}{\sqrt{x^2+a^2}}
=\ln\left|x+\sqrt{x^2+a^2}\right|+C.
$$

## 换元积分法

### 第一类换元

若 $F'=f$，则

$$
\int f(\varphi(x))\varphi'(x)\,\mathrm dx
=F(\varphi(x))+C.
$$

它的本质是逆用链式法则。识别目标是“某个内层函数及其导数”。例如

$$
\int\frac{\mathrm dx}{x^2+a^2}
=\frac1a\int\frac{\mathrm d(x/a)}{1+(x/a)^2}
=\frac1a\arctan\frac xa+C.
$$

### 第二类换元

令 $x=\varphi(t)$，则

$$
\int f(x)\,\mathrm dx
=\int f(\varphi(t))\varphi'(t)\,\mathrm dt.
$$

根式积分常用三角代换：

| 根式 | 常用代换 |
| --- | --- |
| $\sqrt{a^2-x^2}$ | $x=a\sin t$ |
| $\sqrt{x^2-a^2}$ | $x=a\sec t$ |
| $\sqrt{x^2+a^2}$ | $x=a\tan t$ |

???+ example "计算 $\int\sqrt{a^2-x^2}\,\mathrm dx$"
    令 $x=a\sin t$，则 $\mathrm dx=a\cos t\,\mathrm dt$，并可在相应区间取 $\sqrt{a^2-x^2}=a\cos t$。于是

    $$
    \begin{aligned}
    \int\sqrt{a^2-x^2}\,\mathrm dx
    &=a^2\int\cos^2t\,\mathrm dt\\
    &=\frac{a^2}{2}(t+\sin t\cos t)+C\\
    &=\frac12x\sqrt{a^2-x^2}
      +\frac{a^2}{2}\arcsin\frac xa+C.
    \end{aligned}
    $$

## 分部积分

由乘积求导公式得到

$$
\int u\,\mathrm dv=uv-\int v\,\mathrm du.
$$

通常把“求导后变简单”的部分选作 $u$，把容易积分的部分选作 $\mathrm dv$。例如

$$
\int\ln x\,\mathrm dx
=x\ln x-\int1\,\mathrm dx
=x(\ln x-1)+C.
$$

反复分部积分可处理多项式与指数、三角函数的乘积。若积分在变换后重新出现，应把它移到等式同一侧求解。

## 有理函数积分

设

$$
R(x)=\frac{P(x)}{Q(x)},
$$

其中 $P,Q$ 为实系数多项式且 $Q\not\equiv0$。

若 $\deg P\ge\deg Q$，先做多项式除法：

$$
\frac{P(x)}{Q(x)}=S(x)+\frac{R_0(x)}{Q(x)},
\qquad \deg R_0<\deg Q.
$$

由代数基本定理，实系数多项式可分解为一次因子与不可约二次因子的乘积。因此真分式可作部分分式分解：

$$
\frac{R_0(x)}{Q(x)}
=\sum\frac{A_k}{(x-a)^k}
+\sum\frac{B_kx+C_k}{(x^2+px+q)^k}.
$$

其中 $x^2+px+q$ 的判别式小于零。各项最终归结为幂函数、对数函数和反正切函数的积分。

???+ example "线性因子含重根"
    对

    $$
    \int\frac{x^2-x}{(x-2)^3}\,\mathrm dx,
    $$

    先写成

    $$
    \frac{x^2-x}{(x-2)^3}
    =\frac1{x-2}+\frac3{(x-2)^2}+\frac2{(x-2)^3}.
    $$

    逐项积分得

    $$
    \ln|x-2|-\frac3{x-2}-\frac1{(x-2)^2}+C.
    $$

## 三角函数有理式

对 $R(\sin x,\cos x)$ 型积分，可使用万能代换

$$
t=\tan\frac x2.
$$

此时

$$
\sin x=\frac{2t}{1+t^2},
\qquad
\cos x=\frac{1-t^2}{1+t^2},
\qquad
\mathrm dx=\frac{2\,\mathrm dt}{1+t^2}.
$$

原积分因此化为关于 $t$ 的有理函数积分。

在结构更简单时不必机械使用万能代换：

- $\sin x$ 的奇次幂可拆出一个 $\sin x$，令 $u=\cos x$；
- $\cos x$ 的奇次幂可拆出一个 $\cos x$，令 $u=\sin x$；
- 两者均为偶次幂时，使用降幂公式。

## 含根式的代数积分

对

$$
R\left(x,\sqrt[n]{\frac{ax+b}{cx+d}}\right)
$$

型积分，可令

$$
t=\sqrt[n]{\frac{ax+b}{cx+d}},
$$

再把 $x$ 与 $\mathrm dx$ 都表示成 $t$ 的有理式。若出现若干不同次数的根式，可选次数的最小公倍数作统一代换。

含二次根式时，除三角代换外，也可以通过 Euler 代换把根式有理化；选择哪种方法取决于二次式的符号与因式分解形式。

## 含绝对值函数的原函数

计算 $\int|f(x)|\,\mathrm dx$ 时，应先按 $f$ 的符号分段积分，再利用原函数在整个区间上的连续性协调各段常数。

???+ example "$\int|\sin x|\,\mathrm dx$ 的常数不能各段任取"
    在区间 $[2k\pi,(2k+1)\pi]$ 上，$|\sin x|=\sin x$；在 $[(2k+1)\pi,(2k+2)\pi]$ 上，$|\sin x|=-\sin x$。因此可写为

    $$
    F(x)=
    \begin{cases}
    -\cos x+C_{2k},&2k\pi\le x\le(2k+1)\pi,\\
    \cos x+C_{2k+1},&(2k+1)\pi\le x\le(2k+2)\pi.
    \end{cases}
    $$

    在连接点要求连续，得到相邻常数之间的关系。若完全独立地为每一段选择常数，拼接后的函数通常不是整个实轴上的原函数。

## 方法选择顺序

面对一个不定积分，可依次检查：

1. 是否能直接套用基本积分表；
2. 是否存在明显的复合函数及其导数；
3. 分部积分能否降低复杂度；
4. 是否属于有理函数，可先做除法和部分分式；
5. 三角式是否适合降幂、配凑或万能代换；
6. 根式能否通过三角代换或有理化代换消去。

!!! tip "积分后用求导回查结构"
    不定积分的结果可通过求导检验。尤其是部分分式、分部积分和三角代换中，回查能快速发现符号、系数与绝对值遗漏。
