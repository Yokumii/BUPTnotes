# 群论

## 二元运算

二元运算
: 对两个对象进行操作的运算。在离散数学中，一般只研究离散结构（如集合）上的二元运算。

集合上的二元运算
: 处处定义的函数 $f: A \times A \rightarrow A$，同时需要满足封闭性和运算结果唯一，即双射性质。

### 运算的性质

封闭性 (Closure)
: 设集合 $S$ 有二元运算 $*$，若对 $S$ 中的任意两个元素 $a_1$、$a_2$，都有 $a_1 * a_2 \in S$，则称运算 $*$ 对集合 $S$ 封闭。

交换律 (Commutative)
: 设有代数 $(S, *)$，若对任意 $a_1, a_2 \in S$，都符合等式 $a_1 * a_2 = a_2 * a_1$，则称代数 $(S, *)$ 运算符合交换律。交换律也称 Abel 律。

???+ info "交换律的推广"
    如果 $(S, *)$ 运算符合交换律，那么对于运算序列 $a_1 * a_2 * \cdots * a_n$，设 $\theta(1, 2, \ldots, n)$ 为任意重排列，那么有：

    $$a_{\theta(1)} * a_{\theta(2)} * \cdots * a_{\theta(n)} = a_1 * a_2 * \cdots * a_n$$

结合律 (Associative)
: 若 $*$ 是二元运算，且满足 $(x * y) * z = x * (y * z)$，则称 $*$ 具有结合律。在运算过程中不需要再考虑括号。

分配律 (Distributive)
: 一个运算对另一个运算的分配性质。

幂等律 (Idempotent)
: 若 $a * a = a$，则称运算满足幂等律。

!!! note "关于运算性质的注意事项"
    An operation has a property means the statement of the property is true when the operation is used with **any** objects in the structure.

### 运算表

运算表
: 若 $A$ 是有限集，可以通过运算表来定义 $A$ 上的二元运算。

### 特殊元素

单位元 / 幺元 (Identity)
: 若 $e * x = x * e = x$，则称 $e$ 为单位元（中性元）。

零元 (Zero)
: 若 $\theta * x = x * \theta = \theta$，则称 $\theta$ 为零元。

逆元 (Inverse)
: 若 $x * y = y * x = e$，则称 $x$ 与 $y$ 互为逆元。

!!! warning "特殊元素的唯一性"
    1. 单位元及零元具有唯一性
    2. 若 $|A| > 1$，则 $\theta \neq e$
    3. 可结合的运算下，逆元具有唯一性

???+ details "单位元唯一性的证明"
    假设 $e, e'$ 都是单位元，由单位元性质可得：

    $$e = e * e' = e'$$

???+ details "逆元唯一性的证明"
    设 $(S, *)$ 是幺半群，$x \in S$ 可逆，若 $\exists y_1, y_2$ 为 $x$ 的逆元，则：

    $$y_1 = y_1 * e = y_1 * (x * y_2) = (y_1 * x) * y_2 = e * y_2 = y_2$$

## 半群与幺半群

### 半群

半群 (Semigroup)
: 非空集合 $S$ 与满足结合律的二元运算 $*$ 构成的代数结构 $(S, *)$。结合律自然满足封闭性。

    若运算还可交换，则称为 Abel 半群（交换半群）。

### 自由半群

自由半群
: 设 $A$ 为字母集，$A^*$ 为 $A$ 上所有有限字符串的集合（含空串），操作符 $\cdot$ 指连接运算。显然其具有结合律。称 $(A^*, \cdot)$ 为由 $A$ 生成的自由半群。

### 幺半群

幺半群 (Monoid)
: 半群 $(S, *)$ 中存在单位元 $e$，则称为独异点（幺半群）。

!!! tip "幺半群的判定步骤"
    证明 $(S, *)$ 是幺半群：

    1. 是否有封闭性？
    2. 结合律？
    3. 是否存在单位元？

### 广义结合律

!!! abstract "定理：半群的广义结合律（卡特兰律）"
    如果 $a_1, a_2, \ldots, a_n$ 是半群的任意元素（其中 $n \geq 3$），那么在任意元素的乘积中插入有意义的括号形成的乘积是相等的。即任意加括号都成立。

