# 一元线性回归

一元线性回归用直线描述一个自变量与一个因变量之间的平均关系。除了拟合直线，还需要估计误差方差、检验线性关系是否显著，并对均值响应或新观察值给出区间。

## 回归模型

给定观测点 $(x_i,Y_i)$，一元线性回归模型为

$$
Y_i=a+bx_i+\varepsilon_i,\qquad i=1,2,\ldots,n,
$$

其中通常假定

$$
\varepsilon_1,\ldots,\varepsilon_n
\overset{\mathrm{i.i.d.}}{\sim}N(0,\sigma^2).
$$

$a$
: 截距，表示 $x=0$ 时的平均响应。

$b$
: 斜率，表示 $x$ 每增加一个单位时，平均响应的改变量。

$\sigma^2$
: 随机误差的方差，刻画观测值围绕回归直线的波动程度。

因此

$$
E(Y_i)=a+bx_i,\qquad \operatorname{Var}(Y_i)=\sigma^2.
$$

!!! note "自变量的角色"
    经典一元线性回归把 $x_1,\ldots,x_n$ 视为给定常数，随机性来自误差项 $\varepsilon_i$。

## 最小二乘估计

用最小二乘法选择 $a,b$，使残差平方和

$$
Q(a,b)=\sum_{i=1}^{n}(Y_i-a-bx_i)^2
$$

最小。

记

$$
S_{xx}=\sum_{i=1}^{n}(x_i-\overline x)^2
=\sum_{i=1}^{n}x_i^2-\frac1n\left(\sum_{i=1}^{n}x_i\right)^2,
$$

$$
S_{yy}=\sum_{i=1}^{n}(Y_i-\overline Y)^2
=\sum_{i=1}^{n}Y_i^2-\frac1n\left(\sum_{i=1}^{n}Y_i\right)^2,
$$

$$
S_{xy}=\sum_{i=1}^{n}(x_i-\overline x)(Y_i-\overline Y)
=\sum_{i=1}^{n}x_iY_i-\frac1n\left(\sum_{i=1}^{n}x_i\right)
\left(\sum_{i=1}^{n}Y_i\right).
$$

求解正规方程得到

$$
\boxed{
\widehat b=\frac{S_{xy}}{S_{xx}},\qquad
\widehat a=\overline Y-\widehat b\,\overline x
}.
$$

拟合值与残差分别为

$$
\widehat Y_i=\widehat a+\widehat b x_i,
$$

$$
e_i=Y_i-\widehat Y_i.
$$

!!! warning "$S_{xx}=0$ 时无法拟合斜率"
    若所有 $x_i$ 都相同，则自变量没有变化，$S_{xx}=0$，数据无法提供斜率信息。

## 误差方差的估计

残差平方和为

$$
\begin{aligned}
\mathrm{SSE}
&=\sum_{i=1}^{n}(Y_i-\widehat Y_i)^2\\
&=S_{yy}-2\widehat bS_{xy}+\widehat b^2S_{xx}\\
&=S_{yy}-\frac{S_{xy}^2}{S_{xx}}.
\end{aligned}
$$

由于估计了 $a,b$ 两个参数，残差自由度为 $n-2$。因此 $\sigma^2$ 的无偏估计为

$$
\boxed{
\widehat\sigma^2=s^2=\frac{\mathrm{SSE}}{n-2}
}.
$$

在正态误差假设下，

$$
\frac{\mathrm{SSE}}{\sigma^2}\sim\chi^2(n-2).
$$

## 平方和分解与拟合优度

总平方和、回归平方和与残差平方和分别为

$$
\mathrm{SST}=\sum_{i=1}^{n}(Y_i-\overline Y)^2,
$$

$$
\mathrm{SSR}=\sum_{i=1}^{n}(\widehat Y_i-\overline Y)^2,
$$

$$
\mathrm{SSE}=\sum_{i=1}^{n}(Y_i-\widehat Y_i)^2.
$$

它们满足

$$
\boxed{
\mathrm{SST}=\mathrm{SSR}+\mathrm{SSE}
}.
$$

在一元线性回归中，

$$
\mathrm{SSR}=\widehat b^2S_{xx}
=\frac{S_{xy}^2}{S_{xx}}.
$$

决定系数为

$$
\boxed{
R^2=\frac{\mathrm{SSR}}{\mathrm{SST}}
=1-\frac{\mathrm{SSE}}{\mathrm{SST}}
}.
$$

