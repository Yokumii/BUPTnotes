# 关系数据库设计

## 函数依赖

**函数依赖（Functional Dependency, FD）** 是关系数据库设计理论的核心概念。

### 定义

若关系模式 $R$ 上满足函数依赖 $\alpha \rightarrow \beta$，则对 $R$ 的所有合法实例 $r$，其中任意两个元组 $t_1, t_2$：

$$t_1[\alpha] = t_2[\alpha] \implies t_1[\beta] = t_2[\beta]$$

即：$\alpha$ 的值相同则 $\beta$ 的值必然相同，$\beta$ 的值由 $\alpha$ 的值函数决定。

### 超键与候选键

- **超键（Superkey）**：$K \rightarrow R$，即 $K$ 的值能函数决定关系 $R$ 中所有属性的值
- **候选键（Candidate Key）**：最小的超键，即 $K$ 是超键且不存在 $K$ 的真子集也是超键

!!! tip "超键 vs 候选键"
    超键保证唯一性但可能包含冗余属性；候选键是"最精简"的超键，任何真子集都不再是超键。

### 平凡依赖

**平凡依赖（Trivial FD）**：$\beta \subseteq \alpha$ 时，$\alpha \rightarrow \beta$ 总是成立。

例如 $\{A, B\} \rightarrow \{A\}$ 是平凡的。

### 传递依赖

**传递依赖（Transitive Dependency）**：若 $\alpha \rightarrow \beta$ 且 $\beta \rightarrow \gamma$，其中 $\beta \not\supseteq \alpha$（$\beta$ 不是 $\alpha$ 的子集），且 $\beta \rightarrow \alpha$ 不成立（$\beta$ 不能反过来决定 $\alpha$），则 $\gamma$ 对 $\alpha$ 传递依赖。

!!! abstract "传递依赖的关键条件"
    $\beta \rightarrow \alpha$ 不成立这一条件至关重要——若 $\beta \rightarrow \alpha$ 成立，则 $\alpha$ 和 $\beta$ 是等价的，此时 $\alpha \rightarrow \gamma$ 是直接依赖而非传递依赖。

### 部分依赖

**部分依赖（Partial Dependency）**：若 $\alpha \rightarrow \beta$，但存在 $\alpha$ 的真子集 $\gamma \subset \alpha$ 也满足 $\gamma \rightarrow \beta$，则 $\beta$ 对 $\alpha$ 部分依赖。

部分依赖意味着 $\beta$ 不需要 $\alpha$ 的全部属性就能被决定，这是 2NF 要消除的问题。

## 逻辑蕴含与闭包

### 闭包 $F^+$

给定函数依赖集 $F$，其**闭包 $F^+$** 是 $F$ 所能逻辑蕴含的所有函数依赖的集合。

若 $F$ 逻辑蕴含 $\alpha \rightarrow \beta$，记作 $F \models \alpha \rightarrow \beta$，则 $\alpha \rightarrow \beta \in F^+$。

### Armstrong 公理体系

**Armstrong 公理**是推导 $F^+$ 的基础规则，既完备又可靠：

| 公理/规则 | 形式 | 说明 |
| --- | --- | --- |
| 自反律（Reflexivity） | $\beta \subseteq \alpha \implies \alpha \rightarrow \beta$ | 子集总是函数决定自身 |
| 增广律（Augmentation） | $\alpha \rightarrow \beta \implies \gamma\alpha \rightarrow \gamma\beta$ | 两边同时添加任意属性集合 |
| 传递律（Transitivity） | $\alpha \rightarrow \beta, \beta \rightarrow \gamma \implies \alpha \rightarrow \gamma$ | 函数依赖的链式推导 |

**附加推导规则**（可由公理推出）：

| 规则 | 形式 |
| --- | --- |
| 合并律（Union） | $\alpha \rightarrow \beta, \alpha \rightarrow \gamma \implies \alpha \rightarrow \beta\gamma$ |
| 分解律（Decomposition） | $\alpha \rightarrow \beta\gamma \implies \alpha \rightarrow \beta, \alpha \rightarrow \gamma$ |
| 伪传递律（Pseudotransitivity） | $\alpha \rightarrow \beta, \gamma\beta \rightarrow \delta \implies \gamma\alpha \rightarrow \delta$ |

!!! tip "合并律与分解律的推论"
    $\alpha \rightarrow \beta$ 当且仅当 $\alpha \rightarrow \{B_i\}$ 对 $\beta$ 中每个属性 $B_i$ 都成立。

## 属性集闭包 $X^+$

### 算法

给定函数依赖集 $F$ 和属性集 $X$，计算 $X^+$（$X$ 在 $F$ 下能函数决定的所有属性的集合）：

```
X⁺ = X
repeat
    for each α → β in F:
        if α ⊆ X⁺:
            X⁺ = X⁺ ∪ β
until X⁺ no longer changes
```

