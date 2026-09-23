# SIP 信令

## SIP 协议栈

### SIP 与相关协议的关系

* **SIP（Session Initiation Protocol）**：SIP（会话初始协议）是 <u>**应用层**</u> 控制协议，基于文本，独立于底层传输协议。
* **协议栈层次**：
    * **传输层**：SIP 可运行在 TCP、UDP、TLS 等传输协议之上（TLS用于加密安全传输）。
    * **会话描述**：<u>**SIP本身不传送媒体**</u>，它使用 <u>**SDP（会话描述协议）**</u> 作为消息体来协商和描述媒体参数。
    * **媒体传输与控制**：协商完成后，音视频媒体流直接通过 <u>**RTP（实时传输协议）**</u> 传输，并由 <u>**RTCP（RTP控制协议）**</u> 进行质量控制与同步

### SIP 内部分层

1. 语法和编码层：最底层，负责消息解析与扩展BNF编码。
2. 传输层：依赖TCP/UDP定义请求/应答的发送与接收。
3. 事务层（Transaction Layer）：处理重传、超时、请求与应答的匹配（无状态代理不包含此层）。
4. 事务用户层（TU Layer）：最顶层，创建和管理事务。

### SIP 特点

* 应用层协议，独立于较低层传输协议；
* 基于文本的消息编码，易于调试和扩展；
* 在资源受限的环境中信令压缩；
* 具有多个层次的可实现性；
* 通过代理、重定向功能支持用户的移动性；
* 易扩展性；

## SIP 核心组件的功能

* **用户代理 (UA, User Agent)**：代表用户的逻辑实体，分为发起**请求的客户端（UAC）**和**接收请求的服务器（UAS）**
* **代理服务器 (Proxy Server)**：作为中介，接收请求后查询路由并转发到下一跳。它能实现路由寻址、呼叫权限校验和负载均衡。分为有状态和无状态两种
* **注册服务器 (Registrar Server)**：处理用户的 REGISTER 请求，存储用户位置信息，提供用户定位与身份验证服务
* **重定向服务器 (Redirect Server)**：不转发请求，而是通过 3xx 响应将目标终端的新地址直接返回给主叫，由主叫重新发起呼叫（资源消耗低，适合大型网络分流）

## SIP 消息基本结构与类型

**基本结构**：

* **起始行**（指示消息类型/响应状态/版本）
* **消息头**（发送者、接收者、会话标识等）
* **消息体**（可选，通常为 SDP 协议描述的媒体参数）

**请求消息（UAC $\rightarrow$ UAS）**：

| 消息 | 功能 |
|---|---|
| REGISTER | 终端向注册服务器提交位置进行注册 |
| INVITE | 发起多媒体会话，携带SDP协商参数 |
| ACK | 主叫向被叫确认已收到对INVITE的最终响应（如200 OK），是会话建立的必要步骤 |
| OPTIONS | 探测对端能力（支持的方法、编码等），不建立会话 |
| BYE | 终止会话，释放资源 |
| CANCEL | 在会话建立前（如对方未接听）取消正在进行的INVITE请求 |

**响应消息（UAS $\rightarrow$ UAC）**：

| 响应码 | 含义 |
|---|---|
| 1XX (通知服务器或代理正在执行处理，终端应该等待响应) | 100 Trying (处理中，防重传)、180 Ringing (振铃)、183 Session Progress (会话进展) |
| 2XX (请求成功) | 200 OK (请求成功) |
| 3XX (重定向响应，终端应向新地址发起新请求) | 301 Moved Permanently (永久重定向)、302 Moved Temporarily (临时重定向) |
| 4XX (请求失败，终端的请求被拒绝) | 401 Unauthorized (未授权/需鉴权)、404 Not Found (用户不存在) |
| 5XX (服务器内部错误造成请求不能被响应) | 503 Service Unavailable (服务器过载) |
| 6XX (全局错误，所有未来的对该用户的请求都将失败) | 603 Decline (被叫明确拒绝) |

**常用头字段**：

| 头字段名称 | 核心用途与抓包寻找线索 |
|---|---|
| Call-ID | 唯一标识一个会话。同一通电话里所有的请求和响应此值完全相同。 |
| From | 标识请求发起者。格式为 `"显示名" <sip:用户@域名>;tag=xxx`。初始请求必须带 `tag`。 |
| To | 标识请求接收者。注意：UAC 发出初始 INVITE 请求时，`To` 字段没有 `tag`；当被叫 UAS 响应（如 `180 Ringing` 或 `200 OK`）时，会在响应的 `To` 字段中加上它自己生成的 `tag`。 |
| CSeq | 命令序列号。格式为 `数字 + 方法`（如 `1 INVITE`）。在同一个 Dialog 内，每发起一个新的事务请求，该数字就会递增。 |
| Via | 记录消息的传输路径。每经过一个 SIP 代理服务器，都会在顶部新添加一条 Via 记录，用于响应消息原路返回。包含传输协议（如 UDP）和发送方地址。 |
| Contact | 提供直接联系地址（格式通常为 `<sip:用户@具体终端IP:端口>`）。作用是告诉对方：后续的 Dialog 内消息（如 `BYE`、`Re-INVITE`）可以直接发到这个直接地址，不用再盲目绕行代理服务器的寻址数据库。 |
| Expires | 请求的有效期（秒），`Expires: 0` 常用于注销注册 |

