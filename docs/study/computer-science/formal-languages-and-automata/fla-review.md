# 形式语言与自动机复习

本文为形式语言与自动机课程的综合性复习，结合往年真题解析与概念问答，涵盖核心定义、封闭性、Pumping 引理、CFG 变换等重点内容。

## 核心概念速查

文法（Grammar）
: 四元组 $G=(N,T,P,S)$，其中 $N$ 为非终结符有限集，$T$ 为终结符有限集（$N\cap T=\emptyset$），$P$ 为生成式有限集（形如 $\alpha\rightarrow\beta$），$S\in N$ 为起始符。

Chomsky 层级
: 按对生成式的限制程度，将文法分为 0 型（无限制）、1 型（上下文有关）、2 型（上下文无关）、3 型（正则/右线性/左线性），分别对应递归可枚举语言、上下文有关语言、上下文无关语言、正则语言，以及图灵机、线性有界自动机、下推自动机、有限自动机。

DFA（确定性有限自动机）
: 五元组 $M=(Q,T,\delta,q_0,F)$，其中 $\delta:Q\times T\rightarrow Q$。

NFA（非确定性有限自动机）
: 五元组 $M=(Q,T,\delta,q_0,F)$，其中 $\delta:Q\times T\rightarrow 2^Q$。

PDA（下推自动机）
: 七元组 $M=(Q,T,\Gamma,\delta,q_0,z_0,F)$，其中 $\delta:Q\times(T\cup\{\varepsilon\})\times\Gamma\rightarrow 2^{Q\times\Gamma^*}$。

TM（图灵机）
: 七元组 $M=(Q,T,\Gamma,\delta,q_0,B,F)$，其中 $\delta:Q\times\Gamma\rightarrow Q\times\Gamma\times\{L,R\}$。

正则表达式（Regular Expression）
: 由字母表符号、连接 $\cdot$、联合 $+$、闭包 $*$ 运算构成的代数表达式，用于表示正则集。

CNF（Chomsky 范式）
: 生成式仅形如 $A\rightarrow BC$ 或 $A\rightarrow a$，其中 $A,B,C\in N$，$a\in T$。

GNF（Greibach 范式）
: 生成式仅形如 $A\rightarrow a\beta$，其中 $a\in T$，$\beta\in N^*$。

### Chomsky 文法体系总览

| 类型 | 生成式限制 | 语言 | 自动机 |
|------|-----------|------|--------|
| 0 型 | 无限制 | 递归可枚举语言 | 图灵机 |
| 1 型 | $|\alpha|\le|\beta|$ | 上下文有关语言 | 线性有界自动机 |
| 2 型 | $A\rightarrow\alpha,A\in N$ | 上下文无关语言 | 下推自动机 |
| 3 型 | $A\rightarrow\omega B$ 或 $A\rightarrow\omega$ | 正则语言 | 有限自动机 |

> 详细定义与推导机制见 [文法与自动机概述](fla-overview.md)。

## Chomsky 文法体系

Chomsky 文法体系根据对生成式的限制程度，将文法分为四类（0 型到 3 型），每类对应一类语言和一类识别自动机。上面的总览表已给出了完整的对应关系。

