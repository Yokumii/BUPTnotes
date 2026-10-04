# 导数与微分

导数描述函数在一点的局部线性变化率，微分则把这种线性主部单独抽取出来。本章整理导数定义、求导规则、高阶导数以及参数方程和极坐标曲线的求导方法。

## 导数的定义

设函数 $f$ 在 $x_0$ 的某个邻域内有定义。若极限

$$
f'(x_0)=\lim_{x\to x_0}
\frac{f(x)-f(x_0)}{x-x_0}
$$

存在且有限，则称 $f$ 在 $x_0$ 可导。令 $\Delta x=x-x_0$，也可写成

$$
f'(x_0)=\lim_{\Delta x\to0}
\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}.
$$

左导数和右导数分别由 $\Delta x\to0^-$ 与 $\Delta x\to0^+$ 定义。函数在 $x_0$ 可导，当且仅当左右导数都存在且相等。

### 有限增量公式与微分

若 $f$ 在 $x_0$ 可导，则

$$
\frac{\Delta y}{\Delta x}-f'(x_0)\to0,
$$

也就是

$$
\Delta y=f'(x_0)\Delta x+o(\Delta x).
$$

线性主部 $f'(x_0)\Delta x$ 称为函数在 $x_0$ 的微分，记作

$$
\mathrm dy=f'(x_0)\,\mathrm dx.
$$

!!! info "可导必连续"
    由有限增量公式，$\Delta x\to0$ 时 $\Delta y\to0$，因此可导必连续。连续不一定可导，例如 $f(x)=|x|$ 在 $x=0$ 连续但不可导。

## 极值的必要条件

若 $f$ 在内点 $x_0$ 取得局部极值并且在 $x_0$ 可导，则

$$
f'(x_0)=0.
$$

这称为 Fermat 定理。导数为零只是可导函数取得极值的必要条件，不是充分条件；例如 $f(x)=x^3$ 在 $0$ 点导数为零，但没有极值。

## 基本求导规则

若 $u,v$ 可导，则

$$
(u\pm v)'=u'\pm v',
\qquad
(uv)'=u'v+uv',
$$

$$
\left(\frac uv\right)'=\frac{u'v-uv'}{v^2}\quad(v\ne0).
$$

复合函数满足链式法则：

$$
\frac{\mathrm dy}{\mathrm dx}
=\frac{\mathrm dy}{\mathrm du}\frac{\mathrm du}{\mathrm dx}.
$$

若 $y=f(x)$ 存在可导反函数 $x=\varphi(y)$，并且 $f'(x)\ne0$，则

$$
\varphi'(y)=\frac1{f'(x)}.
$$

因此

$$
(\arcsin x)'=\frac1{\sqrt{1-x^2}},
\qquad
(\arccos x)'=-\frac1{\sqrt{1-x^2}},
$$

$$
(\arctan x)'=\frac1{1+x^2}.
$$

### 对数求导

当函数由多个幂、积和商组成时，可以先取对数。例如 $y=u(x)^{v(x)}$ 且 $u(x)>0$，则

$$
\ln y=v(x)\ln u(x),
$$

从而

$$
y'=u(x)^{v(x)}
\left(v'(x)\ln u(x)+v(x)\frac{u'(x)}{u(x)}\right).
$$

## 参数方程求导

若曲线由

$$
x=\varphi(t),\qquad y=\psi(t)
$$

给出，并且 $\varphi'(t)\ne0$，则

$$
\frac{\mathrm dy}{\mathrm dx}
=\frac{\psi'(t)}{\varphi'(t)}.
$$

进一步，

$$
\frac{\mathrm d^2y}{\mathrm dx^2}
=\frac{\mathrm d}{\mathrm dt}
\left(\frac{\psi'(t)}{\varphi'(t)}\right)
\bigg/\varphi'(t)
=\frac{\psi''(t)\varphi'(t)-\psi'(t)\varphi''(t)}{[\varphi'(t)]^3}.
$$

## 极坐标曲线的切线

极坐标曲线 $r=r(\theta)$ 可以参数化为

$$
x=r(\theta)\cos\theta,
\qquad
y=r(\theta)\sin\theta.
$$

因此

$$
\frac{\mathrm dy}{\mathrm dx}
=\frac{r'(\theta)\sin\theta+r(\theta)\cos\theta}
{r'(\theta)\cos\theta-r(\theta)\sin\theta}.
$$

若切线与极轴的夹角为 $\alpha$，半径向量的极角为 $\theta$，则切线与半径向量的夹角 $\varphi=\alpha-\theta$ 满足

$$
\tan\varphi=\frac{r(\theta)}{r'(\theta)}
$$

（分母非零且角度按同一方向约定）。

## 高阶导数

若 $f'$ 仍可导，则其导数称为二阶导数 $f''$。依次定义

$$
f^{(n)}(x)=\frac{\mathrm d^n f}{\mathrm dx^n}.
$$

三角函数的高阶导数具有周期形式：

$$
\frac{\mathrm d^n}{\mathrm dx^n}\sin x
=\sin\left(x+\frac{n\pi}{2}\right),
$$

$$
\frac{\mathrm d^n}{\mathrm dx^n}\cos x
=\cos\left(x+\frac{n\pi}{2}\right).
$$

乘积的 $n$ 阶导数满足 Leibniz 公式：

$$
(uv)^{(n)}
=\sum_{k=0}^{n}\binom nk u^{(k)}v^{(n-k)}.
$$

???+ example "利用 Leibniz 公式求 $x^n/(1-x)$ 的高阶导数"
    写成

    $$
    \frac{x^n}{1-x}=x^n\cdot\frac1{1-x}.
    $$

    使用 Leibniz 公式时，$x^n$ 的 $k$ 阶导数在 $k>n$ 后为零，而

    $$
    \left(\frac1{1-x}\right)^{(m)}
    =\frac{m!}{(1-x)^{m+1}}.
    $$

    因而求导和式只有有限项，通常比先做代数展开更直接。

## 切线、法线与局部形状

若 $f'(x_0)$ 存在，则曲线 $y=f(x)$ 在点 $(x_0,f(x_0))$ 的切线为

$$
y-f(x_0)=f'(x_0)(x-x_0).
$$

当 $f'(x_0)\ne0$ 时，法线斜率为 $-1/f'(x_0)$，法线方程为

$$
y-f(x_0)=-\frac1{f'(x_0)}(x-x_0).
$$

导数还提供函数局部形状的信息：$f'>0$ 的区间上函数递增，$f'<0$ 的区间上函数递减；二阶导数则与凹凸性和极值判别相关，相关结论将在微分中值定理中建立。
