# SQL 进阶

## 连接查询

### 自然连接

```sql
SELECT name, course_id
FROM instructor NATURAL JOIN teaches;
```

!!! note "自然连接 vs 普通连接"
    - **自然连接（NATURAL JOIN）**：在所有同名属性上做等值连接，并**去除重复列**
    - **普通连接（JOIN ... ON）**：需显式指定连接条件，**保留所有列**（含重复列）

```sql
-- 普通连接：保留两份 dept_name
SELECT name, course_id
FROM instructor JOIN teaches ON instructor.ID = teaches.ID;

-- 自然连接：仅保留一份 dept_name
SELECT name, course_id
FROM instructor NATURAL JOIN teaches;
```

!!! warning "自然连接的风险"
    如果两表有**非预期的同名属性**，自然连接会在这些属性上也做等值匹配，可能导致意外结果。建议使用 `JOIN ... ON` 显式指定连接条件。

### 外连接

```sql
-- 左外连接：保留左表所有行，右表无匹配时填充 NULL
SELECT name, course_id
FROM instructor LEFT OUTER JOIN teaches ON instructor.ID = teaches.ID;

-- 右外连接：保留右表所有行
SELECT name, course_id
FROM instructor RIGHT OUTER JOIN teaches ON instructor.ID = teaches.ID;

-- 全外连接：保留两表所有行
SELECT name, course_id
FROM instructor FULL OUTER JOIN teaches ON instructor.ID = teaches.ID;
```

| 类型 | 保留行 | 无匹配时 |
|------|--------|----------|
| 内连接（INNER JOIN） | 仅匹配行 | 丢弃 |
| 左外连接（LEFT OUTER JOIN） | 左表全部 | 右表填 NULL |
| 右外连接（RIGHT OUTER JOIN） | 右表全部 | 左表填 NULL |
| 全外连接（FULL OUTER JOIN） | 两表全部 | 对侧填 NULL |

## 视图

视图（View）是一种**虚拟关系**，不存储实际数据，查询时动态计算。

```sql
CREATE VIEW faculty AS
SELECT ID, name, dept_name
FROM instructor;

CREATE VIEW department_total_salary(dept_name, total_salary) AS
SELECT dept_name, SUM(salary)
FROM instructor
GROUP BY dept_name;
```

!!! abstract "视图的作用"
    视图主要用于**隐藏数据**——简化查询、限制用户可见范围、提供逻辑数据独立性。

### 视图更新

视图的更新操作会被**映射**到底层基本关系上：

```sql
INSERT INTO faculty VALUES('11111', 'Lee', 'Physics');
-- 实际映射为：
INSERT INTO instructor(ID, name, dept_name) VALUES('11111', 'Lee', 'Physics');
```

!!! warning "视图更新的限制"
    - 由**单个基本关系**导出、且包含主键的视图通常可更新
    - 包含**聚集函数**、**多表连接**、**DISTINCT** 的视图一般**不可直接更新**
    - 若视图属性来自表达式（如 `salary * 1.1`），则无法反向映射到基本关系

## 事务

事务（Transaction）
: 由一系列操作组成的**逻辑工作单元**，要么全部执行成功，要么全部回滚

```sql
BEGIN TRANSACTION;

UPDATE account SET balance = balance - 100 WHERE account_id = 'A';
UPDATE account SET balance = balance + 100 WHERE account_id = 'B';

COMMIT;  -- 或 ROLLBACK;
```

!!! abstract "事务的核心特性（ACID）"
    - **Atomicity**（原子性）：事务中的操作要么全部完成，要么全部不执行
    - **Consistency**（一致性）：事务执行前后数据库处于一致状态
    - **Isolation**（隔离性）：并发事务之间互不干扰
    - **Durability**（持久性）：事务提交后结果永久保存

## 完整性约束

### 单关系约束

| 约束 | 语法 | 说明 |
|------|------|------|
| `NOT NULL` | `salary NUMERIC(8,2) NOT NULL` | 属性值不允许为空 |
| `PRIMARY KEY` | `PRIMARY KEY(ID)` | 主键 = NOT NULL + UNIQUE |
| `UNIQUE` | `UNIQUE(name)` | 唯一约束，**允许 NULL** |
| `CHECK` | `CHECK(salary > 0)` | 满足指定条件 |

!!! note "UNIQUE 与 PRIMARY KEY 的区别"
    `UNIQUE` 允许属性值为 `NULL`（多个 NULL 仍可能冲突，取决于数据库实现）；`PRIMARY KEY` 隐含 `NOT NULL`。

### 参照完整性

```sql
FOREIGN KEY (dept_name) REFERENCES department(dept_name)
```

!!! abstract "参照完整性规则"
    外键（FK）的值必须为以下两种之一：
    - **NULL**：表示尚未关联
    - **存在于被引用关系的主键中**：表示有效关联

### 参照完整性：删除 / 更新动作

当被引用关系的元组被删除或更新时，参照关系中的外键如何处理？

```sql
FOREIGN KEY (dept_name) REFERENCES department(dept_name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
```

| 动作 | 含义 |
|------|------|
| `CASCADE` | 级联：删除/更新被引用元组时，自动删除/更新引用元组 |
| `SET NULL` | 将外键设为 NULL |
| `SET DEFAULT` | 将外键设为默认值 |
| `NO ACTION` / `RESTRICT` | 拒绝违反约束的删除/更新操作 |

