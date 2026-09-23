# 传输层

## 传输层提供的服务

传输层提供端到端的可靠、高效、节省开销的服务，事实上提供的是**进程到进程 (Process-to-Process)** 的通信。

<figure markdown="span">
  ![传输层提供端到端服务](https://webp-pic.yokumi.cn/2026/01/20260101170353063.png){ loading=lazy width="70%" }
</figure>

传输层的核心职责包括：

- 屏蔽通信网络的复杂性，向上层提供统一的通信接口
- 通过单一的网络接口提供多个服务访问点 SAP
- 分为无连接的服务和面向连接的服务；在因特网中分别指 UDP 和 TCP

## 传输层协议的基本要素

### 传输层协议 vs. 数据链路层协议

两者都需要处理差错控制、序列顺序、流量控制等问题，但工作环境不同：

- 数据链路层：节点到节点 (Node-to-Node) 的通信
- 传输层：进程到进程 (Process-to-Process) 的通信

### Addressing 寻址

通过**端口号 (Port Number)** 标识消息对应的应用程序。端口号分配方式分为以下几种类型：

Well Known 端口
: 0 ~ 1023，公知的，e.g. HTTP(80)、HTTPS(443)、SMTP(25)

Registered 端口
: 1024 ~ 49151，注册的

Dynamic/Private 端口
: 49152 ~ 65535，动态或私有的

<figure markdown="span">
  ![端口号分类](https://webp-pic.yokumi.cn/2026/01/20260101170356001.png){ loading=lazy width="70%" }
</figure>

即 IP 地址选择主机，Port Number 选择主机上的对应进程。网络层的服务访问点称为 NSAP (Network Service Access Point)，类似地，传输层上的服务访问点称为 **TSAP**。

<figure markdown="span">
  ![TSAP 寻址示意图](https://webp-pic.yokumi.cn/2026/01/20260101170401861.png){ loading=lazy width="70%" }
</figure>

???+ info "Process Server 进程服务器"
    一台机器上可能存在多个服务器进程，其中许多服务很少被使用。如果让这些服务器进程一直活跃并整天监听一个稳定的 TSAP 地址，会浪费资源。所以让**进程服务器**作为不常用服务器的代理——当有客户端请求到来时，进程服务器再启动对应的服务进程。

### Connection Establishment 连接建立

!!! abstract "目标"
    确保收发双方能够正确建立有且只有一个连接。否则，接收方会因为对重复或失败的连接预分配缓存，消耗网络资源（即 DDoS 攻击）。

解决方案：**三次握手 (3-Way Handshake)**

<figure markdown="span">
  ![三次握手示意图](https://webp-pic.yokumi.cn/2026/01/20260101170403937.png){ loading=lazy width="70%" }
</figure>

三种情况：

1. **正常情况**：CR (Connection Request) 正确到达，回送对应的 ACK，然后 Host 1 再回送一个对应 Host 2 发送的 ACK 序号的 ACK
2. **重复的连接请求**：Host 2 无法判断，但 Host 1 在收到 ACK 后发现问题，发出 REJECT
3. **重复的连接请求和重复的 ACK**

### Connection Release 连接释放

!!! abstract "目标"
    - 释放过程不丢包（需要平滑释放/对称释放，即单独释放每个连接）
    - 无半开连接，即一方释放连接但另一方未释放连接

同样可以三次握手来解决：

<figure markdown="span">
  ![连接释放 - 正常情况](https://webp-pic.yokumi.cn/2026/01/20260101170411355.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![连接释放 - 异常情况](https://webp-pic.yokumi.cn/2026/01/20260101170416036.png){ loading=lazy width="70%" }
</figure>

#### Half-open Connection 半开连接

如果初始的 DR 和重传 n 次后都丢失，发送方认为协议失败会强行释放连接，此时接收方由于没有收到任何消息，仍处于挂起状态。

解决方法：

- **Automatically disconnected rule**：在一定时间内，如果接收方没有收到发送方的段，则连接自动断开。但存在问题——如果发送方并不打算断开连接，只是很久没有数据需要发送，会导致接收方将连接错误断开
- **Dummy Segment 哑段**：接收方长时间没有收到发送方的段时，主动发送一个哑段，试探对方是否还在线

### Error Control 差错控制

传输层同样采用 ARQ（自动请求重传协议），每个段有序列号、计时器、校验码，以及对应的 ACK 确认，也需要滑动窗口机制。不过与数据链路层的区别在于：传输层需要动态调整窗口大小，同样需要动态管理缓冲区。

<figure markdown="span">
  ![缓冲区管理方式](https://webp-pic.yokumi.cn/2026/01/20260101170433037.png){ loading=lazy width="70%" }
</figure>

三种缓冲区管理方式：

1. **链式固定大小的缓冲区**：适用于每个段的大小差别不大，每个缓冲区容纳一个段
2. **链式可变大小的缓冲区**
3. **每个连接使用一个大循环缓冲区**

### Flow Control 流量控制

影响流量控制的因素：

1. 接收方缓冲区大小限制
2. 网络的承载能力，即是否发生拥塞

流量控制的一种方式是 **Dynamic Buffer Allocation（动态缓冲区分配）**：

<figure markdown="span">
  ![动态缓冲区分配](https://webp-pic.yokumi.cn/2026/01/20260101170435404.png){ loading=lazy width="70%" }
</figure>

!!! warning "死锁问题"
    上图可能出现死锁：A 发出的 m2 数据丢失，B 未收到所以仅发送 ACK 1，通知 A 可以发送 2 ~ 4。A 发送 m3 和 m4 后，m2 超时需要重传，此时：

    - A 因缓冲区耗尽和重传持续阻塞，无法继续发送
    - B 确认所有已接收数据（ACK = 4），但因未收到 seq = 2 无法释放对应缓冲区，导致 buf = 0

    为避免死锁，每台主机应定期在每个连接上发送控制段，给出确认和缓冲区状态。采用这种方法，死锁迟早会被打破。

### Multiplexing 复用

每个应用程序都需要通过网络发送或接收数据，但物理网络接口只能处理单一的数据流。复用器将不同数据流合并为一个流传送到网络层，接收方通过解复用器按端口号区分，将数据发送给不同的进程。

**Inverse Multiplexing 逆向多路复用**：传统的复用为多个应用程序共享一个网络接口，而逆向多路复用是一个应用程序同时使用多个网络接口（比如一台主机有多个 IP 地址或多个传输链路），在 SCTP 协议中被使用。

<figure markdown="span">
  ![复用与逆向复用](https://webp-pic.yokumi.cn/2026/01/20260101170440919.png){ loading=lazy width="70%" }
</figure>

## Congestion Control 拥塞控制

拥塞发生在路由器上，因此网络层肯定需要检测拥塞。但究其本质，拥塞是由传输层传送到网络中的流量引起的，因此控制拥塞的唯一途径是**传输层放缓往网络中发送数据包的速度**。

### 拥塞控制算法设计目标

- 能有效避免拥塞
- 能有效分配和利用带宽
- 对每个传输实体公平
- 能快速跟踪网络流量需求的变化，收敛速度快

### 衡量拥塞控制的指标

**Efficiency and Power**：$Power = \frac{load}{delay}$

<figure markdown="span">
  ![功率与负载和延迟的关系](https://webp-pic.yokumi.cn/2026/01/20260101170445213.png){ loading=lazy width="70%" }
</figure>

一开始功率随负载增大而增大，延迟保持较低水平不变；超过一定限度后，延迟快速增长（发生拥塞），功率也迅速下降。其中 **Efficient Load（有效负载）** = 达到最大功率时对应的负载值。

### 平衡带宽分配

#### 最大最小公平性 Max-Min Fairness

!!! abstract "基本含义"
    资源分配向量的最小分量的值最大，防止任何网络流被"饿死"，同时尽可能增加每个流的速率。

**原则**：在满足最小需求的前提下，如果分配给一个网络流的带宽无法在不让别的网络流的带宽减少的情况下进一步增大，那么也不继续分配给该网络流更多的带宽。

基本步骤：

1. 先分析通过流最多的链路，对于链路上的 $n$ 个流，每个流分到的带宽为 $\frac{1}{n}$（假设链路总带宽为 1）
2. 对于这 $n$ 个流，其在别的链路上的带宽也一致
3. 如果其余链路上的所有流也还未被分配，则重复上述步骤
4. 如果某链路上的其余流已经被分配，则剩下的一个流可以分到 1 - 已分配的带宽

#### Convergence 收敛

由于需求的变化，网络的理想操作点也随时间推移而改变。良好的拥塞控制算法应迅速收敛到理想的操作点，并跟踪随时变化的操作点。

<figure markdown="span">
  ![收敛性示意图](https://webp-pic.yokumi.cn/2026/01/20260101170449709.png){ loading=lazy width="70%" }
</figure>

### 互联网中的拥塞控制

#### 拥塞控制的基本流程

1. **谁来检测拥塞？** 路由器通过队列长度或线路利用率进行判断
2. **如何通知源主机？**
    - 显式拥塞通知（TCP with ECN）
    - 隐式拥塞通知（RED），或源主机根据自己的丢包情况进行判断
3. **源主机如何采取措施？**
    - 出现拥塞时，降低发送速率
    - 无拥塞时，增大发送速率

#### 控制策略

!!! abstract "目标"
    既最大化效率又满足公平。

<figure markdown="span">
  ![AIMD 策略示意图](https://webp-pic.yokumi.cn/2026/01/20260101170457348.png){ loading=lazy width="70%" }
</figure>

如上图所示：

- $y = x$：公平线，两者分到的带宽相等
- $x + y = 1$：效率线，两者带宽总和为 1，最高效
- 前两者交点 $(0.5, 0.5)$：最优点
- $y = x + a$：加法线，采用 **AIAD** 策略，两者加/减相同的量，只是上下振荡，并不会靠近最优点
- $y = ax, a < 1$：乘法线，采用 **MIMD** 策略，两者乘相同的量，沿乘法线振荡，无法收敛

因此，采用**加法增、乘法减**的策略，即 **AIMD (Additive Increase Multiplicative Decrease)**：

<figure markdown="span">
  ![AIMD 收敛过程](https://webp-pic.yokumi.cn/2026/01/20260101170509893.png){ loading=lazy width="70%" }
</figure>

- 当网络未拥塞时，采用加法递增两者的带宽（向上 45 度）
- 当网络拥塞时，采用乘法递减两者的带宽（指向原点）

AIMD 是 TCP 协议采用的拥塞控制策略。基于以下观点：网络进入拥塞很容易，但从中恢复很难，所以递增过程应该平缓，递减过程应该激进。

## UDP 用户数据报协议

### 概述

- 无连接的
- 不可靠的传输：无 ACK、无差错控制、无流量控制、无拥塞控制
- 尽力而为 (Best Effort)
- 提供了一个与 IP 协议的接口，在此接口上增加通过端口号进行复用的功能
- 可以被用来广播 IPv4 包或组播 IPv4 包和 IPv6 包
- UDP **保留消息边界**，即应用层有多少数据，直接加一个 UDP 头就给下一层（与 TCP 面向字节流的服务不同）

### 应用

以下协议对应的传输层采用 UDP：

- DNS：端口 53
- DHCP：端口 67/68
- RIP

### 数据报格式

<figure markdown="span">
  ![UDP 数据报格式](https://webp-pic.yokumi.cn/2026/01/20260101170513125.png){ loading=lazy width="70%" }
</figure>

#### UDP 校验和与伪头部

一个可选的校验和字段提供了额外的可靠性，校验 UDP 头、数据和**伪头部**。伪头部由一部分 IP Header 组成：

<figure markdown="span">
  ![UDP 伪头部](https://webp-pic.yokumi.cn/2026/01/20260101170517575.png){ loading=lazy width="70%" }
</figure>

注意：伪头部仅在需要计算校验和时添加，并不会加入 IP 包中一起发送出去，所以称其为伪头部。

<figure markdown="span">
  ![UDP 校验和计算范围](https://webp-pic.yokumi.cn/2026/01/20260101170525054.png){ loading=lazy width="70%" }
</figure>

### 复用和解复用

<figure markdown="span">
  ![UDP 复用与解复用](https://webp-pic.yokumi.cn/2026/01/20260101170528918.png){ loading=lazy width="70%" }
</figure>

## TCP 传输控制协议

### 概述

- TCP 协议在不可靠网络上工作，提供面向连接的、可靠的、端到端的**字节流**服务（UDP 协议是面向消息的）
- 面向连接：
    - 全双工
    - 端到端，单播通信，不支持广播和组播
    - 每个 TCP 连接都必须通过 socket 来建立，socket 为四元组 `(srcIP, srcPort, dstIP, dstPort)`，TCP 通过 `(socket1, socket2)` 唯一标识连接
    - 熟知端口：HTTP(80)、HTTPS(443)
- 使用 ARQ 机制：有校验码、序列号、ACK 等，有重传、累积确认、计时器、滑动窗口等机制
- 有拥塞控制
- 面向**字节流 (Byte Stream-Oriented)**：
    - 不保留消息边界，即 TCP 报文段内数据长度由 TCP 协议决定，与上层消息长度无关
    - 给每个数据字节均编号

### TCP 报文段格式

TCP Segment = TCP Header (20 Bytes or more) + Data

一些比较重要的字段：

- **Sequence Number**：该段第一个字节的序号
- **Acknowledgement Number**：下一个期待接收的字节的序号（即已正确接收的最后一个字节序号 + 1，与数据链路层中的滑动窗口协议区分）

<figure markdown="span">
  ![TCP 报文段格式](https://webp-pic.yokumi.cn/2026/01/20260101170539336.png){ loading=lazy width="70%" }
</figure>

控制字段的含义：

- **CWR and ECE**：用于拥塞控制
- **URG**：表示 Urgent Pointer 有效，该指针的数据需要提前处理
- **ACK**：ACK = 1 表示确认号有效（仅当 ACK = 1 时，Window Size 才有效）
- **PSH**：该数据报需要直接交给应用层，优先级低于 URG
- **RST**：表示需要重置连接
- **SYN**：用于请求建立连接
- **FIN**：用于请求断开连接

TCP 中的 Checksum 共 16 bits，覆盖对以下内容的校验：

1. 伪首部：并不是 TCP 报文中真正的内容，但校验时必须包含
2. TCP Header
3. TCP Payload

伪首部的格式如下：

<figure markdown="span">
  ![TCP 伪首部格式](https://webp-pic.yokumi.cn/2026/01/20260101170545319.png){ loading=lazy width="70%" }
</figure>

协议字段表示上层协议，对于 TCP 协议，Protocol = 6。

此外，TCP Header 还支持一些扩展字段：

MSS (Maximum Segment Size)
: 每台主机愿意接收的最大段长度

    - 只包含有效载荷（数据部分），不包括 TCP 首部
    - 一般在建立连接时协商
    - 两个方向上的最大段长度可以不同

Window Scale
: 窗口因子，将 Window Size 左移 Window Scale 位。最终的 Calculated Window Size = Window Size $\times 2^{\text{Window Scale}}$

Timestamp
: 时间戳

    - 可以计算往返时间 RTT
    - 用来计算数据包多久可以认为丢失
    - 同时能防止序号回绕

SACK
: 选择确认

    - 告诉发送方已经接收到的序号范围
    - 发送方可以明确知道重传哪些丢失的帧

### TCP 中的拥塞控制机制

TCP Header 中有 CWR 和 ECE 标志，IP Header 中有 ECN 标志。基本工作机制：

1. 路由器如果检测到拥塞，会将 IP 包中的 ECN 标志置为 11
2. TCP Receiver 收到该 IP 包后，发现 ECN 标志为 1，需要通知发送方产生拥塞，在回送的包中将 **ECE** 标志置 1

    ECE (ECN Echo)
    : ECN 回声标志，用于告知对方"我感知到你的路径上产生了拥塞"

3. TCP Sender 接收到 IP 包后，发现 ECE 标志为 1，知道产生拥塞，需要降低发送速率（实际是减小滑动窗口大小）
4. TCP Sender 再回送一个 IP 包，将 **CWR** 标志置 1

    CWR (Congestion Window Reduced)
    : 拥塞窗口减少标志，用于告诉对方"我已经响应拥塞通知，减小窗口"

5. TCP Receiver 接收到 IP 包后，发现 CWR 标志为 1，知道 TCP Sender 已经响应拥塞，于是在之后发出的 IP 包中清除 ECE 标志

总结：ECE 由接收方设置，CWR 由发送方设置。

### TCP 的连接建立

#### 连接建立过程

TCP 的连接建立为"三次握手"，即"客户端发送 SYN、服务端返回 SYN + ACK、客户端发送 ACK"。具体来说：

1. **第一次握手（SYN）**：客户端发送一个带有 SYN 标志的 TCP 段到服务器，希望建立新的连接。这个段包含一个初始序列号（ISN），这是一个较大的随机值（也可能是根据机器时钟生成的），用于防止 TCP 重放攻击等安全问题，同时标识客户端发送数据的起始点
2. **第二次握手（SYN + ACK）**：服务器接收到客户端的 SYN 请求后，发送一个带有 SYN 和 ACK 标志的 TCP 段作为响应。服务器在响应中包含自己的初始序列号，同时确认客户端的初始序列号（将其加 1 作为确认号。注意区分 TCP 协议和数据链路层中滑动窗口协议关于 ACK 字段含义的差异）
3. **第三次握手（ACK）**：客户端收到服务器的 SYN + ACK 响应后，发送一个带有 ACK 标志的 TCP 段作为确认，确认了服务器的初始序列号（将其加 1 作为确认号）

<figure markdown="span">
  ![TCP 三次握手](https://webp-pic.yokumi.cn/2026/01/20260101170548079.png){ loading=lazy width="70%" }
</figure>

#### 安全性问题

普通的 TCP 连接建立涉及安全隐患，即 **SYN flooding attack（SYN 泛洪攻击）**：攻击者只利用握手阶段的 1/3，即伪造大量的 SYN 包发送给服务器，使服务器处于"半开连接"状态，预分配大量内存并占用服务器的连接队列。由于 SYN 的客户端 IP 地址是伪造的，所以无 ACK 响应，致使服务器消耗内存和资源，无法建立新的连接。

一种解决方式是使用 **SYN Cookie**：不为每个半开连接都分配资源，而是采用延迟分配，在收到 ACK 后才创建连接、分配资源。

#### 序列号占用规则

在 [RFC 793](https://www.rfc-editor.org/rfc/rfc793) 中规定：

> For sequence number purposes, the SYN is considered to occur before the first actual data octet of the segment in which it occurs, while the FIN is considered to occur after the last actual data octet in a segment in which it occurs.

即连接建立和释放过程中的控制消息，虽然实际上都不携带数据（Payload），但对于 SYN 和 FIN 请求，占用 1 个序列号位置（相当于 1 Byte）。对于单独的 ACK，则不占用序列号。

### TCP 的连接释放

传统意义上，TCP 释放连接是"四次挥手"，即"一端发送 FIN、另一端返回 ACK、另一端发送 FIN、一端返回 ACK"。具体过程：

1. **第一次挥手（FIN）**：发起关闭连接的一方发送带有 FIN 标志的 TCP 段，表示它已经完成发送数据，希望关闭到对方方向的连接
2. **第二次挥手（ACK）**：接收方收到 FIN 包后，发送带有 ACK 标志的 TCP 段作为响应。此时，发起方到接收方的连接被关闭，但接收方仍然可以发送数据给发起方
3. **第三次挥手（FIN）**：当接收方也完成数据发送后，发送带有 FIN 标志的 TCP 段，请求关闭到发起方的连接
4. **第四次挥手（ACK）**：发起方收到 FIN 包后，发送带有 ACK 标志的 TCP 段作为响应。此时，接收方到发起方的连接也被关闭

???+ note "三次挥手"
    将中间两次挥手合并为 1 次也是可行的。如果上层在收到关闭连接请求后还有数据需要发送，FIN 包就不会立刻发送。TCP 默认开启了延迟确认机制，此时 ACK 会随要发送的数据一起发出，形成"四次挥手"；但如果上层并无数据需要发送，ACK 就会和 FIN 包合并发送，形成"三次挥手"。

### TCP 的连接模型

<figure markdown="span">
  ![TCP 连接状态模型](https://webp-pic.yokumi.cn/2026/01/20260101170553127.png){ loading=lazy width="70%" }
</figure>

### TCP 的流量控制

同样使用滑动窗口，与数据链路层的区别是面向字节，且窗口大小动态变化。

#### Window Probe 窗口探测

在 TCP 通信中，当接收方缓冲区满时，会告知发送方窗口大小为 0，此时发送方不能继续发送数据。当窗口恢复后，接收方会发送 Window Update 包告知发送方可以继续发送数据。但该包可能丢失，导致死锁。所以引入窗口探测机制：

1. 接收方通告窗口为 0（e.g. Window Size = 0）
2. 发送方停止发送数据，但保持连接
3. 发送方**周期性发送一个 1 字节的数据包**（或旧数据的一部分），强迫接收方回应当前窗口大小
4. 接收方回应 ACK，并通告新的窗口值
    - 若窗口仍为 0，发送方下次继续 probe
    - 若窗口增大了，发送方恢复正常发送

#### Silly Window Syndrome 糊涂窗口综合症

???+ info "概述"
    接收方应用层处理速度有限，每次只读取很少的数据，导致大部分数据还在缓冲区中，TCP 每次将这些很小的窗口通告给发送方，于是发送方也不断发送小包，造成带宽浪费。

    另一种情形是发送方应用层产生的就是持续的小包，同样造成带宽浪费。

    综上，糊涂窗口综合症可能由两方引起：

    1. 接收方不断通知小窗口
    2. 发送方不断发送小包

**发送方：Nagle 算法**

对于发送方，采用 **Nagle 算法**，基本思想是延迟发送小包，只有满足以下条件之一才进行发送：

- 收到之前发送数据的 ACK 回复
- 缓存的小包占满发送窗口的一半
- 缓存的小包 > MSS 最大报文长度

注意：Nagle 算法需要接收方满足"不回复小包的 ACK"，但与 Delayed ACK 一起作用并不能达到很好的效果，所以现代操作系统提供了禁用它的方法。

**接收方：Clark's 解决方案**

当可用窗口太小时，**不通告窗口更新**，直到能接收一个较大段再通告：

- 接收窗口超过 MSS
- 接收缓冲区有一半空了

### TCP 的差错控制

#### 累积确认

<figure markdown="span">
  ![TCP 累积确认](https://webp-pic.yokumi.cn/2026/01/20260101170558057.png){ loading=lazy width="70%" }
</figure>

#### 超时重传

与数据链路层类似，TCP 通信也设置了超时重传，即 **RTO (Retransmission Timeout)**。注意与 **RTT (Round-Trip Time)** 区分——RTT 是数据发送时刻到收到确认所需的时间，即包的往返时间。

RTO 过大和过小都会产生问题。

#### Fast Retransmission 快速重传

<figure markdown="span">
  ![快速重传示意图](https://webp-pic.yokumi.cn/2026/01/20260101170609940.png){ loading=lazy width="70%" }
</figure>

当发送方连续收到 3 个重复的 ACK，它就知道该包可能丢失，无需等待 RTO 超时就直接进行重传。

#### SACK 选择重传

快速重传仅仅解决了超时问题，但并未解决要重传多少包的问题。SACK 在 TCP Header 的 Option 字段被引入，用于告诉发送方"我已经正确接收到的数据"，这样发送方就能只重传丢失的特定的包。

#### 定时器的管理

TCP Timer 包括：

Retransmission Timer 重传计时器
: 即 RTO，超时重传计时

Persistence Timer 持续计时器
: 用于周期性地进行窗口探测，防止窗口为 0 的死锁

Keepalive Timer 保活计时器
: 当另一方始终静默时，发送一个包试探其是否还处于通信状态，防止半开连接

Time-Waited Timer 等待时间计时器
: Time-waited State：主动关闭连接的一方（先发 FIN 的那一方）在完成 TCP 四次挥手后，进入 `TIME_WAIT` 状态。该状态通常持续 `TIME_WAIT = 2 \times MSL`（Maximum Segment Lifetime），即最大报文生存时间的 2 倍

    - 作用一：确保对方正确收到了 ACK，双方都正确关闭连接（为自己第一次发送的 ACK 丢失、对方重发 FIN、自己重新回 ACK 预留时间）
    - 作用二：防止混入新的连接，确保连接已经完全关闭

#### 重传计时器的设置

##### 动态计算

传输层不同于数据链路层，网络情况瞬息万变，RTT 是动态变化的且变化有时还很剧烈，故采用动态的方法计算 RTT。

**Jacobson 算法**：

$$SRTT = \alpha \times SRTT + (1 - \alpha) \times \text{New\_Sample}$$

其中 New_Sample = 收到 ACK 的时刻 - 包发送出去的时刻，一般取 $\alpha = \frac{7}{8}$（越接近 1 越平滑）。

<figure markdown="span">
  ![Jacobson 算法](https://webp-pic.yokumi.cn/2026/01/20260101170612716.png){ loading=lazy width="70%" }
</figure>

$$RTTVAR = \beta \times RTTVAR + (1 - \beta) \times |SRTT - \text{Sample}|$$

一般取 $\beta = \frac{3}{4}$。

最终 RTO 按照如下公式确定：

$$RTO = SRTT + 4 \times RTTVAR$$

???+ note "RFC 6298 中的规定"
    标准 [RFC 6298](https://www.rfc-editor.org/rfc/rfc6298) 中，权值和上述是反的，同时还定义了初始化时：

    - SRTT = measured_RTT
    - RTTVAL = measured_RTT / 2
    - RTO = SRTT + max(G, 4 * RTTVAR)

    其中 measured_RTT 为第一次测量的 RTT 值，G 为时钟粒度。

##### Karn 算法

TCP 使用 RTT 来动态设置重传超时时间（RTO）。但在发生重传的情况下，如果收到一个 ACK，无法知道这个 ACK 是对第一次发送的数据还是对重传数据的响应，因此测量 RTT 会导致"错误关联"。

Karn 算法的核心思想：

1. 当收到的是重传数据包的 ACK，不更新 RTT
2. 在发生重传后，将 RTO 指数性增长（通常加倍）作为退避策略

### TCP 的拥塞控制

虽然在网络层中已经提到过拥塞控制，但实际工作中，网络层产生拥塞一般是因为上层发送的包过多，所以网络层一般用来检查拥塞，并通过显式或隐式通知通知上层，传输层需要控制发送速率（即调整发送窗口大小）。

#### 拥塞窗口

**拥塞窗口 (Congestion Window, cwnd)** 是 TCP 发送方维护的一个状态变量，定义了能够往网络中发送的字节数。速率 = cwnd / RTT。

接收窗口 rwnd 和拥塞窗口 cwnd 都是动态变化的：

$$swnd \leq \min(rwnd, cwnd)$$

通过丢包作为拥塞标志：

- 如何判断产生了拥塞？丢包，通过重传定时器时间内是否收到 ACK 判断
- 如何调整发送速率？正确收到 ACK 增大速率，丢包减小速率

#### Slow-Start 慢启动

慢启动的思想：初始时 cwnd = 1。当发送方每收到一个 ACK，cwnd 的大小就加 1。当发生丢包时，cwnd 重置为 1。

看似线性增长，实则不然：每次 cwnd + 1 后，一次发送的数据也 + 1，同样收到的 ACK 也 + 1，cwnd 一次性 + 2，所以事实上是**指数级增长**。

<figure markdown="span">
  ![慢启动指数增长](https://webp-pic.yokumi.cn/2026/01/20260101170616321.png){ loading=lazy width="70%" }
</figure>

慢启动还可以与 AIMD 结合使用，一旦速度超过慢启动阈值，就从慢启动切换为线性增长。

<figure markdown="span">
  ![慢启动与 AIMD 结合](https://webp-pic.yokumi.cn/2026/01/20260101170625156.png){ loading=lazy width="70%" }
</figure>

当有一个包超时时：$cwnd = 1,\; ssthresh = \frac{1}{2}ssthresh$

#### Fast Recovery 快速恢复

当收到 3 个重复的 ACK 时，慢启动阈值被设置为当前拥塞窗口的一半，拥塞窗口被设置为新的慢启动阈值，然后执行线性增长。即：

$$cwnd = \frac{1}{2}cwnd,\; ssthresh = cwnd$$

<figure markdown="span">
  ![快速恢复](https://webp-pic.yokumi.cn/2026/01/20260101170653528.png){ loading=lazy width="70%" }
</figure>
