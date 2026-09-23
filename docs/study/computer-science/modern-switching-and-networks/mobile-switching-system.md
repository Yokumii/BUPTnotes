# 移动交换系统

## 移动通信的基本概念

* **移动通信的本质**：移动通信本质上是一个在 <u>**复杂、不可靠的物理空间**</u>（大气空间）中，为用户建立 <u>**高效、可靠、安全**</u> 的数字信息通道的任务。
    * 主要关注的是两个方面：<u>**效率**</u> 和 <u>**可靠性**</u>。
* 为了解决资源的稀缺性，网络必须采用 <u>**频率复用**</u> 等技术来提高效率。
* “<u>**蜂窝**</u>”概念的提出解决了移动通信中频率资源有限的问题，蜂窝组网标志着“无线”到“移动”的转变，关键技术包括 <u>**频率复用**</u>、<u>**移动性管理**</u>。
    * 每个蜂窝基站 $\rightarrow$ 一组频段 $\rightarrow$ 一个地理区域，即“蜂窝”/“小区”。
    * 若干相邻小区 $\rightarrow$ 形成一个区群/簇 $\rightarrow$ 可使用整个系统的全部频段。
    * 频段被分配给同一簇内的不同小区，要求相邻小区使用不同子频段。
    * 不同簇内对应位置的小区可以使用相同的子频段 $\rightarrow$ 同频小区 $\rightarrow$ 存在同频干扰
* **无线信道**：移动通信中，移动台和基站之间的信息通道。
    * 分类：
        * 逻辑信道
        * 传输信道
        * 物理信道
    * 特点：多径衰落与时变特征
        * 大尺度衰落：路径损耗 + 阴影衰落
        * 小尺度衰落：多径衰落 + 多普勒频移
    * 抗衰落技术：
        * 分集接收
        * 自适应均衡
        * 纠错编码
* **移动性管理技术**：通过 <u>**位置跟踪**</u>、<u>**无缝切换**</u>、<u>**高效寻呼**</u> 等机制，保证终端在移动中“通信不中断、服务不掉线”：
    * 核心功能：
        * **位置管理**（移动通信的**基础**）：解决“网络如何知道移动终端在哪”问题，确保移动台能在移动中被寻呼到。
            * 位置登记
            * 呼叫传递
            * 位置更新（终端位置变化时上报）
            * 寻呼（Paging）（网络通过全网或区域广播找到空闲状态终端的机制）
        * **切换管理**：实现网络实体跨覆盖区域的无缝业务衔接，保证移动台在移动中通信不中断。它涉及三个关键问题：
            * 越区切换准则（何时切）
            * 切换控制（如何切）
            * 信道分配

## 移动通信系统架构的演进 (2G - 5G)

移动通信系统由 <u>**移动终端（Mobile Terminal, MT）**</u>、<u>**无线接入网（Radio Access Network, RAN）**</u> 和 <u>**核心网（Core Network, CN）**</u> 和 <u>**外网**</u> 四大部分组成。

### GSM（2G）

!!! warning
    完全过时的内容，22 级（2025年）开始应该就不考了。

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629144618904.png){ loading=lazy width="70%" } </figure>

采用**电路交换**，基于模拟/数字技术，主要服务语音业务。

分为：

* **MS（Mobile Station）**：移动台，用户终端设备。包括**移动终端（ME）**、**手机客户识别卡（SIM）**。
* **BSS（Base Station Subsystem）**：无线基站子系统，由 MSC（移动交换中心） 控制，是与 MS 通信的系统设备。主要完成无线发送接收和无线资源管理等功能。包括
    * BTS（Base Transceiver Station）：基站收发信机，完成无线传输、无线与有线的转换、无线分集、无线信道加密。
    * BSC（Base Station Controller）：基站控制器，连接 BTS 与 MSC、为 BTS 和 OMC 的信息交换提供接口，具有控制一个或多个 BTS 的功能。完成无线网路资源的管理、呼叫和通信链路的建立与拆除、本控制区内 MS 越区切换的控制、小区配置数据管理、功率控制等。
