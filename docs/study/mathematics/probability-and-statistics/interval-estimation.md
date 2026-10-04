---
description: 讲解置信区间与置信水平，并整理正态总体均值、方差及双总体参数的区间估计方法。
---

# 区间估计

点估计只给出未知参数的一个估计值；区间估计进一步用随机区间表示估计的不确定性，并在精度与可靠度之间作出权衡。

## 基本概念

设 $\theta$ 是未知参数，$a(X_1,\ldots,X_n)$ 与 $b(X_1,\ldots,X_n)$ 是两个统计量。若

$$
P\left(a(X_1,\ldots,X_n)<\theta<b(X_1,\ldots,X_n)\right)\ge1-\alpha,
$$

则称随机区间 $(a,b)$ 是 $\theta$ 的置信水平为 $1-\alpha$ 的置信区间。

置信水平（Confidence Level）
: 重复抽样并按同一规则构造区间时，区间覆盖真参数的长期比例 $1-\alpha$。

精度（Precision）
: 区间的宽窄。区间越窄，估计越精确。

可靠度（Reliability）
: 区间覆盖真参数的概率保证。置信水平越高，可靠度越高。

!!! warning "置信区间的正确解释"
    参数 $\theta$ 是固定但未知的，随机的是区间端点。得到一个具体区间后，不应说“$\theta$ 以 $95\%$ 的概率落在该区间内”；应说“这种构造方法产生的区间有 $95\%$ 的长期覆盖率”。

通常先给定置信水平 $1-\alpha$，再在满足覆盖率的区间中尽量提高精度。

## 构造思路

区间估计通常从一个分布已知且只通过简单方式依赖未知参数的枢轴量出发：

1. 选取枢轴量 $T(X_1,\ldots,X_n;\theta)$；
2. 找到覆盖概率为 $1-\alpha$ 的分位数区间；
3. 将不等式对未知参数 $\theta$ 反解；
4. 得到置信区间的两个随机端点。

## 单个正态总体均值

设 $X_1,\ldots,X_n$ 来自正态总体 $N(\mu,\sigma^2)$。

### 方差已知：$Z$ 区间

因为

$$
Z=\frac{\overline X-\mu}{\sigma/\sqrt n}\sim N(0,1),
$$

且

$$
P\left(-z_{1-\alpha/2}\le Z\le z_{1-\alpha/2}\right)=1-\alpha,
$$

所以 $\mu$ 的双侧置信区间为

$$
\boxed{
\overline X\pm z_{1-\alpha/2}\frac{\sigma}{\sqrt n}
}.
$$

区间半宽为

$$
d=z_{1-\alpha/2}\frac{\sigma}{\sqrt n}.
$$

常用分位数为 $z_{0.975}=1.96$、$z_{0.95}=1.645$。

### 方差未知：$t$ 区间

因为

$$
T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1),
$$

所以 $\mu$ 的双侧置信区间为

$$
\boxed{
\overline X\pm t_{1-\alpha/2,n-1}\frac{S}{\sqrt n}
}.
$$

!!! note "大样本近似"
    当样本量较大、总体方差未知时，常以 $S$ 代替 $\sigma$，使用

    $$
    \overline X\pm z_{1-\alpha/2}\frac{S}{\sqrt n}
    $$

    作近似置信区间。若总体确为正态分布，使用精确的 $t$ 区间更自然。

### 单侧置信区间

| 条件 | 置信水平 $1-\alpha$ 的区间，$\sigma$ 已知 |
| --- | --- |
| 只需要下置信限 | $\left(\overline X-z_{1-\alpha}\dfrac{\sigma}{\sqrt n},+\infty\right)$ |
| 只需要上置信限 | $\left(-\infty,\overline X+z_{1-\alpha}\dfrac{\sigma}{\sqrt n}\right)$ |

当 $\sigma$ 未知时，将 $\sigma$ 换成 $S$，并将 $z_{1-\alpha}$ 换成 $t_{1-\alpha,n-1}$。

## 两个正态总体的均值差

设两组样本相互独立：

$$
X_1,\ldots,X_{n_1}\sim N(\mu_1,\sigma_1^2),
$$

$$
Y_1,\ldots,Y_{n_2}\sim N(\mu_2,\sigma_2^2).
$$

### 两个方差已知

因为

$$
\overline X-\overline Y
\sim N\left(
\mu_1-\mu_2,
\frac{\sigma_1^2}{n_1}+\frac{\sigma_2^2}{n_2}
\right),
$$

