# 上下文无关文法与下推自动机

## 基本概念

### CFG 定义

上下文无关文法 (CFG, Context-Free Grammar)

: 定义为四元组 $G = (N, T, P, S)$，其中：

    - $N$：非终结符的有限集合
    - $T$：终结符的有限集合
    - $P$：产生式的有限集合，形如 $A \rightarrow \alpha$, $A \in N$, $\alpha \in (N \cup T)^*$
    - $S$：起始符号，$S \in N$

通过 Python 定义 CFG 类如下：

```python
from typing import Set, Tuple, Dict, List
from collections import defaultdict

# Symbol 是终结符或非终结符或它们的集合，统一用 str 表示
Symbol = str
NonTerminal = str
Terminal = str
Production = Tuple[NonTerminal, Tuple[Symbol, ...]]  # 将 A -> aB 用元组表示为 (A, (a, B))

class CFG:
    def __init__(self,
                 N: Set[NonTerminal],
                 T: Set[Terminal],
                 P: Set[Production],
                 S: NonTerminal):
        self.N = N
        self.T = T
        self.P = P
        self.S = S
```

#### 推导树

推导树 (Derivation Tree)

: 以起始符为根节点、非终结符为枝节点、终结符为叶子节点的树结构。叶子从左向右组成的字符串称为推导树的**边缘**，记为 $S \Rightarrow \omega$，说明该文法能产生句子 $\omega$。

#### 最左/最右推导

最左推导 (Leftmost Derivation)

: 每次替换最左边的非终结符，记为 $A \Rightarrow^{lm}* \omega$

最右推导 (Rightmost Derivation)

: 每次替换最右边的非终结符，记为 $A \Rightarrow^{rm}* \omega$

#### 归约

归约 (Reduction)

: 推导树从下到上的构造过程，与推导相反。

#### 二义性

二义性 (Ambiguity)

: 如果对于句子 $\omega \in L(G)$，存在两棵不同的但边缘都为 $\omega$ 的推导树，那么称该上下文无关文法是二义的。

### 产生式标准形式

Chomsky 范式 (CNF)

: 产生式形如 $A \rightarrow BC$ 或 $A \rightarrow a$，其中 $A, B, C \in N$, $a \in T$。简单来说，就是产生式右边只含有非终结符或只含有终结符。

Greibach 范式 (GNF)

: 产生式形如 $A \rightarrow a\beta$，其中 $a \in T$, $\beta \in N^*$。简单来说，就是产生式右边为单个终结符后接零个或多个非终结符。

!!! info "为将所有上下文无关文法统一为范式，需要进行化简，具体见 CFG 变换算法。"

### PDA (下推自动机)

NPDA (非确定性下推自动机)