### 闭包的应用

| 应用 | 方法 |
| --- | --- |
| 测试超键 | $X^+ = R$ 则 $X$ 是超键 |
| 测试函数依赖 | $\beta \subseteq \alpha^+$ 则 $\alpha \rightarrow \beta \in F^+$ |
| 计算 $F^+$ | 对 $R$ 的每个子集 $X$ 计算 $X^+$，得到 $X \rightarrow X^+$ 中的所有 FD |

## 正则覆盖/最小覆盖

**正则覆盖（Canonical Cover）$F_c$** 是与 $F$ 等价（$F_c^+ = F^+$）的最简函数依赖集，满足：

1. 右侧均为单属性
2. 无冗余依赖（删除任何一条依赖后不再等价）
3. 无多余属性（左侧不含可删除的属性）

### 计算算法

1. **合并右侧**：将 $\alpha \rightarrow \beta_1$ 和 $\alpha \rightarrow \beta_2$ 合并为 $\alpha \rightarrow \beta_1\beta_2$
2. **去除多余属性**：逐一检查左侧每个属性是否多余
3. **去除冗余依赖**：逐一检查每条依赖是否冗余

## 多余属性判定

### 左侧多余属性

$\alpha \rightarrow \beta$ 中左侧属性 $A$ 多余的条件：在 $F$ 下 $(\alpha - A)^+$ 包含 $\beta$。

即：去掉 $A$ 后，剩余属性仍能决定 $\beta$。

### 右侧多余属性

$\alpha \rightarrow \beta$ 中右侧属性 $A$ 多余的条件：在修改后的 $F' = F - \{\alpha \rightarrow \beta\} \cup \{\alpha \rightarrow (\beta - A)\}$ 下，$\alpha^+$ 包含 $A$。

即：去掉 $A$ 后，$\alpha$ 仍能通过其他依赖推出 $A$。

!!! tip "判定方法总结"
    - **左侧多余**：用原始 $F$ 计算 $(\alpha - A)^+$，检查是否包含 $\beta$
    - **右侧多余**：用修改后的 $F'$ 计算 $\alpha^+$，检查是否包含 $A$

## 范式

### 1NF（第一范式）

所有属性值都是**原子的（不可再分）**。

### 2NF（第二范式）

在 1NF 基础上，**消除非键属性对候选键的部分依赖**。

即：每个非键属性必须**完全函数依赖**于每个候选键，不能只依赖候选键的某个真子集。

!!! abstract "2NF 要解决的问题"
    部分依赖导致冗余：若非键属性仅依赖候选键的一部分，则候选键其他属性的值变化不影响该非键属性，造成冗余存储和更新异常。

### 3NF（第三范式）

在 2NF 基础上，**消除非键属性对候选键的传递依赖**。

即：每个非键属性必须**直接函数依赖**于候选键，不能通过其他非键属性间接依赖。

形式化定义：对 $F$ 中每条 $\alpha \rightarrow \beta$，以下至少一条成立：

1. $\alpha \rightarrow \beta$ 是平凡的（$\beta \subseteq \alpha$）
2. $\alpha$ 是 $R$ 的超键
3. $\beta - \alpha$ 中的每个属性都属于 $R$ 的某个候选键

!!! tip "3NF 的第三条件"
    第三条件允许主属性（候选键中的属性）之间存在函数依赖，这是 3NF 与 BCNF 的关键区别。

### BCNF（Boyce-Codd 范式）

在 3NF 基础上进一步要求：**所有属性（包括键属性）都必须直接/完全依赖于每个包含它们的候选键**。

形式化定义：对 $F$ 中每条 $\alpha \rightarrow \beta$，以下至少一条成立：

1. $\alpha \rightarrow \beta$ 是平凡的（$\beta \subseteq \alpha$）
2. $\alpha$ 是 $R$ 的超键

!!! abstract "BCNF vs 3NF"
    BCNF 比 3NF 更严格：BCNF 不允许任何非超键的决定因子，即使是主属性之间的依赖也不允许。3NF 的第三条件在 BCNF 中被取消。

    | 范式 | 允许的非超键决定因子 |
    | --- | --- |
    | 3NF | 主属性（候选键中的属性）之间的 FD |
    | BCNF | 不允许任何非超键决定因子 |

## 候选键计算算法

通过属性分类来逐步确定候选键：

| 分类 | 条件 | 说明 |
| --- | --- | --- |
| **L 类** | 仅出现在 FD 左侧 | 必然属于所有候选键 |
| **R 类** | 仅出现在 FD 右侧 | 不可能属于任何候选键 |
| **N 类** | 左右都不出现 | 必然属于所有候选键 |
| **LR 类** | 左右都出现 | 可能属于候选键，需进一步判断 |