???+ details "引理与证明"
    **引理 1：** $(x_1 \cdots x_n) * (y_1 \cdots y_n) = x_1 \cdots x_n y_1 \cdots y_n$ 成立。

    **证明（数学归纳法）：**

    取定 $n \in \mathbb{N}$，对 $m$ 做数学归纳：

    1. 若 $m = 1$：

        $$(x_1 \cdots x_n) y_1 = x_1 \cdots x_n y_1$$

    2. 由 $m \rightarrow m + 1$：

        $$\begin{aligned}
        (x_1 \cdots x_n) * (y_1 \cdots y_{m+1})
        &= (x_1 \cdots x_n) * ((y_1 \cdots y_m) * y_{m+1}) \\
        &= ((x_1 \cdots x_n) * (y_1 \cdots y_m)) * y_{m+1} \\
        &= (x_1 \cdots x_n y_1 \cdots y_m) * y_{m+1} \\
        &= x_1 \cdots x_n y_1 \cdots y_{m+1}
        \end{aligned}$$

    正是广义结合律才保证了幂的定义的合理性。

### 幂

幂 (Powers)
: 定义 $x^n = x^{n-1} * x = x * x * \cdots * x$，并规定 $x^0 = e$。

???+ info "关于 $x^0 = e$ 的规定"
    不做规定时，$x^m * x^n = x^{m+n}, \forall m, n \geq 1$ 是显然的。若希望更完备：

    $$x^m * x^0 = x^m$$

    若此成立，则 $x^0$ 必等于单位元。有了这个规定自然得到了 $x^m * x^n = x^{m+n}$ 对所有 $m, n \geq 0$ 成立。

### 子半群与子幺半群

子半群 (Subsemigroup)
: $(S, *)$ 的子集 $T$，且运算封闭（一定满足结合性）。

子幺半群 (Submonoid)
: $(S, *)$ 的子集 $T$，运算封闭，且幺元 $e \in T$。

!!! warning "注意"
    $T$ 的幺元必须和 $S$ 的幺元相同。

    显然，半群 $(S, *)$ 本身也是 $S$ 的子半群；独异点 $(S, *)$ 本身也是 $S$ 的子独异点；$T = \{e\}$ 一定是群 $(S, *)$ 的子独异点。

### 生成子幺半群

生成子幺半群
: 设 $(S, *)$ 是幺半群，$A \subset S$，则 $A$ 生成的子幺半群记作 $\langle A \rangle = \cap T$，其中 $T \supset A$, $T < S$。即 $\langle A \rangle$ 是所有 $S$ 中包含了 $A$ 的子幺半群的交集。子半群和子幺半群均可按此方式生成。

### 同态

同态 (Homomorphism)
: 保持运算和特殊元素的映射。若 $S$ 和 $T$ 满足幺半群同态关系：

    $$f: (S, \cdot) \rightarrow (T, *) \iff \begin{cases} \text{保持乘法，即 } \forall x, y \in S,\ f(x \cdot y) = f(x) * f(y) \\ \text{保持单位元，即 } f(e) = e' \end{cases}$$

    直观理解：两个元素作运算能映射到另一个集合，另一个集合中的元素作运算也能映射回原集合。

### 同构

同构 (Isomorphism)
: 双射的同态。若 $S$ 和 $T$ 满足幺半群同构关系：

    $$f: (S, \cdot) \rightarrow (T, *) \iff \begin{cases} \text{满足双射，即 } \forall x, y \in S,\ x \leftrightarrow f(x),\ y \leftrightarrow f(y),\ x \cdot y \leftrightarrow f(x) * f(y) \\ \text{保持乘法，即 } \forall x, y \in S,\ f(x * y) = f(x) \cdot f(y) \\ \text{保持单位元，即 } f(e) = e' \end{cases}$$

