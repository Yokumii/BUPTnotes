# SQL 基础

## 概述

SQL（Structured Query Language）基于**集合运算**和**关系运算**，是关系数据库的标准查询语言。SQL 可分为以下几类：

| 类别 | 全称 | 典型语句 |
|------|------|----------|
| DDL | Data Definition Language | `CREATE` / `DROP` / `ALTER` |
| DML | Data Manipulation Language | `SELECT` / `INSERT` / `UPDATE` / `DELETE` |
| DCL | Data Control Language | `GRANT` / `REVOKE` |
| 嵌入式 / 动态 SQL | Embedded / Dynamic SQL | 在宿主语言中嵌入 SQL 语句 |

!!! abstract "核心思想"
    SQL 的查询本质上对应关系代数运算：`SELECT` 对应选择 σ 和投影 Π，`FROM` 对应笛卡尔积，`WHERE` 对应选择条件。

## DDL：数据定义

### 创建表

```sql
CREATE TABLE department (
    dept_name   VARCHAR(20)  NOT NULL,
    building    VARCHAR(15),
    budget      NUMERIC(12,2),
    PRIMARY KEY (dept_name)
);

CREATE TABLE instructor (
    ID          VARCHAR(5)    NOT NULL,
    name        VARCHAR(20)   NOT NULL,
    dept_name   VARCHAR(20),
    salary      NUMERIC(8,2),
    PRIMARY KEY (ID),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name)
);
```

!!! note "完整性约束（Integrity Constraints）"
    常用约束包括：
    - **`NOT NULL`**：属性值不允许为空
    - **`PRIMARY KEY`**：主键约束，隐含 `NOT NULL` + `UNIQUE`
    - **`FOREIGN KEY`**：外键约束，引用另一关系的主键

### 删除表

```sql
DROP TABLE student;
```

!!! warning "DROP vs DELETE"
    `DROP TABLE` 删除整张表（结构 + 数据）；`DELETE FROM` 仅删除表中数据，保留表结构。

### 修改表

```sql
ALTER TABLE instructor ADD birthday DATE;
```

`ALTER TABLE` 可用于添加属性列，多数数据库也支持 `DROP COLUMN` 删除列。

## DML：数据查询

### 基本查询

```sql
SELECT name FROM instructor;
SELECT DISTINCT dept_name FROM instructor;  -- 去重
SELECT * FROM instructor;                   -- 所有属性
```

`SELECT DISTINCT` 对应关系代数中去重运算；省略 `DISTINCT` 时 SQL 默认保留重复元组（与关系代数不同）。

### 重命名

```sql
SELECT ID, name AS instructor_name
FROM instructor;

-- 表级别名
SELECT T.name
FROM instructor AS T;
```

### 字符串匹配

```sql
SELECT name FROM instructor
WHERE name LIKE '%dar%';
```

| 通配符 | 含义 |
|--------|------|
| `%` | 匹配任意长度（含 0）的字符串 |
| `_` | 匹配恰好一个字符 |

### 排序

```sql
SELECT name, salary FROM instructor
ORDER BY salary DESC, name ASC;
```

`DESC` 为降序，`ASC` 为升序（默认）。

### 集合运算

```sql
(SELECT course_id FROM section WHERE year = 2009)
UNION
(SELECT course_id FROM section WHERE year = 2010);

(SELECT course_id FROM section WHERE year = 2009)
INTERSECT
(SELECT course_id FROM section WHERE year = 2010);

(SELECT course_id FROM section WHERE year = 2009)
EXCEPT
(SELECT course_id FROM section WHERE year = 2010);
```

!!! tip "UNION vs UNION ALL"
    - `UNION` 自动去重（对应关系代数 ∪）
    - `UNION ALL` 不去重（对应多集运算）
    - `INTERSECT ALL` 和 `EXCEPT ALL` 同理

### 聚集函数

```sql
SELECT AVG(salary) FROM instructor;
SELECT MIN(salary), MAX(salary) FROM instructor;
SELECT SUM(salary) FROM instructor;
SELECT COUNT(*) FROM instructor;
SELECT COUNT(DISTINCT dept_name) FROM instructor;
```

| 函数 | 含义 |
|------|------|
| `AVG` | 平均值 |
| `MIN` | 最小值 |
| `MAX` | 最大值 |
| `SUM` | 总和 |
| `COUNT` | 计数 |

