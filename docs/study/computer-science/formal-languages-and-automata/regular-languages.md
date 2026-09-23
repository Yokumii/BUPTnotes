# 正则语言与有限自动机

## 有限自动机

### DFA

DFA（确定性有限自动机）是一个五元组 $M = (Q, T, \delta, q_0, F)$：

状态集合 $Q$
: 有限状态集合

输入字母表 $T$
: 有限的输入字母表

转移函数 $\delta$
: $Q \times T \rightarrow Q$，每个状态对每个输入符号有唯一的转移

起始状态 $q_0$
: $q_0 \in Q$

终止状态集合 $F$
: $F \subseteq Q$

$\delta'$ 扩展函数
: 接受字符串输入的状态转移函数：

$$
\delta': Q \times T^* \rightarrow Q
$$

对任何 $q \in Q$，定义如下：

- $\delta'(q, \varepsilon) = q$
- 若 $\omega$ 为字符串，$a$ 为一个字符，则 $\delta'(q, a\omega) = \delta(\delta'(q, \omega), a)$

格局（configuration）
: 当前状态 $q$ 与待输入字符串 $\omega$ 组成的瞬时描述 $(q, \omega)$

被 DFA 接受的字符串
: 输入结束后使 DFA 达到终止状态 $F$ 中某一状态的字符串

### NFA

NFA（非确定性有限自动机）与 DFA 的定义区别仅在于转移函数：

$$
\delta: Q \times T \rightarrow 2^Q
$$

在某个状态对某个输入符号，NFA 可以到达**多个状态**。如果接受字符串后 NFA 能够到达的状态集合与 $F$ 的交集非空，则该字符串被 NFA 接受。

## 正则集与正则式

正则集
: 字母表上一些特殊形式的字符串的集合，是正则式所表示的集合

正则式
: 用类似代数表达式的方式表示正则语言

运算按优先级从高到低排列：

闭包运算 $*$（closure）
: 对字符串集合的重复零次或多次运算

连接运算 $\cdot$（concatenation）
: 两个字符串集合的顺序拼接运算

联合运算 $+$（union）
: 两个字符串集合的并集运算

!!! warning "注意"
    - 正则式相等等价于它们所表示的正则集相等
    - 一个正则式对应一个正则集，但一个正则集可能有多个正确的正则式

## 右线性文法与正则式的等价

右线性文法又称正则文法，右线性文法和正则式都可以表示正则语言。

???+ tip "从右线性文法导出正则式"
    设产生式形如 $x \rightarrow \alpha x + \beta$（即 $x \rightarrow \alpha x$ 和 $x \rightarrow \beta$），其中 $\alpha \in T^*$，$\beta \in (N + T)^*$，$x \in N$，则 $x$ 的解为：

    $$x = \alpha^*\beta$$

    正则集是由右线性文法产生的语言；右线性文法产生的语言都是正则集；一个语言是正则集当且仅当该语言是右线性语言。

## 正则式与有限自动机的等价转换

### DFA 到正则式：状态消去法

???+ info "状态消去法步骤"
    1. 在 DFA 中添加新的起始状态 $q_s$ 和终止状态 $q_f$，并用 $\varepsilon$ 转移连接原起始/终止状态
    2. 逐步消去中间状态，每次消去一个状态时，将其旁路转移合并到剩余状态之间的转移上
    3. 重复步骤 2，直到只剩 $q_s$ 和 $q_f$，此时 $q_s$ 到 $q_f$ 之间的转移标号即为所求正则式

