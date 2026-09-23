# 分组交换

## 路由器的技术演进

从早期的“集中处理、共享总线”（吞吐率受限），演进到现代高端路由器采用的“**分布式处理、交换矩阵（如CLOS结构）**”，实现了控制面与数据转发面的分离。

## MPLS 基本概念及网络组成

### 核心特点

* **面向连接（逻辑连接）**：将传统IP逐跳选路的无连接模式，转变为先建立逻辑连接（标记交换路径LSP），再按指定路径转发
* **支持多协议**：它不仅能支持多种上层网络协议（如IPv4、IPv6等），而且能运行于不同的底层网络之上（如以太网、ATM、FR、PPP等），实现了“<u>**边缘路由，核心交换**</u>（边缘路由保持与现有协议兼容，增强核心网络交换速度。）”
* **标记交换**：使用固定长度的标记进行精确匹配转发，速度快
    * 标记（Label）：一个用于标识一条逻辑连接（FEC）的短定长本地标识符，PDU（分组）允许变长，但标记长度固定。

!!! note "传统 IP 交换 vs MPLS 标签交换"
    * 传统 IP 交换：
        * 寻址方式：采用**最长前缀匹配（Longest Match）**算法。
        * 处理层级：工作在第三层（网络层），每个路由器都要拆开 IP 包头、查找路由表、计算下一跳，判决过程复杂、速度慢。
        * 控制与转发：路由选择和数据转发同时进行（Hop-by-hop，逐跳执行）。
    * MPLS 交换（多协议标记交换）：
        * 寻址方式：采用**精确匹配（Exact Match）**算法。
        * 处理层级：在核心网内工作在第二层和第三层之间。只看固定长度的标签（Label），速度极快，便于保障 QoS。  
        * 控制与转发：控制面（由 IP 路由软件和标签分发协议 LDP 负责算路/分发标签）与转发面（标签置换转发表 LFIB 硬件线速转发）彻底分离。
    
    传统IP交换采用逐跳转发，路由选择与数据转发同时进行，其核心交换机制是**无连接**工作模式。
    
    MPLS将路由选择与数据转发分开进行，在信息传输之前需要建立虚连接，其核心交换机制是**面向连接**的工作模式。

### 核心概念（LER, LSR, FEC, LIB, LSP）

* **LER (Label Edge Router)**：边缘路由器，位于MPLS网络边缘。负责对进入的分组进行分类（划分FEC）、压入标记（Push），并在出网时弹出标记（Pop），执行传统IP路由功能。
* **LSR (Label Switch Router)**：核心交换路由器。仅根据分组上的标记查表进行标记置换（Swap/Replace）和极速转发，不再进行第三层处理。
* **FEC (Forwarding Equivalence Class)**：转发等价类。具有相同转发路径和处理方式的一组数据流，同一FEC分配相同的标记。
* **LIB (Label Information Base)**：标记信息库。保存转发打标分组所需的映射表。
    * LFIB内部表项：转发表中具体包含NHLFE（下一跳标签转发表目）、ILM（输入标签映射，即入标签到NHLFE的映射）和FTN（FEC到NHLFE的映射）。
* **LSP (Label Switched Path)**：标记交换路径。数据在MPLS网络中经过的由多个LSR构成的逻辑传输通路。

## MPLS 交换原理

三个阶段：

1. **连接建立**：通过LDP等协议，在节点间分发标记，形成与FEC对应的LSP路径。
2. **信息交换**（数据传输）：入口LER判定分组FEC并打上标记；核心LSR根据标记极速转发；出口LER去掉标记送达目的地。
3. **连接拆除**：取消标记绑定，释放LSP。

标记操作：

* **压入（Push）**：入口LER将IP分组加上外层标记。
* **置换（Swap/Replace）**：中转LSR查表将入标记替换为下一跳的出标记。
* **弹出（Pop）**：出口LER去掉标记，恢复成普通IP报文。

标记分配方式：