### 分组

```sql
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name;
```

!!! warning "GROUP BY 的重要规则"
    `SELECT` 子句中出现的非聚集属性**必须**出现在 `GROUP BY` 中；否则语义不明确——无法确定该属性取哪个值。

### HAVING 子句

```sql
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name
HAVING AVG(salary) > 42000;
```

!!! note "WHERE vs HAVING"
    - **`WHERE`**：在分组前过滤元组（作用于单行）
    - **`HAVING`**：在分组后过滤组（作用于组级聚集结果）

### 查询执行顺序

SQL 查询的逻辑处理顺序为：

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

## NULL 值

```sql
SELECT name FROM instructor
WHERE salary IS NULL;

SELECT name FROM instructor
WHERE salary IS NOT NULL;
```

!!! warning "NULL 的特殊语义"
    - 任何涉及 `NULL` 的算术运算结果为 `NULL`（如 `5 + NULL = NULL`）
    - 任何涉及 `NULL` 的比较运算结果为 **unknown**（三值逻辑：true / false / unknown）
    - `WHERE` 子句仅保留条件为 **true** 的元组；unknown 和 false 的元组均被排除
    - 聚集函数中 `NULL` 被忽略（`COUNT(*)` 除外）

## 子查询

### 非相关子查询

子查询独立执行，不依赖外层查询：

```sql
SELECT name FROM instructor
WHERE dept_name IN (
    SELECT dept_name FROM department
    WHERE building = 'Taylor'
);
```

### 相关子查询

子查询引用外层查询的属性，每行都重新执行：

```sql
SELECT name, salary FROM instructor AS I
WHERE salary > (
    SELECT AVG(salary) FROM instructor
    WHERE dept_name = I.dept_name
);
```

### 子查询的位置

子查询可出现在以下位置：

| 位置 | 说明 |
|------|------|
| `WHERE` 子句 | 最常见，用于条件过滤 |
| `FROM` 子句 | 生成临时关系供外层查询使用 |
| `SELECT` 子句 | 返回单个值作为输出列 |

### WHERE 子句中的子查询谓词

#### SOME / ALL

```sql
-- 找到比 Biology 系所有教师薪资都高的教师
SELECT name FROM instructor
WHERE salary > ALL (
    SELECT salary FROM instructor
    WHERE dept_name = 'Biology'
);
```

- `> SOME`：大于子查询结果中**至少一个**值
- `> ALL`：大于子查询结果中**所有**值

#### EXISTS / NOT EXISTS

```sql
-- 找出在 2009 年秋季和 2010 年春季都开课的课程
SELECT course_id FROM section AS S
WHERE year = 2009 AND semester = 'Fall'
AND EXISTS (
    SELECT * FROM section AS T
    WHERE year = 2010 AND semester = 'Spring'
    AND T.course_id = S.course_id
);
```

`EXISTS`：子查询结果非空时返回 true。

#### UNIQUE / NOT UNIQUE

```sql
SELECT course_id FROM section
WHERE UNIQUE (
    SELECT course_id FROM section
    WHERE year = 2009 AND semester = 'Fall'
);
```

`UNIQUE`：子查询结果无重复元组时返回 true。

### WITH 子句

```sql
WITH dept_avg(dept_name, avg_salary) AS (
    SELECT dept_name, AVG(salary)
    FROM instructor
    GROUP BY dept_name
)
SELECT dept_name, avg_salary
FROM dept_avg
WHERE avg_salary > 42000;
```

`WITH` 子句定义临时中间关系，可被后续查询引用，作用域仅限当前查询语句。

## 数据修改

### 删除

```sql
DELETE FROM instructor
WHERE dept_name = 'Finance';
```

### 插入

```sql
INSERT INTO instructor
VALUES ('10101', 'Smith', 'Comp. Sci.', 65000);

INSERT INTO instructor(name, dept_name, salary)
SELECT name, dept_name, salary
FROM instructor
WHERE dept_name = 'Music';
```

### 更新

```sql
UPDATE instructor
SET salary = salary * 1.05
WHERE dept_name = 'Comp. Sci.';
```

### 索引

```sql
CREATE INDEX student_idx ON student(ID);
DROP INDEX student_idx;
```

!!! tip "索引的作用"
    索引可加速查询，但会增加插入 / 更新的开销。应在查询频繁的属性上创建索引。