!!! note "同构的性质"
    1. 恒等映射：$S$ 是自己的同构
    2. 若 $f$ 是从 $S \rightarrow T$ 的同构（一一对应），则 $f^{-1}$ 必定存在，且 $f^{-1}$ 是从 $T \rightarrow S$ 的一一对应函数，且一定是同构
    3. 若 $(S, *)$ 有独异点但 $(T, *)$ 没有独异点，则必定不存在从 $S \rightarrow T$ 的同构（常用于证明不存在同构）
    4. 同态和同构均满足像点的乘积等于乘积的像点，区别是同构需要一一对应

### 满同态

!!! abstract "定理 1"
    若 $S$ 和 $T$ 是幺半群，幺元分别为 $e, e'$，$f: S \rightarrow T$ 为满同态映射，则 $f(e) = e'$。

???+ details "证明"
    由同态定义，$\forall a \in S$：

    $$f(e \cdot a) = f(a) * f(e) = f(a)$$

    但首先需要保证 $f(a) \in T$，即满射，才能成立，此时 $f(e) = e'$。

!!! abstract "定理 2"
    若 $S$ 和 $T$ 是幺半群，$S$ 为可交换半群，$f: S \rightarrow T$ 为满同态映射，则 $T$ 也是可交换半群。

???+ tip "构造同构 / 证明是否为同构的步骤"
    1. 构造或直接给出函数 $f: S \rightarrow T$，使得 $f$ 的定义域 $\mathrm{Dom}(f) = S$
    2. 证明 $f$ 是单射 (one-to-one) 的，可用反证法
    3. 证明 $f$ 是满射 (onto) 的 $\Rightarrow$ 故而是双射的
    4. 证明 $f(a \cdot b) = f(a) * f(b)$

    同态无需证明步骤 2、3。

## 商半群

### 积半群

!!! abstract "定理"
    1. 两个半群的笛卡尔积也是半群
    2. 两个幺半群的笛卡尔积也是幺半群，且其幺元为 $(e_S, e_T)$

### 同余关系

同余关系 (Congruence relation)
: 在半群 $(S, *)$ 上的等价关系 $R$，如果满足：任意 $a\,R\,a'$ 并且 $b\,R\,b'$，则 $(a * b)\,R\,(a' * b')$，则称 $R$ 为半群上的同余关系。

!!! warning "注意"
    等价关系不一定是同余关系。等价关系满足自反性、对称性、传递性，但同余关系还额外要求与运算兼容。

???+ tip "证明 $R$ 是半群上的同余关系的步骤"
    1. 等价关系显然（已知给出）
    2. 根据 $a\,R\,a'$ 和 $b\,R\,b'$ 可以推出 $(a * b)\,R\,(a' * b')$

### 商半群