* 核心金律：标记（Label）是由下游分配给上游的！
* **下游主动标记分配（DU模式）**：下游路由器发现新网段后，主动向邻居上游通告“去往某 FEC，请用我分配的标签 X”。
* **下游按需标记分配（DoD模式）**：
    * 上游先发送 `Label Request`（我有去往该 FEC 的需求，向你请求标签）
    * 下游收到后回复 `Label Mapping`（给你绑定好的标签）

!!! note "LDP 的功能是什么？"
    LDP（Label Distribution Protocol）标记分发协议是 MPLS 网络交换节点间交互的协议，用于**创建、维护和删除标签交换路径（LSP）**。

??? info "例题 1"
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626002708630.png){ loading=lazy width="70%" } </figure>

??? info "例题 2"
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626002838147.png){ loading=lazy width="70%" } </figure>

    解答：

    (3) Label Request(123.117)
    (4) Label Request(123.117)
    (5) Label Mapping(123.117, 300)
    (6) Label Mapping(123.117, 200)
    (1) 200
    (2) 300

!!! note "LFIB 表项填写逻辑总结"
    * 一条完整的 LSP 上，前一跳的“出接口（`Out Intf`）和出标签（`Out Label`）”必须完美等于后一跳的“入接口（`In Intf`）和入标签（`In Label`）”。
    * 入口边缘路由器（Ingress LER）：
        * 因为包刚进来，所以其 `In Label` 为 NULL，它需要做 Push 操作填写 `Out Label`。
    * 出口边缘路由器（Egress LER）：
        * 因为是最后一站，其 `Out Label` 变为 NULL，它做 Pop 操作还原成普通 IP。
    * 填写方法：
        1. 先看发出的消息是 Label Mapping（直接通告）还是有 Label Request（一问一答），锁定分配方法。
        2. 锁定目的 IP（FEC），沿着数据的反方向（下游向上游），把 Label Mapping 消息里带的数字，当作前一跳路由器的 Out Label 填进去 。  

## 段路由技术 SR-MPLS

### SR 基本概念与解决的问题

* 什么是**源路由**：源节点（发件人）在报文头部直接规定好数据包在网络中必须经过的中间节点和路径（即一段有序的指令列表），中间节点只需按指令执行即可。
* **“段(Segment)”与“路由”的关系**：Segment是网络指令（去哪里、走哪个接口），路由是动作。多个Segment组成有序的Segment List，串联起来就构成了完整的转发路由。
* **解决了传统网络什么问题**：传统 MPLS LDP 需要中间节点维护庞大的状态信息，容易产生标签黑洞，协议复杂且与IGP难以同步。SR 消除了 LDP，实现“**中间节点无状态**”，极大简化了协议栈，且原生支持TE（流量工程）。
* **SID (Segment ID)**：段标识，是SR域内唯一标识一个Segment的ID
    * Prefix SID（前缀段/全局有效）：相当于目的地址，引导流量沿着 **IGP 最短路径（SPF 算法计算出的开销最小路径）** 转发去往该目的前缀
    * Node SID（特殊的Prefix SID，标识特定节点）：特殊的 Prefix SID，专门针对设备的 Loopback 接口地址进行映射，引导流量沿最短路径去往该节点
    * Adjacency SID（邻接段/本地有效，指定具体的出接口）：相当于出接口，强制指定数据包必须从该特定的外发链路转发出去，不理会 IGP 最短路径如何算路

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626101042783.png){ loading=lazy width="70%" } </figure>

### SR-MPLS 原理

复用现网 MPLS 数据面。将 SID 映射为 MPLS 标记（Label），将 Segment List 直接编码为 MPLS 的标签栈（Label Stack）。源节点压入多层标签，中间节点执行 MPLS 的 Swap 和 Pop 操作。

### SR 数据包转发流程

1. 发包与中间结点解析转发：
    * 源节点将SID列表编码在数据包头部，然后将数据包发送出去；
    * 中间节点收到数据包后，解析出栈顶的SID，如果是本节点的SID，则执行Pop操作，弹出栈顶SID，并根据剩余的SID列表继续转发；如果不是，则退回到传统路由；