!!! tip "选择策略"
    - 需要保持关联数据一致性 → `CASCADE`
    - 允许关联暂时悬空 → `SET NULL`
    - 严格禁止破坏关联 → `NO ACTION` / `RESTRICT`

## 索引

索引可**加速查询**，在频繁查询的属性上创建：

```sql
CREATE INDEX student_id_idx ON student(ID);
CREATE INDEX instructor_name_idx ON instructor(name);

DROP INDEX student_id_idx;
```

!!! warning "索引的开销"
    索引加速查询，但会增加 `INSERT` / `UPDATE` / `DELETE` 的开销（需同步维护索引）。应在查询频繁、更新较少的属性上创建索引。

## 用户自定义类型

### CREATE TYPE

```sql
-- 复合类型
CREATE TYPE Dollars AS NUMERIC(12,2) FINAL;

-- 枚举类型
CREATE TYPE Grade AS ENUM ('A', 'B', 'C', 'D', 'F');

-- 使用自定义类型
CREATE TABLE student_grade (
    course_id VARCHAR(8),
    grade     Grade
);
```

### CREATE DOMAIN

```sql
CREATE DOMAIN SalaryDomain NUMERIC(8,2)
    CONSTRAINT salary_range CHECK (value >= 0);
```

!!! note "TYPE vs DOMAIN"
    - **`CREATE TYPE`**：定义全新数据类型（复合类型、枚举类型、对象类型），不可直接加 `CHECK` 约束
    - **`CREATE DOMAIN`**：基于已有类型的**受约束别名**，可附加 `CHECK` 约束，更灵活

## 授权

### 授权图

<figure markdown="span">
  ![授权图](https://webp-pic.yokumi.cn/2025/10/20251027135156741.png){ loading=lazy width="70%" }
</figure>

### GRANT / REVOKE

```sql
-- 授权
GRANT SELECT ON department TO Amit;
GRANT INSERT, UPDATE ON department TO Satoshi;
GRANT ALL PRIVILEGES ON department TO Amit WITH GRANT OPTION;

-- 撤权
REVOKE SELECT ON department FROM Amit;
REVOKE INSERT ON department FROM Satoshi CASCADE;
```

!!! note "WITH GRANT OPTION"
    `WITH GRANT OPTION` 允许被授权者将权限**转授**给其他用户。撤销时，级联撤销（`CASCADE`）会同时收回所有经由该用户转授出去的权限。

### 权限类别

| 权限类别 | 权限项 |
|----------|--------|
| 数据权限 | `SELECT`（读）、`INSERT`（插入）、`UPDATE`（更新）、`DELETE`（删除） |
| 模式权限 | `INDEX`（创建索引）、`RESOURCES`（创建新关系）、`ALTERATION`（修改关系结构）、`DROP`（删除关系） |

### 角色

```sql
-- 创建角色
CREATE ROLE instructor_role;

-- 为角色授权
GRANT SELECT ON instructor TO instructor_role;
GRANT INSERT ON teaches TO instructor_role;

-- 将角色授予用户
GRANT instructor_role TO Amit;
GRANT instructor_role TO Satoshi;
```

!!! abstract "角色的优势"
    角色是一组权限的集合，将权限授予角色而非单个用户，简化权限管理：
    - 新用户加入时只需 `GRANT role TO user`
    - 权限变更时只需修改角色的权限，所有持有该角色的用户自动生效

## 触发器

触发器（Trigger）
: 一种**存储过程**，在指定事件（INSERT / UPDATE / DELETE）发生时自动执行

```sql
CREATE TRIGGER credits_update
AFTER UPDATE ON takes
REFERENCING NEW ROW AS nrow
             OLD ROW AS orow
FOR EACH ROW
WHEN (orow.grade IS NOT NULL AND nrow.grade IS NOT NULL
      AND orow.grade <> nrow.grade
      AND (nrow.grade = 'A' OR nrow.grade = 'B'))
BEGIN ATOMIC
    UPDATE student
    SET tot_cred = tot_cred +
        (SELECT credits FROM course
         WHERE course_id = nrow.course_id)
    WHERE ID = nrow.ID;
END;
```

!!! note "触发器的组成要素"
    - **时机**：`BEFORE`（事件发生前）或 `AFTER`（事件发生后）
    - **事件**：`INSERT` / `UPDATE` / `DELETE`
    - **粒度**：`FOR EACH ROW`（行级）或 `FOR EACH STATEMENT`（语句级）
    - **条件**：`WHEN` 子句指定触发条件
    - **动作**：`BEGIN ATOMIC ... END` 中定义执行体

???+ info "行级 vs 语句级触发器"
    | 粒度 | 执行次数 | 适用场景 |
    |------|----------|----------|
    | `FOR EACH ROW` | 每受影响行执行一次 | 需逐行处理（如审计每条变更） |
    | `FOR EACH STATEMENT` | 整条语句执行一次 | 需汇总处理（如统计变更总数） |

!!! warning "触发器的使用建议"
    触发器逻辑隐蔽，调试困难，易导致级联触发（触发器 A 触发触发器 B）。应优先使用显式约束和存储过程，仅在约束无法表达时使用触发器。