* **NSS（Network Switching Subsystem）**：交换网路子系统，完成交换功能、完成客户数据、移动性管理、安全性管理所需的数据库功能。
    * MSC（Mobile Switching Center）：移动交换中心，蜂窝通信网络的核心，对位于本 MSC 控制区内的移动用户进行通信控制和管理。完成信道的管理和分配、呼叫的处理和控制、用户位置信息的登记与管理、越区切换和漫游的控制、用户号码和移动设备号码的登记和管理、服务类型的控制、用户鉴权、为系统中连接其他 MSC 和其他公用通信网络（PSTN、ISDN、PDN）提供链路接口。
    * HLR（Home Location Register）：归属位置寄存器，存储本地用户位置信息的数据库。每个用户都必须在某个 HLR（相当于该用户的原籍）中登记。
    * VLR（Visitor Location Register）：访客位置寄存器，存储本地用户位置信息的数据库。一个 VLR 可以为一个或多个相邻 MSC 服务。
    * AUC（鉴权中心）：可靠地识别用户的身份，只允许有权用户接入网络获得服务。
    * EIR（设备标志寄存器）：存储移动台设备参数的数据库。识别用户的 IMEI，对移动设备进行鉴别和监视，拒绝非法移动台入网。
    * SMS-SC（短信息业务中心）：提供点对点短信服务和广播式公共信息服务。
    * GMSC（网关交换中心）：负责移动交换网络与 PSTN 固话网络的互联互通。进行信令控制与话音转发。

??? info "例题 1（2013-2014）"
    写出下列 GSM 网络设备对应功能的序号：

    | 网络设备 | 对应序号 | 功能 |
    | --- | --- | --- |
    | **GMSC** | ① | ① 负责与固定电话网互联互通 |
    | **MSC** | ④ | ② 存放所属网络的用户数据 |
    | **HLR** | ② | ③ 对接入 GSM 网络的用户进行认证 |
    | **BTS** | ⑥ | ④ GSM 网络的交换设备，负责呼叫处理等功能 |
    | **EIR** | ⑦ | ⑤ 分配移动 IP 地址 |
    | **AUC** | ③ | ⑥ 完成空中无线信号的收发 |
    | **GGSN** | ⑤ | ⑦ 对接入 GSM 网络的移动终端设备进行认证 |

### GPRS（2.5G）

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629145442048.png){ loading=lazy width="70%" } </figure>

引入了分组域，呈现电路域与分组域重叠、**电路交换与分组交换共存**的网络结构（增加了SGSN、GGSN网元）。

* BSC 新增 PCU，属于分组域，负责移动分组数据的组装和拆解。
* SGSN：功能类似 MSC/VLR。
* GGSN：功能类似 GMSC。

??? info "例题 1（2016-2017）"
    目前有很多智能手表，比如小米手表、华为手表，主要面向儿童群体。家长可以对儿童手表进行定位、语音通信，大部分产品要求用户的 SIM 卡开通 GPRS 功能。

    1. 以前述手表为例，在下图方框中填入相关的网元（HLR、BSC、GGSN、MSC、VLR、SGSN、BTS、GMSC）；
    2. 并在图中标示出手表发送定位信息和语音通信的路径；
    3. 在这些网元设备中，哪个负责手表 IP 地址的分配？

    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260630111020432.png){ loading=lazy width="70%" } </figure>

    * 儿童手表定位信息一般通过 **GPRS 分组数据业务**上传到服务器，所以走 PS 域：
        * `手表 → BTS → BSC → SGSN → GGSN → Internet → 定位服务器 / 家长手机 App`
        * 其中 HLR 参与用户鉴权、业务签约信息查询等过程
    * 语音通信走**电路交换 CS 域**：
        * `手表 → BTS → BSC → MSC → GMSC → PSTN / 其他移动网`
        * 其中 MSC 需要结合 VLR、HLR 完成用户位置登记、鉴权、呼叫接续等功能
    * 负责手表 IP 地址分配的是： **GGSN**，它是移动分组数据业务的网关，负责与外部 IP 网络互联互通，并为移动终端分配 IP 地址。

### UMTS（3G）

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629145646397.png){ loading=lazy width="70%" } </figure>

* 3GPP-R99：核心网是构建在**电路域**之上的
* **3GPP-R4**：引入了**承载和控制相分离的软交换架构**，将 MSC 拆分为 MSC Server（MSS，控制）和媒体网关（MGW，承载），是**向分组交换演进**的关键一步
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629150121101.png){ loading=lazy width="70%" } </figure>
* **3GPP-R5**：提出全 IP 承载网络，核心网分为电路域（CS，处理语音业务）、分组域（处理数据业务）和**多媒体域（IMS，处理多媒体业务）**。
    * CS 和 IMS 按照控制/承载分离的原则，分别由 MSC Server 和 Call Session Control Function（CSCF）控制。

