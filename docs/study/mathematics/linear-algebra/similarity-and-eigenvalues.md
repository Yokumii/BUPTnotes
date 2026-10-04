# 相抵、相似与特征值

同一个线性映射在不同基下会得到不同矩阵，而相似关系正是“换基但不换映射”。本章先区分相抵、相似与合同，再讨论特征值、特征向量和对角化。

## 线性映射的矩阵

设线性映射 $T:K^n\to K^m$。在定义域基

$$
\mathcal B=(\alpha_1,\ldots,\alpha_n)
$$

和陪域基

$$
\mathcal C=(\beta_1,\ldots,\beta_m)
$$

下，若

$$
T(\alpha_j)=\sum_{i=1}^m a_{ij}\beta_i,
$$

则 $A=(a_{ij})$ 称为 $T$ 在这两组基下的矩阵。对任意 $x$，坐标满足

$$
[T(x)]_{\mathcal C}=A[x]_{\mathcal B}.
$$

矩阵不是映射本身，而是映射在所选坐标系中的表示。

## 三种矩阵关系

| 关系 | 形式 | 典型含义 | 完全不变量 |
| --- | --- | --- | --- |
| 相抵 | $B=PAQ$，$P,Q$ 可逆 | 定义域和陪域分别换基 | 秩 |
| 相似 | $B=P^{-1}AP$ | 同一线性算子换基 | Jordan 结构 |
| 合同 | $B=P^{\mathrm T}AP$ | 二次型换变量 | 实对称情形下的惯性指数 |

!!! warning "三种关系不能混用"
    相似只适用于同阶方阵；合同通常用于对称矩阵和二次型；相抵允许矩形矩阵。三者都保持秩，但只有相似必然保持特征值。

任意 $A\in K^{m\times n}$ 都相抵于

$$
\begin{pmatrix}I_r&0\\0&0\end{pmatrix},
\qquad r=\operatorname{rank}(A).
$$

因此两个同型矩阵相抵，当且仅当它们秩相同。

## 相似变换与不变量

设 $T:K^n\to K^n$，它在旧基下的矩阵为 $A$，新基向量在旧基下的坐标组成可逆矩阵 $P$。若 $T$ 在新基下的矩阵为 $B$，则

$$
AP=PB,
\qquad
B=P^{-1}AP.
$$

相似矩阵具有相同的：

- 行列式、迹和秩；
- 特征多项式、特征值及其代数重数；
- 最小多项式；
- 可逆性、幂零性和可对角化性。

若 $A\sim B$，还可推出

$$
A^m\sim B^m,\qquad
f(A)\sim f(B).
$$

!!! note "同谱不一定相似"
    只有特征值及其代数重数相同，并不足以保证两个矩阵相似；还要比较每个特征值对应的 Jordan 块结构。若二者都可对角化，则同谱可以推出相似。

## 特征值与特征向量

若存在非零向量 $x$，使

$$
Ax=\lambda x,
$$

则 $\lambda$ 是 $A$ 的特征值，$x$ 是属于 $\lambda$ 的特征向量。等价地，

$$
\det(\lambda I-A)=0.
$$

特征多项式

$$
\chi_A(\lambda)=\det(\lambda I-A)
$$

的首项系数为 $1$。若在复数域上按重数列出根 $\lambda_1,\ldots,\lambda_n$，则

$$
\chi_A(\lambda)=\prod_{i=1}^n(\lambda-\lambda_i),
$$

并且

$$
\sum_{i=1}^n\lambda_i=\operatorname{tr}(A),
\qquad
\prod_{i=1}^n\lambda_i=\det A.
$$

属于不同特征值的特征向量线性无关。更一般地，不同特征值对应的特征子空间之和是直和。

### 由已知特征值推出新特征值

若 $Ax=\lambda x$，则：

| 矩阵 | 对应特征值 | 条件 |
| --- | --- | --- |
| $A^m$ | $\lambda^m$ | $m\in\mathbb N$ |
| $aA+bI$ | $a\lambda+b$ | 无额外条件 |
| $f(A)$ | $f(\lambda)$ | $f$ 为多项式 |
| $A^{-1}$ | $\lambda^{-1}$ | $A$ 可逆 |
| $A^*$ | $\det(A)/\lambda$ | $A$ 可逆 |

$A^{\mathrm T}$ 与 $A$ 的特征多项式相同，因此具有相同的特征值，但对应特征向量通常不同。

## 对角化

$A$ 可对角化，是指存在可逆矩阵 $P$，使

$$
P^{-1}AP=\Lambda
=\operatorname{diag}(\lambda_1,\ldots,\lambda_n).
$$

矩阵 $P$ 的列正是 $n$ 个线性无关的特征向量。因此下列条件等价：

1. $A$ 可对角化；
2. $A$ 有 $n$ 个线性无关的特征向量；
3. 各特征子空间维数之和为 $n$；
4. 每个特征值的几何重数都等于代数重数。

其中

$$
\text{几何重数}=\dim\ker(\lambda I-A)
=n-\operatorname{rank}(\lambda I-A).
$$

!!! tip "两个常用充分条件"
    - $A$ 有 $n$ 个互不相同的特征值时，$A$ 可对角化；
    - 实对称矩阵一定可以被正交矩阵对角化。

### 用对角化计算递推数列

Fibonacci 数列满足

$$
\begin{pmatrix}F_{k+1}\\F_k\end{pmatrix}
=
\begin{pmatrix}1&1\\1&0\end{pmatrix}
\begin{pmatrix}F_k\\F_{k-1}\end{pmatrix}.
$$

设

$$
M=\begin{pmatrix}1&1\\1&0\end{pmatrix},
$$

其特征值为

$$
\varphi=\frac{1+\sqrt5}{2},
\qquad
\psi=\frac{1-\sqrt5}{2}.
$$

对角化 $M=P\operatorname{diag}(\varphi,\psi)P^{-1}$ 后，可得

$$
F_n=\frac{\varphi^n-\psi^n}{\sqrt5}.
$$

## Jordan 标准形的角色

当矩阵缺少足够多的线性无关特征向量时，不能对角化，但在复数域上仍可相似化为 Jordan 标准形：

$$
J_k(\lambda)=
\begin{pmatrix}
\lambda&1&&0\\
&\lambda&\ddots&\\
&&\ddots&1\\
0&&&\lambda
\end{pmatrix}.
$$

对角矩阵只是所有 Jordan 块尺寸都为 $1$ 的特殊情形。这解释了为什么“特征值相同”尚不能完整描述相似类。