## 媒体协商 (SDP, RTP, RTCP)

1. SDP 对媒体的描述 使用 类型=值 的文本格式：
    * `o= (所有者与会话ID)`：所有者/创建者和会话标识符，后面通常包含发起方的逻辑 IP。
    * `c= (媒体连接的IP地址)`：连接数据行（格式如 c=IN IP4 10.129.7.127），声明本端接收媒体流的 IP 地址。
    * `m= (媒体名称、端口、传输协议、负载类型PT)`：媒体名称和传输地址。
        * 示例：`m=audio 48906 RTP/AVP 0 8 101` 表明这是一个音频 (audio) 流，本端接收该流的 UDP 端口是 48906，采用 RTP 传输，支持的媒体格式代号（Payload Type）有 0、8、101。
    * `a=rtpmap: (动态绑定编码属性)`：用于动态绑定编码属性。
        * 示例：`a=rtpmap:101 telephone-event/8000` 表明代码 101 代表电话按键事件（DTMF），采样率为 8000 Hz。
2. RTP 与 RTCP 的功能：
    * **RTP (实时传输协议)**：负责传媒体数据。提供负载类型指示、数据分组序号（Sequence Number，用于防丢包/乱序重排）、时间戳（Timestamp，用于播放同步）、同步源标识（SSRC）
    * **RTCP (RTP控制协议)**：负责传控制信息。与RTP端口成对使用（RTP偶数，RTCP相邻奇数）。发送端发SR包（同步时钟、统计数据），接收端发RR包（反馈丢包率、抖动），用于动态调节码率
        * 靠 <u>**SSRC 标识**</u> 和对应 RTP 流绑定，避免控制指令错乱。
3. RTP 负载类型 (Payload Type, PT) 映射：
    * 静态分配（0~34）：不需要额外解释，属于国际标准通用。
        * **0：PCMU** (G.711 $\mu$-law) 
        * **8：PCMA** (G.711 A-law) 
        * **18：G.729**
    * 动态分配（96~127）：需要用到 a=rtpmap: 属性行进行具体说明。
        * 示例：`a=rtpmap:96 H264/90000` $\rightarrow$ 说明代码 96 代表的是 **H.264 视频编码**。
        * 示例：`a=rtpmap:101 telephone-event/8000` $\rightarrow$ 说明代码 101 代表**电话按键事件（DTMF）**。

!!! note "SDP协议格式举例"
    <figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627113303931.png){ loading=lazy width="70%" } </figure>

## SIP 消息流程与状态机

### SIP 注册/注销

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627130558706.png){ loading=lazy width="70%" } </figure>

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627130707689.png){ loading=lazy width="70%" } </figure>

### 正常通话

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627130916843.png){ loading=lazy width="70%" } </figure>

1. A 发 `INVITE` $\rightarrow$ Proxy $\rightarrow$ B
2. B回 `100 Trying` $\rightarrow$ `180 Ringing` $\rightarrow$ 接听发 `200 OK`
3. A收到后发 `ACK`。（**注意，这里由于响应成功，因此 `ACK` 是一个独立的事务，不属于上面 UAC 发出 `INVITE`，UAS 返回响应这一事务**）
4. 随后双方直接通过RTP进行媒体传输。

### 被叫忙

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627131457802.png){ loading=lazy width="70%" } </figure>

A发 `INVITE` $\rightarrow$ B回 `486 Busy here` $\rightarrow$ A回 `ACK`

### 主叫提前挂机 (Cancel)

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627132149296.png){ loading=lazy width="70%" } </figure>

A发 `INVITE` $\rightarrow$ B 180 Ringing $\rightarrow$ A不耐烦发 `CANCEL` $\rightarrow$ B回 `200 OK` (确认Cancel) 并回 `487 Request Terminated` (终止Invite) $\rightarrow$ A发 `ACK`

### 被叫超时未应答

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627132315212.png){ loading=lazy width="70%" } </figure>

### Re-invite会话修改（音频增加视频）

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627132802839.png){ loading=lazy width="70%" } </figure>

音频通话过程中，A发 `re-INVITE`（包含音频+**视频新SDP**，**`CSeq`递增**，`From`、`To`、`Call-ID` 等不变） $\rightarrow$ B回 `200 OK` $\rightarrow$ `ACK`，实现音视频同步传输

### Update会话更新（视频编码切换）

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627133206895.png){ loading=lazy width="70%" } </figure>

A发 `UPDATE`（**修改SDP中的Payload Type**，例如从H.264的96改为H.265的97） $\rightarrow$ B回 `200 OK`，**无需 `ACK`**。

