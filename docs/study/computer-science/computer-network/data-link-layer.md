# 数据链路层

数据链路层对物理层中传输的信号起到差错控制和流量控制的作用，特别是在广播信道中需要解决共享信道冲突，一般由接收方控制发送方。

## 成帧

### 定义

成帧（Framing）：封装网络层 Packet 为 Frame，即在 Packet 前后加上 Header 和 Trailer。

### 要求

数据链路层间是虚拟通信，实际信号通过物理层传输 0/1 比特串，因此要从比特串中正确识别帧（帧同步）：

- Simple：容易实现
- Code Independent：附加内容与传输消息无关
- Efficient：占用带宽尽量小
- Robustness：出错后能重新同步

### 成帧方式

字符计数法（Character Count）
: 每帧之前加一个字符表示帧长度。一错则后续全部错。

字符填充法（Byte Stuffing）
: 用特定标志表示帧的开始和结束。

    <figure markdown="span">
      ![字符填充标志](https://webp-pic.yokumi.cn/2026/01/20260101170023020.png){ loading=lazy width="70%" }
    </figure>

    当帧中数据部分含有 Flag 或 ESC 时，需实现透明传输（Transparent Transmission）——在其前插入一个 ESC：

    <figure markdown="span">
      ![透明传输](https://webp-pic.yokumi.cn/2026/01/20260101170026297.png){ loading=lazy width="70%" }
    </figure>

比特填充法（Bit Stuffing）
: 用连续 6 个 1（`01111110`）作为开始和结束标志；中间部分每出现 5 个 1 后插入 1 个 0，可有效避免误识别且容易解码。

物理层编码违例法（Physical Layer Coding Violations）
: 适用于特殊编码（如 Manchester 编码），用未出现跳变的信号表示帧边界。

## 差错控制

### 基本概念

差错类型
:

    - Lost Frames：帧丢失
    - Damaged Frames：帧损坏

检错（Error Detection）
:

    - Parity Check 奇偶校验：单冗余码
    - CRC 循环冗余校验
    - Checksum：在网络层中使用

纠错（Error Correction）
: 采用纠错码（ECC），分为：

    - FEC 前向纠错：如汉明编码
    - ARQ 自动重传请求：检错 + 重传
    - HEC 混合纠错

### 单比特错误与突发错误

<figure markdown="span">
  ![单比特错误与突发错误](https://webp-pic.yokumi.cn/2026/01/20260101170034059.png){ loading=lazy width="70%" }
</figure>

!!! warning "突发错误长度"
    突发错误长度 = 从第一个错误位到最后一个错误位的比特数。

### ECC 纠错码：汉明距离

在所有合法码字中：

- 检测 $t$ 位错误，需最小汉明距离 $d_{\min} \ge t + 1$
- 纠正 $t$ 位错误，需最小汉明距离 $d_{\min} \ge 2t + 1$

#### 校验位数

只考虑纠正一位错误：

- $m$：原始信息长度
- $r$：校验位长度
- $n = m + r$：码字长度

合法信息共 $2^m$ 个，每个可产生 $n$ 种一位差错，加上自身，共 $(n+1)2^m$ 个码字需由 $n$ 位码字空间 $2^n$ 覆盖：

$$
(n+1)2^m \le 2^n \Leftrightarrow m + r + 1 \le 2^r
$$

#### 汉明编码：纠正一位错误

- 校验位仅放在 $2^i$ 位置处
- 剩余位置填充数据位

<figure markdown="span">
  ![汉明编码校验位放置](https://webp-pic.yokumi.cn/2026/01/20260101170037461.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![汉明编码示例](https://webp-pic.yokumi.cn/2026/01/20260101170040267.png){ loading=lazy width="70%" }
</figure>

### 检错码

偶校验（Even-Parity Checking）
: 在数据后附加 1 位，使码字中 1 的个数为偶数。

多项式编码 / CRC（Cyclic Redundancy Check）
: 也称为 FCS（Frame Check Sequence，帧校验序列）。

    - $M(x)$：将传输比特看成多项式，如 $110001 \Rightarrow x^5 + x^4 + x^0$
    - 运算定义为模 2 运算：$x + y = x - y = x \oplus y$
    - $G(x)$：生成多项式

    ???+ info "CRC 计算过程"
        1. $M(x) \cdot x^r$：在数据右侧增加 $r$ 个 0
        2. $M(x) \cdot x^r / G(x) \cdots R(x)$：除法取余数 $R(x)$
        3. 发送方：$T(x) = M(x) \cdot x^r + R(x) = M(x) \cdot x^r - R(x)$
        4. 接收方：$T(x) / G(x)$，余数一定为 0

    ???+ info "CRC 检错过程"
        1. 接收方收到信息为 $T(x) + E(x)$（$E(x)$ 为错误多项式）
        2. 正常情况：$T(x)/G(x)$ 余数为 0
        3. 出错情况：余数为 $E(x)/G(x)$ 的结果
        4. 只要 $E(x)$ 不整除 $G(x)$，就能捕捉到错误

## 流量控制

### 基本协议

乌托邦单工协议（Utopian Simplex Protocol）
: 假设通信单通、无错、接收方缓存无限——无需差错控制和流量控制。

停等协议（Simplex Stop-and-Wait Protocol for Error-Free Channel）
: 通信单通、无错，但接收方缓存有限，需要 Stop-and-Wait 流量控制：

    - 发送方发送一个 Frame，等待
    - 接收方正确收到后发送 ACK（Acknowledgement）
    - 发送方收到 ACK 后发送下一个 Frame

    若信道不可靠，会出现帧错误、帧丢失或 ACK 丢失：

    <figure markdown="span">
      ![停等协议的问题](https://webp-pic.yokumi.cn/2026/01/20260101170050054.png){ loading=lazy width="70%" }
    </figure>

    !!! tip "序号（Sequence Number）"
        ACK 丢失时，发送方超时后重传相同帧，接收方无法区分新旧帧——通过添加序号解决。链路层仅需 1 bit 序号（编号空间大小为 2）。

PAR 协议（Positive ACK with Retransmission）
: 即 ARQ（Automatic Repeat reQuest）自动重传请求。

    - 每个 Frame 前添加序号，区分重传帧和新帧
    - 链路层序号空间大小为 2
    - 传输层需要更大编号空间

    !!! warning "ACK 也需要序号"
        若 ACK 延迟，发送方可能将旧 ACK 误认为新帧的应答：

        <figure markdown="span">
          ![ACK 延迟问题](https://webp-pic.yokumi.cn/2026/01/20260101170052660.png){ loading=lazy width="70%" }
        </figure>

        解决方法：给 ACK 也添加序号：

        <figure markdown="span">
          ![ACK 序号](https://webp-pic.yokumi.cn/2026/01/20260101170055108.png){ loading=lazy width="70%" }
        </figure>

???+ info "PAR 协议伪代码"
    ```c
    #define MAX_SEQ 1

    typedef enum { frame_arrival, cksum_err, timeout } event_type;
    #include "protocol.h"

    void send() {
        seq_nr next_frame_to_send = 0;
        frame s;
        packet buffer;
        event_type event;

        from_network_layer(&buffer);

        while (true) {
            s.info = buffer;
            s.seq = next_frame_to_send;
            to_physical_layer(&s);
            start_timer(s.seq);
            wait_for_event(&event);

            if (event == frame_arrival) {
                from_physical_layer(&s);
                if (s.ack == next_frame_to_send) {
                    stop_timer(s.ack);
                    from_network_layer(&buffer);
                    next_frame_to_send = 1 - next_frame_to_send;
                }
            }
        }
    }

    void receive() {
        seq_nr frame_expected = 0;
        frame r, s;
        event_type event;

        while (true) {
            wait_for_event(&event);

            if (event == frame_arrival) {
                from_physical_layer(&r);
                if (r.seq == frame_expected) {
                    to_network_layer(&r.info);
                    frame_expected = 1 - frame_expected;
                }
                s.ack = 1 - frame_expected;
                to_physical_layer(&s);
            }
        }
    }
    ```

捎带应答（Piggybacking）
: 全双工通信中，接收方收到帧后不立刻发送 ACK，而是等待网络层有发送请求时将 ACK 添加到待发送帧中一起发送。

    !!! caution "捎带应答的缺点"
        若长时间没有发送请求，会因等待应答造成信道阻塞。

### 滑动窗口协议

!!! abstract "滑动窗口协议特点"
    - 可靠，面向连接的服务
    - 全双工信道
    - 通过 CRC + 重传进行差错控制
    - 通过滑动窗口进行流量控制

#### Protocol 4：大小为 1 的滑动窗口

- 实际是停等协议，但变为全双工
- 两端同时发送数据时可能出现帧重复
- 信道效率低，特别是带宽时延积较大的信道（如卫星通信）

#### Protocol 5：Go Back N（回退 N 步）

- 默认接收窗口 $W_r = 1$
- 窗口约束：$W_t + W_r \le 2^n$，故 $W_t \le 2^n - 1$
- 收到出错帧后，后续帧全部丢弃，直到出错帧被正确重传
- 接收方保持沉默不应答出错帧
- 收到与预期不符的帧时，回送 ACK 为最后一个正确帧的序号；发送方从该 ACK 之后重传
- 发送方在 ACK 或超时后回退到出错帧并重传
- 累计 ACK（Cumulative ACK）：ACK = n 表示 n 及之前所有帧已正确收到
- $n$ bits 序列号：$MAX\_SEQ = 2^n - 1$
- 默认接收方 Buffer = $MAX\_SEQ + 1$

<figure markdown="span">
  ![Protocol 4 vs. Protocol 5](https://webp-pic.yokumi.cn/2026/01/20260101170057964.png){ loading=lazy width="70%" }
</figure>

#### Protocol 6：Selective Repeat（选择重传）

- 只有被拒绝的帧才需重传
- 一般默认 $W_t = W_r = 2^{n-1}$，注意与 GBN 区分
- 接收方 Buffer = $W_r$，帧缓存位置 = $frame.seq \% W_r$，保证窗口内帧不在同一缓存位置
- Frame Timer：发送方每个缓存帧各需一个 Timer
- ACK Timer：仅需一个，以第一个为准
- NCK 加速重传：帧校验出错或与预期不符时发送 NCK，序号为预期帧序号
- 向网络层提交数据为循环过程：从接收窗口下沿依次提交已收帧并向前滑动直到空闲 Buffer 出现

#### 协议比较

<figure markdown="span">
  ![三种滑动窗口协议比较](https://webp-pic.yokumi.cn/2026/01/20260101170100951.png){ loading=lazy width="70%" }
</figure>

### 性能分析

定义传播时延与传输时延之比：

$$
\alpha = \frac{T_{\text{prop}}}{T_{\text{trans}}}
$$

无错停等协议效率
:

$$
\text{efficiency} = \frac{1}{1 + 2\alpha}
$$

有错停等协议效率
:

$$
\text{efficiency} = \frac{1 - p}{1 + 2\alpha}
$$

无错滑动窗口效率
:

$$
\text{efficiency} = \begin{cases}
\dfrac{W_T}{1 + 2\alpha}, & W_T < 1 + 2\alpha \\
1, & W_T \ge 1 + 2\alpha
\end{cases}
$$

无错滑动窗口 + 捎带应答效率
:

$$
\text{efficiency} = \frac{W_T}{2 + 2\alpha}
$$

## 对网络层的服务

无连接服务（Connectionless Services）
:

    - 无确认无连接服务：大多数 LAN 使用
    - 有确认无连接服务：无线系统使用

有确认面向连接服务（Acknowledged Connection-Oriented Services）
: 提供可靠传输，包括流量控制和差错控制。

## 数据链路层实现

<figure markdown="span">
  ![数据链路层实现示意图](https://webp-pic.yokumi.cn/2026/01/20260101170103133.png){ loading=lazy width="70%" }
</figure>

方框内表示一整个 Router，一般有多个接口，其中接口 1 和 2 组成路由器的 NIC（Network Interface Card）。

## 点对点数据链路协议实例

### HDLC（High-Level Data Link Control）

特点
:

    - 可靠，面向连接：流量控制、差错控制；支持 GBN ARQ 和 SR ARQ
    - 同步串行链路传输
    - 差错检测：CRC
    - 不支持链路和网络参数协商
    - 不支持认证

帧类型
: 采用零比特填充。

    <figure markdown="span">
      ![HDLC 帧类型](https://webp-pic.yokumi.cn/2026/01/20260101170106232.png){ loading=lazy width="70%" }
    </figure>

站点类型
:

    <figure markdown="span">
      ![HDLC 站点类型](https://webp-pic.yokumi.cn/2026/01/20260101170111196.png){ loading=lazy width="70%" }
    </figure>

### PPP（Point-to-Point Protocol）

特点
:

    - 只支持点到点
    - 无连接无确认服务（Connectionless unacknowledged service）
    - 采用字节填充
    - 适配多种网络层协议
    - 支持身份认证
    - 物理层可采用异步和同步传输

帧格式
:

    <figure markdown="span">
      ![PPP 帧格式](https://webp-pic.yokumi.cn/2026/01/20260101170113855.png){ loading=lazy width="70%" }
    </figure>

    - Address = `0xFF`：表示支持所有站点
    - Control = `0x03`：表示无编号模式
    - 以上两个字段非必需，可以省略

### HDLC vs. PPP

<figure markdown="span">
  ![HDLC 与 PPP 对比](https://webp-pic.yokumi.cn/2026/01/20260101170116785.png){ loading=lazy width="70%" }
</figure>
