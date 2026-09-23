# 图论

## 图论基本概念

### 图的定义

图 (Graph)
: 具有顶点集 $V$ 的图亦称为 $V$ 上的图 (a graph on $V$)，图 $G$ 的顶点集记为 $V(G)$，边集记为 $E(G)$

邻接 (Adjacency)
: 如果 $\{x, y\}$ 是 $G$ 的一条边，则称两个顶点 $x$ 和 $y$ 是相邻的 (adjacent) 或邻点 (neighbour)，$x, y$ 称为边的端点 (endpoint)；如果两条边 $e \ne f$ 有一个公共端点，则称 $e$ 和 $f$ 是相邻的

邻域 / 邻点集 (Neighborhood)
: 顶点 $v$ 的所有邻点构成的集合，记为 $N(v)$。若 $A$ 是 $V$ 的子集，则 $N(A) = \bigcup_{\nu \in A} N(\nu)$，即 $A$ 中所有顶点的邻点之并

度 (Degree)
: 顶点 $v$ 的邻点数目即为度，记为 $\deg(v)$。度为 $0$ 的顶点称为孤立点 (isolated)；度为 $1$ 的顶点称为悬挂点 (pendant)

!!! abstract "握手定理 (Handshaking Theorem)"

    $$\sum_{v \in V} \deg(v) = 2|E|$$

    无向图中，如果有度为奇数的点，那么这些点的个数必为偶数个。

