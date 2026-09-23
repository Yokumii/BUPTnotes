# 数据库系统引论

## 文件系统的缺陷

传统文件系统在管理数据时存在诸多问题：

数据冗余与不一致（Data Redundancy and Inconsistency）
: 不同部门各自维护数据文件，同一数据多次存储，导致冗余；更新某一份而未同步其他副本时，产生不一致

数据访问困难（Difficulty in Accessing Data）
: 每次新增查询需求都需要编写专门程序，无法通过统一接口灵活检索

数据孤立（Data Isolation）
: 数据分散在不同格式、不同位置的文件中，难以整合与统一处理

完整性问题（Integrity Problems）
: 约束条件（如"年龄必须 > 0"）在文件系统中只能硬编码到应用程序中；DBMS 则通过 `CHECK` 约束集中定义和维护

原子性更新问题（Atomicity of Updates）
: 文件系统中一次更新可能只完成部分就中断（如转账只扣款未入账）；DBMS 通过**事务（transaction）** 保证操作的原子性

并发访问异常（Concurrent Access Anomalies）
: 多用户同时读写同一文件可能出现丢失更新等冲突；DBMS 通过锁机制和事务隔离等级加以控制

安全性问题（Security Problems）
: 文件系统仅提供文件级访问控制，无法对记录甚至字段级别进行精细授权；DBMS 支持细粒度的访问控制策略