### LTE（4G）

!!! warning
    从这里开始也许是新的重点了。

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629154006571.png){ loading=lazy width="70%" } </figure>

从手机 UE，经无线接入网 E-UTRAN，到核心网 EPC，再连接外部 IP 网络。

* **UE（User Equipment）**：用户设备，移动终端。包括**移动终端（ME）**、**用户身份模块（USIM）**。
    * ME（Mobile Equipment） 是手机终端本体，负责无线收发、协议处理、业务运行。
    * USIM 是 SIM/USIM 卡，保存用户身份、鉴权密钥、运营商信息。
* **E-UTRAN**（Evolved Universal Terrestrial Radio Access Network）：无线接入网，**核心网元是 eNodeB**，也就是 **LTE 基站**，负责：
    * 无线资源调度，比如给用户分配时频资源；
    * 无线承载建立与释放；
    * 上下行数据转发；
    * 移动性管理中的切换控制；
    * 加密、完整性保护等部分接入层安全功能。
* **EPC**（Evolved Packet Core）：LTE 的**分组核心网**。LTE 是**全 IP 网络**，语音、视频、网页等业务都承载在 IP 数据通道上，包括以下核心网元：
    * **MME（Mobility Management Entity, 移动管理实体）**：**控制面核心网元**，主要负责用户附着、鉴权、位置管理、寻呼、承载控制和切换控制。图中 eNodeB 到 MME 的接口是 S1-MME，**传控制信令**。
    * **S-GW（Serving Gateway）**：**服务网关**，负责**用户面数据转发**，是 **UE 移动时的数据锚点（eNode 之间切换的锚点）**。eNodeB 到 S-GW 的接口是 S1-U，传用户数据。
    * **P-GW（PDN Gateway）**：**分组数据网网关**，负责**连接外部 IP 网络**，为 **UE 分配 IP 地址**，做计费、策略执行、NAT/防火墙等。
    * **HSS（Home Subscriber Server, 归属签约用户服务器）**：**用户数据库**，保存用户签约信息、鉴权数据、漫游信息等。MME 通过 S6a 接口访问 HSS。
    * **PCRF（Policy and Charging Rules Function）**：**策略与计费规则功能**，决定 QoS、计费策略、业务策略等。它通过 Gx 与 P-GW 交互，通过 Rx 与业务平台交互。

!!! note "一句话总结"
    **eNodeB 管无线接入，MME 管信令和移动性，S-GW 转发数据，P-GW 连接外网，HSS 管用户资料，PCRF 管策略与计费**。

??? info "例题 1"
    LTE 采用扁平化网络架构，WCDMA 网络中原 RNC 的功能主要由 哪个网元设备来承担？

    答：**eNodeB**。

??? info "例题 2"
    LTE 网络中， 移动终端 UE 的 IP 地址由哪个网元设备来分配？

    答：**P-GW**。

??? info "例题 3"
    LTE 网络的一个重要特点是控制平面与用户平面分离，只负责控制信息处理的网元是哪一个？

    答：**MME**。

### SBA（5G）

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629155244595.png){ loading=lazy width="70%" } </figure>

SBA（Service Based Architecture），即**服务化架构**。

* **NG-RAN**（Next Generation Radio Access Network, 无线接入网）：由 **gNB（5G 基站）**组成。
* **NGC（Next Generation Core, 核心网）**：5G 核心网，采用 SBA 架构，核心网元都是**服务化网元（NF）**，通过 **服务化接口（SBI）** 互联。
* **DN**（Data Network, 数据网络）：5G 核心网连接的外部数据网络，可以是互联网、企业网、运营商专网等。

### 4G vs. 5G 的区别

* 演进过程：4G $\rightarrow$ **控制面与用户面分离**（CUPS，Control and User Plane Separation） $\rightarrow$ 4.5G $\rightarrow$ **功能模块化**（SBA，Service-Based Architecture） $\rightarrow$ 5G。
    * 首先将同一设备 S/PGW 同时承担控制 + 数据拆分为 S/PGW-C（控制）和 S/PGW-U（数据），实现控制面与用户面的分离（CUPS）。
    * 进一步将一个大网元（MME）拆成很多小网元（如 AMF、AUSF 和 UDM 等），实现功能模块化（SBA）。
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629160442619.png){ loading=lazy width="70%" } </figure>
    * **允许用户面网元（UPF）根据业务性能差异灵活下沉（部署在靠近用户侧的边缘）**，显著降低网络传输时延，减轻骨干回传网的带宽压力。
