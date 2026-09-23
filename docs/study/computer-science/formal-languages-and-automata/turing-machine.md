# 图灵机

## 基本图灵机

图灵机由阿兰·图灵提出，具有以下两个关键性质：

1. 该模型的每个过程都是有穷可描述的；
2. 过程必须是离散的、可以机械执行的步骤组成。

其简单而强大，可以执行任何计算，是一台通用的计算机。

### 图灵机的形式化定义

图灵机 (TM, Turing Machine)

: 定义为七元组 $M = (Q, T, \Sigma, \delta, q_0, B, F)$，其中：

    - $Q$：有限状态集合
    - $T$：有限输入符号集合，$T \subseteq \Sigma$
    - $\Sigma$：有限带符号集合
    - $\delta$：转移函数，$\delta: Q \times \Sigma \rightarrow Q \times \Sigma \times \{L, R\}$
    - $q_0$：开始状态，$q_0 \in Q$
    - $B$：特殊带符，即空白符，$B \in \Sigma - T$
    - $F$：终态集合，$F \subseteq Q$

!!! info "与一般自动机相比，图灵机多了带符号集合 $\Sigma$ 和空白符 $B$（包含在 $\Sigma$ 内但不在输入符号集 $T$ 内）。"

## 转移函数与格局

### 转移函数

转移函数示例：$\delta(q, a_i) = (p, b, L)$，其中 $q, p \in Q$, $a_i, b \in \Sigma$。表示图灵机在状态 $q$ 读到符号 $a_i$ 时，将 $a_i$ 改写为 $b$，读写头左移，状态变为 $p$。

### 格局 (Configuration)

格局 (Instantaneous Description)

: 形为 $w_1 q w_2$，表示图灵机的瞬时状态：

    - $q$ 为图灵机当前状态
    - $w_1 w_2 \in \Sigma$ 表示带上的内容
    - 读写头正扫描 $w_2$ 的最左字符
    - 若 $w_2 = \varepsilon$，则读写头正扫描空白字符 $B$

### 格局推导规则

!!! abstract "格局推导的完整规则"

    **L 移动（左移）：** 若有 $\delta(q, X_i) = (p, Y, L)$，则

    $$
    X_1 X_2 \cdots X_{i-1} q X_i X_{i+1} \cdots X_n \vdash_M X_1 X_2 \cdots X_{i-2} p X_{i-1} Y X_{i+1} \cdots X_n
    $$

    简单理解为：$X_i$ 被 $Y$ 替换，读写头左移，状态由 $q$ 变为 $p$。但有两个边界情况：

    ???+ warning "L 移动的边界情况"
        1. 当 $i = 1$ 时（读写头已在最左端）：

            $$
            q X_1 X_2 \cdots X_n \vdash_M p Y X_2 \cdots X_n
            $$

            仅替换符号，但读写头无法继续左移。

        2. 当 $i = n$ 且 $Y = B$ 时（替换后最右端变空白）：

            $$
            X_1 X_2 \cdots X_{n-1} q X_n \vdash_M X_1 X_2 \cdots X_{n-2} p X_{n-1} B
            $$

    **R 移动（右移）：** 若有 $\delta(q, X_i) = (p, Y, R)$，则

    $$
    X_1 X_2 \cdots X_{i-1} q X_i X_{i+1} \cdots X_n \vdash_M X_1 X_2 \cdots X_{i-1} Y p X_{i+1} \cdots X_n
    $$

    简单理解为：$X_i$ 被 $Y$ 替换，读写头右移，状态由 $q$ 变为 $p$。同样有两个边界情况：

    ???+ warning "R 移动的边界情况"
        1. 当 $i = 1$ 且 $Y = B$ 时（最左端符号被替换为空白）：

            $$
            q X_1 X_2 \cdots X_n \vdash_M B p X_2 \cdots X_n
            $$

        2. 当 $i = n$ 时（读写头在最右端，右移需要扩展带）：

            $$
            X_1 X_2 \cdots X_{n-1} q X_n \vdash_M X_1 X_2 \cdots X_{n-1} Y p B
            $$

            图灵机自动在右端添加空白符 $B$。

## 图灵机接受的语言

图灵机 $M$ 接受的语言定义为：

$$
L(M) = \{\omega \mid \omega \in T^*, q_0 \omega \vdash^* \alpha_1 p \alpha_2, p \in F, \alpha_1, \alpha_2 \in \Sigma^*\}
$$

即：字符串初始时放在图灵机的带上，图灵机处于状态 $q_0$，读写头在最左单元上；字符串输入使图灵机进入某个终止状态并停机。

## 图灵机的停机问题

???+ warning "图灵机的停机问题是不可解的"
    不存在一个通用算法能够判断任意图灵机在任意输入上是否会停机。这是计算机科学中最著名的不可判定问题之一。

    如果没有特别指出，总是假定图灵机到达终态（接受态）后一定停机。

## 图灵机的构造（例题）

### 例 1

<figure markdown="span">
  ![图灵机构造例1 图1](https://webp-pic.yokumi.cn/2026/01/20260101164946930.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![图灵机构造例1 图2](https://webp-pic.yokumi.cn/2026/01/20260101164950019.png){ loading=lazy width="70%" }
</figure>

### 例 2

<figure markdown="span">
  ![图灵机构造例2](https://webp-pic.yokumi.cn/2026/01/20260101164953913.png){ loading=lazy width="70%" }
</figure>
