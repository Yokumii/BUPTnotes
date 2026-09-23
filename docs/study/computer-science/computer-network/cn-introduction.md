# 计算机网络概述

## 什么是计算机网络

计算机网络
: 一组**自主工作的、相互连接的**（separate but interconnected）计算机的集合

!!! warning "易混淆概念"
    - **分布式系统（Distributed System）**：建立在网络之上的软件系统，对用户透明，表现为一台计算机
    - **计算机网络**：计算机自主工作并通过技术互连，所有计算机对用户可见
    - **Internet（因特网）**：全球范围的互联网，特指诞生于美国的全球性网络
    - **internet（互联网）**：网络的网络（network of networks），泛指任何互连的网络
    - **WWW（万维网）**：运行在 Internet 之上的分布式系统/应用

## 网络服务质量（QoS）

Latency / Delay（延迟）
: 数据传输的绝对时间差

Jitter（抖动）
: 不同数据包到达时间的相对差异

Bandwidth（带宽）
: 网络单位时间内传输的数据量，通常以 bps（比特每秒）为单位

Bit-Error-Rate / BER（比特差错率）
: 传输中出错比特数与总比特数的比率

!!! tip "实时视频会议的关键 QoS 指标"
    Latency 和 Bandwidth 是实时视频会议中最关键的指标。

## 网络硬件组成

节点（Nodes）
: 包括主机/终端（End Systems）和交换设备（Switches / Routers）

通信链路（Communication Links）
: 有线或无线的传输介质

???+ info "Infrastructure Network vs. Ad Hoc Network"
    | 类型 | 特点 |
    |------|------|
    | Infrastructure Network | 基于固定基础设施（路由器、交换机、接入点）构建 |
    | Ad Hoc Network | 去中心化，设备直接相互通信，无需固定基础设施 |

## 网络分类

### 按位置

- **接入网（Access Network）**：连接用户到核心网络的边缘部分
- **数据中心网络（Data Center Network）**：数据中心内部的高速互连网络
- **传输网（Transmission Network）**：核心骨干传输网络

### 按传输技术

单播（Unicasting）
: 点对点链路，中间设备一般为 Router；WAN 通常采用单播以避免通信量过大

广播（Broadcasting）
: 一对多传输；多播（Multicasting）是广播的子集，面向特定组

### 按规模

| 类型 | 全称 | 典型技术 |
|------|------|----------|
| PAN | 个域网 | 蓝牙、RFID |
| LAN | 局域网 | Ethernet、WiFi |
| MAN | 城域网 | Cable TV 广播电视 |
| WAN | 广域网 | 3G、4G、5G |
| The Internet | 因特网 | 全球范围的互连网络 |

!!! note "Internet 与 internet 的区分"
    Internet 特指全球范围的因特网；internet 泛指任何互连的网络（network of networks）。

## 网络体系结构

<figure markdown="span">
  ![网络体系结构示意图](https://webp-pic.yokumi.cn/2026/01/20260101165856712.png){ loading=lazy width="70%" }
</figure>

协议（Protocol）
: 对等层之间通信的规则约定

接口（Interface）
: 相邻两层之间的交互点，**下层为相邻的上一层提供服务/接口**

对等实体（Peers）
: 不同节点上同一层的实体

网络体系结构（Network Architecture）
: **包括 Layers 和 Protocols，不包括 Interface**；协议实现的细节与体系结构无关

协议栈（Protocol Stack）
: 各层协议按层次排列的整体

PDU（Protocol Data Unit）
: 对等层之间虚拟通信的数据包，由协议决定格式

封装（Encapsulation）
: 上层向下层传输时添加**控制消息头**，构成本层的 PDU

## 服务分类

### 面向连接服务（Connection-Oriented）

1. 先建立连接
2. 传送数据（Message 报文 / Packet 分组）
3. 释放资源

!!! info "面向连接的特点"
    传输顺序固定，较为可靠。

### 无连接服务（Connectionless）

!!! info "无连接的特点"
    动态分配资源（数据到达时才分配），每条消息和分组需携带完整目标地址，数据易丢失。

### 服务原语

<figure markdown="span">
  ![服务原语](https://webp-pic.yokumi.cn/2026/01/20260101165859300.png){ loading=lazy width="70%" }
</figure>

基本概念：

SAP（Service Access Point）
: 服务访问点，即接口 Interface

- Service Provider：Layer $n$（下层提供服务）
- Service User：Layer $n+1$（上层使用服务）

???+ info "服务原语示例"
    **DNS 解析过程：**

    <figure markdown="span">
      ![DNS解析的服务原语](https://webp-pic.yokumi.cn/2026/01/20260101165904621.png){ loading=lazy width="70%" }
    </figure>

    **浏览网页过程：**

    <figure markdown="span">
      ![浏览网页的服务原语](https://webp-pic.yokumi.cn/2026/01/20260101165907479.png){ loading=lazy width="70%" }
    </figure>

### 服务与协议的关系

- 本层协议的实现**依赖**下层服务（下层变化可能影响本层协议实现）
- 本层协议的实现**依赖**本层服务支持
- 本层服务不变时，本层协议实现的变化**不影响**上层

## 参考模型

### OSI 七层模型

<figure markdown="span">
  ![OSI七层模型](https://webp-pic.yokumi.cn/2026/01/20260101165911378.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![OSI模型数据传输过程](https://webp-pic.yokumi.cn/2026/01/20260101165914775.png){ loading=lazy width="70%" }
</figure>

!!! abstract "OSI 各层职责"
    数据经中间路由转发时，实际只涉及**物理层、数据链路层、网络层**（1-3 层）；只有两端节点涉及**传输层、会话层、表示层、应用层**（4-7 层）。

### TCP/IP 四层模型

标准定义为 4 层：

| 层 | 核心协议 | 特点 |
|----|----------|------|
| Application | 各种应用协议 | 面向用户 |
| Transport | TCP / UDP | TCP 面向连接；UDP 无连接 |
| Internet | IP | 分组交换、无连接 |
| Link | 各种链路协议 | 负责物理传输 |

<figure markdown="span">
  ![TCP/IP四层模型](https://webp-pic.yokumi.cn/2026/01/20260101165918962.png){ loading=lazy width="70%" }
</figure>

### 五层混合模型

在 TCP/IP 模型基础上将物理层单独划分出来，形成 5 层混合模型：

| 层 | 名称 |
|----|------|
| 5 | Application Layer |
| 4 | Transport Layer |
| 3 | Network Layer |
| 2 | Data Link Layer |
| 1 | Physical Layer |