* **刚性网络 vs. 柔性网络**：
    * 4G 核心网是**刚性网络**，基于传统**物理网元实体**，固定 <u>**连接**</u>、固定 <u>**功能**</u>、固化 <u>**信令交互**</u>，无法灵活扩展和演进。
    * 5G 核心网是**柔性网络**，彻底重构为**基于服务**的架构（SBA）与微服务架构，实现 <u>**软件定义**</u> 的网络功能和网络连接。
* **物理网元实体** $\rightarrow$ **虚拟网络功能**：5G 核心网层面采用云化分布式部署架构，通过 SDN 和 NFV 技术把网元进行**虚拟化**的处理；
* **点对点构架** $\rightarrow$ **基于服务的架构（SBA）**
* **单体式构架** $\rightarrow$ **微服务架构**
* **单一网络** $\rightarrow$ **网络切片**：5G 核心网支持网络切片（Network Slicing），可以在同一物理网络上创建多个虚拟网络，每个切片可以针对不同的业务需求进行优化和定制；

### 演进特点总结

!!! note "架构演进的总体趋势与特点"
    * **架构扁平化**
    * **承载全IP化**
    * **用户面和控制面彻底分离**
    * **功能虚拟化与云化**
    * **服务化与切片化**

## 5G 移动交换系统

* **核心驱动力**：<u>**移动互联网**</u> 和 <u>**物联网**</u> 是5G移动通信发展的两大驱动力

### 5G 的三大应用场景

* **eMBB**（**增强型移动宽带**，Enhanced Mobile Broadband）：针对**3D/超高清视频、VR/AR等大流量**业务；
* **uRLLC**（**超可靠超低时延通信**，Ultra-Reliable and Low Latency Communications）：针对**车联网、工业自动化、无人驾驶**等，提供极低时延和极高可靠性。
* **mMTC**（**大规模机器类通信**，Massive Machine Type Communications）：针对**大规模物联网（环境监测、智慧城市等）**，提供海量连接（100万连接/平方公里）和低功耗

### SBA 架构

5G 核心网采用 SBA（Service Based Architecture，服务化架构），将**网络功能和网络硬件解耦**：

* 传统硬件网元 $\rightarrow$ 多个小的模块化组件 **NF**（Network Function，**网络功能**） $\rightarrow$ 每个 NF 提供多个特定的服务 **NFS**（Network Function Service，**网络功能服务**）；
* NFS 高度独立自治，并通过开放接口来相互通信，可以像搭积木一样组合成大的 NF，以提升业务部署的敏捷性和弹性。
* 网络功能服务自动化管理。由独立的网络功能负责管理网络中的所有功能；
* 网元间通信机制优化。所有网元接口初期采用 HTTP/2 协议，后续可演进至 QUIC/UDP 协议及 SRv6技术。

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629163208035.png){ loading=lazy width="70%" } </figure>

* **核心控制面网元**：
    * **AMF（接入和移动性管理功能）**：负责终端的 <u>**注册**</u>、<u>**连接**</u>、<u>**可达性**</u> 及 <u>**移动性管理**</u>，以及 NAS 信号的加密与完整性保护。
    * **SMF（会话管理功能）**：负责会话管理（会话建立/修改/释放）、UPF的选择和控制、IP地址分配；
    * **UDM（统一数据管理）**、**AUSF（鉴权服务功能）**、**PCF（策略控制功能）**：负责执行用户数据管理、鉴权、策略控制等
    * **NEF（网络开放功能）、NRF（网络存储功能）**：用于帮助 Expose 和 Publish 网络数据，以及**帮助其他节点发现网络服务**。
    * **NSSF（网络切片选择功能）**
* **核心用户面网元**：
    * **UPF（用户平面功能）**：5G 唯一的用户面网元，代替了 4G 的 SGW/PGW。作为移动性锚点和外部数据网（DN）的连接点，执行**报文路由和流量转发**。
* **服务化架构的管理中心 NRF**：
    * **NRF（网络存储功能）**：支持网络功能 NF 的注册登记、NF 服务的状态检测等，实现网络功能的自动化管理、自动选择和自动扩展。
    * 每个 NF 启动时，都必须向 NRF 注册登记，才能为其他 NF 提供服务。
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629164247890.png){ loading=lazy width="70%" } </figure>
* **5G 的数据存储架构**：实现计算与存储分离
    * **UDSF**（Unstructured Data Storage Function，非结构化数据存储功能）：用于**存储所有 NF 的非结构化数据**，被所有 NF 所共享；
    * **UDR**（Unified Data Repository，统一数据仓库）：用于 UDM 存储订阅数据或读取订阅数据以及 PCF 存储策略数据或者读取策略数据等；

