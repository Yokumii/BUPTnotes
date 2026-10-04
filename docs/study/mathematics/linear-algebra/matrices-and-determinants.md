# 行列式与矩阵运算

行列式把方阵的可逆性、体积伸缩和特征值联系起来；矩阵则负责表示线性映射。本章整理行列式、逆矩阵、伴随矩阵、矩阵幂与分块计算，为后续的秩、相似和二次型奠定计算基础。

## 行列式

设 $A=(a_{ij})\in K^{n\times n}$。其行列式可按排列定义为

$$
\det A
=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)
\prod_{i=1}^n a_{i,\sigma(i)}.
$$

这里 $S_n$ 是 $n$ 阶排列的集合，$\operatorname{sgn}(\sigma)$ 由排列的逆序数决定。

行列式的基本性质包括：

1. $\det(A^{\mathrm T})=\det A$；
2. $\det(AB)=\det A\det B$；
3. $\det(kA)=k^n\det A$；
4. 交换两行使行列式变号；一行乘 $k$ 使行列式乘 $k$；一行加上另一行的倍数不改变行列式；
5. 三角矩阵的行列式等于主对角元之积。

!!! warning "行列式不满足加法分配"
    一般没有 $\det(A+B)=\det A+\det B$。行列式只对某一行或某一列分别具有线性性。

### 余子式与代数余子式

删除 $A$ 的第 $i$ 行、第 $j$ 列所得子式记为 $M_{ij}$，代数余子式为

$$
A_{ij}=(-1)^{i+j}M_{ij}.
$$

沿第 $i$ 行或第 $j$ 列展开可得

$$
\det A=\sum_{k=1}^n a_{ik}A_{ik}
=\sum_{k=1}^n a_{kj}A_{kj}.
$$

同一行元素与另一行对应的代数余子式相乘后求和为零，即

$$
\sum_{k=1}^n a_{ik}A_{jk}=0\qquad(i\ne j).
$$

这两类等式合在一起，正是伴随矩阵恒等式 $AA^*=A^*A=(\det A)I$。

### 分块行列式

若相应方阵可逆，则 Schur 补给出

$$
\det\begin{pmatrix}A&B\\C&D\end{pmatrix}
=\det A\det(D-CA^{-1}B),
$$

或

$$
\det\begin{pmatrix}A&B\\C&D\end{pmatrix}
=\det D\det(A-BD^{-1}C).
$$

当 $C=0$ 或 $B=0$ 时，它退化为分块三角矩阵的结论：

$$
\det\begin{pmatrix}A&B\\0&D\end{pmatrix}=\det A\det D.
$$

对 $A\in K^{s\times n}$、$B\in K^{n\times s}$，还有 Sylvester 行列式恒等式

$$
\det(I_s+AB)=\det(I_n+BA).
$$

因此 $AB$ 与 $BA$ 的非零特征值相同，并且代数重数也相同。

## 矩阵乘法与可逆性

若 $A\in K^{m\times n}$、$B\in K^{n\times s}$，则

$$
(AB)_{ij}=\sum_{k=1}^n a_{ik}b_{kj}.
$$

矩阵乘法满足结合律和分配律，但通常不满足交换律。特别地，$AB=0$ 不能推出 $A=0$ 或 $B=0$。

对 $n$ 阶方阵 $A$，下列条件等价：

- $A$ 可逆；
- $\det A\ne0$；
- $\operatorname{rank}(A)=n$；
- $Ax=0$ 只有零解；
- 对任意 $b$，$Ax=b$ 有唯一解；
- $0$ 不是 $A$ 的特征值。

逆矩阵满足

$$
(AB)^{-1}=B^{-1}A^{-1},\qquad
(A^{\mathrm T})^{-1}=(A^{-1})^{\mathrm T}.
$$

!!! tip "由低次多项式恒等式求逆"
    若 $A$ 满足

    $$
    A^2-2A+3I=0,
    $$

    则 $A(2I-A)=3I$，所以

    $$
    A^{-1}=\frac{2I-A}{3}.
    $$

    一般地，只要矩阵多项式恒等式的常数项非零，就可以把它整理成 $A^{-1}$ 的表达式。

