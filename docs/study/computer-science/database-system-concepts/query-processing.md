# 查询处理

## 查询处理的基本步骤

!!! abstract "查询处理的三个阶段"
    查询处理分为以下步骤：

    1. **解析与翻译**（Parsing & Translation）：将 SQL 语句转换为内部表示（如关系代数表达式）
    2. **优化**（Optimization）：选择代价最小的执行计划
    3. **执行**（Evaluation）：按照优化后的计划执行查询

<figure markdown="span">
  ![查询处理步骤](https://webp-pic.yokumi.cn/2025/12/20251201142549755.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![查询处理示意图](https://webp-pic.yokumi.cn/2025/12/20251201142617752.png){ loading=lazy width="70%" }
</figure>

## 查询代价估计

!!! abstract "代价度量"
    查询代价主要以**磁盘 I/O**来衡量。代价公式：

    $\text{Cost} = b \cdot t_T + k \cdot t_S$

    其中：

    - $b$：传输的数据块数（block transfers）
    - $t_T$：每块传输时间
    - $k$：磁盘寻道次数（seeks）
    - $t_S$：每次寻道时间

## 选择操作

### 线性搜索

线性搜索（Linear Search）
: 扫描整个文件的所有块。代价：$b_r \cdot t_T + t_S$

    - 若搜索键为候选键上的等值查询，期望代价：$(b_r/2) \cdot t_T + t_S$

### 二分搜索

二分搜索（Binary Search）
: 要求文件按搜索键有序且连续存储。每次比较代价：$\log_2(b_r) \cdot (t_T + t_S)$

### 索引扫描

!!! abstract "不同索引类型的选择代价"
    以下 $h_i$ 表示索引的层数（高度），$n$ 为满足条件的记录数，$b$ 为这些记录所在的块数。

主索引，候选键，等值查询
: $(h_i + 1) \cdot (t_T + t_S)$ — 索引遍历 + 一块数据

主索引，非候选键，等值查询
: $h_i \cdot (t_T + t_S) + t_S + b \cdot t_T$ — 索引遍历 + 寻道 + 多块数据

辅索引，候选键，等值查询
: $(h_i + 1) \cdot (t_T + t_S)$ — 索引遍历 + 一块数据

辅索引，非候选键，等值查询
: $(h_i + n) \cdot (t_T + t_S)$ — 最坏情况，每条记录在不同块中

