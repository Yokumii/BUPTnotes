# 数据库系统复习

## 核心概念与定义

DBMS（数据库管理系统）
: 按照数据模型组织、存储和管理数据的软件系统，提供数据定义、查询、更新和控制功能。

数据不一致性（Data Inconsistency）
: 同一数据在不同副本中出现不同值的现象，由冗余存储和缺乏统一控制引起。

一致性约束（Consistency Constraints）
: 数据库中数据必须满足的规则，用于保证数据的正确性和有效性。

数据模型（Data Model）
: 描述数据结构、操作和约束的抽象框架。由三部分组成：**数据结构**（数据的组织方式）、**数据操作**（对数据的查询和更新）、**数据约束**（数据的完整性规则）。

三级模式架构（Three-Level Architecture）
: 数据库的抽象层次，分为内模式（物理层）、概念模式（逻辑层）、外模式（视图层）。

| 层次 | 英文名 | 中文名 | 说明 |
|------|--------|--------|------|
| 物理层 | Internal Schema | 内模式 | 数据的物理存储方式和存取路径 |
| 逻辑层 | Conceptual Schema | 概念模式 | 数据的逻辑结构和约束定义 |
| 视图层 | External Schema | 外模式 | 用户所见的数据视图子集 |

数据独立性（Data Independence）
: 修改上层模式不需修改下层应用程序的能力。

物理数据独立性
: 修改内模式（如存储结构、索引策略）不影响概念模式和外模式。

逻辑数据独立性
: 修改概念模式（如增加新字段、新关系）不影响外模式。

模式（Schema）与实例（Instance）
: 模式是数据库的逻辑设计（静态定义），实例是数据库在某一时刻的实际数据（动态内容）。

DDL（数据定义语言）
: 用于定义和修改数据库结构（模式）的语言，如 CREATE、ALTER、DROP。

DML（数据操纵语言）
: 用于查询和更新数据库实例数据的语言，如 SELECT、INSERT、DELETE、UPDATE。

### DBMS 组件

| 组件 | 功能 |
|------|------|
| 存储管理器（Storage Manager） | 负责与文件系统交互，提供缓冲区管理和数据存取 |
| 查询处理器（Query Processor） | 解析和优化查询，生成执行计划 |
| DDL 解释器（DDL Interpreter） | 处理 DDL 语句，更新模式定义并写入数据字典 |
| DML 编译器（DML Compiler） | 将 DML 语句转换为查询执行计划 |

DBA（数据库管理员）
: 负责数据库模式定义、存储结构及存取方法定义、权限管理和日常维护的专职人员。

### 关系模型核心术语

关系（Relation）
: 一个二维表，由行和列组成。

元组（Tuple）
: 关系中的一行，代表一个实体记录。

属性（Attribute）
: 关系中的一列，代表实体的一个特征。

关系实例（Relation Instance）
: 关系在某一时刻的具体元组集合。

关系模式（Relation Schema）
: 关系的名称及其属性集合的描述，如 $R(A_1, A_2, \ldots, A_n)$。

### 键的类型

超键（Superkey）
: 能唯一标识关系中每个元组的属性集（可能包含多余属性）。

候选键（Candidate Key）
: 最小超键，即不含多余属性的超键。一个关系可能有多个候选键。

主键（Primary Key）
: 从候选键中选定一个作为唯一标识，不允许 NULL。

外键（Foreign Key）
: 关系 $R_1$ 中的属性集，其值必须匹配另一个关系 $R_2$ 中主键的某个值，用于建立跨关系引用。

### 完整性约束

实体完整性（Entity Integrity）
: 主键属性不允许取 NULL 值。

参照完整性（Referential Integrity）
: 外键值必须匹配被参照关系的主键值，或为 NULL。

用户定义完整性（User-defined Integrity）
: 用户根据业务需求自定义的约束，如 CHECK 约束。

### 关系代数六种基本运算

| 运算 | 符号 | 说明 |
|------|------|------|
| 选择（Select） | $\sigma$ | 按条件选取元组 |
| 投影（Project） | $\Pi$ | 选取指定属性列 |
| 并（Union） | $\cup$ | 两个关系元组的合并（需兼容） |
| 差（Difference） | $-$ | 属于 $R_1$ 但不属于 $R_2$ 的元组 |
| 笛卡尔积（Cartesian Product） | $\times$ | 两个关系元组的所有组合 |
| rename | $\rho$ | 为关系或属性重命名 |

!!! abstract "关系代数补充运算"
    附加运算可由基本运算推导：交（Intersection）$= R_1 - (R_1 - R_2)$、自然连接（Natural Join）$= \Pi(\sigma(R_1 \times R_2))$、除（Division）等。

### ACID 属性

| 属性 | 说明 |
|------|------|
| 原子性（Atomicity） | 事务是不可分割的最小执行单位，要么全部完成要么全部回滚 |
| 一致性（Consistency） | 事务执行前后数据库必须保持一致性状态 |
| 隔离性（Isolation） | 并发事务互不干扰，中间状态对其他事务不可见 |
| 持久性（Durability） | 事务提交后其结果永久保存，不受系统故障影响 |

### 事务状态

| 状态 | 说明 |
|------|------|
| 活动状态（Active） | 事务正在执行 |
| 部分提交状态（Partially Committed） | 最后一条语句执行后，尚未提交 |
| 提交状态（Committed） | 事务成功完成，结果已持久化 |
| 失败状态（Failed） | 事务无法继续正常执行 |
| 中止状态（Aborted） | 事务已回滚，数据库恢复到事务前状态 |

!!! note "状态转换"
    Active → Partially Committed → Committed；Active / Partially Committed → Failed → Aborted。Aborted 后可选择重启（Active）或终止。