<figure markdown="span">
  ![状态消去法概览](https://webp-pic.yokumi.cn/2026/01/20260101164927593.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![状态消去法具体步骤](https://webp-pic.yokumi.cn/2026/01/20260101164929737.png){ loading=lazy width="70%" }
</figure>

### 正则式到 $\varepsilon$-NFA：归纳构造法

???+ info "归纳构造法"
    根据正则式的结构逐层构造 $\varepsilon$-NFA：
    - 基本情形：单个符号 $a$ 和 $\varepsilon$ 分别构造简单 NFA
    - 联合 $R_1 + R_2$：添加新的起始和终止状态，通过 $\varepsilon$ 转移连接两个子 NFA
    - 连接 $R_1 \cdot R_2$：将 $R_1$ 的终止状态通过 $\varepsilon$ 转移连接到 $R_2$ 的起始状态
    - 闭包 $R_1^*$：添加 $\varepsilon$ 转移形成循环回路

<figure markdown="span">
  ![归纳构造法1](https://webp-pic.yokumi.cn/2026/01/20260101164932613.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![归纳构造法2](https://webp-pic.yokumi.cn/2026/01/20260101164935031.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![归纳构造法3](https://webp-pic.yokumi.cn/2026/01/20260101164938007.png){ loading=lazy width="70%" }
</figure>

## 右线性文法与有限自动机的等价转换

???+ tip "定理"
    由任意右线性文法 $G$ 定义的语言必然能被一个 NFA $M$ 所接受，即 $L(G) = L(M)$。

### 右线性文法到 NFA 的构造

???+ info "构造步骤"
    1. 新增一个状态作为终止状态
    2. 对仍在扩展非终结符的产生式（$A \rightarrow \omega B$），则转移到对应状态 $B$
    3. 对到达终结符的产生式（$A \rightarrow \omega$），则转移到新增的终止状态
    4. 终止状态不存在转移

<figure markdown="span">
  ![右线性文法到NFA构造](https://webp-pic.yokumi.cn/2026/01/20260101164940594.png){ loading=lazy width="70%" }
</figure>

### NFA 到右线性文法的构造

???+ info "构造步骤"
    将 NFA 的每个状态视为非终结符，起始状态对应起始符，终止状态对应能推出终结符串的产生式。转移 $\delta(A, a) = B$ 对应产生式 $A \rightarrow aB$；终止状态 $A \in F$ 还需添加产生式 $A \rightarrow \varepsilon$。

<figure markdown="span">
  ![NFA到右线性文法构造](https://webp-pic.yokumi.cn/2026/01/20260101164944590.png){ loading=lazy width="70%" }
</figure>

## DFA 的极小化

???+ info "填表法（Table-Filling Method）"
    **核心思想：** 如果两个状态在同一输入下转移到可区分的状态，则这两个状态也是可区分的。

    **步骤：**
    1. 初始标记：终态与非终态之间标记为可区分
    2. 递归标记：对未标记的状态对 $(p, q)$，检查每个输入符号 $a$，若 $\delta(p, a)$ 和 $\delta(q, a)$ 已标记为可区分，则标记 $(p, q)$
    3. 重复步骤 2 直到没有新标记产生
    4. 所有未被标记的状态对合并为一个状态

## Pumping 引理

Pumping 引理是判定正则语言的**必要条件**，常用于证明某个语言**不是**正则语言。

???+ tip "定理"
    设 $L$ 是正则集，存在常数 $n$，对字符串 $\omega \in L$ 且 $|\omega| > n$，则 $\omega$ 可以写成 $\omega = \omega_1 \omega_0 \omega_2$，其中：

    - $|\omega_1 \omega_0| \leq n$
    - $|\omega_0| > 0$
    - 对所有的 $i \geq 0$，有 $\omega_1 \omega_0^i \omega_2 \in L$

???+ info "证明非正则语言的四步策略"
    1. **选取 $n$**：对于足够大的常数 $n$
    2. **选取 $\omega$**：找到一个满足 $\omega \in L$ 且 $|\omega| \geq n$ 的字符串
    3. **分析划分**：任选满足 $\omega = \omega_1 \omega_0 \omega_2$ 的划分，其中 $|\omega_1 \omega_0| \leq n$，$|\omega_0| > 0$
    4. **寻找反例**：找到一个 $i$，使得 $\omega_1 \omega_0^i \omega_2 \notin L$

    关键：步骤 3 中需对**所有可能的划分**都进行分析，而非仅针对某一种划分。

## 右线性语言的封闭性

### 并运算封闭

???+ info "文法角度的构造"
    对于右线性语言 $L(G_1)$ 和 $L(G_2)$ 分别由文法 $G_1 = (N_1, T, P_1, S_1)$ 和 $G_2 = (N_2, T, P_2, S_2)$（$N_1 \cap N_2 = \phi$）产生，$L(G) = L(G_1) \cup L(G_2)$ 也为右线性语言。

    构造 $G = (N, T, P, S)$，其中：

    - $N = N_1 \cup N_2 \cup \{S\}$
    - $P = P_1 \cup P_2 \cup \{S \rightarrow S_1 \mid S_2\}$

???+ info "自动机角度的构造"
    添加一个新的初始状态，通过 $\varepsilon$ 转移连接到两个原 NFA 的初始状态，相当于两个自动机并行运行。

### 积运算封闭

???+ info "文法角度的构造"
    对于右线性语言 $L(G_1)$ 和 $L(G_2)$ 分别由文法 $G_1 = (N_1, T, P_1, S_1)$ 和 $G_2 = (N_2, T, P_2, S_2)$（$N_1 \cap N_2 = \phi$）产生，$L(G) = L(G_1) \cdot L(G_2)$ 也为右线性语言。

    构造 $G = (N, T, P, S)$，其中：

    - $N = N_1 \cup N_2$
    - 如果 $A \rightarrow \alpha B \in P_1$，则 $A \rightarrow \alpha B \in P$
    - 如果 $A \rightarrow \alpha \in P_1$，则 $A \rightarrow \alpha S_2 \in P$
    - $P_2 \subseteq P$

???+ info "自动机角度的构造"
    将 $G_1$ 对应的 DFA 的所有终止状态通过 $\varepsilon$ 转移连接到 $G_2$ 对应的 DFA 的初始状态，实现头尾连接。