**算法步骤**：

1. 确定属性分类
2. $L$ 类和 $N$ 类属性一定在候选键中，令 $X = L \cup N$
3. 计算 $X^+$，若 $X^+ = R$，则 $X$ 是唯一候选键
4. 若 $X^+ \neq R$，逐一尝试将 $LR$ 类属性加入 $X$，直到 $X^+ = R$

## 分解

### 定义

将关系模式 $R$ 分解为 $R_1, R_2, \ldots, R_n$，满足 $R = R_1 \cup R_2 \cup \ldots \cup R_n$。

### 无损连接

**无损连接（Lossless-Join）**：分解后的关系通过自然连接能完全恢复原关系的所有信息。

$$r = \Pi_{R_1}(r) \bowtie \Pi_{R_2}(r) \bowtie \ldots \bowtie \Pi_{R_n}(r)$$

**二路分解的无损连接判定**：

$R_1 \cap R_2 \rightarrow R_1$ 或 $R_1 \cap R_2 \rightarrow R_2$ 成立则分解为无损的。

即：两个分解子模式的交集必须能函数决定其中至少一个子模式。

!!! abstract "无损连接的意义"
    无损连接保证分解不会丢失信息——原关系中的每个元组都能通过连接恢复，不会出现"虚假元组"或信息丢失。

### 保持函数依赖

**保持函数依赖（Dependency Preservation）**：

$$\left(F_1 \cup F_2 \cup \ldots \cup F_n\right)^+ = F^+$$

其中 $F_i$ 是 $F$ 在 $R_i$ 上的投影（即仅涉及 $R_i$ 中属性的 FD）。

保持函数依赖意味着分解后无需跨关系检查 FD 约束，所有约束都能在各自的关系内独立验证。

!!! tip "无损连接 vs 保持函数依赖"
    - 无损连接是**必须**保证的（否则分解丢失信息）
    - 保持函数依赖是**尽量**保证的（不保持时验证约束需要连接操作）
    - BCNF 分解总是无损的，但可能无法保持函数依赖
    - 3NF 分解算法既保证无损连接又保持函数依赖

## 3NF 分解算法

**输入**：关系模式 $R$，函数依赖集 $F$ 的正则覆盖 $F_c$

**输出**：满足 3NF、无损连接、保持函数依赖的分解

**步骤**：

1. **求正则覆盖 $F_c$**
2. **为 $F_c$ 中每条 FD $\alpha \rightarrow \beta$ 创建关系模式 $\alpha \cup \beta$**
3. **检查是否包含候选键**：若步骤 2 产生的关系中没有一个包含 $R$ 的候选键，则添加一个包含候选键的关系模式

!!! abstract "3NF 分解算法的性质"
    - 保证结果为 3NF
    - 保证无损连接（因为包含候选键的关系模式确保了连接的无损性）
    - 保证保持函数依赖（每条 FD 的属性都在某个关系模式中）
    - 可能不是 BCNF

## BCNF 分解算法

**步骤**（递归分解）：

1. 找到违反 BCNF 的函数依赖 $\alpha \rightarrow \beta$（$\alpha$ 不是超键）
2. 将 $R$ 分解为两个子模式：
    - $R_1 = \alpha \cup \beta$
    - $R_2 = R - (\beta - \alpha)$
3. 对 $R_1$ 和 $R_2$ 重复上述步骤，直到所有子模式都满足 BCNF

!!! abstract "BCNF 分解算法的性质"
    - 保证结果为 BCNF
    - 保证无损连接（每次二路分解都满足 $R_1 \cap R_2 = \alpha$，且 $\alpha \rightarrow \beta$ 即 $R_1 \cap R_2 \rightarrow R_1$，满足无损条件）
    - **可能无法保持函数依赖**

???+ warning "BCNF 分解的局限"
    当存在主属性之间的函数依赖时，BCNF 分解可能导致某些 FD 的属性被分散到不同关系中，从而无法在单一关系内验证这些约束。例如 $\alpha \rightarrow \beta$ 中 $\beta$ 包含主属性，分解后可能无法保持这条 FD。

## 设计工作流

数据库设计的整体流程：

1. **E-R 模型设计** → 获得概念模型
2. **转换为关系模式** → 获得初始关系模式
3. **识别范式级别** → 分析每条 FD，判断当前模式满足的范式
4. **分解优化** → 根据需要选择 3NF 或 BCNF 分解算法进行规范化

!!! tip "设计决策指南"
    | 场景 | 推荐方案 |
    | --- | --- |
    | 需要同时保证无损连接和保持函数依赖 | 3NF 分解算法 |
    | 需要更严格的范式（消除所有非超键决定因子） | BCNF 分解算法（接受可能丢失 FD 保持性） |
    | FD 涉及主属性间的依赖 | 3NF（BCNF 会过度分解） |