2. 转发过程：
    * 基于 Prefix SID 的转发（全局有效）
        <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626101709148.png){ loading=lazy width="70%" } </figure>
    * 基于 Adjacency SID 的转发路径（本地有效）
        <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626101800303.png){ loading=lazy width="70%" } </figure>
        * Adjacency SID 相当于是对当前节点邻接链路的标识，因此严格指定了转发路径；
        * 以上图为例，R1 收到栈顶为 1012 的数据包后，执行 Pop 操作，弹出栈顶的 1012，并将数据包从指定的接口（R1-R2）转发出去，而不能走 IGP 算出的最短路径；（R1-R3）。后面的路由器同理。
    * 基于 Adjacency SID + Node SID 的转发路径
        <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626101945374.png){ loading=lazy width="70%" } </figure>

??? info "例题 1"
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260630211147855.png){ loading=lazy width="70%" } </figure>

### SRv6 原理与 IPv6 扩展报文头的关系

* SRv6 原理：**SRv6 = SR + Native IPv6**。直接利用IPv6地址（128 bits）作为SID。抛弃了MPLS标签，完全基于原生IPv6标准实现源路由
* 与 IPv6 扩展报文头的关系：SRv6引入了一种新的IPv6扩展头——**SRH** (Segment Routing Header)。当IPv6基础头的Next Header=43且Routing Type=4时，即标识为SRH。SRH中承载了Segment List（沿途的SID列表）和Segments Left（剩余处理节点数）来指导报文逐跳转发。

### SRv6 数据包转发流程

以下图为例：

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626104328703.png){ loading=lazy width="70%" } </figure>

源节点Device A接收到符合指定特征的报文后，需要通过SRv6路径转发该报文。SRv6路径中Device A为源节点，Device C和Device E为Endpoint节点，Device B和Device D为中转节点。报文通过SRv6路径转发的过程为：

1. **源节点 Device A（进行报文引入和封装）**：
    * **封装SRH头**：由于报文必须依次经过 Device C 和 Device E 两个Endpoint节点，因此在 SRH（Segment Routing Header）中，剩余处理节点数 SL（Segments Left）的初始值设为 2-1 = 1，这里 - 1 的原因是其相当于代表一个数组索引，而数组索引是从 0 开始的，因此范围是 0 ～ n - 1，n 为需要经过的 Endpoint 节点数。
    * **封装SID列表**：<u>**倒序压入**</u> 途径节点的 SID 列表，因此 Segment List = [E, C]。
    * **封装IPv6基本头**：IPv6基本头的源地址设为 Device A，目的地址则被设置为当前SL指示的地址，即 Segment List[SL] = C。
    * **转发**：封装完成后，Device A 根据IPv6头中的目的地址查找路由表，将报文转发给下一跳 Device B。
2. 中转节点 Device B 的处理（传统IPv6转发）：Device B 在此路径中是中转节点。根据SRv6的设计，中转节点不参与任何SRv6相关的处理，它甚至可以是不支持SRv6的普通设备。
    * Device B 收到报文后，仅根据IPv6头中的目的地址（此时为 Device C）查找IPv6路由表，将报文当作普通IPv6报文直接转发给 Device C。
    * 因此，SL 和 Segment List 在 Device B 中保持不变，仍然为 SL = 1 和 Segment List = [E, C]。
3. **Endpoint节点 Device C 的处理（SRv6指令处理与地址更新）**：当它收到IPv6目的地址是自己SID的报文时，必须按SRv6的指令进行处理并更新SRH
    * **更新SRH与目的地址**：Device C 检查报文的SRH头，发现 SL > 0（当前SL=1），于是将SL值减 1（更新为0），接着，它将IPv6基本头中的目的地址更新为新SL指示的地址，即 Segment List[SL] = E。
    * **转发**：完成更新后，Device C 根据新的IPv6目的地址（Device E）查找路由表，将报文转发给下一跳 Device D