### 冲突操作与可串行化

冲突操作（Conflicting Operations）
: 两个操作属于不同事务，访问同一数据项，且至少一个是写操作。

冲突可串行化（Conflict Serializability）
: 若一个调度通过交换非冲突操作的顺序可以变为某个串行调度，则该调度是冲突可串行化的。

!!! tip "判定方法"
    优先图（Precedence Graph）无环 → 冲突可串行化。优先图中边 $T_i \to T_j$ 表示 $T_i$ 的冲突操作先于 $T_j$。

### 可恢复性与无级联调度

可恢复调度（Recoverable Schedule）
: 若 $T_j$ 读取了 $T_i$ 写入的数据，则 $T_i$ 必须在 $T_j$ 提交之前提交。

无级联调度（Cascadeless Schedule）
: 若 $T_j$ 读取了 $T_i$ 写入的数据，则 $T_i$ 必须在 $T_j$ 读取之前提交（避免级联回滚）。

!!! warning "层次关系"
    无级联调度 $\implies$ 可恢复调度 $\implies$ 冲突可串行化不一定成立。可恢复是正确恢复的必要条件，无级联是避免级联回滚的更强要求。


## 关系代数图解

<figure markdown="span">
  ![选择运算](https://webp-pic.yokumi.cn/2025/12/20251222234444776.png){ loading=lazy width="70%" }
  <figcaption>选择运算 $\sigma$</figcaption>
</figure>

<figure markdown="span">
  ![投影运算](https://webp-pic.yokumi.cn/2025/12/20251222234535387.png){ loading=lazy width="70%" }
  <figcaption>投影运算 $\Pi$</figcaption>
</figure>

<figure markdown="span">
  ![集合运算](https://webp-pic.yokumi.cn/2025/12/20251222234807804.png){ loading=lazy width="70%" }
  <figcaption>集合运算（并、交、差）</figcaption>
</figure>

<figure markdown="span">
  ![笛卡尔积](https://webp-pic.yokumi.cn/2025/12/20251223112354164.png){ loading=lazy width="70%" }
  <figcaption>笛卡尔积 $\times$</figcaption>
</figure>

<figure markdown="span">
  ![等值连接](https://webp-pic.yokumi.cn/2025/12/20251223112439112.png){ loading=lazy width="70%" }
  <figcaption>等值连接（Equijoin）</figcaption>
</figure>

<figure markdown="span">
  ![自然连接](https://webp-pic.yokumi.cn/2025/12/20251223112458896.png){ loading=lazy width="70%" }
  <figcaption>自然连接（Natural Join）</figcaption>
</figure>

<figure markdown="span">
  ![外连接](https://webp-pic.yokumi.cn/2025/12/20251223112958173.png){ loading=lazy width="70%" }
  <figcaption>外连接（Outer Join）</figcaption>
</figure>

<figure markdown="span">
  ![重命名运算](https://webp-pic.yokumi.cn/2025/12/20251223113125034.png){ loading=lazy width="70%" }
  <figcaption>重命名运算 $\rho$</figcaption>
</figure>

<figure markdown="span">
  ![聚合运算](https://webp-pic.yokumi.cn/2025/12/20251223113200503.png){ loading=lazy width="70%" }
  <figcaption>聚合运算 $\mathcal{G}$</figcaption>
</figure>


## SQL 要点

### DML 查询结构

```sql
SELECT [DISTINCT] target_list
FROM relation_list
[WHERE condition]
[GROUP BY grouping_attributes]
[HAVING group_condition]
[ORDER BY attribute_list [ASC|DESC]]
```

!!! abstract "执行顺序"
    FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY。理解执行顺序是写出正确查询的关键。

### 聚合函数与 NULL 处理

| 函数 | 说明 | NULL 处理 |
|------|------|-----------|
| COUNT(*) | 统计所有元组数（包括 NULL） | NULL 行也计入 |
| COUNT(attr) | 统计指定属性非 NULL 值的个数 | 忽略 NULL |
| SUM(attr) | 求和 | 忽略 NULL |
| AVG(attr) | 求平均值 | 忽略 NULL（只对非 NULL 值计算） |
| MIN(attr) | 最小值 | 忽略 NULL |
| MAX(attr) | 最大值 | 忽略 NULL |

!!! warning "NULL 规则"
    - COUNT(*) 包含 NULL 行；COUNT(attr) 不计 NULL
    - SUM/AVG/MIN/MAX 均忽略 NULL
    - WHERE 中 `attr = NULL` 错误，应使用 `attr IS NULL`
    - NULL 与任何值比较结果均为 unknown（三值逻辑：true/false/unknown）

### 集合运算

```sql
-- 并（自动去重）
(SELECT ...) UNION (SELECT ...)
-- 并（保留重复）
(SELECT ...) UNION ALL (SELECT ...)
-- 交
(SELECT ...) INTERSECT (SELECT ...)
-- 差
(SELECT ...) EXCEPT (SELECT ...)
```

!!! note "兼容性要求"
    参与集合运算的两个查询结果必须**兼容**：属性数相同、对应属性类型可兼容。

### 子查询

```sql
-- IN / NOT IN
WHERE attr IN (SELECT ...)

-- ANY / SOME / ALL
WHERE attr > ANY (SELECT ...)   -- 大于子查询中至少一个值
WHERE attr > ALL (SELECT ...)   -- 大于子查询中所有值

-- EXISTS（存在性检查）
WHERE EXISTS (SELECT ...)       -- 子查询非空则 true

-- UNIQUE（唯一性检查）
WHERE UNIQUE (SELECT ...)       -- 子查询结果无重复则 true

-- WITH（临时视图）
WITH temp(name, budget) AS (
    SELECT ..., ...
    FROM ...
    WHERE ...
)
SELECT ...
FROM temp, ...
WHERE ...
```

!!! tip "EXISTS 与 IN 的区别"
    EXISTS 不返回具体值，只判断子查询是否为空；IN 比较具体值。EXISTS 通常在相关子查询中使用，效率可能更高。

### 数据修改

```sql
-- 删除
DELETE FROM relation
[WHERE condition];

-- 插入
INSERT INTO relation(attr_list)
VALUES (value_list);
-- 或从查询插入
INSERT INTO relation(attr_list)
(SELECT ...);

-- 更新（含 CASE）
UPDATE relation
SET attr = CASE
    WHEN condition1 THEN value1
    WHEN condition2 THEN value2
    ELSE default_value
END
[WHERE condition];
```

### 连接类型

| 连接类型 | SQL 语法 | 说明 |
|----------|----------|------|
| 内连接 | `INNER JOIN` / `JOIN` | 只返回匹配的元组 |
| 左外连接 | `LEFT OUTER JOIN` | 返回左表全部 + 右表匹配（右表不匹配填 NULL） |
| 右外连接 | `RIGHT OUTER JOIN` | 返回右表全部 + 左表匹配（左表不匹配填 NULL） |
| 全外连接 | `FULL OUTER JOIN` | 返回两表全部（不匹配填 NULL） |

!!! abstract "连接语法"
    ```sql
    SELECT R.A, S.B
    FROM R JOIN S ON R.id = S.id;

    SELECT R.A, S.B
    FROM R LEFT OUTER JOIN S ON R.id = S.id;
    ```

### DDL（数据定义）

```sql
CREATE TABLE relation_name (
    attr1 datatype,
    attr2 datatype NOT NULL,
    ...
    PRIMARY KEY (attr_list),
    UNIQUE (attr_list),
    FOREIGN KEY (attr_list) REFERENCES other_relation(attr_list)
        [ON DELETE CASCADE | SET NULL | NO ACTION]
        [ON UPDATE CASCADE | SET NULL | NO ACTION],
    CHECK (condition)
);
```

!!! abstract "约束类型汇总"
    | 约束 | 说明 | 语法位置 |
    |--------|------|----------|
    | NOT NULL | 属性不允许 NULL | 列级 |
    | PRIMARY KEY | 主键（唯一+非空） | 表级或列级 |
    | UNIQUE | 值唯一（允许一个 NULL） | 表级或列级 |
    | FOREIGN KEY | 外键参照完整性 | 表级 |
    | CHECK | 自定义条件 | 表级或列级 |

```sql
ALTER TABLE relation ADD attr datatype;
ALTER TABLE relation DROP attr;
ALTER TABLE relation ADD CONSTRAINT ...;
ALTER TABLE relation DROP CONSTRAINT ...;

DROP TABLE relation;
```

### DCL（数据控制）

```sql
GRANT privilege_list ON relation TO user_list [WITH GRANT OPTION];
REVOKE privilege_list ON relation FROM user_list [CASCADE | RESTRICT];
```

!!! note "常见权限"
    SELECT、INSERT、UPDATE、DELETE、ALL PRIVILEGES。WITH GRANT OPTION 允许被授权者再授权。

### 视图

```sql
CREATE VIEW view_name(attr_list) AS
(SELECT ...);

-- 可更新视图条件：来自单个关系、不含聚合、不含 GROUP BY/HAVING、不含 DISTINCT、
-- 每个被修改属性必须直接来自基础关系的属性
DROP VIEW view_name;
```

### 索引

索引（Index）
: 辅助数据结构，用于加速数据检索，代价是额外存储空间和维护开销。

```sql
CREATE INDEX index_name ON relation(attr_list);
CREATE UNIQUE INDEX index_name ON relation(attr_list);
DROP INDEX index_name;
```

<figure markdown="span">
  ![索引概要](https://webp-pic.yokumi.cn/2025/12/20251206105645370.png){ loading=lazy width="70%" }
  <figcaption>索引类型概要</figcaption>
</figure>


## 数据库设计

### ER 模型

实体（Entity）
: 现实世界中可区分的对象，用矩形表示。

属性（Attribute）
: 实体的特征，用椭圆表示。分类：简单/复合、单值/多值、存储/派生。

联系（Relationship）
: 实体之间的关联，用菱形表示。有基数约束（1:1、1:N、M:N）和参与约束（全参与/部分参与）。

!!! abstract "ER 图核心要素"
    - **实体集**：矩形
    - **联系集**：菱形，标注基数约束
    - **属性**：椭圆，主键属性加下划线
    - **角色**：当同一实体集在联系中多次出现时标注角色名
    - **弱实体集**：双线矩形，依赖标识实体集存在，通过识别联系（双线菱形）关联

<figure markdown="span">
  ![ER 图概要 1](https://webp-pic.yokumi.cn/2025/12/20251224102739271.png){ loading=lazy width="70%" }
  <figcaption>ER 模型核心概念</figcaption>
</figure>

<figure markdown="span">
  ![ER 图概要 2](https://webp-pic.yokumi.cn/2025/12/20251224103056430.png){ loading=lazy width="70%" }
  <figcaption>ER 模型转换规则概要</figcaption>
</figure>

### ER 转关系模式规则

| ER 元素 | 转换规则 |
|---------|----------|
| 强实体集 | 直接建关系，属性为列，主键为主键 |
| 弱实体集 | 建关系，属性含自身属性+标识实体主键，主键为标识主键+弱实体分辨符 |
| 1:1 联系 | 合并到任一端实体，或单独建关系 |
| 1:N 联系 | 合并到 N 端实体（外键指向 1 端），或单独建关系 |
| M:N 系 | 单独建关系，含两端主键为外键，组合为主键 |
| 多值属性 | 单独建关系，含实体主键+多值属性列 |
| 复合属性 | 拆分为多个简单属性列 |

### 特化与泛化

特化（Specialization）
: 从高层实体集向下细化出低层实体集（自顶向下），低层继承高层属性。

泛化（Generalization）
: 从低层实体集向上合并出高层实体集（自底向上），高层为低层的共性抽象。

!!! note "特化/泛化约束"
    - **条件定义**：低层实体由条件区分（如 job_type = 'Student'）
    - **不相交**：低层实体集之间互不重叠（disjoint）
    - **重叠**：低层实体集可能有重叠（overlapping）
    - **完全性**：完全特化（total）要求每个高层实体必须属于某个低层；部分特化（partial）允许不属于任何低层

特化转关系模式：
- 不相交+完全：只建低层关系（每个低层含高层属性+自身特有属性）
- 其他情况：建高层关系+低层关系（低层外键引用高层主键）


## 关系规范化

### 函数依赖（FD）类型

平凡函数依赖（Trivial FD）
: $Y \subseteq X$ 时 $X \to Y$ 是平凡的，必然成立且无实际意义。

部分函数依赖（Partial FD）
: $X \to Y$ 且存在 $X' \subset X$ 使得 $X' \to Y$，即 $Y$ 只依赖 $X$ 的子集。

传递函数依赖（Transitive FD）
: $X \to Y$，$Y \not\to X$，$Y \to Z$，则 $X \to Z$ 是传递依赖。

### Armstrong 公理与附加规则

**三大公理**：

| 公理 | 表达 | 说明 |
|------|------|------|
| 自反律（Reflexivity） | 若 $Y \subseteq X$，则 $X \to Y$ | 平凡依赖必然成立 |
| 增广律（Augmentation） | 若 $X \to Y$，则 $XZ \to YZ$ | 两端同时添加属性 |
| 传递律（Transitivity） | 若 $X \to Y$ 且 $Y \to Z$，则 $X \to Z$ | 依赖可传递推导 |

**附加规则**（可由公理推导）：

| 规则 | 表达 |
|------|------|
| 合并律（Union） | 若 $X \to Y$ 且 $X \to Z$，则 $X \to YZ$ |
| 分解律（Decomposition） | 若 $X \to YZ$，则 $X \to Y$ 且 $X \to Z$ |
| 伪传递律（Pseudotransitivity） | 若 $X \to Y$ 且 $YW \to Z$，则 $XW \to Z$ |

### 属性闭包算法

给定 $F$ 和属性集 $X$，计算 $X$ 的闭包 $X^+$（即 $X$ 能函数决定的所有属性）：

```
result = X
repeat:
    for each FD Y → Z in F:
        if Y ⊆ result:
            result = result ∪ Z
until result 不再变化
```

!!! tip "闭包用途"
    - 判断 $X \to Y$ 是否成立：$Y \subseteq X^+$ 则成立
    - 判断 $X$ 是否为超键：$X^+$ 包含所有属性则 $X$ 是超键
    - 计算候选键：找最小超键

### 正则覆盖算法

正则覆盖（Canonical Cover）$F_c$：不含多余属性、不含冗余 FD 的最小等价 FD 集。

1. 用分解律将右侧为多属性的 FD 拆分为单属性
2. 去除左侧多余属性：对 $X \to Y$，检查 $X$ 的每个子属性 $A$，若 $(X - A)^+ \supseteq Y$（在 $F$ 去掉该 FD 后计算），则 $A$ 多余
3. 去除冗余 FD：对每个 $X \to Y$，若在去掉该 FD 后 $X^+ \supseteq Y$（用剩余 FD 计算），则该 FD 冗余

### 范式递进

| 范式 | 条件 | 解决的问题 |
|------|------|------------|
| 1NF | 属性值不可再分（原子值） | 消除嵌套/复合属性 |
| 2NF | 1NF + 消除部分函数依赖 | 消除非主属性对候选键的部分依赖 |
| 3NF | 2NF + 消除传递函数依赖 | 消除非主属性对候选键的传递依赖 |
| BCNF | 3NF + 每个非平凡 FD 的决定因素都是超键 | 消除主属性间的部分/传递依赖 |

!!! warning "3NF 与 BCNF 的区别"
    3NF 允许非平凡 FD $X \to Y$ 中 $X$ 不是超键，只要 $Y$ 是主属性（属于某个候选键）。BCNF 则要求所有非平凡 FD 的决定因素必须是超键，更为严格。

### 候选键计算方法

1. 只出现在所有 FD 左侧、不出现在右侧的属性 → **必在候选键中**（L 类）
2. 只出现在右侧、不出现在左侧的属性 → **必不在候选键中**（R 类）
3. 既出现在左侧又出现在右侧的属性 → **可能或可能不在**（LR 类）
4. 不出现在任何 FD 中的属性 → **必在候选键中**（N 类）

候选键 = L 类属性 + N 类属性 + LR 类属性中必要的最小组合（使闭包包含所有属性）。

### 无损连接测试

分解 $\{R_1, R_2\}$ 关于 FD 集 $F$ 无损连接的充要条件：

$$(R_1 \cap R_2) \to (R_1 - R_2) \quad \text{或} \quad (R_1 \cap R_2) \to (R_2 - R_1)$$

在 $F$ 的闭包中成立。

!!! note "通用测试（Chase 算法）"
    对多于两个关系的分解，使用 Chase 算法（表格法）：构造初始表格，用 FD 推导行值，若有一行变为全 $a$ 则无损。

### 依赖保持测试

检查分解后的 FD 集是否等价于原 FD 集：

1. 将 $F$ 按 $R_i$ 的属性集投影得到 $F_i = \{X \to Y \in F^+ \mid XY \subseteq R_i\}$
2. 计算 $(\bigcup F_i)^+$，检查是否等于 $F^+$

### 3NF 分解算法

1. 计算 $F$ 的正则覆盖 $F_c$
2. 对 $F_c$ 中每个 $X \to Y$，创建关系 $R_i = XY$
3. 若某 $R_i$ 不包含任何候选键，添加一个包含候选键的关系
4. 去除冗余关系（若 $R_i \subseteq R_j$，去掉 $R_i$）

!!! abstract "3NF 分解保证"
    - 无损连接（因最终含候选键的关系保证）
    - 依赖保持（每个 FD 都在某 $R_i$ 中）

### BCNF 分解算法

1. 初始 $R$ 为原关系
2. 若 $R$ 不满足 BCNF，找违反 FD $X \to Y$（$X$ 不是超键）
3. 分解为 $R_1 = XY$ 和 $R_2 = R - Y$
4. 对 $R_1$、$R_2$ 递归执行
5. 直到所有关系都满足 BCNF

!!! warning "BCNF 分解的限制"
    BCNF 分解保证无损连接，但不保证依赖保持。某些情况下不存在既满足 BCNF 又依赖保持的分解。


## 物理存储与查询

### 存储概述

| 存储层级 | 特点 |
|----------|------|
| 主存（Main Memory） | 速度快、容量小、易失 |
| 磁盘（Disk） | 速度慢、容量大、持久 |
| 磁带（Tape） | 顺序存取、容量极大、用于备份 |

!!! note "磁盘关键参数"
    - 存取时间 = 寻道时间 + 旋转等待时间 + 传输时间
    - 块（Block/Page）是磁盘与主存之间数据传输的单位

<figure markdown="span">
  ![变长记录](https://webp-pic.yokumi.cn/2025/12/20251223133820319.png){ loading=lazy width="70%" }
  <figcaption>变长记录存储结构</figcaption>
</figure>

<figure markdown="span">
  ![B+ 树索引](https://webp-pic.yokumi.cn/2025/12/20251223164901766.png){ loading=lazy width="70%" }
  <figcaption>B+ 树索引结构</figcaption>
</figure>

### 查询处理步骤

1. 解析与翻译（Parsing & Translation）
2. 优化（Optimization）
3. 执行（Execution）

### 代价估算公式

!!! abstract "基本代价参数"
    - $B$：数据块数
    - $T$：元组数
    - $V(A, R)$：属性 $A$ 的不同值数
    - 索引查找代价取决于索引类型（B+ 树：$h$ 次磁盘 I/O + 数据块访问）

| 操作 | 代价（磁盘 I/O） |
|------|-------------------|
| 全表扫描 | $B$（线性搜索） |
| 线性搜索+条件 | $B/2$（平均） |
| 等值选择（主索引） | $h + 1$ |
| 等值选择（辅助索引） | $h + \lceil T/V(A,R) \rceil$ |
| 选择+排序归并连接 | $B(R) + B(S) + B(R) + B(S)$（排序+合并） |
| 选择+嵌套循环连接 | $B(R) + B(R) \cdot B(S)$（最坏情况） |
| 选择+索引嵌套循环 | $B(R) + T(R) \cdot (\text{索引代价})$ |

### 启发式优化步骤

1. **选择运算下推**：尽早执行选择，减少中间结果大小
2. **投影运算下推**：尽早执行投影，减少属性数量
3. **连接运算转换**：将笛卡尔积+选择转换为等值/自然连接
4. **连接顺序优化**：选择使中间结果最小的连接顺序
5. **等价变换**：利用关系代数等价规则重写表达式


## 事务与并发

### ACID（复习）

见核心概念部分。事务是并发控制和恢复的基本单位。

### 冲突可串行化判定

构建**优先图（Precedence Graph）**：

- 对每对冲突操作 $o_i$（来自 $T_i$）和 $o_j$（来自 $T_j$），若 $o_i$ 先于 $o_j$，加边 $T_i \to T_j$
- 优先图**无环** → 冲突可串行化
- 优先图**有环** → 非冲突可串行化

### 两阶段锁（2PL）

两阶段锁协议（Two-Phase Locking）
: 事务分为**增长阶段**（只加锁）和**收缩阶段**（只解锁），一旦释放任何锁就不能再获取新锁。

| 2PL 变体 | 说明 |
|----------|------|
| 严格 2PL（Strict 2PL） | 所有排他锁在事务提交/中止后才释放 |
| 强严格 2PL（Rigorous 2PL） | 所有锁（共享+排他）在事务提交/中止后才释放 |

!!! warning "2PL 保证"
    2PL 保证冲突可串行化，但可能产生死锁。严格 2PL 进一步保证可恢复性和无级联性。

### 意向锁

| 锁类型 | 说明 |
|--------|------|
| IS（意向共享） | 拟对低层加 S 锁 |
| IX（意向排他） | 拟对低层加 X 锁 |
| S（共享锁） | 允许读、禁止写 |
| SIX（共享+意向排他） | 读整个对象+拟对部分加 X 锁 |
| X（排他锁） | 禁止其他读写 |

<figure markdown="span">
  ![锁兼容矩阵](https://webp-pic.yokumi.cn/2025/12/20251215130649461.png){ loading=lazy width="70%" }
  <figcaption>意向锁兼容矩阵</figcaption>
</figure>

!!! note "意向锁规则"
    对树形锁结构：对某节点加 S/X 锁前，必须先对所有祖先节点加相应的意向锁（IS/IX）。

### 死锁处理协议

| 方法 | 说明 |
|------|------|
| 超时法 | 等锁超过阈值则中止并回滚 |
| 等待图法 | 维护等待图，定期检测环 → 发现死锁则选择牺牲者回滚 |
| 预防法 | wait-die（老等新死）或 wound-wait（新伤老等） |


## 恢复系统

### 故障类型

| 故障类型 | 说明 | 恢复策略 |
|----------|------|----------|
| 事务故障 | 单个事务内部错误（如违反约束） | 回滚该事务 |
| 系统故障 | 系统崩溃导致主存数据丢失 | 重做已提交事务 + 回滚未提交事务 |
| 磁盘故障 | 磁盘物理损坏 | 从备份恢复 + 重做日志 |

### WAL（Write-Ahead Logging）

WAL 原则
: 在将修改写入磁盘数据块之前，必须先将对应的日志记录写入稳定存储（日志磁盘）。

!!! abstract "日志记录内容"
    - 事务标识 $T_i$
    - 修改的数据项旧值（用于 undo）
    - 修改的数据项新值（用于 redo）
    - 特殊记录：`<T_i START>`、`<T_i COMMIT>`、`<T_i ABORT>`

### 检查点恢复算法

检查点（Checkpoint）
: 定期将内存中所有已提交事务的修改写入磁盘，并记录检查点信息。

**系统故障恢复步骤**：

1. 从最近的检查点开始扫描日志
2. **重做列表**：检查点之后提交的所有事务
3. **回滚列表**：检查点之后未提交的所有事务
4. 对重做列表中的事务：从日志中 redo 所有修改
5. 对回滚列表中的事务：从日志中 undo 所有修改

!!! tip "检查点加速恢复"
    检查点之前的已提交事务无需 redo（其修改已在检查点时写入磁盘），只需处理检查点之后的事务。


## 考试题型

### SQL 建表题

???+ success "建表题 1：大学数据库（学生、部门、课程）"
    创建 student、department、course 三个表，含所有完整性约束。

    ```sql
    CREATE TABLE department (
        dept_name VARCHAR(20),
        building VARCHAR(15),
        budget NUMERIC(12,2),
        PRIMARY KEY (dept_name)
    );

    CREATE TABLE student (
        ID VARCHAR(5),
        name VARCHAR(20) NOT NULL,
        dept_name VARCHAR(20),
        tot_cred NUMERIC(3,0) DEFAULT 0,
        PRIMARY KEY (ID),
        FOREIGN KEY (dept_name) REFERENCES department(dept_name)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );

    CREATE TABLE course (
        course_id VARCHAR(8),
        title VARCHAR(50),
        dept_name VARCHAR(20),
        credits NUMERIC(2,0),
        PRIMARY KEY (course_id),
        FOREIGN KEY (dept_name) REFERENCES department(dept_name)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        CHECK (credits > 0)
    );
    ```

???+ success "建表题 2：大学数据库（教师、授课、选课）"
    在题 1 基础上继续创建 instructor、section、takes 表。

    ```sql
    CREATE TABLE instructor (
        ID VARCHAR(5),
        name VARCHAR(20) NOT NULL,
        dept_name VARCHAR(20),
        salary NUMERIC(8,2),
        PRIMARY KEY (ID),
        FOREIGN KEY (dept_name) REFERENCES department(dept_name)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        CHECK (salary > 0)
    );

    CREATE TABLE section (
        course_id VARCHAR(8),
        sec_id VARCHAR(8),
        semester VARCHAR(6),
        year NUMERIC(4,0),
        building VARCHAR(15),
        room_number VARCHAR(7),
        time_slot_id VARCHAR(4),
        PRIMARY KEY (course_id, sec_id, semester, year),
        FOREIGN KEY (course_id) REFERENCES course(course_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (building, room_number) REFERENCES classroom(building, room_number)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );

    CREATE TABLE takes (
        ID VARCHAR(5),
        course_id VARCHAR(8),
        sec_id VARCHAR(8),
        semester VARCHAR(6),
        year NUMERIC(4,0),
        grade VARCHAR(2),
        PRIMARY KEY (ID, course_id, sec_id, semester, year),
        FOREIGN KEY (ID) REFERENCES student(ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (course_id, sec_id, semester, year)
            REFERENCES section(course_id, sec_id, semester, year)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    ```

???+ success "建表题 3：银行数据库"
    创建 branch、account、customer、depositor 表。

    ```sql
    CREATE TABLE branch (
        branch_name VARCHAR(15),
        branch_city VARCHAR(15),
        assets NUMERIC(16,2),
        PRIMARY KEY (branch_name)
    );

    CREATE TABLE account (
        account_number VARCHAR(10),
        branch_name VARCHAR(15),
        balance NUMERIC(12,2),
        PRIMARY KEY (account_number),
        FOREIGN KEY (branch_name) REFERENCES branch(branch_name)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        CHECK (balance >= 0)
    );

    CREATE TABLE customer (
        customer_name VARCHAR(15),
        customer_street VARCHAR(15),
        customer_city VARCHAR(15),
        PRIMARY KEY (customer_name)
    );

    CREATE TABLE depositor (
        customer_name VARCHAR(15),
        account_number VARCHAR(10),
        PRIMARY KEY (customer_name, account_number),
        FOREIGN KEY (customer_name) REFERENCES customer(customer_name)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (account_number) REFERENCES account(account_number)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    ```

???+ success "建表题 4：员工-部门数据库"
    创建 employee 和 department 表，含参照完整性。

    ```sql
    CREATE TABLE employee (
        emp_id VARCHAR(5),
        emp_name VARCHAR(20) NOT NULL,
        dept_id VARCHAR(5),
        salary NUMERIC(8,2),
        PRIMARY KEY (emp_id),
        FOREIGN KEY (dept_id) REFERENCES department(dept_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        CHECK (salary > 0)
    );

    CREATE TABLE department (
        dept_id VARCHAR(5),
        dept_name VARCHAR(20) NOT NULL,
        manager_id VARCHAR(5),
        PRIMARY KEY (dept_id),
        FOREIGN KEY (manager_id) REFERENCES employee(emp_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );
    ```

???+ success "建表题 5：图书馆数据库"
    创建 book、member、borrow_record 表。

    ```sql
    CREATE TABLE book (
        book_id VARCHAR(10),
        title VARCHAR(50) NOT NULL,
        author VARCHAR(30),
        publisher VARCHAR(30),
        year NUMERIC(4,0),
        PRIMARY KEY (book_id)
    );

    CREATE TABLE member (
        member_id VARCHAR(10),
        name VARCHAR(20) NOT NULL,
        phone VARCHAR(15),
        PRIMARY KEY (member_id)
    );

    CREATE TABLE borrow_record (
        member_id VARCHAR(10),
        book_id VARCHAR(10),
        borrow_date DATE,
        return_date DATE,
        PRIMARY KEY (member_id, book_id, borrow_date),
        FOREIGN KEY (member_id) REFERENCES member(member_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (book_id) REFERENCES book(book_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    ```

### SQL 查询题

???+ success "查询题 1：查找工资大于 80000 的教师姓名"
    ```sql
    SELECT name
    FROM instructor
    WHERE salary > 80000;
    ```

???+ success "查询题 2：查找所有教师的姓名及所在部门名"
    ```sql
    SELECT instructor.name, department.dept_name
    FROM instructor JOIN department
        ON instructor.dept_name = department.dept_name;
    ```

???+ success "查询题 3：查找 Finance 部门中工资最高的教师"
    ```sql
    SELECT name, salary
    FROM instructor
    WHERE dept_name = 'Finance'
        AND salary = (
            SELECT MAX(salary)
            FROM instructor
            WHERE dept_name = 'Finance'
        );
    ```

???+ success "查询题 4：查找所有至少选了一门课的学生姓名"
    ```sql
    SELECT DISTINCT student.name
    FROM student JOIN takes ON student.ID = takes.ID;
    ```
    或使用 EXISTS：
    ```sql
    SELECT name
    FROM student
    WHERE EXISTS (
        SELECT *
        FROM takes
        WHERE takes.ID = student.ID
    );
    ```

???+ success "查询题 5：查找没有选任何课的学生姓名"
    ```sql
    SELECT name
    FROM student
    WHERE NOT EXISTS (
        SELECT *
        FROM takes
        WHERE takes.ID = student.ID
    );
    ```

???+ success "查询题 6：查找每个部门的平均工资（排除低于 40000 的部门）"
    ```sql
    SELECT dept_name, AVG(salary) AS avg_salary
    FROM instructor
    GROUP BY dept_name
    HAVING AVG(salary) > 40000;
    ```

???+ success "查询题 7：查找工资大于本部门平均工资的教师"
    ```sql
    SELECT instructor.name, instructor.salary, instructor.dept_name
    FROM instructor
    WHERE salary > (
        SELECT AVG(salary)
        FROM instructor AS T
        WHERE T.dept_name = instructor.dept_name
    );
    ```

???+ success "查询题 8：查找选了 Biology 系所有课程的学生"
    ```sql
    SELECT DISTINCT student.ID, student.name
    FROM student
    WHERE NOT EXISTS (
        SELECT course_id
        FROM course
        WHERE dept_name = 'Biology'
        AND course_id NOT IN (
            SELECT takes.course_id
            FROM takes
            WHERE takes.ID = student.ID
        )
    );
    ```

???+ success "查询题 9：给工资低于 70000 的教师涨 5% 工资"
    ```sql
    UPDATE instructor
    SET salary = salary * 1.05
    WHERE salary < 70000;
    ```

???+ success "查询题 10：按工资区间标记教师等级"
    ```sql
    SELECT name,
        CASE
            WHEN salary < 50000 THEN 'Low'
            WHEN salary BETWEEN 50000 AND 80000 THEN 'Medium'
            ELSE 'High'
        END AS level
    FROM instructor;
    ```

### 关系代数题

???+ success "关系代数题 1：查找工资大于 80000 的教师姓名"
    $$\Pi_{\text{name}}(\sigma_{\text{salary} > 80000}(\text{instructor}))$$

???+ success "关系代数题 2：查找 Finance 部门教师与学生的自然连接"
    $$\sigma_{\text{dept\_name} = \text{'Finance'}}(\text{instructor} \bowtie \text{student})$$

???+ success "关系代数题 3：查找选了 Biology 所有课程的学生（使用除法）"
    $$\Pi_{\text{ID, course\_id}}(\text{takes}) \div \Pi_{\text{course\_id}}(\sigma_{\text{dept\_name} = \text{'Biology'}}(\text{course}))$$

### ER 图绘制题

???+ success "ER 题 1：大学数据库"
    需绘制以下实体与联系：

    - 实体集：department、student、instructor、course、section、classroom
    - 联系集：
        - student 与 section 之间的 takes（M:N，含 grade 属性）
        - instructor 与 section 之间的 teaches（1:N）
        - course 与 section 之间的（1:N）
        - department 与 instructor 之间的 works（1:N）
        - department 与 student 之间的（1:N）
        - section 与 classroom 之间的 meets_in（M:N，含 time_slot_id）
    - student 为弱实体集时需标注识别联系（若有）

???+ success "ER 题 2：银行数据库"
    需绘制以下实体与联系：

    - 实体集：branch、account、customer、loan、employee
    - 联系集：
        - customer 与 account 之间的 depositor（M:N）
        - customer 与 loan 之间的 borrower（M:N）
        - branch 与 account 之间的 holds（1:N）
        - branch 与 loan 之间的 originates（1:N）
        - employee 与 branch 之间的 works_for（1:N）

???+ success "ER 题 3：图书馆数据库"
    需绘制以下实体与联系：

    - 实体集：book、member、author、publisher
    - 联系集：
        - member 与 book 之间的 borrow（M:N，含 borrow_date、return_date）
        - book 与 author 之间的 written_by（M:N）
        - book 与 publisher 之间的 published_by（N:1，含 year 属性）
    - book 的属性含多值属性（如多个 author）

???+ success "ER 题 4：公司数据库"
    需绘制以下实体与联系：

    - 实体集：employee、department、project、dependent
    - 联系集：
        - employee 与 department 之间的 works_for（1:N，含 start_date）
        - employee 与 project 之间的 manages（1:N）和 works_on（M:N，含 hours）
        - employee 与 dependent 之间的 dependent_of（1:N）
    - dependent 为弱实体集，依赖 employee（标识联系为 dependent_of）

???+ success "ER 题 5：医院数据库"
    需绘制以下实体与联系：

    - 实体集：patient、doctor、ward、medication、appointment
    - 联系集：
        - patient 与 doctor 之间的 appointment（M:N，含 date、time）
        - patient 与 ward 之间的 admitted_in（N:1，含 admit_date）
        - doctor 与 ward 之间的 assigned_to（N:1）
        - patient 与 medication 之间的 prescribed（M:N，含 dosage、duration）
    - patient 的属性含复合属性（如 address = street + city + zip）

### ER 转关系模式题

???+ success "ER 转 relation 题 1：大学数据库 ER 转关系"
    应用转换规则：

    - **强实体集**直接建关系：department(dept_name, building, budget)、student(ID, name, dept_name, tot_cred)、instructor(ID, name, dept_name, salary)、course(course_id, title, dept_name, credits)、classroom(building, room_number, capacity)
    - **1:N 联系**合并到 N 端：instructor 外键 dept_name → department；student 外键 dept_name → department；section 外键 course_id → course
    - **M:N 联系**单独建关系：takes(ID, course_id, sec_id, semester, year, grade)、teaches(ID, course_id, sec_id, semester, year)、meets_in(building, room_number, course_id, sec_id, semester, year, time_slot_id)
    - 所有 M:N 联系的主键为两端主键的组合

???+ success "ER 转 relation 题 2：公司数据库 ER 转关系"
    应用转换规则：

    - **强实体集**：employee(emp_id, name, address, sex, salary, dept_id)、department(dept_id, dept_name, manager_id)、project(proj_id, name, location, dept_id)
    - **弱实体集**：dependent(emp_id, dep_name, sex, birth_date, relationship)，主键为 emp_id + dep_name，外键 emp_id → employee
    - **1:N 联系**合并到 N 端：employee 外键 dept_id → department；department 外键 manager_id → employee
    - **M:N 联系**单独建关系：works_on(emp_id, proj_id, hours)，主键为 (emp_id, proj_id)

### 超键/候选键验证题

???+ success "键验证题 1：关系 R(A, B, C, D)，F = {A→B, B→C, C→D, D→A}"
    计算各属性的闭包：

    - $A^+ = \{A, B, C, D\}$ → $A$ 是超键
    - $B^+ = \{B, C, D, A\}$ → $B$ 是超键
    - $C^+ = \{C, D, A, B\}$ → $C$ 是超键
    - $D^+ = \{D, A, B, C\}$ → $D$ 是超键

    每个单一属性都能决定所有其他属性，因此候选键为 $\{A\}$、$\{B\}$、$\{C\}$、$\{D\}$（4 个候选键）。

???+ success "键验证题 2：关系 R(A, B, C, D)，F = {AB→C, C→D, D→A}"
    属性分类：
    - L 类（只出现在左侧）：B
    - R 类（只出现在右侧）：无（C 和 D 也出现在左侧）
    - LR 类：A、C、D

    $B$ 必在候选键中。计算 $\{B\}^+ = \{B\}$，不含所有属性，需增加 LR 类属性。

    - $\{AB\}^+ = \{A, B, C, D\}$ → 超键，且 $\{A\}^+ = \{A, D\} \neq$ 全集 → $\{AB\}$ 是候选键
    - $\{BC\}^+ = \{B, C, D, A\}$ → 超键，且 $\{C\}^+ = \{C, D, A\} \neq$ 全集 → $\{BC\}$ 是候选键
    - $\{BD\}^+ = \{B, D, A, C\}$ → 超键，且 $\{D\}^+ = \{D, A, C\} \neq$ 全集 → $\{BD\}$ 是候选键

    候选键为 $\{AB\}$、$\{BC\}$、$\{BD\}$。

???+ success "键验证题 3：用 SQL 验证超键"
    给定关系表 student(ID, name, dept_name, tot_cred)，验证 ID 是否为超键（即 ID 值唯一）。

    ```sql
    -- 验证 ID 是否唯一（无重复）
    SELECT ID, COUNT(*) AS cnt
    FROM student
    GROUP BY ID
    HAVING COUNT(*) > 1;
    -- 若结果为空，则 ID 值唯一，是超键
    ```

    验证 (ID, name) 是否为超键：

    ```sql
    SELECT ID, name, COUNT(*) AS cnt
    FROM student
    GROUP BY ID, name
    HAVING COUNT(*) > 1;
    -- 若结果为空，则 (ID, name) 是超键
    -- 但若 ID 已唯一，(ID, name) 含多余属性，不是候选键
    ```

