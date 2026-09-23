# 介质访问控制子层

介质访问控制（Media Access Control, MAC）子层的核心任务是：为使用共享传输介质的节点隔离来自同一信道上其他节点的信号，协调各节点的传输行为，避免冲突并提高信道利用率。

## 动态信道分配

### 基本假设

1. 独立站点模型
: 各节点独立产生数据帧，帧的到达服从泊松过程。

2. 单信道
: 所有节点共享一条逻辑信道，任何节点发送的数据均可被所有节点接收。

3. 冲突可观测
: 若两个帧同时发送则产生冲突，冲突后所有节点均能感知。

4. 时间模型
: 连续时间（帧可在任意时刻开始发送）或分槽时间（帧只能在时隙起始时刻发送）。

5. 载波监听
: 发送前能否感知信道状态——有载波监听（CSMA）或无载波监听（ALOHA）。

## 随机介质访问控制

### ALOHA 协议

#### Pure ALOHA（纯 ALOHA）

- 任何时刻有数据即可发送；若未收到 ACK 则随机等待后重传。
- **脆弱期（Vulnerable Period）**：$2t_{\text{trans}}$

<figure markdown="span">
  ![Pure ALOHA](https://webp-pic.yokumi.cn/2026/01/20260101170124510.png){ loading=lazy width="70%" }
</figure>

???+ info "Pure ALOHA 流程"
    <figure markdown="span">
      ![Pure ALOHA 流程](https://webp-pic.yokumi.cn/2026/01/20260101170126910.png){ loading=lazy width="70%" }
    </figure>

    若未收到正确 ACK，则随机等待一段时间后重传。

#### Slotted ALOHA（分槽 ALOHA）

- 只能在每个时隙的开始时刻发送数据，需要统一时钟同步。
- **脆弱期**：$t_{\text{trans}}$（相比 Pure ALOHA 减半）

<figure markdown="span">
  ![Slotted ALOHA](https://webp-pic.yokumi.cn/2026/01/20260101170129010.png){ loading=lazy width="70%" }
</figure>

### CSMA 协议族

载波监听多路访问（Carrier Sense Multiple Access）：**发前先听**——若信道空闲以概率 $p$ 发送；若信道忙则等待直至空闲。

- **脆弱期**：$t_{\text{prop}}$

#### Nonpersistent vs. Persistent CSMA

| 策略 | 信道忙时行为 | 特点 |
| --- | --- | --- |
| Nonpersistent CSMA | 等待随机时间后再监听 | 高负载时吞吐量较高 |
| 1-Persistent CSMA | 持续监听至空闲后立即发送（$p=1$） | 低负载时延迟低、吞吐量高；高负载时吞吐量低 |
| p-Persistent CSMA | 监听至空闲后以概率 $p$ 发送 | $p$ 越小，高负载下冲突概率越低 |

???+ tip "$p$ 的作用"
    $p$ 越小，在高负载下随机化程度越好，冲突可能性越低。

### 协议吞吐量对比

<figure markdown="span">
  ![各 MAC 协议吞吐量对比](https://webp-pic.yokumi.cn/2025/07/20250729201448085.png){ loading=lazy width="70%" }
</figure>

!!! abstract "MAC 协议评价指标"
    1. 低负载时的时延
    2. 高负载时的吞吐量（或信道利用率）

    低负载时适合使用竞争方法。

上述协议的共性问题：发送方仅在超时后才知道冲突，**没有检测冲突的能力**。

### CSMA/CD（带冲突检测）

CSMA/CD = Carrier Sense Multiple Access with Collision Detection，是以太网的基础。

!!! abstract "CSMA/CD 基本思想"
    1. 载波监听：发前先听
    2. **发送方**检测冲突
    3. 冲突时停止传输，发送 **Jam Signal（强化信号）**
    4. **退避（Backoff）**：收到 Jam Signal 后等待随机时间再恢复发送（避免重复冲突）

特点：

- 信道为**半双工**（同一时刻节点只能发或收）
- 节省时间和带宽
- 是**以太网**的基础
- 属于无确认无连接服务（Unacknowledged Connectionless Service）

???+ question "冲突检测与脆弱期"
    **Q**：如何检测冲突？

    **A**：通过收线同时从总线接收信号，与发送信号进行比较。由于需要较强信号强度和合适的调制技术，**不适用于无线通信**。

    **Q**：脆弱期多长？

    **A**：Vulnerable Time = $2t_{\text{prop}}$

    **Q**：等待重传的时间如何确定？

    **A**：采用二进制指数退避算法。

#### 二进制指数退避

<figure markdown="span">
  ![二进制指数退避算法](https://webp-pic.yokumi.cn/2026/01/20260101170131152.png){ loading=lazy width="70%" }
</figure>

- 最多尝试 16 次
- 指数上限为 10
- 基础退避时间 = 51.2 μs

## 无线局域网中的 MAC 问题

无线信道无法进行冲突检测（信号强度太小，调制技术限制），CSMA/CD 不适用。

### 隐藏终端问题

<figure markdown="span">
  ![隐藏终端](https://webp-pic.yokumi.cn/2026/01/20260101170137521.png){ loading=lazy width="70%" }
</figure>

A、C 都需要向 B 发送数据，但 A 不在 C 的范围内——C 监听不到 A，导致 C 同时向 B 发送数据，接收方 B 冲突。

### 暴露终端问题

<figure markdown="span">
  ![暴露终端](https://webp-pic.yokumi.cn/2026/01/20260101170140237.png){ loading=lazy width="70%" }
</figure>

B 向 A 发送数据，C 在 B 的范围内，C 监听到 B 后错误地认为不能向 D 发送数据——白白浪费了信道。

### MACA 协议

MACA（Multiple Access Collision Avoidance，冲突避免多路访问）通过 RTS/CTS 预约信道：

1. 发送方 A 发送 **RTS（Request to Send）** 帧（30 字节，含数据包长度信息）
2. 接收方 B 回复 **CTS（Clear to Send）** 帧
3. A 收到 CTS 后开始发送数据
4. B 收到数据后回复 ACK

<figure markdown="span">
  ![MACA 协议示意](https://webp-pic.yokumi.cn/2026/01/20260101170143796.png){ loading=lazy width="70%" }
</figure>

???+ example "MACA 如何解决隐藏/暴露终端"
    对于上图，A 需向 B 发送数据：

    - C 和 E 是暴露终端，D 是隐藏终端
    - A 向 B 发送 RTS → C 和 E 都收到
    - B 向 A 发送 CTS → D 和 E 都收到
    - C 只收到 RTS，保持沉默
    - D 只收到 CTS，也保持沉默
    - E 同时收到 RTS 和 CTS，但 CTS 长度与 RTS 预告不一致，也保持沉默

若两个站点同时向同一接收方发送 RTS：

1. A、B 同时发送 RTS
2. 接收方只回复先到达的 RTS 对应的 CTS
3. 未收到 CTS 的站点采用**指数退避**等待后重试

## 控制介质访问控制

| 方式 | 控制模式 | 机制 |
| --- | --- | --- |
| Polling（轮询） | 集中式 | 主站依次向从站发出请求 |
| Token Passing（令牌传递） | 分布式 | 节点共同维护一个令牌，持有令牌者有权发送 |

## IEEE 802 参考模型

<figure markdown="span">
  ![IEEE 802 参考模型](https://webp-pic.yokumi.cn/2026/01/20260101170146064.png){ loading=lazy width="70%" }
</figure>

IEEE 802 标准只涵盖物理层和数据链路层，并将数据链路层进一步划分为两个子层：

LLC（逻辑链路控制）子层
: - 向网络层提供统一的接口
  - 流量控制与差错控制
  - 通过网桥互连不同 LAN

MAC（介质访问控制）子层
: - 成帧（Framing）
  - 差错检测
  - 物理地址（如 MAC 地址）
  - 多路访问控制
  - LAN 交换

!!! abstract "LLC 与 MAC 的分工"
    不同 LAN 的 MAC 子层不同，但 LLC 子层相同——LLC 为上层屏蔽底层差异。

<figure markdown="span">
  ![IEEE 802 各标准](https://webp-pic.yokumi.cn/2026/01/20260101170148513.png){ loading=lazy width="70%" }
</figure>

## 以太网

### 经典以太网：物理层

#### 物理拓扑

- **总线型**：所有节点共享同一条总线
- **星型**：通过 **Hub（集线器）** 实现——物理上星型，逻辑上总线型

#### 网卡（NIC）

<figure markdown="span">
  ![网卡结构](https://webp-pic.yokumi.cn/2026/01/20260101170150822.png){ loading=lazy width="70%" }
</figure>

#### 布线命名规范

`100 Base-T X` 解读：

- **100**：传输速率，单位 Mbps
- **Base**：基带传输，不需要调制
- **T**：传输媒介（T = 双绞线 Twisted Pair，F = 光纤 Fiber Optics）
- **X**：编码方式（通常为 Manchester 编码）

<figure markdown="span">
  ![经典以太网布线](https://webp-pic.yokumi.cn/2026/01/20260101170154607.png){ loading=lazy width="70%" }
</figure>

???+ tip "选择建议"
    距离长时用粗缆。

#### 中继器（Repeater）

- 属于**物理层**设备
- 半双工
- 将两个总线型以太网段连接

### 经典以太网：MAC 子层协议

- 广播式信道
- 采用 **1-Persistent CSMA/CD**
- **帧间隙（IFP）**：9.6 μs（10 Mbps 以太网），用于节点切换发送/接收模式

#### 帧格式

<figure markdown="span">
  ![以太网帧格式](https://webp-pic.yokumi.cn/2026/01/20260101170157888.png){ loading=lazy width="70%" }
</figure>

- Data 字段：最多 1500 字节，最少 46 字节（不足用 Pad 填充）
- MAC 地址：6 字节，广播地址为 `FF:FF:FF:FF:FF:FF`
- 帧长度：最短 64 字节（含 46 字节数据），最长 1518 字节（含 1500 字节数据）

???+ question "为什么最小帧长为 64 字节？"
    以太网使用 CSMA/CD，必须有足够时间检测冲突。否则数据已经发完才检测到冲突。

    $$\frac{M_{\min}}{B} = 2\tau = 51.2\,\mu\text{s}$$

### 交换式以太网

#### Hub vs. Switch

<figure markdown="span">
  ![Hub vs. Switch](https://webp-pic.yokumi.cn/2026/01/20260101170200819.png){ loading=lazy width="70%" }
</figure>

| 设备 | 行为 | 冲突域 |
| --- | --- | --- |
| Hub | 一个节点的信号向所有其他节点转发 | 所有节点在同一冲突域内，需要 CSMA/CD |
| Switch | 根据目的 MAC 地址选择性转发 | 每个端口独立冲突域，不需要 CSMA/CD |

#### 交换方式

| 方式 | 特点 |
| --- | --- |
| Cut-Through（直通） | 边收边转发，无法检查帧错误，要求输入/输出速率相同 |
| Store-Forward（存储转发） | 缓存整个帧后检查 CRC，再按目的 MAC 转发；支持差错检测和不同速率端口 |

### 快速以太网（100 Mbps）

设计原则：

- **向后兼容**：保持帧格式、接口等不变
- 减少 bit time
- 缩短最大电缆长度（必要牺牲）
- Hub 或 Switch 均可

#### 布线

<figure markdown="span">
  ![快速以太网布线](https://webp-pic.yokumi.cn/2026/01/20260101170203618.png){ loading=lazy width="70%" }
</figure>

| 标准 | 信号频率 | 媒介 | 编码 |
| --- | --- | --- | --- |
| 100Base-T4 | 25 MHz | 4 对双绞线（3 UTP） | 三元信号 6B/8T |
| 100Base-TX | 125 MHz | 2 对双绞线（5 UTP） | 4B/5B（125 MHz × 4/5 = 100 Mbps） |
| 100Base-FX | — | 光纤 | — |

!!! abstract "全双工与 CSMA/CD"
    若使用全双工（Full-Duplex），收发使用两条线，不会产生冲突，**不需要 CSMA/CD**。

#### 自动协商机制

两个不同以太网设备之间自动选择一致的参数（速率和双工模式）进行配置。

### 千兆以太网（1 Gbps）

速度再提升 10 倍，设计原则：

- 无 ACK（发了就完）
- 48-bit 地址格式不变
- 帧格式不变（但进行了扩展，否则最大电缆长度太短）
- 同样分 Switch（全双工，最大电缆长度取决于信号衰减）和 Hub（半双工，存在冲突）

#### 布线

<figure markdown="span">
  ![千兆以太网布线](https://webp-pic.yokumi.cn/2026/01/20260101170205960.png){ loading=lazy width="70%" }
</figure>

#### 载波扩展（Carrier Extension）

CSMA/CD 要求：

$$\frac{M_{\min}}{B} = 2\tau = 51.2\,\mu\text{s}$$

不扩展的话，最大电缆长度仅约 25 m。解决方案：将数据长度扩展至 **512 字节**（用无意义比特填充）。

<figure markdown="span">
  ![载波扩展](https://webp-pic.yokumi.cn/2026/01/20260101170209560.png){ loading=lazy width="70%" }
</figure>

#### 帧突发（Frame Bursting）

载波扩展对信道效率浪费严重。帧突发允许发送方将需要连续发送的帧拼接发送：

- 第一个帧采用载波扩展
- 后续帧直接连续发送（帧之间保留帧间隙）

<figure markdown="span">
  ![帧突发](https://webp-pic.yokumi.cn/2026/01/20260101170215299.png){ loading=lazy width="70%" }
</figure>

#### 流量控制

千兆以太网发送速度极快，若接收方 CPU 短暂繁忙（如 1 ms），就会导致 1953 个帧堆积，极易缓存溢出。

解决方案：**Pause Frame（暂停帧，类型码 0x8808）**——接收方缓存不足时发送该帧，阻止发送方继续发送数据。

### 10G 以太网

- 一般用于**本地骨干网**
- 只支持全双工
- 支持自动协商

#### 布线

<figure markdown="span">
  ![10G 以太网布线](https://webp-pic.yokumi.cn/2026/01/20260101170220896.png){ loading=lazy width="70%" }
</figure>

### 以太网总结

<figure markdown="span">
  ![以太网总结](https://webp-pic.yokumi.cn/2026/01/20260101170223449.png){ loading=lazy width="70%" }
</figure>

!!! abstract "以太网核心参数"
    - 1-Persistent CSMA/CD（使用 Switch 时不需要冲突检测）
    - MAC 地址 = 48 bits
    - 帧大小 = 64 字节 ~ 1518 字节（数据 46 ~ 1500 字节）
    - 拓扑：总线型（仅经典以太网）、星型
    - 物理层编码：Manchester（经典以太网）、8B/6T、4B/5B（百兆以后不再使用 Manchester）

## 无线局域网（802.11）

### 802.11 架构

<figure markdown="span">
  ![802.11 LAN 架构](https://webp-pic.yokumi.cn/2026/01/20260101170226832.png){ loading=lazy width="70%" }
</figure>

AP（Access Point，接入点）
: AP 与外部设备（路由器/交换机）之间有线连接。

BSS（Basic Service Set，基本服务集）
: 内部设备之间采用无线通信，通过 AP 接入外部网络。

### 802.11 MAC 子层

无线通信无法进行冲突检测（信号太弱、调制技术限制）。802.11 MAC 子层提供两种信道接入模式：

PCF（Point Coordination Function，点协调功能，集中式）
: - 由基站（AP）作为点协调控制者
  - 通过 **轮询（Polling）** 为各站点分配信道访问权
  - AP 按预设顺序依次询问站点是否需要发送数据
  - 基站广播 **Beacon Frame（信标帧）**（含系统参数、是否允许发言等）

DCF（Distributed Coordination Function，分布协调功能，分布式）
: - 无中央控制者
  - 通过 **CSMA/CA** 避免冲突

<figure markdown="span">
  ![PCF 与 DCF](https://webp-pic.yokumi.cn/2026/01/20260101170231083.png){ loading=lazy width="70%" }
</figure>

#### CSMA/CA

**发送方流程**：

1. 载波监听等待直到信道空闲，并在 **DIFS** 时间内信道持续空闲后才认为信道空闲
2. 随机退避（0 ~ 15 个时间槽），若信道上有数据发送则暂停计时器；计时器归零时发送帧
3. 若未收到 ACK，采用指数退避，加倍退避时间

**接收方流程**：

1. 正确接收帧后等待 **SIFS** 时间后回复 ACK

???+ tip "IFS 与优先级"
    $t_{\text{SIFS}} < t_{\text{DIFS}}$，保证 **ACK 优先级更高**。

    事实上，为不同类型帧设置不同长度的 **IFS（帧间隔）** 实现优先级服务。

#### CSMA/CA 的两种监听模式

Physical Sense（物理监听）
: 直接监听信道上的信号能量。

Virtual Sense（虚拟监听）
: 每个站点维护一个 **NAV（Network Allocation Vector，网络分配向量）**。

NAV
: 每个帧都携带 NAV，表示该帧预计占用信道的时间长度。站点通过 NAV 确定退避时间，减少冲突。

<figure markdown="span">
  ![CSMA/CA 与 NAV](https://webp-pic.yokumi.cn/2026/01/20260101170242762.png){ loading=lazy width="70%" }
</figure>

#### 段突发（Fragment Burst）

若信道误码率较高，ACK 和重传效率低。短帧出错概率小，因此将长帧分为小的 Fragment 逐段发送以提高可靠性。

<figure markdown="span">
  ![段突发](https://webp-pic.yokumi.cn/2026/01/20260101170246588.png){ loading=lazy width="70%" }
</figure>

#### 省电模式

<figure markdown="span">
  ![省电模式](https://webp-pic.yokumi.cn/2026/01/20260101170249399.png){ loading=lazy width="70%" }
</figure>

#### TXOP（Transmission Opportunities）

原始 CSMA/CA 采用频繁竞争——每次发送都竞争，谁竞争成功谁发。这导致速率异常：

$$\frac{1}{c_{\text{ave}}} = \frac{1}{c_1} + \frac{1}{c_2} \Rightarrow c_{\text{ave}} = \frac{1}{\frac{1}{c_1} + \frac{1}{c_2}}$$

平均数据率小于任何一个站点，造成速率异常。

TXOP 的改进：竞争一次，获得一段传输时间，各站点按比例分享：

$$c = \frac{c_i}{n}$$

例如 6 Mbps 和 54 Mbps 的两个站点，采用 TXOP 后按 3 Mbps 和 27 Mbps 发送帧。

#### 802.11 帧类型

Data Frame（数据帧）
: 承载上层用户数据。

Control Frame（控制帧）
: RTS、CTS、ACK——用于信道预约和确认。

Management Frame（管理帧）
: Authentication / De-authentication、Association、Beacon / Probe Frame——用于网络管理和关联。