: 定义为七元组 $M = (Q, T, \Gamma, \delta, q_0, z_0, F)$，其中：

    - $Q$：有限状态集合
    - $T$：有限输入字母表
    - $\Gamma$：有限下推栈字母表
    - $\delta$：转移函数，$\delta: Q \times (T \cup \{\varepsilon\}) \times \Gamma \rightarrow Q \times \Gamma^*$，其中 $\delta(q, a, Z) = \{(q', \alpha)\}$ 表示当前栈顶为 $Z$，输入字符 $a$，从状态 $q$ 转移到状态 $q'$，栈顶变为 $\alpha$
    - $q_0$：起始状态，$q_0 \in Q$
    - $z_0$：下推栈的起始符号，$z_0 \in \Gamma$
    - $F$：终态集合，$F \subseteq Q$

PDA 的接受方式有两种：

空栈接受 (Acceptance by Empty Stack)

: $L_\emptyset(M) = \{\omega \mid (q_0, \omega, z_0) \vdash^* (q, \varepsilon, \varepsilon)\}$，即输入串被完全消耗且栈被清空。

终态接受 (Acceptance by Final State)

: $L_f(M) = \{\omega \mid (q_0, \omega, z_0) \vdash^* (q_f, \varepsilon, \gamma), q_f \in F\}$，即输入串被完全消耗且到达终态。

!!! info "两种接受方式是等价的：空栈接受的 PDA 可以构造等价的终态接受 PDA，反之亦然。"

## CFG 变换算法

### 删除无用符号

有用符号 (Useful Symbol)

: $X \in (N \cup T)^*$ 为有用符号，当且仅当 $S \Rightarrow^* \alpha X \beta \Rightarrow^* \omega$，即出现在推导出句子的过程中。

生成符号 (Generating Symbol)

: $X \Rightarrow^* \omega$，即能推导出全是终结符的字符串。也称有用非终结符。

可达符号 (Reachable Symbol)

: $S \Rightarrow^* \alpha X \beta$，即从起始符号开始能推导出的所有符号。

!!! warning "有用符号是既生成又可达的符号，化简时先分别找出生成符号和可达符号，再删除非生成符号和不可达符号。执行顺序不能颠倒！"

#### 找出生成符号

???+ info "算法：找出生成符号"
    **输入：** CFG $G = (N, T, P, S)$
    **输出：** $N'$：有用的非终结符集合

    1. $N' \leftarrow \emptyset$
    2. $N'' \leftarrow \{A \mid A \rightarrow \omega \text{ 且 } \omega \in T^*\}$
    3. **while** $N' \neq N''$：
        - $N' \leftarrow N''$
        - $N'' \leftarrow N'' \cup \{A \mid A \rightarrow \alpha \text{ 且 } \alpha \in (T \cup N')^*\}$
    4. **return** $N''$

    简单来说：先把能直接产生终结符串的非终结符加入，再逐轮将能产生上一轮有用非终结符和终结符组合的非终结符加入，直到不能再增加。算法复杂度为 $O(n)$，其中 $n$ 为文法的规模。

#### 找出可达符号

???+ info "算法：找出可达符号"
    **输入：** CFG $G = (N, T, P, S)$
    **输出：** $N'$：可达符号集合

    1. $N' \leftarrow \{S\}$
    2. $N'' \leftarrow N' \cup \{X \mid X \in (N \cup T) \text{ 且存在 } A \rightarrow \alpha X \beta \in P \text{ 且 } A \in N'\}$
    3. **while** $N' \neq N''$：
        - $N' \leftarrow N''$
        - $N'' \leftarrow N' \cup \{X \mid X \in (N \cup T) \text{ 且存在 } A \rightarrow \alpha X \beta \in P \text{ 且 } A \in N'\}$
    4. **return** $N''$

    注意：教材上同时删去了包含不可达符号的产生式。算法复杂度也为 $O(n)$。

#### 删除步骤

!!! abstract "删除无用符号的正确顺序"
    1. 先执行找出生成符号的算法，找出所有生成符号
    2. 删除非生成符号及包含它们的产生式
    3. 再执行找出可达符号的算法，找出所有可达符号
    4. 删除不可达符号及包含它们的产生式

    **顺序不能颠倒！** 如果先删除不可达符号，可能使原本不可生成的符号变得可达，导致错误。

### 消除 epsilon 产生式

epsilon 产生式

: 形如 $A \rightarrow \varepsilon$ 的产生式，会给推导带来麻烦，一般需要删除。除非 $L(G)$ 包含空串，则需保留 $S \rightarrow \varepsilon$。

无 epsilon 文法

: 一个 CFG $G = (N, T, P, S)$，不含有任何 $\varepsilon$ 产生式，或只含有 $S \rightarrow \varepsilon$ 且 $S$ 不在任何产生式的右边。

可空符号 (Nullable Symbol)

: $N_\varepsilon = \{A \mid A \in N \text{ 且 } A \Rightarrow^+ \varepsilon\}$，即所有能推导出 $\varepsilon$ 的非终结符。使用找出生成符号的算法，将终结符替换为 $\varepsilon$ 即可得到。

???+ info "算法：消除 epsilon 产生式"
    **输入：** CFG $G = (N, T, P, S)$
    **输出：** 无 $\varepsilon$ 文法 $G_1 = (N_1, T, P_1, S_1)$

    1. 找出能推出 $\varepsilon$ 的非终结符集合 $N_\varepsilon$
    2. 初始化 $P_1 = \emptyset$
    3. **for each** $A \rightarrow \alpha \in P$：
        - **if** $\alpha \neq \varepsilon$：跳过 $\varepsilon$ 产生式
            - 找出 $\alpha$ 中属于 $N_\varepsilon$ 的符号位置（标记可空符号的位置）
            - **for each** 可能的子集（遍历将可空符号置空的所有排列组合）：
                - 构造将某些位置符号置空后的 $\alpha'$
                - **if** $\alpha' \neq \varepsilon$（确保右部非空）：
                    - $P_1 \gets P_1 \cup \{A \rightarrow \alpha'\}$
    4. **if** $S \in N_\varepsilon$：
        - 引入新的起始符号 $S_1$
        - $N_1 \gets N \cup \{S_1\}$
        - $P_1 \gets P_1 \cup \{S_1 \rightarrow S, S_1 \rightarrow \varepsilon\}$

        **else**：
        - $N_1 \gets N$, $S_1 \gets S$

    5. **return** $G_1 = (N_1, T, P_1, S_1)$

    简单解释：对于一个右侧含可空符号的产生式，枚举其中可空符号是否为空的所有排列组合（除了全为空的情况），生成新的产生式。如果 $S$ 也可以推出 $\varepsilon$，则新加 $S_1$ 作为新起始符。

### 消除单产生式 (Unit Productions)

单产生式 (Unit Production)

: 形如 $A \rightarrow B$, $A, B \in N$ 的产生式。

单元偶对 (Unit Pair)

: $(A, B)$, $A, B \in N$ 为单元偶对，当且仅当 $A \Rightarrow^* B$，且该推导过程仅使用单产生式。

???+ info "算法：消除单产生式"
    **输入：** CFG $G = (N, T, P, S)$
    **输出：** $G_1 = (N, T, P_1, S)$：消除单产生式后的文法

    1. **for each** $A \in N$：
        - $N_A \gets \{A\}$（初始化集合，$N_A$ 是可由 $A$ 通过单产生式推出的非终结符集合）
        - $N' \gets \{C \mid B \rightarrow C \in P \text{ 且 } B \in N_A\} \cup N_A$
        - **repeat**：
            - $N_A \gets N'$
            - $N' \gets \{C \mid B \rightarrow C \in P \text{ 且 } B \in N_A\} \cup N_A$
        - **until** $N_A = N'$

    2. $P_1 \gets \emptyset$

    3. **for each** $B \rightarrow \alpha \in P$：
        - **if** $\alpha \notin N$（不是单产生式）：
            - **for each** $A \in N_B$：
                - $P_1 \gets P_1 \cup \{A \rightarrow \alpha\}$

    4. **return** $G_1 = (N, T, P_1, S)$

    简单来说：对每个非终结符 $A$，找出所有通过单产生式链可到达的非终结符集合 $N_A$，然后将 $N_A$ 中每个非终结符的非单产生式直接复制给 $A$。

### CFG 的化简

!!! abstract "CFG 化简的正确顺序"
    CFG 的化简必须按照以下顺序执行：

    1. 消除 $\varepsilon$ 产生式
    2. 消除单产生式
    3. 消除无用符号

    顺序不能颠倒，否则可能引入新的 $\varepsilon$ 产生式或单产生式。

### 消除左递归

左递归 (Left Recursion)

: 文法存在形如 $A \Rightarrow^+ A\beta$, $A \in N$ 的推导。

循环文法 (Cycle)

: 文法存在形如 $A \Rightarrow^+ A$, $A \in N$ 的推导。

#### 直接左递归的消除

对于产生式 $A \rightarrow A\alpha \mid \beta$（其中 $\beta$ 不以 $A$ 开头），替换为：

$$
A \rightarrow \beta A', \quad A' \rightarrow \alpha A' \mid \varepsilon
$$

#### 一般左递归的消除

???+ info "算法：消除左递归（含间接左递归）"
    **输入：** CFG $G = (N, T, P, S)$
    **输出：** $G' = (N', T, P', S)$：消除左递归后的文法

    1. 按某种顺序排列所有非终结符 $A_1, A_2, \dots, A_n$
    2. $P' \gets \emptyset$
    3. **for** $i = 1$ to $n$：
        - **for** $j = 1$ to $i - 1$（消除间接左递归）：
            - **for each** $A_i \rightarrow A_j \gamma \in P$：
                - **for each** $A_j \rightarrow \delta \in P'$：
                    - 用 $A_i \rightarrow \delta \gamma$ 替换 $A_i \rightarrow A_j \gamma$
                - 从 $P$ 中移除 $A_i \rightarrow A_j \gamma$
        - 初始化：$\alpha \gets \{\text{形如 } A_i \rightarrow A_i \gamma\}$（左递归规则）
        - 初始化：$\beta \gets \{\text{形如 } A_i \rightarrow \delta \mid \delta \text{ 不以 } A_i \text{ 开头}\}$（非左递归规则）
        - **if** $\alpha \neq \emptyset$（存在直接左递归）：
            - 引入新非终结符 $A_i'$
            - $N' \gets N' \cup \{A_i'\}$
            - $P' \gets P' \cup \{A_i \rightarrow \beta A_i' \mid \beta \in \beta\}$（注：对每个 $\beta$ 添加 $A_i \rightarrow \beta A_i'$）
            - $P' \gets P' \cup \{A_i' \rightarrow \gamma A_i' \mid A_i \rightarrow A_i \gamma \in \alpha\}$（注：对每个 $\gamma$ 添加 $A_i' \rightarrow \gamma A_i'$）
            - $P' \gets P' \cup \{A_i' \rightarrow \varepsilon\}$

        **else**：
            - $P' \gets P' \cup \{A_i \rightarrow \delta\}$（所有以 $A_i$ 为左部的规则）

    4. **return** $G' = (N', T, P', S)$

### 一般 CFG -> CNF

将一般 CFG 转换为 Chomsky 范式的步骤：

???+ info "算法：CFG 转换为 CNF"
    1. 化简 CFG（消除 $\varepsilon$ 产生式、消除单产生式、消除无用符号）
    2. 对于产生式 $A \rightarrow D_1 D_2 \cdots D_n \in P$, $n \ge 2$：
        - 如果 $D_i \in N$，则 $B_i = D_i$
        - 如果 $D_i \in T$，则引入新非终结符 $B_i$ 和 $B_i \rightarrow D_i$
        - 如此，产生式变为 $A \rightarrow a$ 或 $A \rightarrow B_1 B_2 \cdots B_n$，已达到 CNF 的形式要求
    3. 对于产生式 $A \rightarrow B_1 B_2 \cdots B_n$, $n \ge 3$ 进一步拆分：
        - $A \rightarrow B_1 C_1$
        - $C_1 \rightarrow B_2 C_2$
        - $\cdots$
        - $C_{n-2} \rightarrow B_{n-1} B_n$

### 一般 CFG -> GNF

将一般 CFG 转换为 Greibach 范式的步骤：

???+ info "算法：CFG 转换为 GNF"
    1. 先将一般 CFG 变换为 Chomsky 范式
    2. 消除左递归
    3. 回代：
        - 消除左递归后，$A_i$ 的产生式右部最左侧要么是比 $i$ 大的非终结符，要么是终结符
        - 将 $A_n$ 回代回 $A_{n-1}$ 的产生式；$A_{n-1}$ 回代回 $A_{n-2}$ 的产生式；依此类推
    4. 将 $A_i'$ 的产生式右部左侧的非终结符也进行代换

!!! info "GNF 转换的完整步骤比较复杂，往年题似乎没有出现过完整的 GNF 转换。"

## CFG 与 PDA 的相互变换

### CFG => PDA

设 CFG $G = (N, T, P, S)$，构造与之等价的**空栈接受 PDA** $M = (Q, T, \Gamma, \delta, q_0, z_0, F)$：

???+ info "构造方法：CFG 转 PDA"
    令：

    - $Q = \{q\}$（单状态）
    - $\Gamma = N \cup T$
    - $q_0 = q$
    - $z_0 = S$
    - $F = \emptyset$

    转移函数按如下方式构造：

    1. $\forall A \in N$，$\delta(q, \varepsilon, A) = \{(q, \beta) \mid A \rightarrow \beta \in P\}$

        即：遇到栈顶是非终结符 $A$ 时，不消耗输入，用 $A$ 的某个产生式的右部 $\beta$ 替换栈顶的 $A$。

    2. $\forall a \in T$，$\delta(q, a, a) = \{(q, \varepsilon)\}$

        即：遇到栈顶是终结符 $a$ 且当前输入也是 $a$ 时，消耗输入 $a$ 并弹出栈顶的 $a$。

    注：$A \rightarrow \varepsilon$ 这种产生式变换为 $\delta(q, \varepsilon, A) = \{(q, \varepsilon)\}$。

!!! info "由于对栈中非终结符的替换总是在栈顶进行，因此 PDA 实际上模拟的是文法的最右推导过程。"

### PDA => CFG

设空栈接受的 PDA $M = (Q, T, \Gamma, \delta, q_0, z_0, F)$，其接受的语言为 $L_\emptyset(M)$，构造 CFG $G = (N, T, P, S)$，使 $L(G) = L_\emptyset(M)$。

???+ info "构造方法：PDA 转 CFG（最复杂的构造）"
    **非终结符的含义：**

    非终结符形为 $[q, A, p]$，$q, p \in Q$, $A \in \Gamma$。其含义是：在状态 $q$ 下栈顶为 $A$ 时，接受某字符串后转移到状态 $p$ 且弹出栈顶 $A$。

    **构造产生式集合 $P$ 的步骤：**

    1. $\forall q \in Q$，将 $S \rightarrow [q_0, z_0, q]$ 加入产生式集合 $P$

        即：起始符号可以推导出从初始状态 $q_0$、栈顶为 $z_0$ 开始，到达任意状态 $q$ 且弹出 $z_0$ 的过程。

    2. $(p, \varepsilon) \in \delta(q, a, A)$（即栈顶 $A$ 被直接弹出），将 $[q, A, p] \rightarrow a$ 加入 $P$

        即：一步转移（弹出栈顶 $A$，不压入新符号）对应产生式 $[q, A, p] \rightarrow a$。

    3. $(p, B_1 B_2 \cdots B_k) \in \delta(q, a, A)$, $k \ge 1$, $B_i \in \Gamma$，则枚举所有可能的状态序列 $q_1, q_2, \cdots, q_k \in Q$，将

        $$
        [q, A, q_k] \rightarrow a [p, B_1, q_1] [q_1, B_2, q_2] \cdots [q_{k-1}, B_k, q_k]
        $$

        加入 $P$。

        即：压入 $k$ 个栈符号时，需要枚举中间状态序列来确保每个栈符号依次被弹出。

    4. 可将非终结符 $[q, A, p]$ 替换为大写字母符号表示以简化书写。

    **直观理解：**

    PDA 的一次转移可能将栈顶 $A$ 替换为多个栈符号 $B_1 B_2 \cdots B_k$。要让 $[q, A, q_k]$ 表示"从状态 $q$ 开始，栈顶为 $A$，最终到达状态 $q_k$ 且 $A$ 完全被弹出"，需要保证中间的每个 $B_i$ 也依次被弹出。这就需要枚举所有可能的状态序列 $q_1, \cdots, q_k$ 来"串联"每个栈符号的弹出过程。

???+ info "算法：PDA 转 CFG（伪代码）"
    **输入：** PDA $M = (Q, T, \Gamma, \delta, q_0, z_0, F)$
    **输出：** CFG $G = (N, T, P, S)$

    1. $N \gets \{[p, A, q] \mid p, q \in Q, A \in \Gamma\} \cup \{S\}$
    2. $P \gets \emptyset$
    3. **for each** $q \in Q$：
        - $P \gets P \cup \{S \rightarrow [q_0, z_0, q]\}$
    4. **for each** $(q, a, A) \in Q \times (T \cup \{\varepsilon\}) \times \Gamma$：
        - **for each** $(p, B_1 B_2 \cdots B_k) \in \delta(q, a, A)$：
            - **for each** 状态序列 $q_1, q_2, \cdots, q_k \in Q$：
                - **if** $k \ge 1$：
                    - $P \gets P \cup \{[q, A, q_k] \rightarrow a [p, B_1, q_1] [q_1, B_2, q_2] \cdots [q_{k-1}, B_k, q_k]\}$
                - **else**（$k = 0$）：
                    - $P \gets P \cup \{[q, A, p] \rightarrow a\}$

    5. **return** $G = (N, T, P, S)$

## 上下文无关语言的泵浦引理

设 $L$ 是上下文无关语言，存在常数 $p$（泵浦长度），如果 $\omega \in L$ 且 $|\omega| \ge p$，则 $\omega$ 可以写为：

$$
\omega = \omega_1 \omega_2 \omega_0 \omega_3 \omega_4
$$

并满足以下条件：

1. $\omega_2 \omega_3 \ne \varepsilon$（即至少有一个非空）
2. $|\omega_2 \omega_0 \omega_3| \le p$（泵浦部分长度不超过 $p$）
3. 对于所有 $i \ge 0$，有 $\omega_1 \omega_2^i \omega_0 \omega_3^i \omega_4 \in L$

!!! info "简单来说：存在两个靠得很近的子串，它们可以重复任意多次，但二者重复次数相同，所得的新串仍是 CFL。与正则语言的泵浦引理不同，CFL 的泵浦要求 $\omega_2$ 和 $\omega_3$ 的重复次数相同（因为它们对应推导树中同一非终结符的两条路径）。"

### 证明策略

使用泵浦引理证明某语言不是 CFL 的策略与正则语言类似：

1. 假设 $L$ 是 CFL，则存在泵浦长度 $p$
2. 选择一个足够长的字符串 $\omega \in L$, $|\omega| \ge p$
3. 对 $\omega$ 的所有可能分解 $\omega = \omega_1 \omega_2 \omega_0 \omega_3 \omega_4$，找到某个 $i$ 使得 $\omega_1 \omega_2^i \omega_0 \omega_3^i \omega_4 \notin L$
4. 结论：$L$ 不是 CFL

## CFL 的封闭性

### 并运算封闭

对于上下文无关语言 $L(G_1)$ 和 $L(G_2)$ 分别由文法 $G_1 = (N_1, T_1, P_1, S_1)$ 和 $G_2 = (N_2, T_2, P_2, S_2)$（$N_1 \cap N_2 = \phi$）产生，$L(G) = L(G_1) \cup L(G_2)$ 也是 CFL。

构造 $G = (N, T, P, S)$，其中：

- $N = N_1 \cup N_2 \cup \{S\}$
- $T = T_1 \cup T_2$
- $P = P_1 \cup P_2 \cup \{S \rightarrow S_1 \mid S_2\}$
- $S = S$

### 连接运算封闭

对于上下文无关语言 $L(G_1)$ 和 $L(G_2)$ 分别由文法 $G_1 = (N_1, T_1, P_1, S_1)$ 和 $G_2 = (N_2, T_2, P_2, S_2)$（$N_1 \cap N_2 = \phi$）产生，$L(G) = L(G_1) \cdot L(G_2)$ 也是 CFL。

构造 $G = (N, T, P, S)$，其中：

- $N = N_1 \cup N_2 \cup \{S\}$
- $T = T_1 \cup T_2$
- $P = P_1 \cup P_2 \cup \{S \rightarrow S_1 S_2\}$
- $S = S$

!!! info "与并运算构造的区别只有新加入的产生式：并运算用 $S \rightarrow S_1 \mid S_2$，连接运算用 $S \rightarrow S_1 S_2$。"

### 闭包运算封闭

CFL 对 Kleene 闭包（$L^*$）也是封闭的。构造方法：添加新起始符号 $S$ 和产生式 $S \rightarrow S_0 S \mid \varepsilon$。

### 交集不封闭

!!! warning "CFL 对交运算不封闭"

    反例：设 $L_1 = \{a^n b^n c^m \mid n, m \ge 0\}$ 和 $L_2 = \{a^m b^n c^n \mid n, m \ge 0\}$，两者都是 CFL。

    但 $L_1 \cap L_2 = \{a^n b^n c^n \mid n \ge 0\}$，这不是 CFL（可用泵浦引理证明）。

### 补集不封闭

!!! warning "CFL 对补运算不封闭"

    如果 CFL 对补运算封闭，那么由于 $L_1 \cap L_2 = \overline{\overline{L_1} \cup \overline{L_2}}$，而 CFL 对并运算封闭，这将推导出 CFL 对交运算也封闭，与前述结论矛盾。因此 CFL 对补运算不封闭。
