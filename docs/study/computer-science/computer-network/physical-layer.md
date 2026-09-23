# 物理层

物理层是计算机网络体系结构的最底层，负责在物理媒体上传输原始比特流，为数据链路层提供透明的比特传输服务。本文围绕带宽与信道容量、传输介质、数字通信系统、复用技术和交换方式等核心主题展开。

## 基本概念

信道带宽
: $f_{max} - f_{min}$，单位 Hz

    - **Analog Bandwidth**：模拟信号用 Hz 表示
    - **Digital Bandwidth**：数字信号用 bps 表示
    - **Low-pass channel**：低通信道，$f_{min} = 0$
    - **Band-pass channel**：带通信道，$f_{min} > 0$

比特率 (Bit Rate)
: 单位 bps，表示每秒传输的比特数

波特率 (Baud Rate)
: 单位 Baud，每秒信号单元的数量

    设一个信号单元的时间为 $T$，则：

    $$\text{Baud Rate} = \frac{1}{T}$$

    $$\text{Bit Rate} = \text{Baud Rate} \times \log_2(\text{有效状态数})$$

信道容量
: 信道的最大数据率

吞吐量
: 单位时间内网络实际传送的数据位数，单位 bps

带宽时延积 (Bandwidth-Delay Product)
: 表示充满整个链路的 bit 数，反映信道的缓存能力

    $$\text{BDP} = \text{propagation delay} \times \text{bandwidth}$$

!!! info "时延的组成"
    - **发送时延 (Transmission Delay)**：$\displaystyle\frac{\text{Message Length (bits)}}{\text{Bandwidth (bps)}}$
    - **传播时延 (Propagation Delay)**：$\displaystyle\frac{\text{length of physical link}}{\text{propagation speed in medium}}$
    - 节点处理时延
    - 排队时延

## 信道容量

### 无噪信道 — Nyquist Bit Rate

理想无噪信道的最大传输速率由奈奎斯特公式（Nyquist Bit Rate, 1924）给出：

$$C = 2 \times B \times \log_2(L)$$

其中 $C$ 为信道容量（bps），$B$ 为带宽（Hz），$L$ 为信道级数（即有效状态数）。

???+ warning "注意"
    上述公式给出的是理想情况下的最大传输速率，实际信道通常有噪声。

### 有噪信道 — Shannon Capacity

有噪信道的传输速率由香农公式（Shannon Capacity, 1948）给出：

$$C = B \times \log_2\left(1 + \frac{S}{N}\right)$$

其中 $S/N$ 为**信噪比 (SNR)**，也可用分贝表示：

$$\text{SNR}_{db} = 10 \log_{10}\left(\frac{S}{N}\right)$$

## 传输介质

### 分类总览

传输介质可分为导向型（有线）和非导向型（无线）两大类：

导向型
: - **双绞线 (Twisted Pair)**
    - **同轴电缆 (Coaxial Cable)**
    - **光纤 (Fiber Optics)**
    - 电力线 (Power Lines)

非导向型
: - **无线电 (Radio)**
    - **地面微波 (Microwave)** 与 **卫星通信 (Satellite)**
    - 红外线与可见光通信

### 频率范围

| 传输介质 | 频率范围 |
|---|---|
| 双绞线 | $0 \sim 10^8$ Hz |
| 同轴电缆 | $10^3 \sim 10^9$ Hz |
| 光纤 | $10^{14} \sim 10^{15}$ Hz（可见光范围） |
| 无线电波 | $10^4 \sim 10^9$ Hz |

### 传输介质的关键特性

- 带宽
- 传播时延
- 最大传输距离（不加放大器）
- 抗干扰能力
- 安全性
- 安装维护难度与成本

### 双绞线 (Twisted Pair)

- 两根通电铜导线拧合在一起，使产生的磁场相互抵消
- 既能传模拟信号（电话线），又能传数字信号（以太网）
- 拧得越紧，辐射强度越小，抗干扰能力越强
- UTP（无屏蔽）与 STP（有屏蔽）；STP 多一层 Metal Shield，减少向外辐射和衰减，增强抗干扰能力
- Category 编号越大，带宽越高

