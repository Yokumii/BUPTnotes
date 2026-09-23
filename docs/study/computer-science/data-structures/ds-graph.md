# 图

## 基本概念

图 (Graph)
: 由顶点集 $V$ 和边集 $E$ 构成的数据结构，记为 $G = (V, E)$。顶点表示数据元素，边表示元素之间的关系

有向图 (Directed graph / Digraph)
: 每条边都有方向，用有序对 $\langle v_i, v_j \rangle$ 表示，从 $v_i$ 指向 $v_j$

无向图 (Undirected graph)
: 边没有方向，用无序对 $(v_i, v_j)$ 表示

完全图 (Complete graph)
: 任意两个顶点之间都存在边的图。无向完全图有 $\dfrac{n(n-1)}{2}$ 条边；有向完全图有 $n(n-1)$ 条边

<figure markdown="span">
  ![图的基本概念——有向图与无向图](https://webp-pic.yokumi.cn/2026/01/20260101154659673.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![图的基本概念——完全图与稀疏图](https://webp-pic.yokumi.cn/2026/01/20260101154704693.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![图的基本概念——连通性相关术语](https://webp-pic.yokumi.cn/2026/01/20260101154708522.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![图的基本概念——权与网](https://webp-pic.yokumi.cn/2026/01/20260101154715309.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![图的基本概念——子图与生成子图](https://webp-pic.yokumi.cn/2026/01/20260101154718123.png){ loading=lazy width="70%" }
</figure>


## 图的基本存储结构

### 邻接矩阵

邻接矩阵 (Adjacency matrix)
: 用一个 $n \times n$ 的矩阵 $A$ 表示图中顶点间的关系：

    - 无向图：$A[i][j] = 1$ 表示顶点 $i$ 与 $j$ 之间有边，$A[i][j] = 0$ 表示无边
    - 有向图：$A[i][j] = 1$ 表示从 $i$ 到 $j$ 有弧
    - 网（带权图）：$A[i][j] = w_{ij}$ 表示边权值，$\infty$ 表示无边

!!! note "邻接矩阵特点"

    - 无向图的邻接矩阵是对称矩阵
    - 无向图中顶点 $i$ 的度 = 第 $i$ 行（或列）元素之和
    - 有向图中顶点 $i$ 的出度 = 第 $i$ 行元素之和，入度 = 第 $i$ 列元素之和
    - 空间复杂度 $O(n^2)$，适合稠密图
    - 判定两顶点是否相邻的时间复杂度为 $O(1)$

<figure markdown="span">
  ![邻接矩阵存储结构示意](https://webp-pic.yokumi.cn/2026/01/20260101154725396.png){ loading=lazy width="70%" }
</figure>

### 邻接表

邻接表 (Adjacency list)
: 为每个顶点建立一个单链表，链表中存放与该顶点相邻的所有顶点信息

!!! note "邻接表特点"

    - 空间复杂度 $O(n + e)$，适合稀疏图
    - 无向图每条边在两个顶点的链表中各出现一次，表结点总数为 $2e$
    - 有向图每条弧只在弧尾顶点的链表中出现一次，表结点总数为 $e$
    - 查找顶点 $i$ 的所有邻接点需遍历第 $i$ 个链表，时间复杂度 $O(\deg(i))$
    - 判定两顶点是否相邻的时间复杂度为 $O(\deg(i))$

<figure markdown="span">
  ![邻接表存储结构示意](https://webp-pic.yokumi.cn/2026/01/20260101154735056.png){ loading=lazy width="70%" }
</figure>


## 最小生成树

生成树 (Spanning tree)
: 连通图 $G$ 的极小连通子图，包含 $G$ 中所有 $n$ 个顶点，但仅含 $n - 1$ 条边

最小生成树 (Minimum spanning tree, MST)
: 在带权连通图中，所有生成树中边的权值之和最小的那棵

!!! abstract "MST 性质"

    - MST 的边数 = 顶点数 - 1
    - 若图中各边权值互不相等，则 MST 唯一
    - MST 不一定唯一，但权值之和一定相同

???+ note "Prim 算法"

    从某个顶点出发，逐步将距离当前生成树最近的顶点加入，直至包含所有顶点。

    - 时间复杂度：$O(n^2)$，适合稠密图
    - 空间复杂度：$O(n)$

???+ note "Kruskal 算法"

    将所有边按权值从小到大排序，依次选取不与已选边构成回路的边加入生成树，直至选够 $n - 1$ 条边。

    - 时间复杂度：$O(e \log e)$，适合稀疏图
    - 空间复杂度：$O(e)$

<figure markdown="span">
  ![最小生成树算法示意](https://webp-pic.yokumi.cn/2026/01/20260101154741249.png){ loading=lazy width="70%" }
</figure>


## 拓扑排序

拓扑排序 (Topological sorting)
: 对有向无环图 (DAG) 的所有顶点排成一个线性序列，使得对于图中每条弧 $\langle v_i, v_j \rangle$，$v_i$ 在序列中排在 $v_j$ 的前面

!!! note "拓扑排序前提"

    - 图必须是有向图
    - 图中不能有回路（即必须是 DAG）
    - 若图中存在回路，则不存在拓扑排序

### 无前驱的顶点优先算法

!!! abstract "算法步骤"

    1. 从图中选择一个没有前驱（入度为 0）的顶点并输出
    2. 删除该顶点及其所有出边
    3. 重复步骤 1 和 2，直到全部顶点已输出或剩余顶点中没有入度为 0 的顶点（后者说明图中存在回路）

<figure markdown="span">
  ![无前驱的顶点优先拓扑排序算法示意](https://webp-pic.yokumi.cn/2026/01/20260101154747595.png){ loading=lazy width="70%" }
</figure>

### 无后继的顶点优先算法

!!! abstract "算法步骤"

    1. 从图中选择一个没有后继（出度为 0）的顶点并输出
    2. 删除该顶点及其所有入边
    3. 重复步骤 1 和 2，直到全部顶点已输出或剩余顶点中没有出度为 0 的顶点（后者说明图中存在回路）

!!! warning "注意"

    无后继优先算法输出的拓扑序列是**逆序**的，即先输出的顶点在拓扑序列中排在最后。

<figure markdown="span">
  ![无后继的顶点优先拓扑排序算法示意](https://webp-pic.yokumi.cn/2026/01/20260101154750269.png){ loading=lazy width="70%" }
</figure>


## 关键路径

### AOE 网

AOE 网 (Activity On Edge network)
: 用顶点表示事件，用边表示活动的带权有向图，边上的权值表示活动的持续时间

!!! note "AOE 网特点"

    - 只有一个源点（入度为 0，表示工程开始）和一个汇点（出度为 0，表示工程结束）
    - 源点到汇点的最长路径即为关键路径
    - 关键路径上的所有活动都是关键活动，缩短关键活动可以缩短工期

<figure markdown="span">
  ![AOE网示例——顶点表示事件、边表示活动](https://webp-pic.yokumi.cn/2026/01/20260101154800230.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![AOE网示例——关键路径标识](https://webp-pic.yokumi.cn/2026/01/20260101154803528.png){ loading=lazy width="70%" }
</figure>

### 关键术语

事件最早发生时间 $ve(v)$
: 从源点到事件 $v$ 的最长路径长度，决定了以 $v$ 为弧尾的所有活动的最早开始时间

事件最迟发生时间 $vl(v)$
: 在不推迟整个工程完成的前提下，事件 $v$ 最迟必须发生的时间

活动最早开始时间 $e(a_i)$
: 等于活动 $a_i$ 的弧尾事件（起始事件）的最早发生时间：$e(a_i) = ve(\text{弧尾})$

活动最迟开始时间 $l(a_i)$
: 等于活动 $a_i$ 的弧头事件（终止事件）的最迟发生时间减去活动持续时间：$l(a_i) = vl(\text{弧头}) - \text{duration}(a_i)$

关键活动
: 满足 $l(a_i) - e(a_i) = 0$ 的活动，即时间余量为零、没有任何拖延余地

<figure markdown="span">
  ![关键路径关键术语定义](https://webp-pic.yokumi.cn/2026/01/20260101154807518.png){ loading=lazy width="70%" }
</figure>

### 求解方法

关键路径即源点到汇点最长的路径。求解步骤如下：

!!! abstract "步骤 1：计算事件最早发生时间 $ve$"

    从源点开始，沿正向拓扑序列依次计算：

    $$ve(\text{源点}) = 0$$

    $$ve(v_j) = \max\{ve(v_i) + \text{weight}(\langle v_i, v_j \rangle) \mid \langle v_i, v_j \rangle \in E\}$$

    即取所有到达 $v_j$ 的路径中权值之和的最大值。

!!! abstract "步骤 2：计算事件最迟发生时间 $vl$"

    从汇点开始，沿逆向拓扑序列依次计算：

    $$vl(\text{汇点}) = ve(\text{汇点})$$

    $$vl(v_i) = \min\{vl(v_j) - \text{weight}(\langle v_i, v_j \rangle) \mid \langle v_i, v_j \rangle \in E\}$$

    即保证后继事件能最早发生，所以取最小差值。

!!! abstract "步骤 3：计算活动最早/最迟开始时间"

    对每条边（活动）$a_k = \langle v_i, v_j \rangle$：

    $$e(a_k) = ve(v_i)$$

    $$l(a_k) = vl(v_j) - \text{weight}(a_k)$$

!!! abstract "步骤 4：确定关键路径"

    关键路径由所有满足 $l(a_k) - e(a_k) = 0$ 的活动（边）组成，即时间余量为零的边构成的路径。

???+ tip "要点"

    - 关键路径可能不止一条
    - 只有缩短所有关键路径上的关键活动，才能缩短整个工期
    - 缩短某个关键活动后，关键路径可能发生变化

