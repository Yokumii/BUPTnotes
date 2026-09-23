# 网络层

网络层是处理**端到端(end-to-end)传输**的最底层。

<figure markdown="span">
  ![网络层的位置](https://webp-pic.yokumi.cn/2026/01/20260101170252001.png){ loading=lazy width="70%" }
</figure>

**跳(Hop)**：主机之间通信，经过一个路由器就是一跳。

网络层的主要功能：

1. **网络互联(Internetworking)**：将异构网络实现互联，向上(传输层)提供统一接口
2. **编址(Addressing)**：保证设备接口地址（IP Address）唯一且格式统一
3. **组包(Packeting)**：将上层数据封装为包(Packet)
4. **路由(Routing)**：选路，决定数据包的下一跳，通过路由器(Router)实现
5. **分片(Fragmenting)**：适应不同数据链路层的 MTU，对数据报进行分段

## 网络层提供的服务

网络层向传输层提供服务，要求：

- 路由技术独立：传输层不需知道路由器技术，接口透明统一
- 传输层对路由完全透明
- 传输层获得的网络地址格式统一

分为两种方式：

虚电路(Virtual Circuit)
: Connection-Oriented，面向连接

数据报(Datagram)
: Connectionless，无连接

两者都属于**分组交换(Packet Switching)**，区别如下：

数据报
: 每个包携带目的地的完整地址；路由器通过动态更新的路由表转发；包到达目的地可能乱序（每个包可能走不同路径）

虚电路
: 传输前先建立端到端虚拟电路；传输中数据包携带 **VCI(Virtual Circuit Identifier)** 作为地址标识，比标准地址短得多；所有包沿 VC 路径路由，到达目的地一定按序

## 路由

路由表 = 路由算法 + 路由协议。根据路由算法和路由协议产生、更新路由表，再根据路由表选路、转发数据包。

### 路由算法的设计原则

- 正确性
- 简单性
- 偯壮性
- 可快速收敛到稳定状态
- 公平性
- 最优策略：最小化转发延时、最大化网络吞吐量

### 路由算法分类

静态路由(Nonadaptive/Static Routing)
: 提前计算出路由表，往往不改变，需要手动维护，不能根据网络实时流量和拓扑变化动态调整

动态/自适应路由(Adaptive Routing)
: 能适应**网络拓扑(Topology)** 和**业务量(Traffic)** 的变化

### 基本概念

**最优化原则**：最优路径上的任意两点间的路径也是最优的。

**汇集树(Sink Tree)**：以目的地节点为根，由所有源节点到目的节点的最优路径构成；因为是树，显然无环。

### 路由思想与策略

!!! note "注意"
    以下阐述的是路由思想或寻找最优路径的思想，在实际环境中并不能有效工作。

**最短路算法**（Dijkstra 算法）：

1. 建立有向加权图——节点为路由器（不含主机），边为通信线路，边权可为跳数、传输时延、物理距离等
2. 通过 Dijkstra 算法寻找最短路

**泛洪(Flooding)**：

基本过程：将数据包转发给每个邻居；邻居再将收到的包转发给除来路外的所有链路（防止原路返回）。

???+ note "泛洪的优缺点"
    **优点**

    - 不需要路由表，简单粗暴
    - 不需要网络信息
    - 鲯棒性好：所有路径都会被尝试，至少有一个包按最短路由到达目的地
    - 在建立路由表时可能较为有用

    **缺点**

    - 产生大量重复包
    - 可能有多个重复包到达目的节点

限制泛洪的手段：

跳计数器(Hop Counter)
: 每个包携带一个 Hop Counter，一般初始化为源到目的的距离或子网半径；每跳减 1，为 0 时丢弃

序列号(Sequence Number)
: 发送方在每个包前添加序列号；路由器记录每个发送方的最大序列号，避免重复转发

### 距离矢量选路 DVR(Distance Vector Routing)

#### 执行步骤

- 每个路由器维持一个路由表，包括到其他路由的最短距离和使用的下一跳接口
- 每个路由器**周期性**（RIP: 30s）播报自己的路由表
- 路由器根据收到的邻居路由表更新自己的路由表
- 如果一段时间内（RIP: 180s）没收到某路由器的路由表，则将该路由器从路由表中删除（距离设为 $\infty$）
- 迭代至各路由器路由表均不变化后，构建路由表结束

#### 特点

!!! abstract "一句话概括"
    路由器**周期性**地向**所有邻居** **广播**整个**路由表**。

1. 邻接节点之间共享网络信息（路由表）
2. 只和初始邻接节点共享信息
3. 对所有接口广播信息
4. 周期性地广播

#### 无穷计数问题(Count-to-Infinity)

<figure markdown="span">
  ![无穷计数问题](https://webp-pic.yokumi.cn/2026/01/20260101170257907.png){ loading=lazy width="70%" }
</figure>

节点 A 下线后，其余节点之间由于**只知道距离不知道路径**，相互传递距离、反复更新距离（如 B 认为可通过 C 到达 A，距离更新为 $1+2=3$，C 又认为可通过 B 到达 A，循环直到 $\infty$）。

!!! info "RIP 协议规定"
    权重（按跳数 Hop 计）> 16 即认为是 $\infty$，即节点已断开。

RIP(Routing Information Protocol) 属于一种路由协议，使用 DVR 路由算法。

### 链路状态选路 LSR(Link State Routing)

与 DVR 不同，LSR 中每个路由器向网络中的**所有路由器**共享信息。路由器在本地构建已知最优网络拓扑图后，发送一个 **Link-State Packet** 给所有路由器（Flooding）。主要特点：

1. 共享整个网络的拓扑结构信息
2. 向网络中的所有路由器共享
3. 当网络拓扑结构改变时进行共享

#### 执行步骤

对每个路由器：

1. **从相邻节点学习**：广播/多播 HELLO Packet 给邻接节点；邻接节点回复包含自己名字(Route IDs)的包
2. **测量通信线路开销**：通过 Echo Packet 测量往返延时 RTT，或测量信道带宽等参数
3. **构建 Link-State Packet**：

    <figure markdown="span">
      ![LSP 格式](https://webp-pic.yokumi.cn/2026/01/20260101170300058.png){ loading=lazy width="70%" }
    </figure>

    - Seq 字段：序列编号，用于检查是否是新的 LSP（新的继续 Flooding，重复或比已收到最大编号小的则丢弃）
    - Age 字段：寿命，避免 LSP 包无限泛滥，删除循环路由
    - 当周期性或监听到某些事件（如节点下线）后构建 LSP 包

4. **发送 Link-State Packet**：采用泛洪策略实现可靠发送；每个节点有错误侦测机制，收到正确包后回复确认包
5. **计算新路由**：收到所有 LSP 包后，在本地运行 Dijkstra 算法，计算通往每个目的节点的最短路径，保存到路由表

#### 采用 LSR 的协议

- IS-IS 协议
- OSPF 协议

### 层次选路 Hierarchical Routing

将距离较近的（如同一单位内）路由划分为同一个**域(Region)**，在网络内先按域路由，进入域后再选路至路由器。

## 拥塞控制 Congestion Control

### 拥塞

拥塞即网络负载超过了网络可用资源（CPU 处理速度、Buffer 缓冲队列长度、Bandwidth 链路带宽）。拥塞症状（判断指标）：

- Long Delay
- 较高的丢包率(Lost Packet)

!!! warning "注意"
    上述症状不能用来判断所有网络是否拥塞；无线网络丢包还需考虑误码等因素。

拥塞控制与流量控制不同：流量控制只是两个站点间的本地协调；拥塞控制是整个网络范围的全局问题。

### 解决方式

???+ info "解决方式分类"
    从产生拥塞的问题看：
    
    - 增加资源：网络供给(Networking Provision)、业务感知路由(Traffic aware-routing)
    - 减少负载：准入控制(Admission control)、流量限制(Traffic throttling)、负载掉落(Load shedding)
    
    从作用的时间节点看：
    
    - 预防性控制：前三种
    - 反应性措施：后两种

#### 流量调节 Traffic Throttling

基于反馈的解决方案，需要路由器感知拥塞。基本步骤：

1. **拥塞检测**：
    - 输出链路利用率：不够精确
    - 排队分组：计算路由器中缓存的数据包数量
    - 分组丢包数量：但太迟
    - 估计队列延时(queuing delay)：通过 EWMA 计算，$d_{new} = \alpha d_{old} + (1-\alpha)s$，其中 $\alpha$ 是平滑因子，$s$ 是最近采样的队列长度

2. **拥塞通知**：

    抑制分组(Choke Packet)
    : 路由器发送 Choke Packet 给源节点，包含拥塞目的节点信息；发送方原始包被标记以避免产生更多 Choke Packet。实际效果不佳——网络已拥塞还需产生 Choke Packet 传输

    ECN(Explicit Congestion Notification)
    : 在 IP 和 TCP 中使用；IP Header 中设 2bits 拥塞控制位：默认 00，路由器检测到拥塞设为 11；目的端通过传输层发送 Congestion Signal 给源端

3. **业务量限制**：收到 Choke Packet 后，源节点减少发送到某目的地的业务量（如减小发送窗口）

??? note "拥塞恢复时"
    路由器不会通知端节点恢复业务量；需发送方自行推测和试探。如 TCP 的 AIMD 机制：拥塞时窗口减半，然后逐步增加，无丢包继续加大，丢包则再次降速。

#### 负载掉落 Load Shedding

关键问题是选择丢弃哪些数据，需根据不同应用场景选择。

**RED(Random Early Detection)**：路由器在路由完全失效前随机丢弃一部分包；不（显式）通知源节点，源节点因未收到 ACK 而感知拥塞并降低发送速度——即**隐式通知**。

举例：

1. 发送方发出序号 4、5、6 的数据帧
2. 路由器收到序号 4 的帧，接收并回复 ACK 4
3. 路由器收到序号 5 的帧，因 RED 机制选中而被丢弃
4. 路由器收到序号 6 的帧，缓存但期望收到 5，回复 ACK 4
5. 发送方收到两个重复的 ACK 4，推断后续数据可能丢包

!!! info "TCP 规定"
    源节点收到 3 个及以上相同 ACK，则认为发生拥塞。

## 服务质量 Quality of Service

### QoS 参数

- **Reliability**：可靠性，包括错误率和丢包率
- **Delay**：延迟
- **Jitter**：抖动
- **Bandwidth**：带宽

针对不同应用场景，对参数要求各不相同，需提供个性化服务。

### 提升服务质量的技术

#### 流量整形 Traffic Shaping

实际网络中往往出现**突发流量(Traffic Burst)**。流量整形去除或减少突发流量，使实时传输速率接近平均速率。

漏桶(Leaky Bucket)
: 桶就是一个 Buffer 队列，通过匀速从队列中拿出数据分组实现匀速传输；桶满则丢弃新来数据或等待队列空

令牌桶(Token Bucket)
: 路由器匀速产生令牌，桶满则丢弃多余令牌；数据包到达队列后需消耗令牌发送（1 Token = 1 Packet）；令牌桶不限制数据队列缓存，不丢弃数据帧；可接受一定突发流量（突发时一次性消耗所有令牌）

令牌桶突发数据持续时间计算：

令突发持续时间 $S$ sec，令牌桶容量 $B$ Bytes，令牌产生速率 $R$ Bytes/s，最大输出速率 $M$ Bytes/s，则：

$$S = \frac{B}{M - R}$$

#### 分组调度 Packet Scheduling

先进先出队列(FIFO Queuing)
: 先到达的包先发出；后到达的包可能因队列空间不够而被丢弃

优先级队列(Priority Queuing)
: 数据包经分类器按优先级存入不同队列；空闲时高优先级队列先处理发送；对低优先级不公平——如果高优先级队列一直有数据，低优先级无法发出

公平队列(Fair Queuing)
: 每个流都有一个队列，循环处理发送每个队列中的数据包

公平加权队列(Weighted Fair Queuing)
: 根据优先级对数据加权，循环按权值处理每个优先队列（如权值 3 的一次发送 3 个包，权值 2 的一次发送 2 个包）

<figure markdown="span">
  ![加权公平队列示例](https://webp-pic.yokumi.cn/2026/01/20260101170304376.png){ loading=lazy width="70%" }
</figure>

每个包的到达时间和长度已知，发送完成时间根据以下公式：

$$Finish\_time_i = max(Arrival\_time_i, Finish\_time_{i-1}) + \frac{Length_i}{Weight_i}$$

## 网络互联 Internetworking

不同网络的协议不同，在不同网络间传输信息需实现网络互联。

### 分片 Fragmentation

不同网络的 **MTU(Maximum Transmission Unit)** 不同，网络层传输数据时需进行分片处理。e.g. 以太网 Ethernet's MTU = 1500 Bytes。

## IP 协议(Internet Protocol)

- 无连接的网络层协议
- 数据报电路
- 尽力而为(Best-effort)提供服务
- 路由算法为分层路由、距离矢量选路和链路状态选路的结合

### IP 数据包格式

#### IPv4 帧格式

<figure markdown="span">
  ![IPv4 帧格式](https://webp-pic.yokumi.cn/2026/01/20260101170310695.png){ loading=lazy width="70%" }
</figure>

各字段说明：

Version(版本)
: 数据报属于协议的哪个版本

IHL(IP Header Length)
: IPv4 头长度不固定（因 Option 字段）。IHL 为 4bits，表示范围 5~15，对应头长度需 $\times 4$，即 20~60 Bytes

Type of Service(服务类型)
: 共 8bits，前 6bits 表示服务类型，后 2bits 是 ECN 显式拥塞通知位

Total Length(总长度)
: 头长度 + 数据字段长度；共 16bits，最大 65535 Bytes

Identification(标识)
: 区分当前分段属于哪个数据包；同一数据包的所有分段标识位相同

DF(Don't Fragment)
: 告知路由器不要分片；可用于发现路径 MTU

MF(More Fragment)
: 告知路由器数据报的所有分段是否均到达；除最后分段外，其余 MF = 1

Fragment Offset(分段偏移量)
: 该段在数据报中的位置，必须是 **8 的整数倍**；仅指数据部分不包括首部；共 13 位，实际偏移量 = offset $\times 8$

Time to Live(生存期)
: 类似跳计数器

Protocol Field(协议字段)
: 上层协议（TCP/UDP 等）

Checksum(头部检验和)
: 共 16 位，只对头部校验，不对数据校验

Source/Destination IP Address
: 源地址 / 目标地址

Options(选项)
: 长度 0~40 Bytes，包括：

    - Security 安全性
    - Strict source routing option 严格源选路：源节点指定完整路径，每跳严格按路径传递
    - Loose source routing option 宽松源选路：源节点指定几个必须经过的路由器
    - Record route option 记录路由：通知沿途路由器将 IP 地址添加至选项字段
    - The Timestamp option 时间戳

### IP 地址

#### IPv4 地址

##### 概述

- 发展过程：分类地址 $\rightarrow$ 子网 $\rightarrow$ 超网 $\rightarrow$ 无类别地址
- 共 32 位，采用点分十进制
- 每个**网络接口(Network Interface)**有唯一 IP 地址（IP 地址与接口绑定；一台设备有 2 个接口则有 2 个 IP 地址）

##### 分类地址

地址 32 位分为网络号和主机号：

<figure markdown="span">
  ![分类地址](https://webp-pic.yokumi.cn/2026/01/20260101170313783.png){ loading=lazy width="70%" }
</figure>

- **A 类**：第 1 位标识，网络号 7 位，主机号 24 位；网络总数 $2^7=128$，每网络最多 $2^{24}-2$ 台主机
    - 网络地址：主机号全为 0
    - 广播地址：主机号全为 1
- **B 类**：前 2 位标识，网络号 14 位，主机号 16 位；网络总数 $2^{14}$，每网络最多 $2^{16}-2$ 台主机
- **C 类**：前 3 位标识，网络号 21 位，主机号 8 位；网络总数 $2^{21}$，每网络最多 $2^{8}-2=254$ 台主机
- 组播地址(Multicast)
- 保留地址

通过第一个字节的十进制数快速判定类别：

类别
: 第一个字节范围

    A 类
    : 0~127

    B 类
    : 128~191

    C 类
    : 192~223

三类地址的默认掩码：

类别
: 默认掩码

    A 类
    : 255.0.0.0

    B 类
    : 255.255.0.0

    C 类
    : 255.255.255.0

计算网络地址：通过掩码和 IP 地址按位与运算。

特殊 IP 地址：

特殊地址
: 含义

    0.0.0.0
    : 当前主机/本机

    网络号全为 0
    : 本地网络内的主机

    255.255.255.255
    : 本网广播

    主机号全为 1
    : 远程网络广播

    127 开头
    : 环回地址，用于测试

##### 子网划分 Subnetting

向主机号借 n 位作为**子网号(Subnetid)**，实现对大型网络的划分。子网划分对外部不可见。

通过子网掩码和 IP 地址按位与运算可得到网络地址。

设计子网划分：

1. 确定各地址块大小（所需地址位数 $< 2^n-2$，n 为主机位数）
2. 从主机地址最高位开始确定子网号；一般先从地址块空间大的子网开始分配，否则可能导致大地址块无法分配

##### 超网划分 Supernetting

C 类地址单个网络最多 254 台主机，为解决主机数不够用，将多个网络合并成一个大网。

<figure markdown="span">
  ![超网划分示例](https://webp-pic.yokumi.cn/2026/01/20260101170317269.png){ loading=lazy width="70%" }
</figure>

上图超网掩码第三字节为 $11111100=252$，与 IP 地址按位与运算得到超网地址；相当于主机号向网络号借了 2 位。

##### 无类别地址与 CIDR

网络号和主机号长度不固定，解决了分类地址造成的地址枯竭等问题。

CIDR(Classless InterDomain Routing)
: 地址格式形如 `a.b.c.d/x`，其中 $x$ 为网络号位数（前缀长度），地址块的地址数 $N = 2^{32-x}$

CIDR 除表示子网外，也可将多个子网聚合为超网。但合并多个小网为大网会使地址空间被放大，因此引入**最长匹配原则**。

最长匹配原则示例：

<figure markdown="span">
  ![CIDR 路由聚合示例](https://webp-pic.yokumi.cn/2026/01/20260101170319918.png){ loading=lazy width="70%" }
</figure>

三所大学的 IP 地址可被聚合成前缀 **192.24.0.0/19**（共 8192 个地址），伦敦将聚合前缀发送给纽约，节省路由表规模，但引入了 1024 个不属于三所大学的地址。

<figure markdown="span">
  ![CIDR 最长匹配原则](https://webp-pic.yokumi.cn/2026/01/20260101170323128.png){ loading=lazy width="70%" }
</figure>

未分配的 1024 个前缀地址被分配给旧金山。纽约有两条路由信息：

- 聚合前缀：192.24.0.0/19 $\rightarrow$ 伦敦
- 更具体前缀：192.24.12.0/22 $\rightarrow$ 旧金山

当数据包目的地址为 192.24.12.5 时，纽约路由器匹配两个前缀，根据**最长匹配前缀原则**选择匹配位数最多的前缀，数据包被发送到旧金山。

##### 路由

主机定义的路由(Host-specific Routing)
: 路由表目的节点地址就是相应主机

网络定义的路由(Network-specific Routing)
: 路由表目的节点为网络号，同一网络上的所有主机被视为一个实体

默认路由(Default Routing)
: 0.0.0.0，路由器没有指定路由信息时连接互联网的剩余部分默认走这条路由

##### NAT(Network Address Translation)

给公司分配 1 个或少量的 IP 地址，公司网络内部节点有唯一的私有地址（不允许出内部网络）。专用地址范围：

- 10.0.0.0 ~ 10.255.255.255/8
- 172.16.0.0 ~ 172.31.255.255/12
- 192.168.0.0 ~ 192.168.255.255/16

数据报发送到外部网络时，通过 NAT Router 将内部私有地址转换为全局共享 IP 地址。多个内部主机同时访问外部主机时，NAT 路由器转换表还需记录内部端口号以识别不同主机。基本过程：

1. 内部主机发出请求包至 NAT 路由器（私有地址不同，本地端口号可能相同）
2. NAT 路由器将私有地址转换为全局 IP 地址，同时更改传输层全局端口号
3. 外部主机应答包到达 NAT 路由器后，根据端口号查表得到源 IP 地址和源端口号，转发给正确的内部主机

动态 NAT 表项
: 内部主机需访问公网时才建立；动态创建和回收（连接关闭或长久未使用时回收）

静态 NAT 表项
: 手动创建并配置；映射关系固定

#### IPv6 地址

##### 设计目标

1. 支持更大的地址空间
2. 减小路由表大小
3. 简化协议，加速路由器处理数据包速度
4. 安全性
5. 关注服务质量（尤其是实时数据）
6. 支持组播
7. 主机漫游时无需改变地址
8. 允许协议的演进与共存

??? note "漫游(Roam)"
    漫游指设备在不同网络间移动（如从家里 WiFi 切换到公司网络）时保持连接不中断的能力。传统 IPv4 地址与物理网络绑定，网络变动会重新分配 IP 地址。IPv6 的 MIPv6 机制：

    1. 设备有 **Home Address**（家乡地址），永久不变
    2. 到达新网络时获取 **Care-of Address**（照管地址），表示在新网络中的实际地址
    3. 外界仍通过 Home Address 通信，数据由 **Home Agent**（家乡代理）转发到 Care-of Address

##### 头格式与地址格式

<figure markdown="span">
  ![IPv6 帧格式](https://webp-pic.yokumi.cn/2026/01/20260101170326460.png){ loading=lazy width="70%" }
</figure>

- **VER(版本)**：IP 协议版本
- **PRI(区分服务)**：优先级
- **Flow Label(流标号)**：控制传输时占用的带宽和时延，仍处于试验阶段
- **Payload Length(有效载荷长度)**：包头 40 Bytes 后的字节数
- **Next Header(下一个头)**：Payload 中除数据外还支持 6 个扩展头（相当于 IPv4 的 Option 字段）
- **Hop Limit(跳数限制)**：相当于 IPv4 的 TTL 字段
- **Source/Destination Address**：128 位地址，16 Bytes，分成 8 组书写，每组 4 个十六进制数，组间用 `:` 间隔

IPv6 地址简化表示：

- 一组内可忽略前导 0：$XXXX:0123:XXXX \rightarrow XXXX:123:XXXX$
- 多组全 0 可用双冒号合并：$8000:0000:0000:0000:0123:0000:89AB:CDEF \rightarrow 8000::123:0:89AB:CDEF$
- 一个 IPv6 地址中**最多只能有 1 个双冒号**

## ICMP(Internet Control Message Protocol)

ICMP 消息封装在 IP 数据包的数据部分。

<figure markdown="span">
  ![ICMP 消息类型](https://webp-pic.yokumi.cn/2026/01/20260101170330311.png){ loading=lazy width="70%" }
</figure>

**回应请求/应答(ECHO Request/Reply)**：主机发送回应请求给目的地址，检测可达性或在线状态。ping 命令即用此协议。

## ARP(Address Resolution Protocol)

ARP 解决从网络层 IP 地址到数据链路层 MAC 地址的映射问题。工作原理：

1. 查路由表未查到目的 IP 对应的 MAC 地址时，在本网内广播 ARP 包，询问"某 IP 地址的 MAC 地址是什么？"
2. 对应 IP 的站点收到广播包后，回复自己的 MAC 地址信息给路由器（单播）

可能的问题：

- **没人回答**：说明目的地不可达，路由器回复 ICMP 报错信息
- **多人回答**：路由器一般以最先或最后收到的回复为准。存在 **ARP Spoofing(ARP 欺骗)** 安全隐患——恶意节点发送大量 ARP 包篡改 ARP 表，将数据包转发到恶意节点

## RARP(Reverse ARP)

已知 MAC 地址，需要知道自己的 IP 地址。主要用于初始化建立连接时，站点不知自己的 IP 地址，向网络内发送询问，RARP Server 回复其 IP 地址。

## DHCP(Dynamic Host Configuration Protocol)

- 属于**应用层协议**
- Client-Server 模式工作
- 提供自动配置的 IP 地址和其他配置信息（网关、网络掩码、DNS 服务器等）给网络中的主机，使用 **UDP** 携带消息
- 提供**租赁(Leasing)**和**续租(Renewal)**服务

### 工作流程

<figure markdown="span">
  ![DHCP 工作流程](https://webp-pic.yokumi.cn/2026/01/20260101170336912.png){ loading=lazy width="70%" }
</figure>

1. **Discover(发现)**：客户端广播寻找 DHCP 服务器（服务器用 UDP 67 端口，客户端用 UDP 68 端口）
2. **Offer(提供)**：DHCP Server 响应，提供 IP 地址等配置信息
3. **Request(请求)**：可能有多个 Offer 或多个 DHCP Server，客户端选择一个 Offer 并请求使用
4. **ACK(确认)**：DHCP Server 确认请求，正式分配 IP 地址等配置信息

### DHCP Relay Agent

子网内无 DHCP Server 时，MAC 地址只能在本子网内传播，无法跨路由器。DHCP Relay Agent 解决此问题：

<figure markdown="span">
  ![DHCP Relay Agent](https://webp-pic.yokumi.cn/2026/01/20260101170339548.png){ loading=lazy width="70%" }
</figure>

1. DHCP Relay 收到 Discover，记住客户端原始 IP
2. DHCP Relay 将请求以单播方式转发给 DHCP Server
3. DHCP Relay 将 DHCP Server 的回复转发给客户端

## 路由协议

互联网被分为无数个**自治系统(AS, Autonomous System)**，分别使用不同的路由协议（IGP），不同 AS 间路由也使用路由协议（EGP）；每个 AS 有唯一编号。

<figure markdown="span">
  ![自治系统与路由协议](https://webp-pic.yokumi.cn/2026/01/20260101170343680.png){ loading=lazy width="70%" }
</figure>

具体协议：

- **IGP**：
    - RIP：使用 DVR 距离矢量选路
    - OSPF：使用 LSR 链路状态选路
- **EGP**：
    - BGP：使用路径矢量选路(Path Vector Routing)

### RIP(Routing Information Protocol)

- 使用 DVR 距离矢量选路
- 使用跳数作为路径权重
- 最大跳数为 16
- 路由表定期发送时间为 30s
- RIP 消息通过 **UDP** 包传输

### OSPF(Open Shortest Path First)

#### 概述

- 使用 LSR 链路状态选路
- 允许管理员根据服务类型设置代价，但实际部署通常只根据带宽设置
- OSPF 消息直接通过 **IP** 包传输

#### OSPF 报文类型

报文类型
: 功能

    Hello
    : 发现邻居

    LSU(Link State Update)
    : 发送 LSA(Link-State Advertisement)给邻居，通知网络状态

    LSAck(Link State Ack)
    : 邻居回复确认收到 LSA

    DBD(Database Description)
    : 描述数据库摘要

    LSR(Link State Request)
    : 从邻居请求特定的 LSA

#### 工作流程

1. **建立邻居关系**：向同一链路上的邻居路由器发送 Hello 报文
2. **交换链路信息**：
    - 邻居路由器回送 DBD（数据库摘要）
    - 路由器发送 LSR，请求特定 LSA
    - 邻居路由器回送 LSU，发送 LSA 给路由器
    - 路由器发送 LSAck，确认收到 LSA

#### RIP vs. OSPF

<figure markdown="span">
  ![RIP vs OSPF](https://webp-pic.yokumi.cn/2026/01/20260101170348554.png){ loading=lazy width="70%" }
</figure>

### BGP(Border Gateway Protocol)

- 使用 Path Vector Routing 路径矢量选路
- 允许按"策略"选路（如避开某些特定 AS）
- 可根据链路带宽、容量、拥塞倾向、质量、安全性选择路径
- 偏好走中间 AS 数更小的路径
- 自动避免环路问题
- 使用 **TCP** 协议传输报文（可靠传输）

## QoS 保障实例——保证转发 Assured Forwarding

<figure markdown="span">
  ![保证转发](https://webp-pic.yokumi.cn/2026/01/20260101170307628.png){ loading=lazy width="70%" }
</figure>

1. 所有业务被划分为 4 个优先级
2. 通过 Traffic Policer 的令牌桶机制进行流量整形
3. 在 Traffic Policer 处，每个优先级下又被分类为 3 种丢弃优先级（丢包可能性大小）
4. 最终有 12 种服务等级
5. 每个 Packet 的 IP Header 的 **ToS 字段**携带 DSCP(6bits) + ECN(2bits)：
    - **DSCP(Differentiated Services Code Point)**：服务等级
    - **ECN(Explicit Congestion Notification)**：拥塞控制
6. 路由器根据以下机制进行分组调度：
    - **WFQ(Weighted Fair Queuing)**：按优先级公平调度
    - **RED(Random Early Detection)**：主动丢弃机制，丢弃概率即前面划分的丢弃优先级