商半群 (Quotient semigroup)
: 按以下步骤定义等价类上的二元运算：

    1. $S = \{a, b, c, \ldots, a', b', c', \ldots\}$
    2. 设等价类 $[a] = \{a, a', \ldots\},\ [b] = \{b, b', \ldots\},\ [c] = \{c, \ldots\},\ \ldots$
    3. $S/R = \{[a], [b], [c], \ldots\}$
    4. 定义运算 $[a] \otimes [b] = [a * b]$

!!! note "商半群的运算"
    $\otimes$ 是等价类之间的运算，可以用代入等价类中的元素进行计算，即 $[a] \otimes [b] = [a * b]$。

???+ details "幺半群导出的商半群也是幺半群"
    **证明：**

    $$[a] \otimes [e] = [a * e] = [a] = [e * a] = [e] \otimes [a]$$

### 自然同态

自然同态 (Natural homomorphism)
: 定义 $f_R: S \rightarrow S/R$，由 $f_R(a) = [a]$ 给出，显然是满射 (onto)。

### 同态基本定理

!!! abstract "同态基本定理 (Fundamental Homomorphism Theorem)"
    设 $f: S \rightarrow T$ 是同态，$R$ 是 $S$ 上的关系且被定义为 $a\,R\,b \iff f(a) = f(b)$，那么有：

    1. $R$ 是同余关系
    2. $T$ 和 $S/R$ 同构

## 群

### 逆元

逆元 (Inverse)
: 令 $(S, *)$ 是一个幺半群，$x \in S$。当 $\exists y \in S,\ x * y = y * x = e$，则称 $y$ 为 $x$ 的逆元，记为 $x^{-1}$。

    单位元一定是可逆的。逆元是唯一的。

### 群的定义

群 (Group)
: 定义 1：若 $(S, *)$ 是一个幺半群，且每一个元素均可逆，则 $(S, *)$ 构成一个群。

    定义 2（拓展半群的定义）：

    1. **封闭性 (Closure)** — 运算封闭性
    2. **结合律 (Associativity)** — 结合律
    3. **单位元 (Identity)** — 存在单位元
    4. **逆元 (Inverse)** — 每个元素都有逆元

!!! abstract "引理"
    $(S, *)$ 是幺半群，令 $G$ 是其所有可逆元素构成的子集，则 $(G, *)$ 是群。

### 群的性质

!!! note "群的基本性质"
    1. $(a^{-1})^{-1} = a$
    2. $(ab)^{-1} = b^{-1}a^{-1}$
    3. $ab = ac \Rightarrow b = c$（左消去律）
    4. $ba = ca \Rightarrow b = c$（右消去律）

???+ details "群定义可以减弱为 $ea = a$"
    事实上，群的定义可以减弱为 $ea = a$（左单位元）。

    **证明：** $ae = aa^{-1}(a^{-1})^{-1} = e(a^{-1})^{-1} = ea = a$

### 几类特殊的群

阿贝尔群 / 交换群 (Abelian group)
: $(G, *)$，$\forall x, y \in G$，$x * y = y * x$。

平凡群
: $(\{e\}, *)$。

$n$ 阶一般线性群 $GL_n(\mathbb{R})$
: $n \times n$ 阶可逆实矩阵构成的乘法群：

    $$GL_n(\mathbb{R}) = \{A \in M_n(\mathbb{R}) : \det(A) \neq 0\}$$

### 子群

子群 (Subgroup)
: $H$ 是 $G$ 的子群，记作 $H < G$，满足：

    1. $e \in H$
    2. 封闭性
    3. 都有逆元

    也可压缩为：

    1. 非空 $H \subset G$
    2. $\forall x, y \in H,\ xy^{-1} \in H$

!!! tip "子群判定方法"
    上述压缩条件也可作为子群的判定方法。

### 群同态

群同态 (Group homomorphism)
: $(G, *), (G', *')$ 是两个群，$f: G \rightarrow G'$ 是一个群同态，那么有：

    1. $f(e) = e'$
    2. $f(a^{-1}) = (f(a))^{-1}$
    3. $H$ 是 $G$ 的一个子群，则 $f(H) = \{f(h) \mid h \in H\}$ 也是 $G'$ 的一个子群

???+ info "行列式是群同态"
    $\det: GL_n(\mathbb{R}) \rightarrow (\mathbb{R}, *)$ 是一个乘法群同态，即行列式是一般线性群到实数乘群的一个群同态。

    对 $SL_n(\mathbb{R}) = \{A \in GL_n(\mathbb{R}) : \det(A) = 1\}$，显然 1 是 $(\mathbb{R}, *)$ 的单位元，那么：

    $$SL_n(\mathbb{R}) = \det^{-1}(1) = \det^{-1}(\{1\})$$

    即特殊线性群是那些映射到单位元元素的矩阵的集合，它是实数乘群中单位元的一个原象，也是正规子群。

满同态
: 满射的群同态。

单同态
: 单射的群同态。

!!! note "单同态的判定"
    单同态当且仅当 $\mathrm{Ker}(f) = \{e\}$。要证明群同态是单射，只需证 $\mathrm{Ker}(f) = \{e\}$。

### 核与像

核 (Kernel)
: $f: G \rightarrow G'$ 是群同态，$\mathrm{Ker}(f) = \{a \in G \mid f(a) = e'\}$。

像 (Image)
: $f: G \rightarrow G'$ 是群同态，$\mathrm{Im}(f) = f(G) = \{y \in G' : \exists x \in G,\ y = f(x)\}$。

### 同态基本定理（群）