### 5G无线接入网（RAN）的重构

* **BBU $\rightarrow$ CU + DU**：打破了 4G 基站 BBU + RRU 的刚性组合。将原 BBU 重构为 <u>**CU（集中式单元，处理非实时高层协议）**</u> 和 <u>**DU（分布式单元，处理实时底层协议）**</u> 两个逻辑实体，可合设也可分离部署。
* CU/DU 分离的核心原因：增强小区间深度协作、**满足 5G 多样化业务对时延/带宽的差异化需求**、增加**组网灵活性**（支持合设或分布式分离部署）。  

### 5G 无线关键技术

* 大规模天线技术（Massive MIMO）
* 毫米波通信（mmWave）
* 增强载波技术（Carrier Aggregation, CA）
* 超密集组网：在热点区域大量部署微基站/皮基站，大幅提升频谱效率和系统容量
* 新型多址接入：如 NOMA（非正交多址接入），允许多用户同时占用全部带宽，利用功率域复用，并在接收端采用 SIC（串行干扰消除）技术分离信号
* 先进编码技术：5G控制信道采用 Polar码（极化码，适用于短码长控制信息传输）和 LDPC码（低密度奇偶校验码，适用于大数据量用户数据传输）以满足大数据量和高吞吐需求

### 5G 网络关键技术

* 5G 网络切片：定制性、隔离/专用性、质量可保证、统一平台，实现**按需组网**
    * **网络切片**：提供特定网络能力的、端到端的**逻辑专用网络**。
    * 一个网络切片实例是由**网络功能和所需的物理/虚拟资源的集合**，具体可包括接入网、核心网、传输承载网及应用。
* 多接入边缘计算（MEC）：将5G的 UPF 和计算/存储资源下沉部署到**网络边缘（更接近用户侧）**，降低网络时延
    * 典型应用：例如**视频监控应用**，通过 MEC 本地分析处理视频，提取有价值部分回传，极大节省核心网传输带宽，并提供超低时延服务（把 MEC 部署在 UPF 之前）

## 5G 信令流程

### 5G 注册基本流程

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629171807481.png){ loading=lazy width="70%" } </figure>

1. **UE $\rightarrow$ AMF 初始注册请求**
2. **AMF $\rightarrow$ AUSF / UDM 鉴权请求**
3. **进行合法性检查（双向鉴权）**：
    * UDM 确认用户购买过 5G 服务
    * 指示 AUST / AMF 和 UE 进行双向鉴权
4. **AMF $\leftrightarrow$ UDM / PCF 获取签约数据和网络使用要求**：鉴权成功后，AMF从UDM和PCF获取用户的签约数据和用网策略
5. **AMF $\rightarrow$ UE 接受注册请求**：AMF 通知 UE 初始注册完成，可以接入网络

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629172524687.png){ loading=lazy width="70%" } </figure><figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629172549721.png){ loading=lazy width="70%" } </figure><figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629172700605.png){ loading=lazy width="70%" } </figure>

### PDU 会话建立流程

* **PDU 会话**：<u>**用户设备（UE）**</u> 与 <u>**数据网络（DN）**</u> 之间建立的**端到端逻辑连接**，用于传输**分组数据单元（PDU）**，是5G网络中数据通信的核心载体。
* 核心作用：
    * 建立数据通路
    * 承载 QoS 需求
    * 绑定网络切片
* **SSC（会话和业务连续性）模式**：为了支持高移动性场景（如地铁手游、V2X），5G支持不同的SSC模式。
    1. SSC mode 1：
        * PDU 会话建立后，无论UE移动到哪个地理位置，其锚点 UPF 保持不变
        * 适用于任何需要**长连接且不能接受 IP 变更**的场景：**运营商语音/视频类**、**企业视频会议**等
    2. SSC mode 2：
        * 网络主动释放当前 PDU 会话，并指示 UE 立即向同一数据网络发起新的会话建立请求，可选择新的锚点 UPF
        * 适用于对**短暂中断不敏感**的消费级业务：**普通网页浏览**、**社交媒体刷新**等
    3. SSC mode 3：
        * 在网络释放旧连接前，先建立一条新的通往新锚点 UPF 的 PDU 会话连接，“双通道”并行，待新路径就绪后再释放旧路径
        * 适用于高移动性场景下的**实时交互类**业务：**移动中游戏**（如地铁打手游）、**车联网V2X通信**等
