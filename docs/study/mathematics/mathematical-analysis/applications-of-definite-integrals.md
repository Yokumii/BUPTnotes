# 定积分的几何应用

定积分的几何应用都遵循同一思路：先在局部写出面积、体积、弧长或曲面面积的微元，再在参数区间上求和取极限。关键是选对表示方式并确认符号、区间和是否重复计数。

## 平面图形的面积

### 直角坐标

若 $f(x)\ge g(x)$，则两条曲线在 $[a,b]$ 之间围成的面积为

$$
S=\int_a^b\bigl(f(x)-g(x)\bigr)\,\mathrm dx.
$$

若上下关系会改变，应先求交点并分段积分，或对差的绝对值积分。

### 参数方程

若曲线由

$$
x=x(t),\qquad y=y(t),\qquad \alpha\le t\le\beta
$$

给出，则有向面积可由

$$
S=\int y\,\mathrm dx
=\int_\alpha^\beta y(t)x'(t)\,\mathrm dt
$$

计算。实际面积需结合曲线方向取绝对值或分段处理。对闭曲线，也常使用

$$
S=\frac12\oint(x\,\mathrm dy-y\,\mathrm dx).
$$

### 极坐标

由极坐标曲线 $r=r(\theta)$、射线 $\theta=\alpha$ 与 $\theta=\beta$ 围成的面积为

$$
S=\frac12\int_\alpha^\beta r^2(\theta)\,\mathrm d\theta.
$$

若求两条极坐标曲线之间的面积，应使用外半径平方减内半径平方，并检查图形是否在所选角度区间内被重复描绘。

???+ example "三叶玫瑰线单瓣与总面积"
    对 $r=a\sin3\theta$，一瓣可取 $0\le\theta\le\pi/3$。单瓣面积为

    $$
    S_1=\frac12\int_0^{\pi/3}a^2\sin^23\theta\,\mathrm d\theta
    =\frac{\pi a^2}{12}.
    $$

    三瓣总面积为

    $$
    S=3S_1=\frac{\pi a^2}{4}.
    $$

## 平行截面法求体积

若立体在位置 $x$ 处与 $x$ 轴垂直的截面面积为 $A(x)$，则

$$
V=\int_a^bA(x)\,\mathrm dx.
$$

它适用于截面形状已知但未必是旋转体的情形。

### 旋转体体积

区域 $0\le y\le f(x)$ 绕 $x$ 轴旋转时，圆盘法给出

$$
V=\pi\int_a^b[f(x)]^2\,\mathrm dx.
$$

若截面是内外半径分别为 $r(x)$、$R(x)$ 的圆环，则

$$
V=\pi\int_a^b\bigl(R^2(x)-r^2(x)\bigr)\,\mathrm dx.
$$

也可以使用柱壳法。例如平面区域绕 $y$ 轴旋转时，若竖条高度为 $h(x)$，则

$$
V=2\pi\int_a^b xh(x)\,\mathrm dx
$$

（区间位于 $x\ge0$ 时）。

## 平面曲线的弧长

### 直角坐标

若 $y=f(x)$ 在 $[a,b]$ 上光滑，则弧长为

$$
L=\int_a^b\sqrt{1+[f'(x)]^2}\,\mathrm dx.
$$

若用 $x=g(y)$ 表示，则

$$
L=\int_c^d\sqrt{1+[g'(y)]^2}\,\mathrm dy.
$$

### 参数方程

若 $x=x(t)$、$y=y(t)$，则

$$
L=\int_\alpha^\beta
\sqrt{[x'(t)]^2+[y'(t)]^2}\,\mathrm dt.
$$

### 极坐标

若 $r=r(\theta)$，则

$$
L=\int_\alpha^\beta
\sqrt{r^2(\theta)+[r'(\theta)]^2}\,\mathrm d\theta.
$$

???+ example "摆线一拱的弧长"
    摆线可参数化为

    $$
    x=a(t-\sin t),
    \qquad
    y=a(1-\cos t),
    \qquad 0\le t\le2\pi.
    $$

    因为

    $$
    x'=a(1-\cos t),\qquad y'=a\sin t,
    $$

    所以

    $$
    \sqrt{x'^2+y'^2}
    =2a\sin\frac t2
    $$

    在 $[0,2\pi]$ 上非负。于是

    $$
    L=\int_0^{2\pi}2a\sin\frac t2\,\mathrm dt=8a.
    $$

## 曲率

参数曲线 $x=x(t)$、$y=y(t)$ 的曲率为

$$
\kappa=
\frac{|x'y''-y'x''|}{(x'^2+y'^2)^{3/2}}.
$$

对显函数 $y=f(x)$，公式化为

$$
\kappa=
\frac{|f''(x)|}{\bigl(1+[f'(x)]^2\bigr)^{3/2}}.
$$

曲率半径为 $\rho=1/\kappa$。曲率越大，曲线弯曲越剧烈。

## 旋转曲面的面积

### 显函数绕坐标轴旋转

若 $y=f(x)$ 在 $[a,b]$ 上非负，绕 $x$ 轴旋转所得曲面面积为

$$
S=2\pi\int_a^bf(x)
\sqrt{1+[f'(x)]^2}\,\mathrm dx.
$$

若曲线绕 $y$ 轴旋转且 $x\ge0$，则

$$
S=2\pi\int_a^b x
\sqrt{1+[f'(x)]^2}\,\mathrm dx.
$$

### 参数方程

参数曲线绕 $x$ 轴旋转时，

$$
S=2\pi\int_\alpha^\beta
|y(t)|\sqrt{[x'(t)]^2+[y'(t)]^2}\,\mathrm dt.
$$

绕 $y$ 轴旋转时，把半径 $|y(t)|$ 换成 $|x(t)|$。

### 极坐标

极坐标曲线绕极轴旋转时，曲面面积为

$$
S=2\pi\int_\alpha^\beta
|r(\theta)\sin\theta|
\sqrt{r^2(\theta)+[r'(\theta)]^2}\,\mathrm d\theta.
$$

!!! warning "先判断曲线是否重复描绘"
    极坐标曲线和参数曲线常在不同参数区间重复经过同一段轨迹。若直接在完整周期上积分，面积、弧长或曲面面积可能被重复计算。应先根据对称性和描绘方向确定最小有效区间，再乘以对称倍数。

## 建模检查清单

- 面积：确认上减下、外减内，并在交点处分段；
- 体积：确认采用圆盘、圆环、柱壳还是一般截面；
- 弧长：确认参数区间只描绘一次，并使用速度的模；
- 曲面面积：确认旋转半径取非负值；
- 极坐标：确认 $r<0$ 时点的实际方位，以及对称倍数是否正确。