!!! abstract "群的同态基本定理"
    设 $f: G \rightarrow G'$ 是同态，$R$ 是 $G$ 上的关系且被定义为 $a\,R\,b \iff f(a) = f(b)$，那么有：

    1. $R$ 是同余关系
    2. $G'$ 和 $G/R$ 同构

### 同构

同构 (Isomorphism)
: 双射的同态。

### 群的直积

群的直积 (Direct product)
: $(x, y) * (x', y') = (x \circ_1 x', y \circ_2 y')$。

### 有限群

有限群 (Finite group)
: $G$ 是有限群 $\iff$ $G$ 是一个有限集合。

群的阶 (Order of group)
: 若 $x \in G$，如果存在最小正整数 $n \in \mathbb{N}$ 使得 $x^n = e$，则 $|x| = n$；若不存在，则 $|x| = \infty$。

!!! note "命题"
    有限群的每一个元素经过有限次自乘都可以得到单位元。

### 循环群

循环群 (Cyclic group)
: 令 $G = \langle x \rangle$ 是有限循环群，假设 $|x| = n$，则 $G = \{e, x, x^2, \ldots, x^{n-1}\}$，其中元素两两不同，则称有限群 $G$ 的阶为 $n$。可以用 Cayley 图进行可视化表示。

!!! note "循环群的性质"
    1. 任意 $n$ 阶循环群互相同构，无限循环群也是互相同构的
    2. 任意循环群都是交换群
    3. 令 $G = \langle x \rangle$ 为无限循环群，$G$ 只有两个生成元分别为 $x, x^{-1}$

???+ info "几类特殊的循环群"
    $(\mathbb{Z}, +) = \langle 1 \rangle$，1 或 $-1$ 是它的生成元，为无限循环群。

### Lagrange 定理

!!! abstract "Lagrange 定理"
    若 $H$ 是 $G$ 的子群，则 $|H|$ 整除 $|G|$。

### 陪集

左陪集
: $H$ 是 $G$ 的一个子群，$aH = \{ah \mid h \in H\}$，$a \in G$。陪集一般不是子群。

    定义 $f: H \rightarrow aH,\ f(x) = ax$，显然是双射，则 $|H| = |aH|$。

!!! note "命题"
    两个左陪集要么相等要么无交，所有陪集构成群的一个分拆。可以定义为商集 $G/H$。

右陪集
: $Ha = \{ha \mid h \in H\}$，$a \in G$。

???+ info "如何赋予商集一个群的结构？"
    这正是正规子群和商群所解决的问题。

### 正规子群

正规子群 (Normal subgroup)
: $N < G$，$\forall a \in G,\ aN = Na$，记作 $N \lhd G$。

### 商群

商群 (Quotient group)
: 通过正规子群来生成商集，并定义二元运算为：

    $$aN \times bN = [a] \circ [b] = [a * b] = abN$$

    其单位元为 $eN = N$，逆元为 $a^{-1}N$。

    同时有函数 $f_R: G \rightarrow G/R$，$f_R(a) = aN$，则 $f_R$ 是由 $G \rightarrow G/R$ 的同态，一般记为 $G/N$。

!!! abstract "定理"
    设 $G$ 的正规子群 $N$，设定义在 $G$ 上的关系 $R: a\,R\,b \iff ab^{-1} \in N$，那么有：

    1. $R$ 是 $G$ 上的同余关系
    2. $N = [e]$

???+ details "证明"
    **自反性：** $aa^{-1} = e \in N \Rightarrow a\,R\,a$

    **对称性：** 若 $a\,R\,b$，则 $ab^{-1} \in N$，由于其存在逆元，则 $(ab^{-1})^{-1} = ba^{-1} \in N \Rightarrow b\,R\,a$

    **传递性：** 若 $a\,R\,b,\ b\,R\,c$，则 $ab^{-1}, bc^{-1} \in N$，由封闭性，$ab^{-1}bc^{-1} = ac^{-1} \in N \Rightarrow a\,R\,c$

    **同余关系：** 由运算封闭性与 $N$ 的正规性可证。