所以 $\mu_1-\mu_2$ 的双侧置信区间为

$$
\boxed{
(\overline X-\overline Y)
\pm z_{1-\alpha/2}
\sqrt{\frac{\sigma_1^2}{n_1}+\frac{\sigma_2^2}{n_2}}
}.
$$

### 方差未知但相等

当 $\sigma_1^2=\sigma_2^2=\sigma^2$ 未知时，定义合并方差

$$
S_p^2
=\frac{(n_1-1)S_1^2+(n_2-1)S_2^2}
{n_1+n_2-2}.
$$

则

$$
T=
\frac{(\overline X-\overline Y)-(\mu_1-\mu_2)}
{S_p\sqrt{1/n_1+1/n_2}}
\sim t(n_1+n_2-2).
$$

因此 $\mu_1-\mu_2$ 的双侧置信区间为

$$
\boxed{
(\overline X-\overline Y)
\pm t_{1-\alpha/2,n_1+n_2-2}
S_p\sqrt{\frac1{n_1}+\frac1{n_2}}
}.
$$

!!! warning "合并方差的前提"
    该 $t$ 区间要求两个正态总体方差相等。若不能接受等方差假设，应改用 Welch 区间，而不是机械合并样本方差。

## 单个正态总体方差

设 $X_1,\ldots,X_n$ 来自 $N(\mu,\sigma^2)$，且 $\mu$ 未知。由

$$
\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),
$$

得到 $\sigma^2$ 的双侧置信区间

$$
\boxed{
\left(
\frac{(n-1)S^2}{\chi^2_{1-\alpha/2,n-1}},
\frac{(n-1)S^2}{\chi^2_{\alpha/2,n-1}}
\right)
}.
$$

标准差 $\sigma$ 的置信区间只需对两个端点开平方：

$$
\boxed{
\left(
\frac{\sqrt{n-1}\,S}{\sqrt{\chi^2_{1-\alpha/2,n-1}}},
\frac{\sqrt{n-1}\,S}{\sqrt{\chi^2_{\alpha/2,n-1}}}
\right)
}.
$$

!!! warning "卡方分布不对称"
    两个端点分别使用不同的卡方分位数，不能像正态区间一样写成“估计值 $\pm$ 误差”。

## 两个正态总体的方差比

设两组正态样本相互独立，$\nu_1=n_1-1$、$\nu_2=n_2-1$。因为

$$
\frac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2}
\sim F(\nu_1,\nu_2),
$$

所以 $\sigma_1^2/\sigma_2^2$ 的双侧置信区间为

$$
\boxed{
\left(
\frac{S_1^2/S_2^2}{F_{1-\alpha/2,\nu_1,\nu_2}},
\frac{S_1^2/S_2^2}{F_{\alpha/2,\nu_1,\nu_2}}
\right)
}.
$$

## 样本量的确定

当总体标准差 $\sigma$ 已知，希望均值置信区间在置信水平 $1-\alpha$ 下的半宽不超过 $d$ 时，

$$
z_{1-\alpha/2}\frac{\sigma}{\sqrt n}\le d.
$$

因此

$$
\boxed{
n\ge\left(\frac{z_{1-\alpha/2}\sigma}{d}\right)^2
}.
$$

实际取样本量时应向上取整。

## 公式选择表

| 参数 | 条件 | 枢轴量 | 分布 |
| --- | --- | --- | --- |
| $\mu$ | 正态总体，$\sigma^2$ 已知 | $(\overline X-\mu)/(\sigma/\sqrt n)$ | $N(0,1)$ |
| $\mu$ | 正态总体，$\sigma^2$ 未知 | $(\overline X-\mu)/(S/\sqrt n)$ | $t(n-1)$ |
| $\mu_1-\mu_2$ | 独立正态总体，方差已知 | 标准化的 $\overline X-\overline Y$ | $N(0,1)$ |
| $\mu_1-\mu_2$ | 独立正态总体，未知等方差 | 合并方差标准化 | $t(n_1+n_2-2)$ |
| $\sigma^2$ | 正态总体，均值未知 | $(n-1)S^2/\sigma^2$ | $\chi^2(n-1)$ |
| $\sigma_1^2/\sigma_2^2$ | 两个独立正态总体 | $(S_1^2/\sigma_1^2)/(S_2^2/\sigma_2^2)$ | $F(n_1-1,n_2-1)$ |