<figure markdown="span">
  ![DBMS 与文件系统对比](https://webp-pic.yokumi.cn/2025/09/20250908162649298.png){ loading=lazy width="70%" }
</figure>

!!! abstract "DBMS vs 文件系统"
    DBMS 作为**集中式数据管理**系统，应用程序通过抽象接口（如 SQL）访问数据，不再直接操作文件；由此实现**数据独立性**——物理存储变化不影响上层应用。

## 数据库系统发展简史

| 时期 | 特征 | 代表性事件 |
|------|------|------------|
| 1950s | 磁带存储，顺序访问 | 批处理为主 |
| 1960s-70s | 硬磁盘出现，随机访问 | IMS 1968、CODASYL 1971、Codd 1970 提出关系模型、System R / Ingres |
| 1980s | 商业化关系数据库 | SQL 标准确立、Oracle / DB2 等商用产品成熟 |
| 1990s | 数据挖掘与 Web | 决策支持系统、OLAP、Web 数据库 |
| 2000s | XML 数据管理、NoSQL | BigTable / HBase、MongoDB、Redis 等 |
| 2010s | SQL 回归、云数据库、AI+DB | NewSQL、云原生 DB、自动化调优 |

???+ info "关键里程碑"
    - **IMS**（1968）：IBM 的层次模型数据库系统
    - **IDMS**：网状模型数据库
    - **CODASYL**（1971）：网状模型标准化委员会
    - **Codd**（1970）：提出关系模型，奠定关系数据库理论基础
    - **NoSQL**（2000s）：应对大数据场景的非关系型数据库运动

## 三级模式架构

数据库系统采用三级模式架构，实现数据的抽象与独立性：

<figure markdown="span">
  ![三级模式架构](https://webp-pic.yokumi.cn/2025/09/20250908174622882.png){ loading=lazy width="70%" }
</figure>

### 物理级（Internal Schema）

物理模式 / 内模式（Physical Schema / Internal Schema）
: 描述数据的**物理存储方式**，包括文件组织、索引结构、存储分配等

???+ info "物理数据独立性"
    物理级到逻辑级的映射（物理/逻辑映射）使得物理存储的改变（如更换索引结构）不影响逻辑模式——即**物理数据独立性**。

### 逻辑级（Conceptual Schema）

逻辑模式 / 概念模式（Conceptual Schema / Logical Schema）
: 描述数据库的**整体逻辑结构**，包括所有实体、属性、关系和约束

???+ info "逻辑数据独立性"
    逻辑级到视图级的映射（视图/逻辑映射）使得逻辑模式的改变（如新增字段）不影响已有视图——即**逻辑数据独立性**。

### 视图级（External Schema）

外模式 / 视图模式（External Schema / View Schema）
: 为不同用户/应用定制的**局部数据视图**，隐藏无关数据，简化访问

!!! abstract "三级架构的核心价值"
    三级模式架构通过两级映射实现数据独立性：**物理数据独立性**保护应用不受存储变化影响，**逻辑数据独立性**保护视图不受逻辑结构变化影响。这使得数据库系统成为应用与数据之间的稳定抽象层。

## DBMS 系统结构

<figure markdown="span">
  ![DBMS 系统结构](https://webp-pic.yokumi.cn/2025/09/20250915130945083.png){ loading=lazy width="70%" }
</figure>

DBMS 的功能模块可分为两大类：

查询处理器（Query Processor）
: 负责接收、解析、优化和执行用户查询，包含 DDL 编译器、DML 编译器、查询优化器等

存储管理器（Storage Manager）
: 负责数据的物理存储与检索，向上层提供抽象接口

存储层包含以下关键组件：

数据文件（Data Files）
: 存储数据库的实际数据记录

索引文件（Indices）
: 提供快速查找数据记录的辅助结构

数据字典（Data Dictionary / Metadata）
: 存储数据库的**元数据**——模式定义、约束、用户权限等

统计数据（Statistical Data）
: 记录数据分布和访问频率等信息，供查询优化器使用

## 数据模型

数据模型
: 描述数据结构、数据操作和约束规则的**抽象框架**

    三个组成要素：

    - **数据结构**：数据的组织方式（层次、网状、关系等）
    - **数据操作**：对数据的检索与更新操作
    - **约束规则**：数据必须满足的完整性约束

### 基于对象的模型

实体-联系模型（E-R Model）
: 用实体、属性和联系描述现实世界的语义结构，主要用于数据库概念设计

面向对象模型（OO Model）
: 将数据封装为对象，支持继承、多态等面向对象特性

### 基于记录的模型

层次模型（Hierarchical Model）
: 用树形结构组织数据，父子关系唯一（如 IMS）

网状模型（Network Model）
: 用网状结构组织数据，允许多个父节点（如 CODASYL）

关系模型（Relational Model）
: 用二维表组织数据，基于严格的数学理论；是目前最主流的数据模型

!!! tip "数据模型演进"
    层次和网状模型是早期主流，关系模型自 1970 年 Codd 提出后逐渐取代它们，成为现代数据库的基石。面向对象和 E-R 模型主要用于设计和建模阶段。

## 数据库语言

DDL（Data Definition Language）
: 定义和修改数据库模式，包括创建/删除表、定义约束等。DDL 语句的执行结果存入数据字典

DML（Data Manipulation Language）
: 对数据库中的数据进行操作，包括查询（query）和更新（insert / delete / update）

!!! abstract "SQL 统一了 DDL 与 DML"
    现代关系数据库使用 SQL 同时涵盖 DDL 和 DML 功能，不再严格区分两者。

## 数据库用户

最终用户（End Users）
: 通过应用程序或查询界面使用数据库的普通用户

应用程序员（Application Programmers）
: 开发数据库应用程序的软件工程师，使用 DML 嵌入式调用或 API 访问数据

数据库管理员（DBA）
: 负责数据库的总体管理：模式定义、存储结构规划、权限控制、性能调优、备份恢复

DBMS 设计者（DBMS Designers）
: 负责设计和实现 DBMS 软件本身的系统工程师

## 应用体系结构

<figure markdown="span">
  ![应用体系结构](https://webp-pic.yokumi.cn/2025/09/20250915133237318.png){ loading=lazy width="70%" }
</figure>

二层 C/S 结构（2-Tier Client/Server）
: 客户端直接连接数据库服务器，客户端承担部分业务逻辑

三层 C/S 结构（3-Tier Client/Server）
: 客户端 → 应用服务器（中间层，承载业务逻辑） → 数据库服务器；分层更清晰，安全性和可维护性更好

B/S 结构（Browser/Server）
: 三层架构的 Web 化形式：浏览器 → Web 服务器 → 数据库服务器；客户端无需安装专用软件

???+ info "架构演进趋势"
    从二层到三层再到 B/S，核心趋势是将业务逻辑从客户端剥离到中间层，实现**瘦客户端**和**集中管理**。现代微服务架构进一步将中间层拆分为多个独立服务。