* **SSC 模式选择**：
    1. PCF $\rightarrow$ UE：提供SSCMSP（SSC mode selection policy）
    2. SMF 针对 UE 请求 SSC mode、签约、本地策略，确定 SSC mode

!!! note "关于PDU会话的知识点"
    * 一个用户可以同时有多个PDU会话
    * 一个PDU会话可以通过不同QoS Flow满足不同类型的业务需求
    * PDU会话创建后，不是静态不变的，也是可以修改和释放的

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629174009031.png){ loading=lazy width="70%" } </figure>

1. **UE $\rightarrow$ AMF PDU 会话建立请求**
2. **AMF 查询 UE 基本信息后交由 SMF 处理**
3. **SMF $\leftrightarrow$ PCF 获取会话建立策略**
4. **SMF $\leftrightarrow$ UPF 选择合适的锚点 UPF**：为建立 PDU 会话做好信令准备
5. **SMF $\leftrightarrow$ 无线基站 & UE 按指定要求建立PDU会话上行通道**
6. **SMF $\leftrightarrow$ UPF 按照指定要求建立PDU会话下行通道**

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629174524359.png){ loading=lazy width="70%" } </figure><figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629174541859.png){ loading=lazy width="70%" } </figure>

### 业务请求流程

* UE 触发的业务请求：
    * 终端发送上行信令
    * 终端需要发送上行数据
    * 响应网络的寻呼请求
    * 激活用户面连接
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629174951203.png){ loading=lazy width="70%" } </figure>
* 网络触发的业务请求：
    * 网络需要向终端发送信令
        * 若 UE 处于空闲状态，网络会先发起寻呼 Paging 请求
        * 若 UE 处于连接状态， 则用户面激活，发送业务请求
        <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629175137348.png){ loading=lazy width="70%" } </figure>

## 基于 IMS 的移动实时通信

### IMS（IP 多媒体子系统）

* IMS（IP多媒体子系统）本质：一种基于 **IP 网络**的多媒体服务框架，采用 **SIP 协议**进行呼叫控制，具有**与接入网络无关**的特性。
    * 以 SIP 协议为核心实现端到端呼叫控制，并通过 SDP 等协议协商媒体参数
    * 执行用户数据、策略、计费操作时用 Diameter 协议
    * 媒体网关控制用 H.248 协议
    * 媒体流用 RTP 协议

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629201355643.png){ loading=lazy width="70%" } </figure>

* IMS 核心控制网元
    * **P-CSCF（代理-呼叫会话控制功能）**：IMS 的第一接触点，负责信令代理、安全性检查及计费策略下载。
    * **I-CSCF（查询-呼叫会话控制功能）**：相当于网关或入口，负责在用户注册/呼入时进行 S-CSCF 分配与路由查询，同时对外隐藏本网拓扑。
    * **S-CSCF（服务-呼叫会话控制功能）**：IMS 的核心控制节点，负责用户认证（鉴权）、注册管理、业务触发和会话路由。
    * **MGCF（媒体网关控制功能）** 与 **BGCF（出口网关控制功能）**：MGCF 协调 IMS 与 PSTN 或电路域的交互，BGCF 则负责选择与外部网络的接口点。
* 双重用户标识（IMS-HSS 侧开通）：
    * **IMPI（私有标识）**：格式通常为 $IMSI@ims...$，仅用于网络的注册和鉴权，常见于注册流程；
    * **IMPU（公有标识）**：格式为 $sip:...$ 或 $tel:...$，用于用户的**呼叫和寻址**，常见于会话流程。
### IMS 用户注册流程

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629202007963.png){ loading=lazy width="70%" } </figure>

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629202029021.png){ loading=lazy width="70%" } </figure>

### IMS 会话流程

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629202058113.png){ loading=lazy width="70%" } </figure>

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629202150854.png){ loading=lazy width="70%" } </figure><figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260629202201231.png){ loading=lazy width="70%" } </figure>


### VoNR

* **5G 语音标配 —— VoNR**：在 5G NR 网络上原生承载的高清音视频通话技术。它完全依靠 **IMS** 来管理语音呼叫连接的建立、维护和释放。