### 同轴电缆 (Coaxial Cable)

- 比 双绞线 有更好的屏蔽性和更大的带宽
- 50-ohm 电缆：基带同轴（早期以太网）
- 75-ohm 电缆：宽带同轴（适合传输模拟信号，如电视网）
- 抗干扰能力较强

### 光纤 (Fiber Optics)

利用光的全反射原理传输信号。

多模光纤 (Multimode)
: 多种入射角，不同模之间有干扰

单模光纤 (Single-mode)
: 只有一种入射角，模间干扰小，**带宽更宽**

???+ note "光纤环网"
    <figure markdown="span">
      ![光纤环网](https://webp-pic.yokumi.cn/2026/01/20260101165921513.png){ loading=lazy width="70%" }
    </figure>

    - **Optical Receiver**：将光信号转化为电信号（光敏电阻）
    - **Signal Regenerator**：对电信号放大整形，可选择发送到计算机或继续传输
    - **Optical Transmitter**：将电信号重新转化为光信号（发光二极管）

光纤的优点：带宽大、抗干扰能力强、安全性好、轻便。

### 无线传输介质

相较于有线传输，无线传输具有更高的误码率、更大的传播时延和传输损耗，安全性也更弱。同一空间内同一频率会相互干扰，带宽不可再生。

#### 无线电波 (Radio)

<figure markdown="span">
  ![无线电波传播方式](https://webp-pic.yokumi.cn/2026/01/20260101165924652.png){ loading=lazy width="70%" }
</figure>

- 低频段：波长较大，可沿地球表面传播
- 高频段：波长较小，沿直线传播，需中继站
- 超高频以上：需视距范围内中继站传播

#### 地面微波 (Microwave)

直线传输，适合长距离通信，需地面中继站（典型设备：**Repeater 中继器**，负责信号整形和放大）才能实现远距离传输。

### 卫星通信

通信卫星相当于微波通信中 中继器 的角色，但在大气层以外。

转发器 (Transponder)
: 卫星上的典型设备，工作流程：

    - 监听地面天线发出的上行电波
    - 对收到的电波进行放大 (Amplify)
    - 以**另一种频率**的下行电波**广播**发送给范围内的地面天线

<figure markdown="span">
  ![通信卫星分类](https://webp-pic.yokumi.cn/2026/01/20260101165934036.png){ loading=lazy width="70%" }
</figure>

通信卫星按轨道高度分类：

GEO
: 地球同步轨道，覆盖全球所需卫星数量少，但时延高

MEO
: 中地轨道

LEO
: 近地轨道，时延低但需要更多卫星

!!! abstract "卫星通信的特点"
    - 传播时延长
    - 先天的广播介质
    - 传输成本与传输距离无关
    - 不受地面环境影响

## 数字通信系统

<figure markdown="span">
  ![数字通信系统示意图](https://webp-pic.yokumi.cn/2026/01/20260101165936526.png){ loading=lazy width="70%" }
</figure>

### 典型设备

Modem（调制/解调器）
: 将信号调整为适合信道传输的频率范围：基带信号 $\rightarrow$ 带通信号

    - **基带信号**：$0 \sim f_{max}$ Hz
    - **带通信号**：$f_1 \sim f_2$ Hz，$f_1 > 0$

Codec（编解码器）
: 将模拟信号与数字信号相互转换

Multiplexer（多路复用器）
: 将多路信号复用在一条传输介质上，提高信道利用率

信道编码器
: 将 01 信号转化为抗干扰能力更强的方波

### 线路编码 (Line Code)

用于基带传输 (Baseband Transmission)。

<figure markdown="span">
  ![线路编码](https://webp-pic.yokumi.cn/2026/01/20260101165939948.png){ loading=lazy width="70%" }
</figure>

NRZ（不归零编码）
: 抗干扰能力不强

Manchester 编码
: 用 "low to high" 表示 0，"high to low" 表示 1；电平变化发生在时钟周期中间，具有**自同步**功能

AMI 编码
: 1 用 "+1""-1" 间隔表示

???+ note "线路编码的评价指标"
    <figure markdown="span">
      ![时钟恢复示意](https://webp-pic.yokumi.cn/2026/01/20260101165941748.png){ loading=lazy width="70%" }
    </figure>

    - **时钟恢复 (Clock Recovery)**：能否从信号流中提取时钟频率
    - **平衡信号 (Balanced Signals)**：能否消除直流分量；Manchester 和 AMI 编码均可
    - **带宽效率 (Bandwidth Efficiency)**：Manchester 编码仅 50%

### 调制技术 (Modulation)

用于带通传输 (Passband Transmission)。

<figure markdown="span">
  ![调制技术](https://webp-pic.yokumi.cn/2026/01/20260101165946092.png){ loading=lazy width="70%" }
</figure>

从上到下依次为：

- 原始二进制信号
- **2ASK**：振幅调制（幅移键控）
- **2FSK**：频率调制
- **2PSK**：相位调制

#### 多级调制技术

同时利用振幅和相位表示比特位，提高每个信号单元携带的比特数。

- **QPSK**：正交相移键控
- **QASK**：正交幅度调制

<figure markdown="span">
  ![多级调制技术](https://webp-pic.yokumi.cn/2026/01/20260101165948313.png){ loading=lazy width="70%" }
</figure>

星座图中：振幅对应点与原点的距离，相位对应点与原点的连线和 x 轴的夹角。

### 模拟信号数字化 — PCM

PCM（Pulse Coding Modulation，脉冲编码调制）将模拟信号转化为数字信号，分为三个阶段：

1. **采样 (Sampling)**：根据 Nyquist 理论，采样率应至少是信号最高频率的 2 倍
2. **量化 (Quantizing)**
3. **编码 (Encoding)**

典型设备：Codec 编解码器。

## 复用技术 (Multiplexing)

复用技术将多路信号合并到一条传输介质上，提高信道利用率。关键设备：**Multiplexer**（如 DSLAM 数字用户线接入复用器）。

### 频分复用 (FDM)

将多路信号通过傅里叶变换分成频率范围各不相同的信号合成一路传输，再通过带通滤波器分离。信号之间一般存在**保护频带**。

### 时分复用 (TDM)

将每路信号在时间上分为多个**时隙 (Timeslot)**，信号被分到不同时间片发送。

#### 同步时分复用 (Synchronous TDM)

每个发送帧都为每路信号保留固定空间。缺点是数字信号传输往往不连续，易造成资源浪费。在电话网络中应用较广。

#### 统计时分复用 (Statistical TDM)

只发送需要发送的数据，按需复用，但需要加上地址头 (Address) 作为用户标识。

<figure markdown="span">
  ![时分复用](https://webp-pic.yokumi.cn/2026/01/20260101165950402.png){ loading=lazy width="70%" }
</figure>

- T1 线路：24 路
- E1 线路：30/32 路（其中 2 路为控制信号）

### 码分复用 (CDM)

不同用户可在任意时间使用整个频带发送信息，通过编码理论区分不同用户。

!!! tip "码分复用的通俗类比"
    如同教室中不同小组用不同语言同时讨论——需要接收某组信息时，只需知道该组使用的"语言"，屏蔽其他组。但组越多，噪声越大，接收越困难。

### 波分复用 (WDM)

波长与频率成反比，故 波分复用 与 频分复用 类似，主要用于**光纤通信**。

<figure markdown="span">
  ![波分复用](https://webp-pic.yokumi.cn/2026/01/20260101165953058.png){ loading=lazy width="70%" }
</figure>

!!! summary "线路编码 vs 调制"
    - **Line Code（线路编码）**：用于基带传输 (Baseband Transmission)
    - **Modulation（调制）**：用于带通传输 (Passband Transmission)

## 应用示例：电话网

### 传统电话网

<figure markdown="span">
  ![电话网示例](https://webp-pic.yokumi.cn/2026/01/20260101165955810.png){ loading=lazy width="70%" }
</figure>

1. 语音信号通过**本地环路 (Local Loop)** 到达 **Codec**，将模拟信号转化为数字信号
2. 语音信号带宽约 $4$ kHz，根据 Nyquist 定理需 $8k$ 采样率（每 $125\,\mu s$ 采样一次），1 sample = 8 bits（非线性编码），比特率 = $8k \times 8 = 64$ kbps
3. Codec 将数字信号通过**中继线 (Trunk)** 发往路由器/交换机，使用时分复用

### 通过电话线接入网络

<figure markdown="span">
  ![电脑通过电话线接入网络](https://webp-pic.yokumi.cn/2026/01/20260101170003131.png){ loading=lazy width="70%" }
</figure>

电脑发送 01 比特串，先通过 **Modem**（使用 QAM 正交幅度调制）将数字信号转化为模拟信号，后续步骤类似电话网络。

<figure markdown="span">
  ![ADSL 频谱分配](https://webp-pic.yokumi.cn/2026/01/20260101170008122.png){ loading=lazy width="70%" }
</figure>

其中 $-1$ bit 是因为 1 位用于检错。

### DSL — 数字用户线

DSL 在短距离内可提供较大带宽，但随距离增加带宽急剧下降。

#### ADSL — 非对称数字用户线

将本地环路上的 $1.1$ MHz 频谱分为 256 条独立信道（每条约 $4.3$ kHz）：

- Channel 0：**POTS 电话服务**
- Channel 1--4：保护隔离
- 剩余 250 条分为上行流 (Upstream) 和下行流 (Downstream)，其中 2 条用于控制，实际用于用户数据的是 248 条

#### DMT — 离散多音调制

<figure markdown="span">
  ![DMT 离散多音调制](https://webp-pic.yokumi.cn/2026/01/20260101170010366.png){ loading=lazy width="70%" }
</figure>

## 交换方式

### 电路交换 (Circuit Switching)

面向连接的交换方式，过程分为三个阶段：

1. 电路建立 (Circuit Establishment)
2. 数据传输 (Data Transfer)
3. 电路释放 (Circuit Disconnect)

!!! abstract "电路交换的优缺点"
    **优点**
    
    - 时延小
    - 传输质量好
    - 易于控制
    
    **缺点**
    
    - 建立连接需较长时间
    - 带宽固定，不灵活
    - 双方不发送数据时浪费信道
    
    典型例子：电话网

### 报文交换 (Message Switching)

在每个节点，收到的整个报文被存储后再转发（Store-and-Forward）。

<figure markdown="span">
  ![报文交换](https://webp-pic.yokumi.cn/2026/01/20260101170013580.png){ loading=lazy width="70%" }
</figure>

缺点：需较大缓存空间，不适合大消息传输。典型例子：邮局。

### 分组交换 (Packet Switching)

数据发送前被分为不同的**分组 (Packet)**，每个分组独立进行路由选择（需携带路由信息），每个分组到达节点后进行**存储-转发**，资源**动态分配**。

<figure markdown="span">
  ![分组交换与电路交换对比](https://webp-pic.yokumi.cn/2026/01/20260101170018125.png){ loading=lazy width="70%" }
</figure>

## 物理层协议规范

物理层协议从以下四个方面规定接口标准：

机械特性 (Mechanical Features)
: 接口形状和尺寸、引线数目和排列、固定和锁定装置等

电气特性 (Electrical Features)
: 电缆线上的电压范围

功能特性 (Functional Features)
: 某条线上出现的某一电平的电压的意义

过程特性 (Procedure Features)
: 对于不同功能的各种可能事件的出现顺序
