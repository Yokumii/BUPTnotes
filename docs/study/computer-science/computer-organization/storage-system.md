# 存储系统

## 存储器概述

### 存储器的分类

存储器可从多个维度分类：

按介质
: 半导体存储器、磁介质存储器、光存储器

按与 CPU 的耦合程度
: 内存（主存 + Cache）、外存

按读写功能
: 读写存储器 RWM、只读存储器 ROM

按掉电后信息是否保持
: 易失性、非易失性

按数据存取的随机性
: 随机存取 RAM（给定地址即可拿到数据，与前一个访问地址无关）、顺序存取 SAM（如磁带）、直接存取 DAM（确定区域后顺序存取）

习惯分类
: RAM vs. ROM；SRAM vs. DRAM（内存条）vs. 闪存

### 存储器的目标

存储器设计追求**大容量、高速度、低价格**，三者互相矛盾，因此采用层次结构来兼顾。

<figure markdown="span">
  ![存储器层次结构](https://webp-pic.yokumi.cn/2026/01/20260101165207592.png){ loading=lazy width="70%" }
</figure>

### 并行技术

- **单体多字**：一个读写体，每次存取多个字
- **多体单字**：多个读写体，交叉编址，向多个地址读取内容

### 存储容量与存取速度

存储容量
: 存储字数（存储单元数） $\times$ 存储字长（每单元的比特数）

访问时间 / 存取时间 $T_A$
: 从启动一次存储器操作到该操作完成所经历的时间，即从存储器接收到读/写命令到信息被读出或写入完成所需的时间

存取周期 $T_m$
: 存储器在连续读写过程中，完成一次完整的读/写操作所需的全部时间，即 CPU 连续两次独立访问存储器的最小时间间隔

???+ note "存取周期 vs. 存取时间"
    存取周期 $T_m$ 一般大于存取时间 $T_A$，因为存储器完成读/写操作后一般需要一段恢复内部状态的复原时间：

    $$T_m = T_A + \text{恢复时间}$$

存储器带宽
: 单位时间内能传输的信息量

## SRAM 存储器

### 基本结构

SRAM 的存储元使用**六晶体管 MOS** 来记忆信息，静态是指即使信息被读出后，它仍保持其原状态而**不需要再生（非破坏性读出）**。

<figure markdown="span">
  ![SRAM 基本结构1](https://webp-pic.yokumi.cn/2026/01/20260101165215121.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![SRAM 基本结构2](https://webp-pic.yokumi.cn/2026/01/20260101165219490.png){ loading=lazy width="70%" }
</figure>

### 基本时序

#### 读周期

<figure markdown="span">
  ![SRAM 读周期时序](https://webp-pic.yokumi.cn/2026/01/20260101165225529.png){ loading=lazy width="70%" }
</figure>

#### 写周期

<figure markdown="span">
  ![SRAM 写周期时序](https://webp-pic.yokumi.cn/2026/01/20260101165228414.png){ loading=lazy width="70%" }
</figure>

## DRAM 存储器

### 概述

DRAM 靠 **MOS 管中栅极电容**是否存储电荷来表示 0 和 1。其需要的 MOS 管和 SRAM 相比更少，所以体积更小，集成度更高，但是由于存在漏电，需要周期性对电容进行充电，防止内容丢失，我们称该过程为**动态刷新**。

<figure markdown="span">
  ![DRAM 写操作](https://webp-pic.yokumi.cn/2026/01/20260101165232536.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![DRAM 读操作（含刷新）](https://webp-pic.yokumi.cn/2026/01/20260101165234926.png){ loading=lazy width="70%" }
</figure>

???+ warning "DRAM 的破坏性读出"
    DRAM 的读操作相当于对原来充满电的电容进行放电或对原来没电的电容进行充电，所以对原数据具有**破坏性**。在读出后还需要进行**刷新**，将数据**回写**，以恢复原信息。

    笔记本电脑的浅睡眠模式下，数据没有被存入硬盘，所以需要不断刷新 DRAM，此时的耗电量就主要来自对 DRAM 的刷新。

### SRAM vs. DRAM 对比

| **对比项**   | **SRAM**        | **DRAM**           |
| --------- | --------------- | ------------------ |
| **速度**    | **快**（10ns 级）   | 慢（几十 ns）           |
| **集成度**   | 低               | **高（适合大容量）**       |
| **功耗**    | 高（持续维持状态）       | 低（尽管需刷新，但每位电路简单）   |
| **成本**    | 高               | 低                  |
| **送地址**   | 行列地址同时送         | **行列地址分两次送（分时复用）** |
| **破坏性读出** | 非破坏性（静态）        | 破坏性（动态）            |
| **刷新机制**  | 无需刷新            | 需要定期**刷新**         |
| **结构复杂度** | 使用 6 个晶体管       | 使用 1 个晶体管 + 1 个电容  |
| **用途**    | 高速缓存（Cache）、寄存器 | 主存（RAM）、显存等        |

<figure markdown="span">
  ![SRAM vs DRAM](https://webp-pic.yokumi.cn/2026/01/20260101165239383.png){ loading=lazy width="70%" }
</figure>

### DRAM 芯片的逻辑结构

<figure markdown="span">
  ![DRAM 芯片逻辑结构](https://webp-pic.yokumi.cn/2026/01/20260101165246063.png){ loading=lazy width="70%" }
</figure>

???+ note "DRAM 地址线分时复用"
    DRAM 是**按行刷新**。地址线只有 20 条，行地址和列地址分别先后通过地址线送入地址锁存器，实现地址线的分时复用。RAS（行地址有效信号）先于 CAS（列地址有效信号）有效，即**先送入行地址，再送入列地址**。

#### 读时序

<figure markdown="span">
  ![DRAM 读时序1](https://webp-pic.yokumi.cn/2026/01/20260101165248355.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![DRAM 读时序2](https://webp-pic.yokumi.cn/2026/01/20260101165253187.png){ loading=lazy width="70%" }
</figure>

重要参数：

- $t_{RAC}$：从 RAS 信号有效到有效数据开始读出的时间间隔，也称**读访问时间**
- $t_{CAC}$：从 CAS 信号有效到有效数据开始读出的时间间隔
- $t_{RC}$：连续两个 RAS 下降沿之间的最短间隔，即**读周期时间**
- $t_{PC}$：连续两个 CAS 下降沿之间的最短间隔，即**页模式下的读或写周期**

#### 写时序

<figure markdown="span">
  ![DRAM 写时序1](https://webp-pic.yokumi.cn/2026/01/20260101165257475.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![DRAM 写时序2](https://webp-pic.yokumi.cn/2026/01/20260101165304737.png){ loading=lazy width="70%" }
</figure>

### DRAM 的刷新

集中式刷新
: 在整个刷新间隔内，前一段时间进行读/写周期，需要进行刷新操作时，暂停读/写周期，逐行刷新整个存储器。但在刷新时间内，处理器无法访问存储器。

分散式刷新
: 每一行的刷新操作被均分分配到刷新周期内，通过以下 2 种方式进行刷新操作：

    1. 用 RAS 启动刷新操作，但需要外部刷新地址计数器
    2. 用先送 CAS、再送 RAS 表示启动刷新操作，DRAM 内部有自动递增的刷新地址计数器

???+ example "分散式刷新的典型计算"
    某 DRAM 有 1024 行，若刷新周期为 8 ms，则必须在 8 ms 内把所有 1024 行刷新一遍，即每隔 $8\text{ms} \div 1024 = 7.8\mu\text{s}$ 刷新一行。

### DRAM 控制器

<figure markdown="span">
  ![DRAM 控制器结构](https://webp-pic.yokumi.cn/2026/01/20260101165311586.png){ loading=lazy width="70%" }
</figure>

DRAM 控制器包含以下组件：

- **地址多路开关**：分时送出行、列或刷新地址
- **定时发生器**：提供 RAS、CAS 和写信号 WR
- **仲裁电路**：裁定 CPU 的访问请求和刷新定时器的刷新请求，优先进行刷新
- **刷新定时器**：定时提供刷新请求

### 存储器芯片性能改进

DRAM 性能改进主要通过以下思路：

- 允许重复存取行缓冲区而无需增加另外的行存取时间：**快页模式 FPM**、**扩展数据输出 EDO**、**增强型 DRAM / CDRAM**
- 增加时钟信号，使存储器与处理器保持同步：**同步 DRAM（SDRAM）**

#### 快页模式 DRAM（FPM）

<figure markdown="span">
  ![快页模式 DRAM](https://webp-pic.yokumi.cn/2026/01/20260101165317998.png){ loading=lazy width="70%" }
</figure>

快页模式 DRAM 能从同一行连续访问读取后续数据。

#### 增强型 DRAM / CDRAM

通过在 DRAM 中增加一个小容量的 SRAM，暂时保存最近访问一行的数据。通过比较器判别下次访问是否还是该行，如果是则直接从 SRAM 中读出，无需再次访问 DRAM。且刷新该行和读 SRAM 可并行，即刷新和访问不冲突。

???+ note "突发模式（Burst Mode）"
    连续变动列地址，会使 SRAM 中相应位组连续读出，被称为**突发模式（Burst Mode）**。

#### 同步 DRAM（SDRAM）

<figure markdown="span">
  ![SDRAM 概述1](https://webp-pic.yokumi.cn/2026/01/20260101165323639.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![SDRAM 概述2](https://webp-pic.yokumi.cn/2026/01/20260101165330487.png){ loading=lazy width="70%" }
</figure>

##### 内存模块的封装

- **DIMM（Dual In-line Memory Module，双边接触内存模块）**：通过字扩展和位扩展的方式增加容量

<figure markdown="span">
  ![DDR3 内存模块](https://webp-pic.yokumi.cn/2026/01/20260101165343291.png){ loading=lazy width="70%" }
</figure>

???+ example "DDR3 内存参数计算"
    以 DDR3-1600 为例：

    - 后缀 1600 表示数据总线传输速率为 $1600\text{MT/s}$（Mega Transfers per second）
    - DDR3 在每个时钟周期内传输 2 次数据，所以对应的时钟频率是 $800\text{MHz}$
    - DDR3 每个时钟周期预取 8 字节，对应的存储器核心频率为 $1600\text{MT/s} \div 8 = 200\text{MHz}$
    - DDR3 对应的数据总线宽度为 64 位（8 字节），由此可计算内存带宽

### DRAM 主存读/写正确性校验

实际场景中（尤其是服务器），为提高数据读写的正确性与可靠性，引入附加位作为纠错码。

## 只读存储器和闪存

### 特点

- 只能读出，不能写入
- 不易失
- 只读存储器写入数据的过程称为对其**编程**

### 分类

掩模式只读存储器 MASK ROM
: 不能进行重写

一次可编程只读存储器 PROM
: 双极型 PROM 包括熔丝烧断型和 PN 结击穿型

多次可编程只读存储器
: 包括以下几类：

    - **光擦除 EPROM**：利用雪崩注入，擦除是对**所有**存储单元进行，不能实现选择性擦除
    - **电擦除 EEPROM / E²PROM**
    - **电改写 EAROM**

闪存 Flash Memory
: 分为 NAND 闪存和 NOR 闪存两种类型

    NAND 闪存
    : 只允许顺序**按页（Page）存取**数据

        <figure markdown="span">
          ![NAND 闪存](https://webp-pic.yokumi.cn/2026/01/20260101165354003.png){ loading=lazy width="70%" }
        </figure>

        - 优点：按页写入和读出擦除，写入和擦除速度快
        - 缺点：随机访问困难，无法只写单字节

    NOR 闪存
    : 具有完整地址/数据结构，能快速随机地读取任一单元

        - 优点：随机访问，读出快；能只写单字节
        - 缺点：写入和擦除速度慢

<figure markdown="span">
  ![NAND vs NOR](https://webp-pic.yokumi.cn/2026/01/20260101165408213.png){ loading=lazy width="70%" }
</figure>

???+ important "为什么计算机必须有 ROM？"
    任何计算机必须有经过编程的 ROM（称为 **BIOS**，它保存着计算机最重要的基本输入输出的程序、开机后自检程序和系统自启动程序），用于计算机程序的初始装入。如果都是 RAM，那么计算机初始状态下根本不存在程序和数据。

## 并行存储器

### 双端口存储器 DPRAM

#### 基本结构

<figure markdown="span">
  ![双端口存储器基本结构](https://webp-pic.yokumi.cn/2026/01/20260101165416606.png){ loading=lazy width="70%" }
</figure>

#### 实例：IDT7133

<figure markdown="span">
  ![IDT7133 双端口存储器](https://webp-pic.yokumi.cn/2026/01/20260101165423845.png){ loading=lazy width="70%" }
</figure>

???+ note "Busy Flag 仲裁机制"
    Busy Flag 用于控制能否访问，防止左右端口同时访问同一个地址造成冲突。Busy = 0 表示不能访问。

    <figure markdown="span">
      ![Busy Flag 仲裁方式](https://webp-pic.yokumi.cn/2026/01/20260101165433946.png){ loading=lazy width="70%" }
    </figure>

### 多模块交叉存储器

存储器按模块化组织，多个模块组成的主存储器线性编址，但各模块内的地址安排分为 2 种方式：

#### 顺序方式

<figure markdown="span">
  ![顺序方式编址](https://webp-pic.yokumi.cn/2026/01/20260101165436168.png){ loading=lazy width="70%" }
</figure>

- 地址寄存器高 2 位用于选择模块，低 3 位用于选择模块中的字
- 只能串行访问各模块，带宽受到限制
- 一个模块故障不影响其他模块

#### 交叉方式

<figure markdown="span">
  ![交叉方式编址](https://webp-pic.yokumi.cn/2026/01/20260101165441281.png){ loading=lazy width="70%" }
</figure>

- 与顺序方式的区别是，地址寄存器高 3 位用来选择字，低 2 位用来选择模块
- 连续地址分布在相邻的不同模块内，同一个模块内的地址不连续
- 对连续字的成块传送可以实现多模块流水式并行存取，提升带宽

#### 多模块交叉存储器的特点

<figure markdown="span">
  ![多模块交叉存取时序](https://webp-pic.yokumi.cn/2026/01/20260101165446878.png){ loading=lazy width="70%" }
</figure>

1. 对单独一个模块来说，CPU 访存到读出信息的存取周期为 $T$；但 CPU 可以连续访问多个模块，读写过程几乎重叠，只需要等待**总线传送周期** $\tau$

2. 若模块字长 = 数据总线宽度，存储器的交叉模块数为 $m$，则：

    **交叉存取度**：

    $$m = \frac{T}{\tau}$$

    连续读出 $m$ 个字的用时：

    $$t_1 = T + (m - 1)\tau$$

    而对于顺序方式存储器：

    $$t_2 = mT$$

#### 举例：二模块交叉存储器

<figure markdown="span">
  ![二模块交叉存储器实例](https://webp-pic.yokumi.cn/2026/01/20260101165451023.png){ loading=lazy width="70%" }
</figure>

- 共有 8 个 2 MB 的存储体，地址寄存器高 3 位用于选择存储体
- 1 个存储体由 2 个模块组成，每个容量为 1 MB（$256\text{K} \times 32$ 位），由 8 片 DRAM 芯片组成
- 1 个模块内有 256K 个字，所以用 18 位（分为行列地址各 9 条）选择模块内字地址
- A2 用于模块选择，偶地址在模块 0，奇地址在模块 1
- 低 4 位字节允许，用于确定读 8 位还是 16 位
- 在存储器进行读操作时，读出数据后需要进行回写再生数据。对于单个模块需要等待刷新完成，但对于交叉方式，下一个连续地址可以从另一个模块直接读出，访问和刷新不存在冲突，只需等待总线传输时间

## Cache 存储器

### 局部性原理

程序倾向于一次又一次地访问相同或邻近的数据项集合。

时间局部性
: 被引用过一次的内存位置在不久之后可能被多次引用

空间局部性
: 被引用过一次的内存位置在近期可能引用其附近的位置

### Cache 概述

Cache 是一个小而快的存储器，作为大而慢的存储器的缓冲区域：

- 由高速 **SRAM** 组成
- 利用局部性原理，可以在 Cache 中完成大多数访问
- 全部由**硬件**调度，对用户透明（不可见）

???+ note "Cache 为什么不能用软件来调度？"
    Cache 如果用软件来做，软件本身还涉及从内存中取指和执行，速度更慢了，反而失去了 Cache 的意义。

### 三级存储系统

<figure markdown="span">
  ![三级存储系统1](https://webp-pic.yokumi.cn/2026/01/20260101165504702.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![三级存储系统2](https://webp-pic.yokumi.cn/2026/01/20260101165511484.png){ loading=lazy width="70%" }
</figure>

???+ note "多级 Cache"
    如果 CPU 和主存速度差距较大，常采用多级 Cache 系统，解决主存速度慢的问题。

### Cache 基本工作原理

Cache 命中（Cache Hit）
: 程序直接在 Cache 中找到所需的块

Cache 缺失（Cache Miss）
: 程序在 Cache 中未找到所需的块，Cache 需要从下一层取该块

Cache 缺失分为以下几种类型：

冷启缺失 / 义务缺失 Cold Miss
: Cache 为空，开机时必然存在

冲突缺失 Conflict Miss
: 下层的多个数据块映射到该层 Cache 的同一位置

容量缺失 Capacity Miss
: 活动的 Cache 块数 > Cache 容量

<figure markdown="span">
  ![Cache 工作原理](https://webp-pic.yokumi.cn/2026/01/20260101165515208.png){ loading=lazy width="70%" }
</figure>

???+ info "CAM（内容可寻址存储器）"
    CAM（Content Addressable Memory），即输入一个数据项，硬件将其与所有存储项进行快速匹配，给出数据项的匹配信息（即地址）。同时也支持按地址进行读写操作。

Cache 的控制部件需要实现：

- **地址变换**：主存与 Cache 地址间的映射
- **替换算法**：Cache Miss 时替换 Cache 中的内容
- **更新算法**：保持主存与 Cache 内容的一致性

### 主存和 Cache 的分块

两者的块大小需要相同，但块数显然主存 >> Cache。例如：

<figure markdown="span">
  ![主存和 Cache 分块](https://webp-pic.yokumi.cn/2026/01/20260101165519108.png){ loading=lazy width="70%" }
</figure>

主存地址共 $n$ 位 = 块号（$m$ 位） + 块内地址（$b$ 位）

Cache 地址共 $l$ 位 = 块号（$c$ 位） + 块内地址（$b$ 位）

### Cache 的结构

<figure markdown="span">
  ![Cache 结构](https://webp-pic.yokumi.cn/2026/01/20260101165521949.png){ loading=lazy width="70%" }
</figure>

### 主存与 Cache 的地址映射

#### 全相联映射

主存中的块能装入 Cache 中的任意位置，一个主存中的块和所有 Cache 中的块均构成映射。

<figure markdown="span">
  ![全相联映射](https://webp-pic.yokumi.cn/2026/01/20260101165526514.png){ loading=lazy width="70%" }
</figure>

主存地址格式：

```
+--------------------+--------------------+
|       Tag (高位)   |   Block Offset     |
+--------------------+--------------------+
      ↑                  ↑
  匹配标记区          定位块内字节
```

匹配过程：

1. 从 CPU 中的某地址读出 1 个字
2. 将其拆分为 Tag 和 Block Offset 两部分
3. 将 Tag 与 Cache 中所有块的 Tag **同时**进行比较
4. 命中 → 返回块内偏移字节

!!! abstract "全相联映射的特点"
    - **优点**：冲突概率低，空间利用率高，命中率高
    - **缺点**：逐行比较速度慢；需要 CAM

#### 直接映射

多个主存单元对应一个 Cache 块，一个主存块只能复制到 Cache 的一个特定行上。即 $m$ 行 Cache 的行号 $i$ 和主存的块号 $j$ 有如下函数关系：

$$j \% m = i$$

显然，这种方式容易产生冲突缺失。

主存地址结构分为 3 部分：

```
+-----------+--------------+------------------+
|   Tag     |  Line Index  | Block Offset 偏移 |
+-----------+--------------+------------------+
```

- Block Offset 部分不变，由块大小决定
- Line Index，即行号，如果有 $R$ 位，则分别对应 Cache 块内的 $0 \sim 2^{R} - 1$ 行
- Tag，同样作为标签进行匹配，位数 = 主存地址长度 - 前两者的位数

!!! abstract "直接映射的特点"
    - **优点**：不需要 CAM（一对一映射），简单快速
    - **缺点**：块冲突概率最高，空间利用率最低

#### v 路组相联映射

组相联可以说是前两种的组合。它将 Cache 分为 $u$ 组，每组 $v$ 行，主存块 $j$ 放到哪一组中是固定的，即组号 $q$ 满足 $j \% u = q$；但主存块在组内的具体哪行并不固定，需要根据 Tag 逐个进行匹配（类似全相联映射），不过每组的行数并不多。

主存地址格式：

```
+-----------+--------------+------------------+
|   Tag     |   Set Index  | Block Offset 偏移 |
+-----------+--------------+------------------+
```

计算地址位数时，先得到 Block Offset 的位数，然后根据块大小计算出需要多少块，再根据 Cache 容量计算出 Cache 的总行数。$v$ 路组相联即说明每组有 $v$ 行，由此算出组数，得到 Set Index 的位数，最后得到 Tag 的位数。

匹配过程：

1. 根据 Set Index 选择组
2. 根据 Tag 匹配组内标签（需要 $v$ 个比较器）
3. 命中 → 返回块内偏移字节

!!! abstract "v 路组相联映射的特点"
    - **性能**介于全相联映射和直接映射之间
    - 需要 CAM / $v$ 个比较器

### Cache 块替换策略

随机替换法 RAND
: 随机选择一块替换

先进先出 FIFO
: First-In First-Out，替换最早进入 Cache 的块

最少使用 LFU
: Least Frequently Used，将最近一段时间内访问次数最少的块替换出。需要对每个 Cache 块设定访问计数器。

最久未使用 LRU
: Least Recently Used，将近期内最长时间未被访问过的数据块换出。需要对每个 Cache 块设定计时器，一旦被访问，计时器清 0。

???+ note "符合局部性原理的替换策略"
    前两种（RAND、FIFO）并不符合局部性原理，而后两种（LFU、LRU）满足局部性原理，因此在实际中更常使用。

### Cache 写操作

#### 写命中（Write Hit）

写穿透 Write Through
: 写操作同时更新 Cache 和低一级存储器，保持一致性，但会占用总线带宽

写回 Write Back
: 只写入 Cache，当出现 Cache 缺失需要将该 Cache 块替换出时，才将 Cache 数据写回存储器。需额外维护一个修改标记位（Dirty，脏位）。

#### 写缺失（Write Miss）

写分配 Write-Allocate
: 先加载低一层的块到 Cache 中，然后再更新 Cache

非写分配 Non-Write-Allocate
: 直接写入低一层，不加载到 Cache 中

???+ note "两种典型搭配"
    - **Write-Through + Non-Write-Allocate**：都是往下写，简单易实现，适用于不常写的数据
    - **Write Back + Write-Allocate**：只对当前层进行修改，性能高，适合频繁写操作

### Cache 性能指标

命中率 $h$
: 设 $N_c$ 为在 Cache 中完成存取的总次数，$N_m$ 为在主存中完成存取的总次数：

    $$h = \frac{N_c}{N_c + N_m}$$

平均访问时间 $t_a$
: 设 $t_c$ 为命中 Cache 时的访问时间，$t_m$ 为未命中时在主存中的访问时间：

    $$t_a = ht_c + (1 - h)t_m$$

访问效率 $e$

$$e = \frac{t_c}{t_a} = \frac{t_c}{ht_c + (1-h)t_m} = \frac{1}{h + (1 - h)\frac{t_m}{t_c}}$$

缺失率
: $1 - h$

命中时间 Hit Time
: 从 Cache 传送一个字到 CPU 的时间

## 虚拟存储器

### 概述

进程共享 CPU 和主存资源带来的问题是，程序所需的存储空间随进程的增加将远超过主存空间。为解决这一问题，在主存之上又"抽象"出一层内存空间——虚存，来更好地管理内存空间。

虚拟存储器是一个容量非常大的存储器的逻辑模型，其为用户提供了一个比实际主存空间大得多的程序地址空间，并对用户是透明的（不可见的）。

虚拟存储器被组织为一个存放在**磁盘**上的连续地址单元的数组：

<figure markdown="span">
  ![虚拟存储器概念](https://webp-pic.yokumi.cn/2026/01/20260101165530760.png){ loading=lazy width="70%" }
</figure>

### 主存 - 外存层次

虚拟存储器事实上就是把主存和外存统一为抽象的虚拟内存，与 Cache - 主存层次类似，都需要进行地址变换，将虚拟地址和物理地址进行映射。

???+ note "虚存 vs. Cache"
    - 虚存主要用来解决**存储容量**问题，而 Cache 主要解决的是**存储速度**问题
    - 均利用了程序的局部性原理
    - Cache 管理由**硬件**完成，而虚存的管理由**软件（操作系统）和硬件**共同完成

### 存储管理方式

#### 段式存储管理

利用程序的模块化特性，将一个程序划分为多个段进行存储。需要使用段表进行查询，段表包括段名称、段起点、段长度，以及是否装入内存的标记等。

<figure markdown="span">
  ![段式存储管理](https://webp-pic.yokumi.cn/2026/01/20260101165533197.png){ loading=lazy width="70%" }
</figure>

段式存储管理的地址变换过程：

<figure markdown="span">
  ![段式地址变换](https://webp-pic.yokumi.cn/2026/01/20260101165535525.png){ loading=lazy width="70%" }
</figure>

!!! abstract "段式存储管理的优缺点"
    - **优点**：有利于按段实现信息共享和内存保护
    - **缺点**：容易导致主存中的碎片问题，由于各段长度不等，出现不好用的碎块

#### 页式存储管理

段式存储管理由于段的长度不同会产生碎片问题。页式存储管理通过将虚存和主存空间均分为大小相同的页，以页为单位进行信息交换。

其中，虚拟地址分为虚拟页号 VPN 和页内地址 VPO，物理地址分为物理页号 PPN 和页内地址 PPO，其中页号不同，页内地址一致。

<figure markdown="span">
  ![页式存储管理1](https://webp-pic.yokumi.cn/2026/01/20260101165538390.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![页式存储管理2](https://webp-pic.yokumi.cn/2026/01/20260101165541206.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![页式存储管理3](https://webp-pic.yokumi.cn/2026/01/20260101165546539.png){ loading=lazy width="70%" }
</figure>

!!! abstract "页式存储管理的优缺点"
    - **优点**：页面大小固定，页表简单，调入方便
    - **缺点**：处理、保护、共享不如段式方便

#### TLB 快表

普通的页式存储管理有一定问题：先要访问主存查询页表，然后还要访问一次主存取出页内容，需要 2 次访存。所以引入快表 TLB（Translation Lookaside Buffer），查表时同时访问快表和页表，如果命中快表，则直接根据对应的物理页号取出内容。

<figure markdown="span">
  ![TLB 快表](https://webp-pic.yokumi.cn/2026/01/20260101165553953.png){ loading=lazy width="70%" }
</figure>

##### v 路组相联 TLB 访问

<figure markdown="span">
  ![v 路组相联 TLB](https://webp-pic.yokumi.cn/2026/01/20260101165556190.png){ loading=lazy width="70%" }
</figure>

在页号字段继续划分出页标签 Tag 字段和组索引 Index 字段，和主存 - Cache 中的 v 路组相联类似。

???+ question "为什么"TLB 命中 + 页表缺失"不可能？"
    - TLB 是页表的**缓存**
    - TLB 中的信息**必须来自页表**
    - 如果页表中都没有该项（或页不在内存），TLB 根本不可能提前装到该项

???+ question "为什么"Cache 命中 + 页表缺失"不可能？"
    - Cache 使用的是**物理地址访问**
    - 若页表都还没得到物理地址，**根本没法查 Cache**

#### 多级页表

对于页数很多的情况（e.g. 4 KB 页大小，48 位虚拟地址，每个页表项 8 Bytes 的系统），共有 $2^{48} \div 2^{12} = 2^{36}$ 个页，页表空间 = $2^{39} = 512\text{GB}$，但页表需要放在主存中，显然不可能有这么大的主存，故需要引入多级页表。

##### 二级页表

<figure markdown="span">
  ![二级页表](https://webp-pic.yokumi.cn/2026/01/20260101165558796.png){ loading=lazy width="70%" }
</figure>

- 一级页表：放在主存中，每个页表项指向二级页表
- 二级页表：每个页表项指向一个页。如果二级页表指向的页均未被分配，则无需创建该二级页表，将其对应的一级页表设置为 NULL 即可

##### k 级页表的地址翻译

<figure markdown="span">
  ![k 级页表地址翻译](https://webp-pic.yokumi.cn/2026/01/20260101165604293.png){ loading=lazy width="70%" }
</figure>

#### 页面替换算法

当 CPU 所需的数据或指令不在主存时，即页并未被调入主存中，此时会产生**缺页（Page Fault）**异常（中断），需要通过对应的缺页处理程序从外存（磁盘）调入页面。如果主存的页面已经全部占满，则需要使用算法进行页面替换。

???+ note "缺页 vs. Cache 缺失"
    - 缺页至少涉及一次磁盘的存取，损失比 Cache 未命中大得多
    - 页面替换是由操作系统**软件**实现的

常用的页面替换算法包括：LRU、LFU、FIFO

写回操作：

- 如果页被调入主存后被修改了，则需要重新写入外存，保持主存和外存的数据一致性
- 在页表中设置 1 位**修改位**，用于标识该页是否被修改

#### 段页式虚拟存储器

段页式存储器是段式和页式的结合体：

- 程序先按逻辑进行分段，然后把每段分成固定大小的页
- 操作系统对主存的调入和调出是按页进行的，但又可以按段实现共享和保护
- 需要多次查表（段表 + 页表），开销大

<figure markdown="span">
  ![段页式存储管理](https://webp-pic.yokumi.cn/2026/01/20260101165606758.png){ loading=lazy width="70%" }
</figure>
