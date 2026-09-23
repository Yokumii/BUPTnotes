# 关系模型

## 关系数据结构

### 基本概念

域（Domain）
: 一组具有相同数据类型的值的集合，即属性的**取值范围**

笛卡尔积（Cartesian Product）
: 给定一组域 $D_1, D_2, \ldots, D_n$，它们的笛卡尔积为

$$D_1 \times D_2 \times \cdots \times D_n = \{(d_1, d_2, \ldots, d_n) \mid d_i \in D_i\}$$

关系（Relation）
: 笛卡尔积的**子集**，即在 $D_1 \times D_2 \times \cdots \times D_n$ 上具有实际意义的元组集合

!!! abstract "关系的本质"
    关系是笛卡尔积中有意义的子集——并非所有组合都有实际意义，只有满足特定语义约束的子集才构成一个关系。引入**属性名**后，关系的列顺序可以任意交换（满足交换律），因为属性名标识了每列的含义而非位置。

## 关系模式

关系模式（Relation Schema）
: 关系的**逻辑描述**，记作 $R(A_1, A_2, \ldots, A_n)$，其中 $R$ 为关系名，$A_i$ 为属性名

关系实例（Relation Instance）
: 关系模式 $R$ 在某一时刻的具体元组集合，记作 $r(R)$

!!! tip "模式与实例的区别"
    **模式**是稳定的、逻辑的定义（"表的结构"）；**实例**是动态的、随时间变化的数据（"表的内容"）。

## 关系实例的性质

<figure markdown="span">
  ![关系实例示例](https://webp-pic.yokumi.cn/2025/09/20250915141852439.png){ loading=lazy width="70%" }
</figure>

关系实例呈现为二维表，具有以下性质：

属性（Attribute）
: 表的**列**，每个属性对应一个域

元组（Tuple）
: 表的**行**，每个元组是关系的一个元素

- **列顺序无关**：属性名标识含义，列可任意交换
- **行顺序无关**：元组是无序集合
- **属性值原子**：每个属性的域必须是**不可再分**的原子值
- **属性名唯一**：同一关系中属性名不能重复
- **元组不重复**：关系中不允许出现完全相同的两个元组

## 键

超键（Super Key）
: 能**唯一标识**关系中元组的属性集合；任何包含候选键的属性集都是超键

候选键（Candidate Key）
: **最小超键**——满足唯一性且不可缩减（去掉任一属性就不再唯一）

主键（Primary Key）
: 从候选键中**选定**的一个，用于唯一标识元组；主键**不允许为 NULL**

外键（Foreign Key）
: 关系 $R_1$ 中的属性（组），它**引用**关系 $R_2$ 的主键；外键可以为 NULL，也可以引用同一关系的主键（自引用）

???+ info "键的层次关系"
    超键 $\supset$ 候选键 $\supset$ {主键}。选择主键的原则：值稳定、尽量短、不含过多属性。

## 完整性约束

实体完整性（Entity Integrity）
: 主键属性**不允许取空值（NULL）**——因为主键用于唯一标识元组，空值将无法区分不同元组

参照完整性（Referential Integrity）
: 外键的取值要么为 **NULL**，要么必须**等于**被引用关系中某个元组的主键值

!!! warning "完整性约束的意义"
    实体完整性保证了每个元组可被唯一识别；参照完整性保证了关系之间的引用一致性——被引用的元组必须存在，防止"悬空引用"。

## 关系代数

关系代数是关系模型的理论操作语言，运算对象和结果都是关系。

### 基本运算

选择（Selection） $\sigma_p(r)$
: 从关系 $r$ 中选取满足条件 $p$ 的元组（按行过滤）

    $$\sigma_{\text{salary} > 50000}(\text{Employee})$$

投影（Projection） $\Pi_{A_1, \ldots, A_n}(r)$
: 从关系 $r$ 中选取指定属性列，并**自动去重**

    $$\Pi_{\text{name, salary}}(\text{Employee})$$

并（Union） $r \cup s$
: 两个关系 $r$ 和 $s$ 的元组合并（去重）；要求属性个数相同且对应域兼容

差（Set Difference） $r - s$
: 在 $r$ 中但不在 $s$ 中的元组；同样要求属性个数和域兼容

笛卡尔积（Cartesian Product） $r \times s$
: $r$ 的每个元组与 $s$ 的每个元组拼接；若两关系有同名属性，需先使用**重命名**运算区分

重命名（Rename） $\rho_x(E)$
: 将表达式 $E$ 的结果关系命名为 $x$，或对其属性重命名

    $$\rho_{R(A_1, A_2)}(E)$$

### 附加运算

以下运算可由基本运算导出：

交（Intersection） $r \cap s$
: 同时存在于 $r$ 和 $s$ 中的元组

    $$r \cap s = r - (r - s)$$

连接（Join / Theta Join） $r \bowtie_{A\theta B} s$
: 在笛卡尔积上按条件 $A\theta B$ 进行选择

    $$r \bowtie_{A\theta B}\, s = \sigma_{A\theta B}(r \times s)$$

自然连接（Natural Join） $r \bowtie s$
: 在所有**同名属性**上等值连接，并去除重复列

除（Division） $r \div s$
: 选取 $r$ 中与 $s$ 的所有元组都匹配的属性组

赋值（Assignment） $r \leftarrow E$
: 将表达式 $E$ 的结果赋给关系名 $r$，用于简化复杂表达式的书写

## 外连接

外连接保留未匹配的元组，用 NULL 填充缺失部分：

左外连接（Left Outer Join） $r \bowtie_L s$
: 保留 $r$ 中所有元组，$s$ 中无匹配的属性填 NULL

右外连接（Right Outer Join） $r \bowtie_R s$
: 保留 $s$ 中所有元组，$r$ 中无匹配的属性填 NULL

全外连接（Full Outer Join） $r \bowtie_F s$
: 保留两侧所有元组，无匹配处均填 NULL

!!! tip "连接 vs 外连接"
    自然连接（内连接）只保留匹配的元组；外连接则保证至少一侧的全部元组不丢失，适用于报表、统计等需要完整数据的场景。

## NULL 值

NULL
: 表示**未知**（unknown）或**不存在**的值

NULL 的运算规则：

- 与 NULL 的算术运算结果为 NULL：$5 + \text{NULL} = \text{NULL}$
- 与 NULL 的比较运算结果为 **unknown**（在逻辑判断中视为 **false**）
- 聚合函数（SUM、AVG 等）忽略 NULL 值

!!! warning "NULL 在关系代数中的影响"
    NULL 值使得比较运算产生**三值逻辑**（true / false / unknown），而非传统二值逻辑。这增加了查询条件和完整性约束的复杂性。

## 数据库修改

删除（Delete） $r \leftarrow r - E$
: 从关系 $r$ 中删除满足表达式 $E$ 的元组

插入（Insert） $r \leftarrow r \cup E$
: 向关系 $r$ 中插入表达式 $E$ 计算得出的元组

更新（Update） $r \leftarrow \Pi_{F_1, \ldots, F_i}(r)$
: 对关系 $r$ 中指定属性的值进行修改；$F_i$ 为更新表达式（如 $F_i = \text{salary} \times 1.1$ 表示薪资增加 10%）

!!! abstract "修改的本质"
    删除、插入、更新均可视为关系代数运算的赋值形式——先通过代数表达式计算出目标子集，再对原关系做集合运算。