<figure markdown="span">
  ![Chomsky 文法体系关系图](https://webp-pic.yokumi.cn/2026/01/20260101165112550.png){ loading=lazy width="70%" }
</figure>

## 右线性文法、正则式和有限自动机

右线性文法（正则文法）、正则式和有限自动机三者在描述能力上等价，可以相互转换：

<figure markdown="span">
  ![右线性文法、正则式与有限自动机的关系](https://webp-pic.yokumi.cn/2026/01/20260101165115498.png){ loading=lazy width="70%" }
</figure>

## 语言的封闭性

### 上下文无关语言的封闭性

对并、积（连接）、闭包、置换封闭，对交和补**不封闭**。

#### 并封闭

对于 $L(G_1)$ 和 $L(G_2)$ 分别由 $G_1=(N_1,T_1,P_1,S_1)$ 和 $G_2=(N_2,T_2,P_2,S_2)$（$N_1\cap N_2=\emptyset$）产生，$L(G_1)\cup L(G_2)$ 也为 2 型语言。

构造 $G=(N,T,P,S)$：

- $N=N_1\cup N_2\cup\{S\}$
- $T=T_1\cup T_2$
- $P=P_1\cup P_2\cup\{S\rightarrow S_1\mid S_2\}$
- $S=S$

#### 积运算封闭

$L(G_1)\cdot L(G_2)$ 也为 2 型语言。构造 $G=(N,T,P,S)$：

- $N=N_1\cup N_2\cup\{S\}$
- $T=T_1\cup T_2$
- $P=P_1\cup P_2\cup\{S\rightarrow S_1S_2\}$
- $S=S$

!!! warning "交集和补集不封闭"
    存在两个 CFL $L_1$ 和 $L_2$，使得 $L_1\cap L_2$ 不是 CFL。例如 $L_1=\{a^n b^n c^m\}$ 和 $L_2=\{a^m b^n c^n\}$，交集为 $\{a^n b^n c^n\}$，这不是 CFL。同理，CFL 的补集也不一定封闭。

### 右线性语言的封闭性

#### 并封闭

**文法角度**：对于 $L(G_1)$ 和 $L(G_2)$（$N_1\cap N_2=\emptyset$），构造 $G=(N,T,P,S)$：

- $N=N_1\cup N_2\cup\{S\}$
- $P=P_1\cup P_2\cup\{S\rightarrow S_1\mid S_2\}$

**自动机角度**：添加新的初始状态，分别向两个自动机的初始状态做 $\varepsilon$ 转移。

<figure markdown="span">
  ![右线性语言并封闭——自动机角度](https://webp-pic.yokumi.cn/2026/01/20260101165103237.png){ loading=lazy width="70%" }
</figure>

#### 积运算封闭

**文法角度**：构造 $G=(N,T,P,S)$：

- $N=N_1\cup N_2$
- 若 $A\rightarrow\alpha B\in P_1$，则 $A\rightarrow\alpha B\in P$
- 若 $A\rightarrow\alpha\in P_1$，则 $A\rightarrow\alpha S_2\in P$
- $P_2\subseteq P$

**自动机角度**：头尾连接——将第一个自动机的终止状态通过 $\varepsilon$ 转移连接到第二个自动机的初始状态。

<figure markdown="span">
  ![右线性语言积运算封闭——自动机角度](https://webp-pic.yokumi.cn/2026/01/20260101165106611.png){ loading=lazy width="70%" }
</figure>

## Pumping 引理

Pumping 引理用于证明某个语言**不是**某类语言（正则语言或 CFL），是必要条件而非充分条件。

### 正则语言的 Pumping 引理

**定理**：设 $L$ 是正则集，存在常数 $n$，对 $\omega\in L$ 且 $|\omega|>n$，则 $\omega$ 可写成 $\omega=\omega_1\omega_0\omega_2$，其中 $|\omega_1\omega_0|\le n$，$|\omega_0|>0$，对所有 $i\ge 0$，有 $\omega_1\omega_0^i\omega_2\in L$。

**4 步证明策略**：

1. 对于足够大的 $n$；
2. 找到一个满足条件的串 $\omega\in L$（$|\omega|\ge n$）；
3. 任选满足 $\omega=\omega_1\omega_0\omega_2$（$|\omega_1\omega_0|\le n$，$|\omega_0|>0$）的分解；
4. 找到一个 $i$，使得 $\omega_1\omega_0^i\omega_2\notin L$。

???+ success "例题：证明 $L=\{0^k1^k\mid k\ge 1\}$ 不是正则语言"

    1. 设 $n$ 为 Pumping 引理常数；
    2. 取 $\omega=0^n1^n\in L$，$|\omega|=2n>n$；
    3. 由于 $|\omega_1\omega_0|\le n$ 且 $\omega_1\omega_0$ 位于 $\omega$ 的前 $n$ 位内，故 $\omega_0$ 只包含 $0$，设 $\omega_0=0^m$（$m>0$）；
    4. 取 $i=2$，则 $\omega_1\omega_0^2\omega_2=0^{n+m}1^n$，其中 $0$ 的个数与 $1$ 的个数不相等，故 $\omega_1\omega_0^2\omega_2\notin L$；

    因此 $L$ 不是正则语言。

### CFL 的 Pumping 引理

**定理**：设 $L$ 是上下文无关语言，存在常数 $p$，若 $\omega\in L$ 且 $|\omega|\ge p$，则 $\omega$ 可写为 $\omega=\omega_1\omega_2\omega_0\omega_3\omega_4$，使得 $\omega_2\omega_3\ne\varepsilon$，$|\omega_2\omega_0\omega_3|\le p$，对所有 $i\ge 0$，有 $\omega_1\omega_2^i\omega_0\omega_3^i\omega_4\in L$。

**证明策略**：与正则语言类似——取足够长的串，对所有合法分解，找到一个 $i$ 使得泵出后的串不在语言中。

!!! warning "CFL Pumping 引理的要点"
    CFL Pumping 引理中 $\omega_2$ 和 $\omega_3$ 的重复次数**必须相同**（都是 $i$），这意味着只能证明那些需要两个子串以不同速率增长才能满足的语言不是 CFL。

## CFG 变换例题

CFG 化简的标准步骤为：消除 $\varepsilon$ 产生式 → 消除单产生式 → 消除无用符号。化简后可进一步转换为 CNF 或 GNF。

### 例题 1：CFG 化简与 CNF 转换（某年期末 B 卷）

<figure markdown="span">
  ![例题 1 原题](https://webp-pic.yokumi.cn/2026/01/20260101165030839.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    1. **先化简 CFG**（消除 $\varepsilon$ 产生式、单产生式、无用符号）：

    ```
    N = { A, B, C, D, S }
    T = { a, b, c }
    P:
    A -> b
    B -> A C | B C | b
    C -> b
    D -> a B | c
    S -> A B | A C | B C | C D D | b
    S = S
    ```

    2. **转换为 CNF**：将终结符用新非终结符替换，将右部长度超过 2 的生成式逐步拆分：

    ```
    N = { A, B, C, D, S, E, G }
    T = { a, b, c }
    P:
    A -> b
    B -> A C | B C | b
    C -> b
    D -> E B | c
    S -> A B | A C | B C | C G | b
    E -> a
    G -> D D
    S = S
    ```

### 例题 2：CFG 化简与 CNF 转换（21-22 期末试题 4）

<figure markdown="span">
  ![例题 2 原题](https://webp-pic.yokumi.cn/2026/01/20260101165035724.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    1. **先化简 CFG**（A 不可达，删除）：

    ```
    N = { B, S }
    T = { a, b, c }
    P:
    B -> a B B | b | c S
    S -> a B | b b
    S = S
    ```

    2. **转换为 CNF**：

    ```
    N = { S, B, C, D, E, F }
    T = { a, b, c }
    P:
    S -> C C | D B
    B -> D F | E S | b
    C -> b
    D -> a
    E -> c
    F -> B B
    S = S
    ```

### 例题 3：CFG 化简与 CNF 转换（21-22 期末试题 5）

<figure markdown="span">
  ![例题 3 原题](https://webp-pic.yokumi.cn/2026/01/20260101165033718.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    已经是最简的 CFG，直接转换为 Chomsky 范式：

    ```
    N = { S, A, B }
    T = { a, b, c }
    P:
    S -> C C | A B
    A -> C F | D S | a
    B -> D G | E S | b
    C -> b
    D -> a
    E -> c
    F -> D A
    G -> B B
    S = S
    ```

### 例题 4：含 $\varepsilon$ 产生式和单产生式的化简（19-20 期末试题 5）

<figure markdown="span">
  ![例题 4 原题](https://webp-pic.yokumi.cn/2026/01/20260101165043504.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    A 可致空，$(A,B)$ 是单元偶对，C 非生成。化简后：

    ```
    N = { A, B, D, S }
    T = { a, b, c, d }
    P:
    A -> a b B
    B -> a | a A
    D -> d d d
    S -> a | a A | b | b A | c c D
    S = S
    ```

### 例题 5：含 $\varepsilon$ 产生式和单产生式的化简（19-20 期末试题 4）

<figure markdown="span">
  ![例题 5 原题](https://webp-pic.yokumi.cn/2026/01/20260101165046193.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    A 可致空，$(S,A)$ 和 $(S,B)$ 是单元偶对，C 非生成，D 不可达。化简后：

    ```
    N = { A, B, S }
    T = { a, d }
    P:
    A -> a B
    B -> a | a A
    S -> a | a A | d d d
    S = S
    ```

### 例题 6：含 $\varepsilon$ 产生式和单产生式的化简（19-20 期末试题 3）

<figure markdown="span">
  ![例题 6 原题](https://webp-pic.yokumi.cn/2026/01/20260101165051631.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    A 可致空，$(S,B)$、$(S,C)$、$(S,D)$ 是单元偶对，C 非生成，D 不可达。化简后：

    ```
    N = { A, B, S }
    T = { a, d }
    P:
    A -> a B
    B -> A a | a
    S -> A a | a | a a | d d
    S = S
    ```

### 例题 7：含 $\varepsilon$ 产生式和单产生式的化简（19-20 期末试题 2）

<figure markdown="span">
  ![例题 7 原题](https://webp-pic.yokumi.cn/2026/01/20260101165055762.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    A 可致空，$(S,B)$ 和 $(S,C)$ 是单元偶对，C 非生成，D 不可达。化简后：

    ```
    N = { A, B, S }
    T = { a }
    P:
    A -> a B
    B -> a | a A
    S -> a | a A | a a a
    S = S
    ```

### 例题 8：含 $\varepsilon$ 产生式和单产生式的化简（19-20 期末试题 1）

<figure markdown="span">
  ![例题 8 原题](https://webp-pic.yokumi.cn/2026/01/20260101165058211.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    A 可致空，$(S,B)$ 和 $(S,C)$ 是单元偶对，C 非生成，D 不可达。化简后：

    ```
    N = { A, B, S }
    T = { a }
    P:
    A -> a B
    B -> a | a A
    S -> a | a A
    S = S
    ```

### 例题 9：CNF 转换（21-22 期末试题 3）

<figure markdown="span">
  ![例题 9 原题](https://webp-pic.yokumi.cn/2026/01/20260101165038070.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    已经是最简的 CFG，Chomsky 范式如下：

    ```
    N = { A, B, C, D, S, E, F }
    T = { a, b, c }
    P:
    S -> C A | D B
    A -> C D A | D S | a
    B -> D F | E S | b
    C -> b
    D -> a
    E -> c
    F -> B B
    S = S
    ```

### 有限自动机转换例题

#### 例题 A：正则式 → NFA → DFA（22-23 期末试题 1、2、3）

<figure markdown="span">
  ![有限自动机转换例题 A 原题](https://webp-pic.yokumi.cn/2026/01/20260101164956549.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    <figure markdown="span">
      ![转换后的 NFA](https://webp-pic.yokumi.cn/2026/01/20260101164959213.png){ loading=lazy width="70%" }
    </figure>

#### 例题 B：正则式 → NFA → DFA（19-20 期末试题 5 之一）

<figure markdown="span">
  ![有限自动机转换例题 B 原题](https://webp-pic.yokumi.cn/2026/01/20260101165001562.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    转换后的 NFA：

    <figure markdown="span">
      ![转换后的 NFA](https://webp-pic.yokumi.cn/2026/01/20260101165005169.png){ loading=lazy width="70%" }
    </figure>

    转换后的 DFA：

    <figure markdown="span">
      ![转换后的 DFA](https://webp-pic.yokumi.cn/2026/01/20260101165007425.png){ loading=lazy width="70%" }
    </figure>

#### 例题 C：正则式 → NFA → DFA（19-20 期末试题 5 之二）

<figure markdown="span">
  ![有限自动机转换例题 C 原题](https://webp-pic.yokumi.cn/2026/01/20260101165010500.png){ loading=lazy width="70%" }
</figure>

???+ success "解析"

    转换后的 NFA：

    <figure markdown="span">
      ![转换后的 NFA](https://webp-pic.yokumi.cn/2026/01/20260101165012839.png){ loading=lazy width="70%" }
    </figure>

    转换后的 DFA：

    <figure markdown="span">
      ![转换后的 DFA](https://webp-pic.yokumi.cn/2026/01/20260101165015277.png){ loading=lazy width="70%" }
    </figure>

## PDA 与 CFG 的相互变换

### CFG → PDA

设 CFG $G=(N,T,P,S)$，构造空栈接受的 PDA $M=(Q,T,\Gamma,\delta,q_0,z_0,F)$：

- $Q=\{q\}$，$\Gamma=N\cup T$，$z_0=S$，$F=\emptyset$
- $\forall A\in N$：$\delta(q,\varepsilon,A)=\{(q,\beta)\mid A\rightarrow\beta\in P\}$（非终结符出栈替换）
- $\forall a\in T$：$\delta(q,a,a)=\{(q,\varepsilon)\}$（终结符匹配消耗）

### PDA → CFG

设空栈接受的 PDA $M=(Q,T,\Gamma,\delta,q_0,z_0,F)$，构造 CFG $G=(N,T,P,S)$：

- 非终结符形为 $[q,A,\gamma]$，表示从状态 $q$、栈顶 $A$ 到状态 $\gamma$ 的过程
- $\forall q\in Q$：$S\rightarrow[q_0,z_0,q]$
- $(\gamma,\varepsilon)\in\delta(q,a,A)$：$[q,A,\gamma]\rightarrow a$
- $(\gamma,B_1B_2\cdots B_k)\in\delta(q,a,A)$：枚举所有状态序列 $q_1\cdots q_k$，$[q,A,q_k]\rightarrow a[\gamma,B_1,q_1][q_1,B_2,q_2]\cdots[q_{k-1},B_k,q_k]$

> 详细算法见 [上下文无关文法和下推自动机](cfg-and-pda.md)。

## 图灵机构造

图灵机是形式语言与自动机理论中最强大的计算模型，能够识别递归可枚举语言（0 型语言）。构造图灵机的核心是设计状态转移函数 $\delta:Q\times\Gamma\rightarrow Q\times\Gamma\times\{L,R\}$，使得机器能正确识别目标语言。

> 详细构造方法见 [图灵机](turing-machine.md)。

## 常见问答

!!! abstract "概念问答"

    ### 为什么要消除左递归？

    以后的句法分析算法不适用于左递归，会引起死循环。在编写 $E$ 的递归下降解析函数时，直接在函数开头递归调用自己，输入字符串完全没有消耗，这种递归调用就会变成一种死循环。

    ### 2 型语言（上下文无关语言）有什么用？

    可定义程序设计语言、进行语法分析、简化语言翻译。上下文无关文法能够解析递归结构（如嵌套括号、if-else 语句），是编译器中语法分析器的基础。

    ### 正则语言有什么用？

    编译器中使用正则表达式、正则语言和 DFA 等工具实现了词法分析，即将输入的字符串分解成一个个的单词流——诸如编程语言中的关键字、标识符这样有特定意义的单词。

    ### 上下文无关文法构造等价的下推自动机时，为什么这么构造？

    由于对栈中非终结符的替换总是在栈顶进行，PDA 实际上模拟的是文法的**最右推导**过程。栈从左到右对应句型中尚未被替换的非终结符，每次栈顶替换就是一个最右推导步骤。

