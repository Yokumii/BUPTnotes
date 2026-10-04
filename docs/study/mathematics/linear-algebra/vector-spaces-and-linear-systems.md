# 向量组与线性方程组

向量组的线性相关性决定了它携带多少独立信息；线性方程组的解则由系数矩阵和增广矩阵的秩共同决定。本章把张成空间、基、极大线性无关组与方程组的解空间统一起来。

## 线性组合与张成空间

给定向量 $\alpha_1,\ldots,\alpha_s\in K^n$，所有线性组合组成的集合

$$
\operatorname{span}(\alpha_1,\ldots,\alpha_s)
=\left\{\sum_{i=1}^s k_i\alpha_i:k_i\in K\right\}
$$

称为这组向量的张成空间。

若向量组 $\mathcal A$ 中每个向量都能由向量组 $\mathcal B$ 线性表示，则

$$
\operatorname{span}(\mathcal A)\subseteq\operatorname{span}(\mathcal B),
\qquad
\operatorname{rank}(\mathcal A)\le\operatorname{rank}(\mathcal B).
$$

若两组向量可以互相线性表示，则称它们等价；此时它们张成同一个空间，秩也相同。

## 线性相关与线性无关

向量组 $\alpha_1,\ldots,\alpha_s$ 线性相关，当且仅当存在不全为零的数 $k_1,\ldots,k_s$，使

$$
k_1\alpha_1+\cdots+k_s\alpha_s=0.
$$

以下条件与线性相关等价：

- 至少有一个向量可以由其余向量线性表示；
- 齐次方程 $Ax=0$ 有非零解，其中 $A=(\alpha_1,\ldots,\alpha_s)$；
- $\operatorname{rank}(A)<s$；
- 当 $s=n$ 时，$\det A=0$。

!!! info "向量个数超过空间维数"
    $K^n$ 中任意 $n+1$ 个向量必线性相关，因为对应齐次方程有 $n$ 个方程、至少 $n+1$ 个未知量。

若 $\alpha_1,\ldots,\alpha_s$ 线性无关，而加入 $\beta$ 后线性相关，则 $\beta$ 可由 $\alpha_1,\ldots,\alpha_s$ 唯一线性表示。

### 极大线性无关组

从向量组中选出一组线性无关向量，并且其余向量均可由它们线性表示，这组向量称为原向量组的极大线性无关组。极大线性无关组所含向量个数就是向量组的秩。

求法如下：

1. 把向量作为矩阵的列；
2. 只做行初等变换，把矩阵化为阶梯形；
3. 原矩阵中与主元列对应的列构成一个极大线性无关组。

!!! warning "必须回到原矩阵取列"
    行变换保持列向量之间的线性关系，却改变了列向量本身。主元列的编号从阶梯形矩阵中读取，实际向量必须从原矩阵中选取。

## 基、维数与坐标

向量空间 $V$ 的一组基，是一组既线性无关又能张成 $V$ 的向量。若

$$
\mathcal B=(\beta_1,\ldots,\beta_n)
$$

是 $V$ 的基，则任意 $v\in V$ 都有唯一表示

$$
v=x_1\beta_1+\cdots+x_n\beta_n.
$$

列向量 $(x_1,\ldots,x_n)^{\mathrm T}$ 称为 $v$ 在基 $\mathcal B$ 下的坐标。有限维空间任意两组基含有相同数目的向量，该数称为维数：

$$
\dim\operatorname{span}(\alpha_1,\ldots,\alpha_s)
=\operatorname{rank}(\alpha_1,\ldots,\alpha_s).
$$

## 线性方程组的判定 { #linear-system-solvability }

考虑

$$
Ax=b,
$$

其中 $A\in K^{m\times n}$，增广矩阵记为 $(A\mid b)$。Rouché–Capelli 定理给出：

$$
Ax=b\text{ 有解}
\Longleftrightarrow
\operatorname{rank}(A)=\operatorname{rank}(A\mid b).
$$

进一步，设这个公共秩为 $r$：

| 条件 | 解的情况 |
| --- | --- |
| $r=n$ | 唯一解 |
| $r<n$ | 无穷多解，有 $n-r$ 个自由变量 |
| $\operatorname{rank}(A)<\operatorname{rank}(A\mid b)$ | 无解 |

对齐次方程 $Ax=0$，它总有零解，并且

$$
Ax=0\text{ 有非零解}
\Longleftrightarrow
\operatorname{rank}(A)<n.
$$

当 $A$ 是 $n$ 阶方阵时，这又等价于 $\det A=0$。

## 解空间与基础解系

齐次方程的解集

$$
\ker A=\{x:Ax=0\}
$$

是一个向量空间。秩—零化度定理给出

$$
\dim\ker A=n-\operatorname{rank}(A).
$$

$\ker A$ 的任意一组基称为 $Ax=0$ 的基础解系。若基础解系为 $\eta_1,\ldots,\eta_{n-r}$，则通解为

$$
x=k_1\eta_1+\cdots+k_{n-r}\eta_{n-r}.
$$

非齐次方程 $Ax=b$ 有解时，任取一个特解 $x_0$，全部解为

$$
x=x_0+x_h,
\qquad x_h\in\ker A.
$$

因此非齐次解集不是一般意义下的向量空间，而是齐次解空间的一个仿射平移。

??? example "由两个解构造通解"
    若 $\gamma_1$、$\gamma_2$ 都满足 $Ax=b$，则

    $$
    A(\gamma_1-\gamma_2)=0.
    $$

    所以两个特解之差必属于齐次解空间。反过来，给一个特解加上任意齐次解，仍是非齐次方程的解。

## 子空间的和与直和

对子空间 $U,W\subseteq V$，有维数公式

$$
\dim(U+W)=\dim U+\dim W-\dim(U\cap W).
$$

若 $U\cap W=\{0\}$，则每个 $u+w$ 的表示唯一，记为

$$
U\oplus W.
$$

更一般地，若 $V_1,\ldots,V_s$ 的任意一组非零分量之和不可能为零，则

$$
V_1+\cdots+V_s=V_1\oplus\cdots\oplus V_s.
$$

这一观点会在特征子空间分解和矩阵多项式中再次出现。