## 伴随矩阵 { #adjugate-matrix }

伴随矩阵（Adjugate Matrix）定义为代数余子式矩阵的转置：

$$
A^*=(A_{ji})_{n\times n}.
$$

核心恒等式为

$$
AA^*=A^*A=(\det A)I.
$$

当 $A$ 可逆时，

$$
A^{-1}=\frac1{\det A}A^*.
$$

对 $n$ 阶方阵，常用性质如下：

$$
\begin{aligned}
\det(A^*)&=(\det A)^{n-1},\\
(A^{\mathrm T})^*&=(A^*)^{\mathrm T},\\
(AB)^*&=B^*A^*,\\
(kA)^*&=k^{n-1}A^*.
\end{aligned}
$$

当 $n\ge2$ 时，还有

$$
(A^*)^*=(\det A)^{n-2}A.
$$

伴随矩阵的秩由 $A$ 的秩完全决定：

$$
\operatorname{rank}(A^*)=
\begin{cases}
n,&\operatorname{rank}(A)=n,\\
1,&\operatorname{rank}(A)=n-1,\\
0,&\operatorname{rank}(A)\le n-2.
\end{cases}
$$

??? note "为什么中间情形的秩恰为 1"
    当 $\operatorname{rank}(A)=n-1$ 时，至少有一个 $n-1$ 阶子式非零，所以 $A^*\ne0$。另一方面 $AA^*=0$，而 $Ax=0$ 的解空间是一维的，因此 $A^*$ 的每一列都落在同一个一维零空间中，故 $\operatorname{rank}(A^*)=1$。

## 矩阵幂的常用方法

计算 $A^m$ 时，优先寻找矩阵的结构。

### 幂零分解

若 $A=I+N$ 且 $N^r=0$，则二项式展开有限终止：

$$
A^m=(I+N)^m
=\sum_{k=0}^{r-1}\binom{m}{k}N^k.
$$

同理，若 $N^r=0$，则

$$
(I+N)^{-1}=I-N+N^2-\cdots+(-1)^{r-1}N^{r-1}.
$$

### 秩一矩阵

若 $A=uv^{\mathrm T}$，则

$$
A^2=(v^{\mathrm T}u)A,
$$

从而对 $m\ge1$，

$$
A^m=(v^{\mathrm T}u)^{m-1}A.
$$

### 对角化

若 $A=P\Lambda P^{-1}$，则

$$
A^m=P\Lambda^mP^{-1}.
$$

对角化的判定与应用将在[相似、特征值与对角化](similarity-and-eigenvalues.md)中展开。

## 分块矩阵

分块初等变换与普通初等变换一致，但“数乘”中的标量要替换为尺寸匹配的可逆矩阵。只要每一步对应左乘或右乘可逆分块矩阵，就不会改变秩。

当 $A$ 可逆时，分块消元给出

$$
\begin{pmatrix}
I&0\\-CA^{-1}&I
\end{pmatrix}
\begin{pmatrix}
A&B\\C&D
\end{pmatrix}
=
\begin{pmatrix}
A&B\\0&D-CA^{-1}B
\end{pmatrix}.
$$

于是

$$
\operatorname{rank}
\begin{pmatrix}A&B\\C&D\end{pmatrix}
=\operatorname{rank}(A)+\operatorname{rank}(D-CA^{-1}B).
$$

若 $A$ 与 Schur 补 $S=D-CA^{-1}B$ 都可逆，则

$$
\begin{pmatrix}A&B\\C&D\end{pmatrix}^{-1}
=
\begin{pmatrix}
A^{-1}+A^{-1}BS^{-1}CA^{-1}&-A^{-1}BS^{-1}\\
-S^{-1}CA^{-1}&S^{-1}
\end{pmatrix}.
$$

!!! warning "分块运算仍需检查条件"
    分块矩阵中的块通常不交换。使用类似标量的消元、因式分解或行列式公式前，必须确认块的尺寸、可逆性以及所需的交换条件。
