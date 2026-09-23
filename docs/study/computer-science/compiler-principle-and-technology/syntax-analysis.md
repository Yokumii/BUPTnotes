# 语法分析

## 语法分析简介

!!! abstract ""

    语法分析程序的地位：

    <figure markdown="span">
      ![语法分析程序的地位](https://webp-pic.yokumi.cn/2025/09/20250923102353002.png){ loading=lazy width="70%" }
    </figure>

    词法分析程序接受字符流（即源程序），输出记号流，作为语法分析程序的输入（按照**自左向右**的顺序扫描输入的记号序列），语法分析程序会根据语法规则，判断输入的记号流是否合法，并输出分析树。

    分析方法包括：**自顶向下**和**自底向上**。

语法错误如何处理？

* 错误处理目标：发现错误位置/性质，迅速恢复，不影响对正确程序的处理效率
* 错误恢复策略：紧急恢复、短语级恢复、出错产生式、全局纠正

## 自顶向下分析方法

### 递归下降分析

核心思想是：

- 对每一个非终结符构造一个分析函数
- 用前看符号指导产生式规则的选择

由于上下文无关文法（CFG）中所有的产生式左边只有一个非终结符，所以我们在调用产生式规则的函数后，就分为两种情况：

1. 遇到终结符，则直接把这个终结符和句子中对应位置的 token 进行比较，判断是否符合即可；符合就继续，不符合就返回（回溯）
2. 遇到非终结符，则调用这个非终结符对应的函数（可能会递归的调用，所以叫递归下降文法）

!!! warning "递归下降分析的问题"

    1. 如果语法存在左递归（形如 $A\Rightarrow^+ A\beta,A\in N$ 的推导），则会导致递归调用无限进行下去，使得分析过程陷入死循环
    2. 通过回溯不断试探，效率低

### 递归调用预测分析

从递归下降分析方法的问题来看，优化的点就在于解决回溯，实现一种确定的、不带回溯的方法。

如何克服回溯？**能够根据所面临的输入符号准确地指派一个候选式去执行任务**。因此通常需要对文法进行改造：

* 消除文法的二义性
* 消除左递归
* 提取左公共因子
* 非终结符号 $A$ 的所有候选式的开头终结符号集两两互不相交，即 $FIRST(\alpha_i)\cup FIRST(\alpha_j)=\emptyset (i\ne j)$

!!! info ""

    $FIRST(\alpha_i)$: 由 $\alpha_i$ 开始推导，可以推导出的所有**开头终结符号**的集合。

???+ info "FIRST 集合的求解方法"

    对于产生式 $A\rightarrow \beta_1\beta_2\cdots\beta_n$，根据开头的 $\beta_1$ 分情况讨论：

    1. $\beta_1$ 是终结符，则 $\beta_1\in FIRST(A)$
    2. $\beta_1$ 是非终结符，则 $FIRST(\beta_1)\subseteq FIRST(A)$

    针对 $\varepsilon$ 产生式的 FIRST 集合，还需要处理：

    * 如果 $A\rightarrow\varepsilon$ 也是产生式，则 $\varepsilon\in FIRST(A)$
    * 如果 $A\rightarrow\beta_1\cdots\beta_{i-1}\beta_i\cdots\beta_n$，其中 $FIRST(\beta_1)$ 到 $FIRST(\beta_{i-1})$ 均含有 $\varepsilon$，则将 $FIRST(\beta_i)\subseteq FIRST(A)$
    * 同理如果 $FIRST(\beta_1)$ 到 $FIRST(\beta_n)$ 均含有 $\varepsilon$，则 $\varepsilon\in FIRST(A)$

    这里的额外处理事实上有一个专门的术语：**NULLABLE 集合**，即所有可直接或间接推导出空串的集合。

    上述对 $\varepsilon$ 产生式的处理可以简化为：如果 $A\rightarrow XY$ 且 $X\in NULLABLE$，则 $FIRST(A)=FIRST(X)\cup FIRST(Y)$

#### 预测分析程序的转换图构造方法

**1. 消除左递归**

> 这里主要以消除直接左递归为主，实际题目中很少出现间接左递归。

消除直接左递归：假如有 $A_i\rightarrow A_i\alpha\mid \beta$，则引入一个新的非终结符 $A^\prime_i$，并添加产生式：

$$
\begin{aligned}
A_i&\rightarrow \beta A^\prime_i\\
A^\prime_i&\rightarrow \alpha A^\prime_i\mid\varepsilon
\end{aligned}
$$

消除间接左递归：在消除 $A_i$ 后面的 $A_j$ 的直接左递归之前，发现有 $A_j\rightarrow A_i\gamma$，则用所有已经在新文法产生式中的 $A_i\rightarrow \delta$ 替换 $A_i$，即将产生式 $A_j\rightarrow A_i\gamma$ 替换为：

$$
A_j\rightarrow \delta\gamma
$$

直至 $\delta$ 最前面为终结符或大于等于 $A_j$ 的非终结符。

**2. 提取左公因子**

如果有产生式形如：$A\rightarrow\alpha\beta_1\mid\alpha\beta_2$，则提取左公因子 $\alpha$，将产生式替换为：

$$
\begin{aligned}
A&\rightarrow\alpha A^\prime\\
A^\prime&\rightarrow\beta_1\mid\beta_2
\end{aligned}
$$

**3. 绘制转换图**

对于每一个非终结符号 $A$，创建一个初态和终态，对于每个产生式 $A\rightarrow X_1X_2\cdots X_n$ 构造一条从初态到终态的路径，有向边依次为 $X_i$。

**4. 化简状态转换图**

反复代入化简。

<figure markdown="span">
  ![状态转换图化简](https://webp-pic.yokumi.cn/2025/10/20251019142131825.png){ loading=lazy width="70%" }
</figure>

**5. 预测分析程序的实现**

<figure markdown="span">
  ![预测分析程序转换图](https://webp-pic.yokumi.cn/2025/10/20251019142325813.png){ loading=lazy width="70%" }
</figure>

```c title="c"
void procE(void) {
    procT();
    if (char == '+') {
        forward pointer;
        procE();
    }
}
```

简单来说：

* 对于 $\varepsilon$ 的有向边一般不做任何处理
* 遇到终结符则移动记号流的指针指向后一个待读入的字符
* 遇到非终结符则调用它的对应函数

### 非递归预测分析 / LL(1) 分析算法

#### 分析过程

上面的方法中，虽然不存在回溯和死循环，但函数的调用还是存在嵌套的，所以引入非递归预测分析方法，它通过**分析表**和**分析栈**联合控制，消除递归。

<figure markdown="span">
  ![预测分析程序模型](https://webp-pic.yokumi.cn/2025/10/20251019143133757.png){ loading=lazy width="70%" }
</figure>

按照个人理解，分析表是用来解决回溯的，而符号栈则是用来解决函数的递归调用的。

**输入**：符号串 $\omega$（词法分析输出的记号流）；文法的预测分析表 $M$。

**初始化**：

1. 将符号串 $\omega$ 放入输入缓冲区，注意后面要添加一个 `$`
2. 将 `$` 放入符号栈，再将文法的起始符号 $S$ 入栈，此时栈顶元素 $X=S$
3. pointer 指向输入缓冲区的第一个符号，代表当前输入符号 $a$

**执行分析**：根据符号栈栈顶元素 $X$ 和输入符号 $a$ 执行如下循环过程：

1. 若 $X=a=$ `$`，则分析成功，停止
2. 若 $X=a\ne$ `$`，说明当前栈顶的终结符命中输入，匹配成功，将 $X$ 弹出，同时 pointer 前移
3. 若 $X\in V_T,X\ne a$，说明发现错误
4. 若 $X\in V_N$，则访问分析表 $M[X,a]$：
    1. 若 $M[X,a]=X\rightarrow Y_1Y_2\cdots Y_n$，则将 $X$ 弹栈，然后按照 $Y_n,\cdots,Y_2,Y_1$ 的顺序压入栈
    2. 若 $M[X,a]=X\rightarrow \varepsilon$，则将 $X$ 弹栈
    3. 若 $M[X,a]=X\rightarrow error$，即分析表中没有任何内容，出错

**输出**：每次命中分析表对应的产生式时，输出产生式，最终结果为依次调用的产生式序列，相当于一个最左推导的过程。

#### 预测分析表的构造

**1. 改写文法**：消除左递归 + 消除左公因子

**2. 构造 FIRST 集合**

**3. 构造 FOLLOW 集合**

???+ info "FOLLOW 集合"

    **FOLLOW 集合的定义**：假定 $S$ 是文法 $G$ 的开始符号，对于 $G$ 的任何非终结符号 $A$，集合 $FOLLOW(A)$ 是在所有句型中，紧跟 $A$ 之后出现的终结符号或 `$` 组成的集合。

    $$FOLLOW(A)=\{a\mid S\Rightarrow^* \cdots Aa\cdots,a\in V_T\}$$

    特别地，若有 $S\Rightarrow^*\cdots A$，则规定 `$` $\in FOLLOW(A)$。

    **FOLLOW 集合的构造方法**：

    1. 对于起始符号 $S$，`$` $\in FOLLOW(S)$
    2. 若有 $A\rightarrow\alpha B\beta$，则 $FIRST(\beta)\subseteq FOLLOW(B)$，注意除去 $\varepsilon$
    3. 若有 $A\rightarrow\alpha B$ 或 $A\rightarrow\alpha B\beta,\beta\Rightarrow^*\varepsilon$，则 $FOLLOW(A)\subseteq FOLLOW(B)$

    **FOLLOW 集合的意义**？确定某个非终结符可能出现在产生式右侧的上下文环境。举个例子，当栈顶为 $X$，读入的符号为 $a$，但 $a$ 不在任何 FIRST 集合中，如果有 $X \rightarrow\varepsilon$，那么 $a$ 必须是 $X$ 的后继字符才能保证最终句子是一个符合语法的句子，即此时调用 FOLLOW 集合。

**4. 预测分析表的构造**：对于每条产生式 $A\rightarrow \alpha$：

* 对所有终结符 $a\in FIRST(\alpha)$，$\{A\rightarrow\alpha\}\subseteq M[A,a]$
* 对 $\varepsilon\in FIRST(\alpha)$，则对所有 $b\in FOLLOW(A)$，$\{A\rightarrow\alpha\}\subseteq M[A,b]$

最终留空处均为 error。

#### LL(1) 文法

可以用上述方法解析的文法称之为 LL(1) 文法，即**从左 (L) 向右读入一个程序，最左 (L) 推导，采用一个 (1) 前看符号**。要求对应的预测分析表不含**多重表项**，也就是要求：对所有产生式 $A\rightarrow u_1\mid u_2\mid \cdots\mid u_n$，有：

$$
\begin{aligned}
&FIRST(u_1)\cap \cdots \cap FIRST(u_n)=\emptyset,\text{即 FIRST 集合互不相交}\\
u_i\Rightarrow^*\varepsilon,&FIRST(u_i)\cap FOLLOW(A)=\emptyset,i=1,2,\cdots,n,\text{即 FOLLOW(A) 与所有 FIRST 集合互不相交}
\end{aligned}
$$

## 自底向上分析方法

LL(1) 分析法的优点是不需要回溯，构造方法较简单，且分析速度非常快。缺点是对语法的限制太强，能满足此要求的语法相当少。因此，引入现在被广泛使用的自底向上分析方法。

* 对输入串的扫描：自左向右
* 分析树的构造：自底向上
* 分析过程：从输入符号串开始分析 $\rightarrow$ 查找当前句型的"可归约串" $\rightarrow$ 使用规则归约成相应的非终结符号 $\rightarrow$ 重复

### 移进-归约分析

#### 分析过程

1. 把输入符号逐个地移进符号栈中（即"移进"）
2. 当栈顶的符号串形成某个产生式的一个候选式（右部）时，把该符号串替换（归约）为该产生式的左部符号（即"归约"）
3. 重复步骤 2 直到栈顶符号串不再是"可归约串"为止
4. 重复步骤 1 ～ 3 直到归约出文法起始符号 $S$
5. 接收：宣布分析成功，停止分析
6. 错误处理：调用错误处理程序进行诊断和恢复

简单来说，"移进"相当于"往栈里装符号，等待形成句法单位"，"归约"相当于"识别出一个语法成分，用它的非终结符替代"。

#### 规范归约

假定 $\alpha$ 为文法 $G$ 的一个句子，若右句型序列 $\alpha_n,\alpha_{n-1},\cdots,\alpha_1,\alpha_0$ 满足：

1. $\alpha_n=\alpha$，$\alpha_0=S$
2. $\forall 0<i\le n$，$\alpha_{i-1}$ 是经过把 $\alpha_i$ 的**句柄**替换为相应产生式的左部符号而得到的

规范归约相当于最右推导的逆过程，每次只归约当前句型中的**句柄（handle）**，也就是**恰好能还原出上一步最右推导的右部**的那一部分。

### LR 分析方法

LR 分析是移进-归约分析的一种规范化、自动化的实现方法。即**从左 (L) 向右扫描输入符号串，为输入符号串构造一个最右 (R) 推导的逆过程，采用 k 个前看符号**。

LR 分析法的基本思想是在归约的过程中，一方面记住移入和归约的整个符号串（历史信息），另一方面通过产生式推测未来可能碰到的输入符号（预测信息）。

#### LR 分析程序的模型及工作过程

<figure markdown="span">
  ![LR分析程序模型](https://webp-pic.yokumi.cn/2025/10/20251019193813073.png){ loading=lazy width="70%" }
</figure>

栈包括：（两者同步变化）

* 状态栈 S
* 符号栈 X

分析表包括：

* **动作表 action**：用于指导分析器在**遇到不同输入符号时**应采取的动作
    * $action[S_m,a_i]$：$S_m$ 遇到输入符号 $a_i$ 时的动作
    * **shift** $S$（移进）：将当前输入符号 $a_i$ 和状态 $S=goto[S_m,a_i]$ 压入栈
    * **reduce** by $A\rightarrow\beta$（归约）：若 $\left|\beta\right|=r$，则从栈中弹出 $r$ 项，栈顶变为 $S_{m-r}$，然后把 $A$ 和状态 $S=goto[S_{m-r},A]$ 压入栈
    * **accept**：宣布分析成功，停止分析
    * **error**：调用出错处理程序
* **状态转移表 goto**：用于指导分析器**在采取归约动作后**应转移到的新状态
    * $goto[S_m,X]$：$S_m$ 经过 $X$ 的后继状态

!!! info "活前缀"

    一个规范句型的一个前缀，如果不含句柄之后的任何符号，则称它为该句型的一个活前缀。

#### LR(0) 算法

!!! info "形态 / LR(0) 项目"

    一个产生式的解析程度，用一个产生式加一个位置黑点 $\cdot$ 来表示，黑点左边表示已解析的部分，右部表示待解析的部分。

产生式 $A\rightarrow XYZ$ 有 4 种 LR(0) 项目：

* $A\rightarrow\cdot XYZ$：起始形态
* $A\rightarrow X\cdot YZ$
* $A\rightarrow XY\cdot Z$
* $A\rightarrow XYZ\cdot$：已完成形态/归约项目
* 文法起始符号 $S$ 的归约项目又称之为**接收项目**

根据圆点 $\cdot$ 后的第一个符号又可以分为：

* **移进项目**：圆点后第一个符号为终结符号的 LR(0) 项目
* **待约项目**：圆点后第一个符号为非终结符号的 LR(0) 项目

??? info "拓广文法"

    通过在原始文法中添加一个新的开始符号 $S^\prime$ 和产生式 $S^\prime\rightarrow S$，使得文法开始符号仅出现在一个产生式的左边，从而使分析器只有一个接受状态。

???+ info "闭包 closure(I) 的构造"

    设 $I$ 是文法 $G$ 的一个 LR(0) 项目集合，则 $closure(I)$ 是从 $I$ 出发构造的项目集合：

    1. $I$ 中的每一个 LR(0) 项目均属于 $closure(I)$
    2. 若 $A\rightarrow\alpha\cdot B\beta\in closure(I)$，且有产生式 $B\rightarrow \eta$，若 $B\rightarrow\cdot\eta\notin closure(I)$，则将 $B\rightarrow\cdot\eta$ 加入
    3. 重复步骤 2 直至 $closure(I)$ 不再增大

    $B\rightarrow\cdot\eta$ 称之为 $A\rightarrow\alpha\cdot B\beta$ 的**延伸形态**。

!!! info "转移函数 go"

    $go[I,X]=closure(J)$，其中 $J=\{A\rightarrow\alpha X\cdot\beta\mid A\rightarrow\alpha\cdot X\beta\in I\}$

##### 构造 LR(0) 项目集规范族

1. 构造文法 $G$ 的拓广文法 $G^\prime$
2. $C=\{closure(\{S^\prime\rightarrow\cdot S\})\}$
3. 对于 $C$ 中的每一个项目集 $I$ 和每一个文法符号 $X$，如果 $go[I,X]$ 不为空且不在 $C$ 中，则将 $go[I,X]$ 加入 $C$
4. 重复步骤 3 直至 $C$ 不再更新

<figure markdown="span">
  ![LR(0)活前缀识别DFA](https://webp-pic.yokumi.cn/2025/10/20251019222419394.png){ loading=lazy width="70%" }
</figure>

这个状态转移图一般称之为**识别文法 $G^\prime$ 所有活前缀的 DFA**。

##### LR(0) 项目集中的冲突

!!! info "可折叠形态"

    某状态/项目集中，只有一个项目，且该项目为归约项目。

1. **移进-归约**冲突：既包含不可折叠形态，又包含可折叠形态
2. **归约-归约**冲突：包含多条可折叠形态

##### 判断某文法是否属于 LR(0) 文法

一个文法是 LR(0) 文法，每个状态/项目集中：

1. 要么所有 LR(0) 项目都是"移进-待约项目"
2. 要么只含有唯一的归约项目
3. 起始符号不出现在任何产生式右部

#### SLR(1) 算法

由于 LR(0) 不向前看下一个符号，大大增加了冲突的可能，因此这种冲突通过向前看若干个输入符号或许能够解决。

!!! info "SLR(1) 的核心思想"

    利用 **FOLLOW 集**来解决冲突。

如果当：

* $FOLLOW(A)\cap FOLLOW(B)=\emptyset$
* 终结符号 $b\notin FOLLOW(A),b\notin FOLLOW(B)$

则冲突消失，决策如下：

1. 当下一个读入符号 $x=b$ 时，移进 $b$
2. 当下一个读入符号 $x\in FOLLOW(A)$ 时，用 $A\rightarrow\alpha$ 归约
3. 当下一个读入符号 $x\in FOLLOW(B)$ 时，用 $B\rightarrow\beta$ 归约

##### SLR(1) 分析表的构造算法

1. 构造 $G^\prime$ 的 LR(0) 项目集规范族 $C=\{I_0,I_1,\cdots,I_n\}$
2. 对于状态 $I_i$ 的分析动作：
    1. 若 $A\rightarrow \alpha\cdot a\beta\in I_i$，且 $go(I_i,a)=I_j$，则 $action[i,a]=S_j$
    2. 若 $A\rightarrow \alpha\cdot\in I_i$，则对 $\forall a\in FOLLOW(A)$，$action[i,a]=R\space A\rightarrow\alpha$
    3. 若 $S^\prime\rightarrow S\cdot\in I_i$，则 $action[i,\$]=accept$
3. 若 $go(I_i,A)=I_j$，$A$ 为非终结符，则 $goto[i,A]=j$
4. 剩余空白项均置为 error

**定理**：***每一个 SLR(1) 文法都是无二义的文法***，但并非无二义的文法都是 SLR(1) 文法。

#### LR(1) 算法

SLR(1) 算法向前查看下一个符号，并利用 FOLLOW 集进行识别，但这样仍然不准确，仍会导致冲突。而 LR(1) 算法更加强大，利用了**展望符（lookahead）**。

!!! info "LR(1) 项目"

    $[A\rightarrow\alpha\cdot\beta,a]$，$a$ 即为展望符，表示在当前处理到 $A\rightarrow\alpha\cdot\beta$ 时，下一个读入的终结符必须是 $a$ 才能进行正确归约。

??? info "延伸形态"

    若一个形态的黑点后是非终结符，形如 $C=[A\rightarrow\alpha\cdot B\beta,a]$，且有 $B\rightarrow\eta,b\in FIRST(\beta a)$，则 $C^\prime=[B\rightarrow\cdot\eta,b]$ 是 $C$ 的延伸形态。

    展望符为 $B$ 之后的符号串 $\beta$ + 原展望符 $a$ 的 FIRST 集合，即 $FIRST(\beta a)$。

???+ info "LR(1) 闭包的构造"

    1. $I$ 中的每一个 LR(1) 项目均属于 $closure(I)$
    2. 若 $[A\rightarrow\alpha\cdot B\beta,a]$，且有产生式 $B\rightarrow \eta$，且 $b\in FIRST(\beta a)$，若 $[B\rightarrow\cdot\eta,b]\notin closure(I)$，则加入
    3. 重复步骤 2 直至 $closure(I)$ 不再增大

##### 构造 LR(1) 项目集规范族

1. 构造文法 $G$ 的拓广文法 $G^\prime$
2. $C=\{closure(\{[S^\prime\rightarrow\cdot S,\$]\})\}$
3. 对于 $C$ 中的每一个项目集 $I$ 和每一个文法符号 $X$，如果 $go[I,X]$ 不为空且不在 $C$ 中，则将 $go[I,X]$ 加入 $C$
4. 重复步骤 3 直至 $C$ 不再更新

##### LR(1) 分析表的构造算法

1. 构造 $G^\prime$ 的 LR(1) 项目集规范族 $C=\{I_0,I_1,\cdots,I_n\}$
2. 对于状态 $I_i$ 的分析动作：
    1. 若 $[A\rightarrow \alpha\cdot a\beta,b]\in I_i$，且 $go(I_i,a)=I_j$，则 $action[i,a]=S_j$
    2. 若 $[A\rightarrow \alpha\cdot,a]\in I_i$，且 $A\ne S^\prime$，则 $action[i,a]=R\space A\rightarrow\alpha$
    3. 若 $[S^\prime\rightarrow S\cdot,\$]\in I_i$，则 $action[i,\$]=accept$
3. 若 $go(I_i,A)=I_j$，$A$ 为非终结符，则 $goto[i,A]=j$
4. 剩余空白项均置为 error

##### LR(1) 文法

要求每个状态中：

1. 不能同时含有 $[A\rightarrow\alpha\cdot a\beta,b]$ 和 $[B\rightarrow\eta\cdot,a]$（否则"移进-归约"冲突）
2. 不能同时含有 $[A\rightarrow\alpha\cdot,a]$ 和 $[B\rightarrow\beta\cdot,a]$（否则"归约-归约"冲突）

#### LALR(1) 算法

LR(1) 构造算法复杂且状态数量多。LALR(1) 算法的基本思想是将 LR(1) 项目集规范族中的所有**同心状态集**合并。

??? info "同心集"

    如果两个 LR(1) 项目集去掉展望符之后是相同的，则称这两个项目集具有相同的心（core），即这两个项目集是同心集。

??? info "项目集的核（kernel）"

    除去初态项目集外，一个项目集的核是由该项目集中那些圆点不在最左边的项目组成。初态项目集的核只有 $[S^\prime\rightarrow\cdot S,\$]$。

##### LALR(1) 项目集中的冲突

合并可能导致"归约-归约"冲突，但**不会引入新的"移进-归约"冲突**。

##### 判断 LALR(1) 文法

1. 先判断是否属于 LR(1) 文法
2. 如果不存在同心集，则是 LALR(1) 文法
3. 如果存在同心集，先合并，再检查是否有"归约-归约"冲突

##### LALR(1) vs. LR(1) vs. SLR(1)

- LALR(1) 形式上与 LR(1) 相同
- 大小上与 SLR(1)/LR(0) 相当
- 分析能力介于 SLR(1) 与 LR(1) 之间

## 文法分类总结

<figure markdown="span">
  ![文法分类](https://webp-pic.yokumi.cn/2025/10/20251021003007262.png){ loading=lazy width="70%" }
</figure>

"二义性文法"表示那些无论如何都无法消除二义性的文法，它们不可能被任何确定性分析方法识别。

左侧的分析方法又可以分为自顶向下和自底向上，其中越外层表示的能处理的文法范围越大，分析能力越强，越内层针对文法的限制越多。