$R^2$ 表示模型解释的样本总变异比例。它越接近 $1$，样本点围绕拟合直线越集中。

!!! warning "$R^2$ 不是因果证据"
    较大的 $R^2$ 只表明样本中的线性拟合较强，不能单独证明因果关系，也不能替代残差分析和模型假设检查。

## 线性回归的显著性检验

线性关系是否显著可归结为检验

$$
H_0:b=0,\qquad H_1:b\ne0.
$$

若拒绝 $H_0$，说明样本提供了显著的线性关系证据。

### $t$ 检验

在模型假设下，

$$
\widehat b\sim N\left(b,\frac{\sigma^2}{S_{xx}}\right).
$$

以 $s$ 代替 $\sigma$ 后，

$$
T=\frac{\widehat b-b}{s/\sqrt{S_{xx}}}
\sim t(n-2).
$$

检验 $H_0:b=0$ 时，统计量为

$$
T=\frac{\widehat b\sqrt{S_{xx}}}{s}.
$$

显著性水平 $\alpha$ 下的双侧拒绝域为

$$
|T|\ge t_{1-\alpha/2,n-2}.
$$

### $F$ 检验

构造统计量

$$
F=\frac{\mathrm{SSR}/1}{\mathrm{SSE}/(n-2)}.
$$

在 $H_0:b=0$ 下，

$$
F\sim F(1,n-2).
$$

拒绝域为

$$
F\ge F_{1-\alpha,1,n-2}.
$$

!!! info "一元回归中两个检验等价"
    对同一个双侧斜率检验，$F=T^2$。因此 $t$ 检验与 $F$ 检验给出相同结论；$F$ 检验天然是右侧检验，因为平方和之比越大，反对 $H_0$ 的证据越强。

## 斜率的置信区间

由

$$
\frac{\widehat b-b}{s/\sqrt{S_{xx}}}\sim t(n-2),
$$

得到 $b$ 的置信水平 $1-\alpha$ 的双侧置信区间：

$$
\boxed{
\widehat b
\pm t_{1-\alpha/2,n-2}\frac{s}{\sqrt{S_{xx}}}
}.
$$

若该区间不包含 $0$，则在显著性水平 $\alpha$ 下拒绝 $H_0:b=0$。

## 均值响应的估计

给定 $x_0$，平均响应为

$$
\mu(x_0)=E(Y\mid x_0)=a+bx_0.
$$

其点估计为

$$
\widehat Y_0=\widehat a+\widehat b x_0.
$$

由

$$
\frac{\widehat Y_0-\mu(x_0)}
{s\sqrt{\dfrac1n+\dfrac{(x_0-\overline x)^2}{S_{xx}}}}
\sim t(n-2),
$$

得到 $\mu(x_0)$ 的双侧置信区间：

$$
\boxed{
\widehat Y_0
\pm t_{1-\alpha/2,n-2}s
\sqrt{\frac1n+\frac{(x_0-\overline x)^2}{S_{xx}}}
}.
$$

## 新观察值的预测

在 $x=x_0$ 处的新观察值为

$$
Y_0=a+bx_0+\varepsilon_0.
$$

仍用 $\widehat Y_0=\widehat a+\widehat b x_0$ 作点预测。由于新观察还包含新的随机误差 $\varepsilon_0$，预测区间为

$$
\boxed{
\widehat Y_0
\pm t_{1-\alpha/2,n-2}s
\sqrt{1+\frac1n+\frac{(x_0-\overline x)^2}{S_{xx}}}
}.
$$

| 目标 | 标准误中的根号项 |
| --- | --- |
| 平均响应 $\mu(x_0)$ | $\sqrt{\dfrac1n+\dfrac{(x_0-\overline x)^2}{S_{xx}}}$ |
| 新观察值 $Y_0$ | $\sqrt{1+\dfrac1n+\dfrac{(x_0-\overline x)^2}{S_{xx}}}$ |

!!! tip "预测区间总是更宽"
    均值响应区间只反映回归直线估计的不确定性；新观察值的预测区间还要包含个体误差，因此根号内多出一项 $1$。

!!! warning "谨慎外推"
    当 $x_0$ 远离 $\overline x$ 时，区间会因 $(x_0-\overline x)^2/S_{xx}$ 增大而变宽。若 $x_0$ 超出已观测自变量范围，线性关系本身也未必仍然成立。

*[SST]: Total Sum of Squares，总平方和
*[SSR]: Regression Sum of Squares，回归平方和
*[SSE]: Error Sum of Squares，残差平方和