## SDL (规范描述语言)

**元素**：<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627133440078.png){ loading=lazy width="70%" } </figure>

!!! note "核心概念：对话 (Dialog) vs. 事务 (Transaction)"
    1. 事务 (Transaction) ：
        * 定义：从客户端发出请求（Request）到服务端回送最终响应（Final Response）的完整过程 。
        * 特殊注意：对于 INVITE 请求，
            * 如果回应是 2xx（成功），则随后的 ACK 确认是一个独立的事务；
            * 如果回应是 非-2xx（失败），则 ACK 属于原 INVITE 事务的一部分。
    2. 对话 (Dialog) ：
        * 定义：由一组特定标识符关联起来的完整呼叫生命周期（包含多个事务，如呼叫建立、媒体修改、挂机）。
        * **Dialog 唯一标识三元组**（极端重要）：由 <u>**Call-ID**</u>、<u>**From 字段的 tag**</u> 和 <u>**To 字段的 tag**</u> 共同组成 。 
        * in-dialog 消息的判断依据：后续消息（如 Re-INVITE、UPDATE、BYE 等）如果携带了已经建立的会话的这三个标识（尤其是 To 字段已经有了最初响应生成的 tag），Wireshark 就会将其标记为 in-dialog（在对话内）。

### ICT (Invite Client Transaction) 

ICT，即 Invite 客户端事务，是指发起 `INVITE` 请求的客户端（UAC）在整个事务中的状态机，通常即主叫方。包括 `Init`、`Calling`、`Proceeding`、`Completed`、`Terminated` 五个状态。

1. **Init (初始状态)**：
    * 输入：**事务用户层（TU）**向下发起一个 INVITE 请求时；
    * 动作：
        1. 启动 **Timer A（用于控制 INVITE 请求的重传间隔）**
        2. 启动 **Timer B（用于控制整个事务的总体超时时间）**
    * 输出：向底层网络发送 INVITE 请求
    * 状态转移：进入 **Calling** 状态
2. **Calling (呼叫状态)**：
    * **输入：Timer A 超时**，说明刚发送的 INVITE 暂未得到任何回应
        * 动作：
            1. 将 Timer A 的时间值**加倍并重置**
            2. **重新发送 INVITE**，且状态保持在 Calling 不变
    * **输入：Timer B 超时**，说明整个事务超时，对方一直无响应
        * 动作：
            1. 向 TU 报告超时事件
            2. 停止 Timer A
        * 状态转移：进入 **Terminated** 状态
    * **输入：传输层错误 (Transport Error)**，底层报告传输失败时
        * 动作：
            1. 停止 Timer B
            2. 向 TU 报告传输错误
            3. 停止 Timer A
        * 状态转移：进入 **Terminated** 状态
    * **输入：收到 1xx 响应**，说明远端服务器或被叫已经开始处理呼叫
        * 动作：
            1. 向 TU 报告收到临时响应
            2. 停止重传定时器 Timer A
        * 状态转移：进入 **Proceeding** 状态
    * **输入：收到 2xx 响应**，说明远端服务器或被叫已经成功处理呼叫
        * 动作：
            1. 停止 Timer A 和 Timer B
            2. 向 TU 报告收到成功响应
        * 状态转移：进入 **Terminated** 状态，需要特别注意：**对于 2xx 响应的 ACK 确认属于一个全新的独立事务，不由当前 ICT 处理**。
    * **输入：收到 3xx/4xx/5xx/6xx 响应**，即错误/重定向响应，说明呼叫失败或被拒接
        * 动作：
            1. 停止 Timer A 和 Timer B
            2. 向 TU 报告收到失败响应
            3. 向网络发送 ACK 确认（**非 2xx 的 ACK 属于当前事务的一部分**）
            4. 启动 Timer D（Timer D 的作用就是让状态机停留一段时间，专门用来吸收和处理服务端可能的重传报文）
        * 状态转移：进入 **Completed** 状态

<figure markdown="span">   ![](https://webp-pic.yokumi.cn/2026/06/20260627135738057.png){ loading=lazy width="70%" } </figure>

注意，**Terminated 才是状态机的终点**。无论是呼叫成功建立、彻底超时、底层报错，还是经历了完整的失败确认流程，最终都会汇聚到此状态。到达此状态后，ICT 的生命周期正式结束，系统分配给该事务的内存和资源将被释放。Completed 状态只是一个中间状态，专门用来处理非 2xx 响应的 ACK 确认和可能的重传报文，之后仍然会进入 Terminated。

### IST / NICT / NIST

* IST (Invite 服务端事务)：被叫方。接收INVITE，发送180/200，并等待ACK
* NICT (非Invite 客户端事务)：用于REGISTER、SUBSCRIBE等，无Calling状态，直接进入 Trying → Proceeding → Completed
* NIST (非Invite 服务端事务)：接收非INVITE请求，生成并保障响应送达