4. 中转节点 Device D 的处理（传统IPv6转发）：与 Device B 同理，略。
5. **Endpoint节点 Device E 的处理（解封装与原始转发）**：Device E 既是 Endpoint 节点，也是该SRv6路径的尾节点。
    * **SRv6路径终结**：Device E 收到报文后，检查SRH头，发现 SL = 0，这意味着SRv6显式路径的引导已经结束。
    * **解封装与转发**：Device E 会对报文进行解封装操作，删除外层封装的 IPv6基本头和 SRH扩展头。随后，**提取出内部的原始报文**，并根据原始报文的目的地址进行最终的业务转发。

## 网络切片技术

* **什么是网络切片**：在同一个物理的、共享的网络基础设施上，切分出多个虚拟的**逻辑网络**，每个逻辑网络服务于具有特定SLA（如带宽、时延）需求的**特定业务或行业**（如5G场景的eMBB、uRLLC、mMTC）。
* **为什么要引入网络切片技术**：为了满足不同业务（自动驾驶要求低时延、大视频要求大带宽、物联网要求海量连接）的**差异化需求**，提供**严格的资源隔离**和**确定性的SLA保障**，这是传统VPN（仅隔离逻辑路由）无法实现的。
* **网络切片实现与 IPv6 扩展报文头的关系**：业界主流采用基于**Slice ID（切片ID）**的网络切片方案。
    * Slice ID 在全局唯一标识一个切片网络。在数据面转发时，最常见的方式是封装在IPv6的HBH（Hop-by-Hop，逐跳选项扩展头）中，或者直接利用源地址的一部分来进行标识。路由器根据报文扩展头中的Slice ID将报文送入对应的物理或逻辑预留通道转发。

!!! note "切片 vs. VPN"
    * VPN（Virtual Private Network，虚拟专用网络）：
        * 逻辑隔离，安全可达，多租户复用网络
        * 适用于企业内部网络互联、远程办公等场景
    * 网络切片（Network Slicing）：
        * 提供端到端的资源隔离，SLA 确定性保障，独立拓扑
        * 适用于5G、工业互联网、智能交通等需要严格SLA的场景
    * 关系：
        * 切片是更高级的 VPN，VPN 是切片里的一种业务承载方式
        * 切片管管道，VPN 管业务
    
## APN6（应用感知的 IPv6 网络）

### APN6 基本概念

* **什么是 APN6**：APN6（Application-aware IPv6 Network，应用感知的 IPv6 网络）是一种新型网络架构，网络能够直接识别数据报文所属的应用类型，并为其分配相应的资源。
* **为什么引入**：传统TCP/IP分层解耦导致网络成为“哑管道”，无法感知具体应用。为了满足运营商打造“智能管道”、保障行业关键业务网络质量以及满足自动驾驶等特殊业务明确的SLA需求，引入APN6让“应用驱动网络”。

### 应用感知信息

* **应用感知标识（APN ID）**：包括APP-Group-ID（应用组标识）和User-Group-ID（用户组标识），用于精准识别流量身份
* **应用感知参数（APN-Para）**：可选部分。包含应用对网络提出的Intent（意图需求）和具体的网络性能参数（如要求时延<50ms）

### APN6 解决方案（主机侧、网络侧）

* **主机侧（终端/服务器）**：如果应用终端或服务器具备能力，可以直接在发送的数据包的IPv6扩展头中写入APN信息
* **网络侧（网络设备协同）**：
    * **APN-Edge（边缘节点）**：对于不具备能力的主机，边缘路由器通过五元组等信息进行匹配，为报文打上APN ID标识（通常通过DOH目的选项扩展头封装）
    * **APN-Head（头节点）**：根据报文携带的应用信息，将流量引入到满足其SLA需求的隧道（如SRv6 TE Policy）中
    * **APN-Midpoint / Endpoint**：中间节点基于APN信息提供随流检测(iFIT)等增值服务；尾节点负责解封装，将报文还原
    * **APN-Controller（控制器）**：集中下发标记策略和转发策略
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260626112148778.png){ loading=lazy width="70%" } </figure>