<figure markdown="span">
  ![握手定理](https://webp-pic.yokumi.cn/2026/01/20260101155319290.png){ loading=lazy width="70%" }
</figure>

### 有向图的度

入度 (In-degree)
: 顶点 $v$ 的入度 $\deg^-(v)$ 是指向 $v$ 的边数

出度 (Out-degree)
: 顶点 $v$ 的出度 $\deg^+(v)$ 是从 $v$ 出发的边数

度 (Degree)
: $\deg(v) = \deg^-(v) + \deg^+(v)$

!!! abstract "有向图握手定理"

    $$\sum_{v \in V} \deg^-(v) = \sum_{v \in V} \deg^+(v) = |E|$$

<figure markdown="span">
  ![有向图握手定理](https://webp-pic.yokumi.cn/2026/01/20260101155322664.png){ loading=lazy width="70%" }
</figure>

### 子图与图的运算

阶 (Order)
: 一个图的顶点个数称为它的阶，记为 $|G|$；边数记为 $\|G\|$

平凡图 (Trivial graph)
: 阶为 $0$ 或 $1$ 的图

生成子图 (Spanning subgraph)
: 删边不删点

导出子图 (Induced subgraph)
: 若 $G' \subseteq G$ 且 $G'$ 包含了 $E$ 中所有满足 $x, y \in V'$ 的边 $xy$，则称 $G'$ 是 $G$ 的导出子图（删点不删边）

图的收缩 (Contraction)
: 将一条边的两个端点合并为一个顶点，并删除该边

<figure markdown="span">
  ![图的收缩](https://webp-pic.yokumi.cn/2026/01/20260101155310258.png){ loading=lazy width="70%" }
</figure>

补图 (Graph complement)
: 相对于完全图的补

<figure markdown="span">
  ![补图](https://webp-pic.yokumi.cn/2026/01/20260101155313070.png){ loading=lazy width="70%" }
</figure>

关联矩阵 (Incidence matrices)
: 第 $i$ 行表示第 $i$ 个顶点与哪些边连接，第 $j$ 列表示第 $j$ 条边连接哪些顶点

<figure markdown="span">
  ![关联矩阵](https://webp-pic.yokumi.cn/2026/01/20260101155316020.png){ loading=lazy width="70%" }
</figure>

### 独立性

独立 (Independent)
: 互不相邻的顶点/边称独立顶点/独立边

独立集 (Independent set)
: 顶点集或边集中没有两个元素是相邻的

稳定集 (Stable set)
: 独立的顶点集也称作稳定集

### 特殊图结构

完全图 $K_n$
: 所有顶点两两相邻的图，$n$ 个顶点的完全图记为 $K_n$

<figure markdown="span">
  ![完全图](https://webp-pic.yokumi.cn/2026/01/20260101155331444.png){ loading=lazy width="70%" }
</figure>

环图 $C_n$
: 顶点依次相连形成闭合环路的图

<figure markdown="span">
  ![环图](https://webp-pic.yokumi.cn/2026/01/20260101155340226.png){ loading=lazy width="70%" }
</figure>

轮图 $W_n$
: 在环图 $C_n$ 的基础上增加一个中心顶点与所有环上顶点相连。$W_n$ 有 $n+1$ 个顶点，中心点度为 $n-1$，边上 $n$ 个点度为 $3$

<figure markdown="span">
  ![轮图](https://webp-pic.yokumi.cn/2026/01/20260101155343047.png){ loading=lazy width="70%" }
</figure>

n 维体图 / 超立方体 $Q_n$
: $n$ 维超立方体图，顶点对应 $n$ 位二进制串，相邻顶点仅差一位

<figure markdown="span">
  ![超立方体图](https://webp-pic.yokumi.cn/2026/01/20260101155352937.png){ loading=lazy width="70%" }
</figure>

柏拉图图 (Plato graphs)
: 对应五种柏拉图体的图结构

<figure markdown="span">
  ![柏拉图图](https://webp-pic.yokumi.cn/2026/01/20260101155359965.png){ loading=lazy width="70%" }
</figure>

彼德森图 (Petersen graph)
: 经典的 10 顶点 15 边图，常用作反例

<figure markdown="span">
  ![彼德森图](https://webp-pic.yokumi.cn/2026/01/20260101155403581.png){ loading=lazy width="70%" }
</figure>

二分图 (Bipartite Graph)
: 顶点集可划分为两个不相交的子集，使得每条边的两端点分别属于不同子集

    判定方法：

    - 可以用两种颜色染色
    - 图中不存在长度为奇数的回路

<figure markdown="span">
  ![二分图](https://webp-pic.yokumi.cn/2026/01/20260101155409133.png){ loading=lazy width="70%" }
</figure>

完全二分图 $K_{m,n}$
: 二分图中，$V_1$ 的每个顶点与 $V_2$ 的每个顶点都相邻

<figure markdown="span">
  ![完全二分图](https://webp-pic.yokumi.cn/2026/01/20260101155417452.png){ loading=lazy width="70%" }
</figure>

### 图的同构

图的同构 (Graph Isomorphism)
: 若存在双射 $\varphi: V(G) \to V(H)$，使得 $xy \in E(G) \iff \varphi(x)\varphi(y) \in E(H)$，则称 $G$ 与 $H$ 同构

<figure markdown="span">
  ![图的同构](https://webp-pic.yokumi.cn/2026/01/20260101155424413.png){ loading=lazy width="70%" }
</figure>

图不变量 (Graph invariants)
: 对于图上的一个映射，如果对每个同构图它均取相同的值，则称为图不变量。顶点数、边数、两两相邻的最大顶点数等都是图不变量

### 路径与连通性

路 (Path)
: 顶点序列 $x_0, x_1, \dots, x_n$ 中所有 $x_i$ 均互不相同，$x_0$ 和 $x_n$ 由路 $P$ 连接，称为路的端点；$x_1, \dots, x_{n-1}$ 称为内部顶点。路的边数称为路的长度，长度为 $k$ 的路记为 $P^k$

简单路 (Simple path)
: 不包含重复边的路

独立路 (Independent path)
: 若其中任意一条路不包含另一条路的内部顶点，则称它们是独立路

连通图 (Connected graph)
: 非空图 $G$ 中任意两个顶点之间均有一条路相连

连通分支 (Connected component)
: 图 $G$ 的极大连通子图

割点 (Cut vertex)
: 删除该顶点及其所有关联边后，连通分支数增加

割边 (Cut edge)
: 删除该边后，连通分支数增加

点连通度 (Connectivity)
: 使得 $G$ 是 $k$-连通的最大整数 $k$，记为 $\kappa(G)$

边连通度 (Edge connectivity)
: 记为 $\lambda(G)$

<figure markdown="span">
  ![连通度示例](https://webp-pic.yokumi.cn/2026/01/20260101155427620.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![连通度示例2](https://webp-pic.yokumi.cn/2026/01/20260101155434809.png){ loading=lazy width="70%" }
</figure>

!!! note "有向图的连通性"

    - **强连通**：有向图中任意两个顶点 $a, b$ 之间都存在从 $a$ 到 $b$ 和从 $b$ 到 $a$ 的路径
    - **弱连通**：忽略方向后对应的无向图是连通的

### 圈与围长

圈 (Cycle)
: 闭合路径 $x_0 x_1 \dots x_{k-1} x_0$

围长 (Girth)
: 图 $G$ 中最短圈的长度，记为 $g(G)$

周长 (Circumference)
: 图 $G$ 中最长圈的长度

弦 (Chord)
: 不在圈上但连接圈中两个顶点的边

导出圈 (Induced cycle)
: 不含弦的圈，即 $G$ 的导出子图是个圈



## Euler 与 Hamilton 回路

### 欧拉回路

欧拉回路 (Euler tour)
: 通过图的每条边恰好一次的闭途径

欧拉通路 (Euler path)
: 通过图的每条边恰好一次的路径（非闭合）

欧拉图 (Eulerian graph)
: 包含欧拉回路的图

!!! abstract "欧拉回路的充要条件（无向图）"

    - **回路**：连通图是欧拉的，当且仅当它的每个顶点度为偶数
    - **通路**：连通图 $G$ 存在从 $a$ 到 $b$ 的欧拉路径，当且仅当 $G$ 是连通的，且除 $a$ 和 $b$（$a \ne b$）的度为奇数之外，没有其他度为奇数的顶点

!!! abstract "欧拉回路的充要条件（有向图）"

    - **回路**：连通图是欧拉的，当且仅当 $G$ 是连通的，且每个顶点的出度 = 入度
    - **通路**：连通图 $G$ 含有欧拉通路，当且仅当 $G$ 是连通的，且除两个顶点外其余每个顶点入度 = 出度，且此两点满足 $\left|\deg^+(u) - \deg^-(v)\right| = 1$

### 哈密尔顿回路

哈密尔顿回路 (Hamiltonian circuit)
: 遍历 $G$ 中每一个顶点且只遍历一次的回路

哈密尔顿通路 (Hamiltonian path)
: 遍历 $G$ 中每一个顶点且只遍历一次的路径

!!! warning "注意"
    哈密尔顿回路仅有充分条件和必要条件，**没有充要条件**，这与欧拉回路不同。

### 充分条件

!!! abstract "Dirac 定理"

    对于简单连通图 $G$，如果 $G$ 的顶点数 $n \ge 3$，且所有顶点的度都 $\ge \dfrac{n}{2}$，那么 $G$ 存在哈密尔顿回路。

!!! abstract "Ore 定理"

    对于简单连通图 $G$，如果 $G$ 的顶点数 $n \ge 3$，且对于每一对不相邻的顶点 $u, v$，都有 $\deg(u) + \deg(v) \ge n$，那么 $G$ 存在哈密尔顿回路。

???+ note "Dirac vs Ore"
    Dirac 定理是 Ore 定理的特例：若所有顶点的度 $\ge n/2$，则对任意不相邻的 $u, v$，$\deg(u) + \deg(v) \ge n/2 + n/2 = n$，自然满足 Ore 定理的条件。

### 必要条件

!!! abstract "哈密尔顿回路的必要条件"

    设无向图 $G = (V, E)$，非空子集 $V_1 \subset V$，则

    $$p(G - V_1) \le |V_1|$$

    其中 $p(G - V_1)$ 为图 $G$ 删除 $V_1$ 中的节点后的连通分支数。

    此条件可用于判断某图**不是**哈密尔顿图：若删除某顶点子集后连通分支数超过删除的顶点数，则不存在哈密尔顿回路。



## 平面图

### 定义

平面图 (Planar graph)
: 如果一个图能画在平面上使得它的边仅在端点相交，则称这个图为可嵌入平面的，或称为平面图。平面图 $G$ 的这样一种画法称为 $G$ 的一个平面嵌入

面 (Face)
: 一个平图 $G$ 把平面划分成若干个连通区域，这些区域的闭包称为 $G$ 的面

面的次数
: 面边界回路的长度称为面的次数，记为 $\deg(f)$ 或 $d(f)$

外部面 (Outer face)
: 每个平图恰有一个无界的面，称为外部面

### 性质与定理

!!! abstract "面的次数之和与边数关系"

    $$\sum d(f) = 2\varepsilon$$

!!! abstract "Euler 公式"

    若 $G$ 是连通平图，则有：

    $$\nu - \varepsilon + \phi = 2$$

    其中 $\nu$ 为顶点数，$\varepsilon$ 为边数，$\phi$ 为面数。

!!! tip "推论"
    简单平面图一定存在一个度数小于 $5$ 的顶点。

### 平面图的判定

#### 必要条件

!!! abstract "必要条件"

    1. 若 $G$ 是 $v \ge 3$ 的简单平面图，则 $\varepsilon \le 3\nu - 6$
    2. Euler 公式：$\nu - \varepsilon + \phi = 2$

#### Kuratowski 定理

!!! abstract "Kuratowski 定理（库拉托夫斯基定理）"

    一个图是平面图，当且仅当它不包含 $K_{3,3}$ 或 $K_5$ 的剖分图。

剖分图 (Subdivision)
: 把 $G$ 的边进行一系列剖分得到的图。也可理解为：用路径 (Path) 代替边 (Edge)

初等细分 (Elementary subdivision)
: 把边 $(u, v)$ 删除，添加一个点 $w$，再添加两条边 $(u, w)$ 和 $(w, v)$

同胚 (Homeomorphic)
: 经初等细分得到的新图和原图称为是同胚的

???+ note "柏拉图体 (Platonic Solids)"

    柏拉图体是正多面体，共有五种：正四面体、正六面体（立方体）、正八面体、正十二面体、正二十面体。

    顶点数、边数（棱数）、面数的关系：

    其中 $v$ 表示顶点数，$e$ 表示棱数，$f$ 表示面数，$k$ 为每个顶点的出发边数目，$l$ 为每个面上的边数目：

    $$\sum \deg(v) = 2e = fl = kv$$

<figure markdown="span">
  ![柏拉图体1](https://webp-pic.yokumi.cn/2026/01/20260101155359965.png){ loading=lazy width="70%" }
</figure>



## 图着色

### 基本定义

着色数 $\chi(G)$
: 图 $G$ 的着色数 (chromatic number)，即给 $G$ 的顶点染色使得相邻顶点颜色不同所需的最少颜色数

着色类型
: 包括点着色、边着色、面着色三种

色多项式 $P_G(k)$
: 图 $G$ 用 $k$ 种颜色染色的方法数

### 常见图的点着色数

| 图类型 | 着色数 $\chi(G)$ |
| --- | --- |
| 零图（无边只有顶点） | $1$ |
| 完全图 $K_n$ | $n$ |
| 非零二部图 | $2$ |

!!! abstract "着色数上界"

    简单图的点着色数 $\le$ 最大度数 $+ 1$，即 $\chi(G) \le \Delta(G) + 1$

### 非连通图的着色

!!! abstract "非连通图的色多项式"

    如果 $G$ 为非连通图，那么它的色多项式等于它的所有连通分量的色多项式的乘积：

    $$P_G(k) = \prod_{i} P_{G_i}(k)$$

### 商图

商图 (Quotient graph)
: 把图的顶点按照某种等价类规则划分，直观上就是把两个点捏在一起

<figure markdown="span">
  ![商图](https://webp-pic.yokumi.cn/2026/01/20260101155259206.png){ loading=lazy width="70%" }
</figure>

### 构建色多项式

#### 删边法

通过删边得到容易计算色多项图的子图。

<figure markdown="span">
  ![删边法构建色多项式](https://webp-pic.yokumi.cn/2026/01/20260101155301779.png){ loading=lazy width="70%" }
</figure>

#### Welch-Powell 算法（韦尔奇鲍威尔法）

1. 将顶点按照度数递减排序
2. 用第一种颜色对度数最大的顶点以及和该点不相邻的所有顶点进行染色
3. 对剩余顶点重复上述步骤

#### 递推法

<figure markdown="span">
  ![递推法构建色多项式](https://webp-pic.yokumi.cn/2026/01/20260101155303820.png){ loading=lazy width="70%" }
</figure>

### 色多项式性质

<figure markdown="span">
  ![色多项式性质](https://webp-pic.yokumi.cn/2026/01/20260101155306586.png){ loading=lazy width="70%" }
</figure>


## 匹配与稳定匹配

### 匹配的定义

匹配 / 对集 (Matching)
: 图的一个边子集，其中任何两条边不相邻（不共享端点）

最大匹配 (Maximum matching)
: 边数最多的匹配

完美匹配 / 完全匹配 (Perfect/Complete matching)
: 所有顶点都包含在匹配中的匹配

<figure markdown="span">
  ![匹配定义](https://webp-pic.yokumi.cn/2026/01/20260101155250010.png){ loading=lazy width="70%" }
</figure>

### Hall 婚姻定理

!!! abstract "Hall 婚姻定理 (Hall's Marriage Theorem)"

    二部图 $G = (X \cup Y, E)$ 中存在将 $X$ 中每个顶点都匹配的匹配，当且仅当对 $X$ 的任意子集 $A$，都有 $|N(A)| \ge |A|$。

<figure markdown="span">
  ![Hall 婚姻定理](https://webp-pic.yokumi.cn/2026/01/20260101155256964.png){ loading=lazy width="70%" }
</figure>

### 稳定匹配问题

!!! abstract "问题描述"

    给出一个 $n$ 个男性的集合 $M$ 和 $n$ 个女性的集合 $W$，找到一个"稳定"匹配。

    - 每位男性根据对女性的心仪程度从高至低进行排名
    - 每位女性根据对男性的心仪程度从高至低进行排名

不稳定对 (Unstable pair)
: 给出一个完美匹配 $S$，男性 $m$ 和女性 $w$ 是不稳定对，如果同时满足：

    - $m$ 相比起当前配偶，更喜欢 $w$
    - $w$ 相比起当前配偶，更喜欢 $m$

稳定匹配 (Stable matching)
: 一个不包含不稳定对的完美匹配

### Gale-Shapley 算法

Gale-Shapley 算法又称延迟决定法，用于求解稳定匹配问题。

<figure markdown="span">
  ![Gale-Shapley 算法流程](https://webp-pic.yokumi.cn/2026/01/20260101160025369.png){ loading=lazy width="70%" }
</figure>

???+ example "Gale-Shapley 算法实现（C++）"

    ```cpp
    #include<iostream>
    using namespace std;
    const int N = 10005;
    int M[N] = {0}, W[N] = {0}; // 第0个元素表示已经配对的男性/女性个数
    int M_pri[N][N] = {0}, W_pri[N][N] = {0}; // 第0个元素记录男生m的寻找进度

    void getPri(int n);
    void G_S(int num);
    void output(int num);
    bool lovemore(int m, int w, int num);

    // 获取心仪程度输入
    void getPri(int n) {
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                cin >> M_pri[i][j]; // 第i位男性对女性心仪程度排名
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                cin >> W_pri[i][j]; // 第i位女性对男性心仪程度排名
    }

    // Gale-Shapley 算法
    void G_S(int num) {
        int m, w;
        while (M[0] != num) { // 男生们还未完成配对
            w = m = 0;
            while (M[++m] != 0); // 找到第一个未配对的男生m
            w = M_pri[m][++M_pri[m][0]]; // m心中排名第一的女生w
            if (W[w]) { // 女生已经在约会
                if (lovemore(m, w, num)) { // w更爱m
                    M[W[w]] = 0; // w甩了当前配对
                    M[m] = w;
                    W[w] = m;
                } else continue;
            } else { // 女生自由状态，成功配对
                M[m] = w;
                M[0]++;
                W[w] = m;
                W[0]++;
            }
        }
    }

    // 判断w是不是更爱m
    bool lovemore(int m, int w, int num) {
        for (int i = 0; i < num; i++) { // 按排名从高到低
            if (W_pri[w][i] == W[w]) return false; // 先找到w当前配对
            if (W_pri[w][i] == m) return true;  // 先找到m，说明更爱m
        }
    }

    void output(int num) {
        for (int i = 1; i <= num; i++)
            cout << "(" << i << ", " << M[i] << ")" << endl;
    }

    void solve() {
        int n;
        cin >> n;
        getPri(n);
        G_S(n);
        output(n);
    }

    int main() {
        solve();
        return 0;
    }
    ```


## 图论题型

### 度序列可简单图化

!!! abstract "可简单图化的充要条件"

    <figure markdown="span">
      ![度序列可简单图化条件](https://webp-pic.yokumi.cn/2026/01/20260101155441793.png){ loading=lazy width="70%" }
    </figure>

???+ example "例题"

    <figure markdown="span">
      ![度序列可简单图化例题](https://webp-pic.yokumi.cn/2026/01/20260101155447470.png){ loading=lazy width="70%" }
    </figure>

    **解法**：每次将度序列按非递增顺序排列，删除度最大的节点，更新其他节点的度，重新排列，继续重复上述过程。有两种不合理的情况：

    1. 某次排序后，最大的度数 $d_1$ 超过了剩余的顶点数
    2. 对最大度数后面的 $d_1$ 个数各减 $1$ 后，出现了负数

???+ example "应用：Frogs' Neighborhood"

    **Description**：未名湖附近共 $N$ 个大小湖泊 $L_1, L_2, \cdots, L_n$（其中包括未名湖），每个湖泊 $L_i$ 里住着一只青蛙 $F_i$（$1 \le i \le N$）。如果湖泊 $L_i$ 和 $L_j$ 之间有水路相连，则青蛙 $F_i$ 和 $F_j$ 互称为邻居。已知每只青蛙的邻居数目 $x_1, x_2, \cdots, x_n$，给出每两个湖泊之间的相连关系。

    **Input**：第一行是测试数据的组数 $T$（$0 \le T \le 20$）。每组数据包括两行，第一行是整数 $N$（$2 < N < 10$），第二行是 $N$ 个整数 $x_1, x_2, \cdots, x_n$（$0 \le x_i \le N$）。

    **Output**：如果不存在可能的相连关系，输出 "NO"；否则输出 "YES"，并用 $N \times N$ 的矩阵表示湖泊间的相邻关系。

    **参考代码（C++）**：

    ```cpp
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    #include <algorithm>
    using namespace std;

    struct node {
        int degree, id; // 顶点的度数和标号
    } v[20];

    int map[20][20];

    bool cmp(node a, node b) {
        return a.degree > b.degree; // 按度数降序排序
    }

    int main() {
        int t, n, flag;
        scanf("%d", &t);
        while (t--) {
            scanf("%d", &n);
            for (int i = 0; i < n; i++) {
                scanf("%d", &v[i].degree);
                v[i].id = i;
            }
            memset(map, 0, sizeof(map));
            flag = 1;
            for (int k = 0; k < n; k++) {
                sort(v + k, v + n, cmp);
                int i = v[k].id;
                int d1 = v[k].degree;
                if (d1 > n - k - 1) { flag = 0; break; }
                for (int r = 1; r <= d1 && flag; r++) {
                    int j = v[k + r].id;
                    if (v[k + r].degree <= 0) { flag = 0; break; }
                    v[k + r].degree--;
                    map[i][j] = map[j][i] = 1;
                }
            }
            if (flag) {
                printf("YES\n");
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        if (j) printf(" ");
                        printf("%d", map[i][j]);
                    }
                    printf("\n");
                }
            } else printf("NO\n");
            if (t) printf("\n");
        }
        return 0;
    }
    ```

### 通过邻接矩阵计算通路数

!!! abstract "Counting Paths by Adjacency Matrices"

    邻接矩阵 $A$ 的 $k$ 次幂 $A^k$ 的第 $(i, j)$ 元素表示从顶点 $i$ 到顶点 $j$ 的长度为 $k$ 的通路数目。

    类似求传递闭包的方法。

<figure markdown="span">
  ![邻接矩阵计算通路数](https://webp-pic.yokumi.cn/2026/01/20260101155450541.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![邻接矩阵通路数示例](https://webp-pic.yokumi.cn/2026/01/20260101155459543.png){ loading=lazy width="70%" }
</figure>
