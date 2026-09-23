# 应用层

在传输层往上，特别是应用层，协议由二进制协议变成了文本型协议，即协议数据往往是面向人类的具有可读性的文本，直接进行字符串解析即可。

!!! abstract "应用层的特点"
    - 为用户提供多种应用服务
    - 协议繁多、复杂，但没有统一的协议，基本是一个应用服务对应一个协议

## DNS 域名系统

### 概述

DNS（Domain Name System，域名系统）

: 用于将域名解析为 IP 地址的分布式数据库系统

    - C/S 模式
    - 使用 UDP 53 端口
    - 域名命名空间采用分层命名方式
    - 分布式数据库

### 分层命名空间

Hierarchical Namespace，即分层命名空间，如下图所示：

<figure markdown="span">
  ![DNS 分层命名空间](https://webp-pic.yokumi.cn/2026/01/20260101170655992.png){ loading=lazy width="70%" }
</figure>

这种结构类似于一棵倒挂的树（Root 在顶部），每个节点有自己的子节点，但也受上层的唯一性约束。

### 资源记录

Resource Records（资源记录，简称 RR）

: DNS 系统中最基本的数据单元，记录了某个域名所对应的信息。每个域名都有一个或多个同类型或不同类型的资源记录

每个 RR 包括以下字段：

- **Name**：域名，e.g. `www.bupt.edu.cn`
- **Type**：类型，包括：
    - **A**：IPv4 地址记录，将域名映射到 IPv4 地址
    - **AAAA**：IPv6 地址记录
    - **MX**：邮件交换记录，指明接收邮件服务器
    - **CNAME**：Canonical Name，即域名别名
    - **HINFO**：Host Information
- **Class**：通常是 `IN`，表示 Internet
- **TTL**：生存时间（Time to Live），指示此记录可被缓存多长时间（以秒为单位）

???+ tip "TTL 与缓存"
    一次询问 DNS 后，得到了该域名对应的 IP 地址，本机可以缓存该资源记录 TTL 秒；在 TTL 时间内（有效期），再次访问该域名，不需要再进行询问。

多个 A 记录对应多个 IP 地址，DNS 轮询返回不同的 IP，实现简单的负载分担：

```
www.example.com. IN A 192.0.2.1
www.example.com. IN A 192.0.2.2
www.example.com. IN A 192.0.2.3
```

对于邮件服务，多个 MX 记录提供多个邮件服务器备份，优先级数字越小，优先级越高：

```
example.com. IN MX 10 mail1.example.com.
example.com. IN MX 20 mail2.example.com.
```

优先访问 mail1，如果它不可达，才访问 mail2。

### DNS 功能架构

<figure markdown="span">
  ![DNS 功能架构](https://webp-pic.yokumi.cn/2026/01/20260101170700100.png){ loading=lazy width="70%" }
</figure>

### DNS 客户端

DNS 客户端运行在用户电脑上，用于解析域名为 IP 地址，工作流程如下：

1. 在浏览器中输入网址，DNS 客户端获得该域名
2. DNS 客户端先在本地缓存中查找是否有该域名的缓存记录，如果有，直接返回 IP 给浏览器
3. 如果没有，则向本地指定的 Local DNS Server 发出查询请求（递归查询），由 DNS Server 完成后续查询操作
4. DNS Server 如果查到，返回给 DNS Client，将域名的资源记录缓存 TTL 时间，同时返回给浏览器

### DNS 服务器层级

DNS 并不是由一个服务器完成解析的，而是多个层级、不同职责的服务器共同完成。不同层级的命名空间形成一个 "Zone"，归不同的 DNS Server 管辖。

| **类型** | **描述** | **举例** |
| --- | --- | --- |
| 根域名服务器（Root DNS Server） | 负责 .（根）顶级域名，告诉你 .com、.cn 等顶级域的服务器地址。全球共 13 个组（A~M），分布在多个镜像服务器上 | `A.root-servers.net` |
| 顶级域服务器（TLD DNS Server） | 管理 .com、.org、.cn 等顶级域，告诉你某个域名的权威服务器在哪 | 负责 .com 的服务器 |
| 权威域名服务器（Authoritative DNS Server） | 最终提供域名 $\rightarrow$ IP 的精确信息。由网站拥有者或 DNS 提供商（如 Cloudflare、阿里云）运营 | `ns1.example.com` |
| 递归解析器（Recursive Resolver） | 为客户端完成整个查询过程：从根 $\rightarrow$ TLD $\rightarrow$ 权威服务器，并将结果返回给用户。通常由 ISP 或公共 DNS 提供商（如 Google）提供 | `8.8.8.8`（Google DNS） |

???+ info "各层级知道的信息"
    | **层级** | **知道的信息** |
    | --- | --- |
    | 本地解析器 | 根服务器的 IP（root hints） |
    | 根服务器 | 所有 TLD 的权威服务器 |
    | TLD 服务器 | 子域（如 example.com）的 NS 记录 |
    | 子域服务器 | 其自身域内所有主机名的记录 |

### 域名解析

#### 解析过程

1. 应用层尝试连接某 URL
2. 应用层向 **本地名字服务器 Local Name Server** 发出请求
3. Local Name Server：监听 UDP 53 端口，如果有本地缓存，则直接返回；如果没有，则执行步骤 4

!!! note "Local Name Server 与 Recursive Resolver"
    Local Name Server 和 Recursive Resolver 实际上是一个实体，即客户端的应用层向它发起请求，剩下的查询过程完全由它负责，所以称为递归查询。

4. Local Name Server 进行迭代查询：
    1. 首先询问 **Root 根服务器**；根服务器告诉你 TLD 顶级域服务器的地址
    2. 然后询问 **TLD 顶级域服务器**（比如 .com）
    3. 逐次询问，直到到达 **Authoritative 权威服务器**
    4. **Authoritative 权威服务器**会告诉你域名对应的 IP 地址
5. DNS Resolver 递归解析器获得 IP 地址，再返回给浏览器

<figure markdown="span">
  ![DNS 迭代查询过程](https://webp-pic.yokumi.cn/2026/01/20260101170705710.png){ loading=lazy width="70%" }
</figure>

#### 递归查询 vs. 迭代查询

| **项目** | **递归查询（Recursive）** | **迭代查询（Iterative）** |
| --- | --- | --- |
| 查询方式 | 查询者把"完全查询任务"交给对方，对方必须返回最终结果 | 查询者逐级向不同服务器查询，对方只返回下一跳 |
| 常见角色 | 用户主机向本地 DNS 发起的是递归查询 | 本地 DNS 向根/TLD/权威服务器发送的是迭代查询 |
| 优点 | 简化客户端负担 | 服务器负担小，架构更分布式 |
| 缺点 | 服务器压力较大（特别是做递归的） | 查询者需要具备完整解析逻辑 |

### DNS 缓存

<figure markdown="span">
  ![DNS 缓存](https://webp-pic.yokumi.cn/2026/01/20260101170708730.png){ loading=lazy width="70%" }
</figure>

### DNS 报文格式

DNS 报文格式分为查询和响应两种，根据 RFC 1035 标准，DNS 报文封装格式如下：

```
+------------------------------------------+
|                  Header                  |
+------------------------------------------|
|                  Question                |
+------------------------------------------|
|                   Answer                 |
+------------------------------------------|
|                 Authority                |
+------------------------------------------|
|                 Additional               |
+------------------------------------------+
```

其中，DNS Header 的长度固定为 12 Bytes，包含识别码、标志、字段数等。

#### Header Section Format

```
0         5  6  7  8         11             15
+---------------------------------------------+
|                       ID                    |
+---------------------------------------------|
| QR | Opcode | AA | TC | RD | RA | Z | RCODE |
+---------------------------------------------|
|                     QDCOUNT                 |
+---------------------------------------------|
|                     ANCOUNT                 |
+---------------------------------------------|
|                     NSCOUNT                 |
+---------------------------------------------|
|                     ARCOUNT                 |
+---------------------------------------------+
```

主要字段说明：

- **ID**：0 $\sim$ 15 bits，共 2 Bytes，查询标识符（客户端生成，由服务端返回结果，客户端通过它来匹配查询和响应）
- **QR**：查询/响应，1 bit。Query = 0，Response = 1
- **OPCODE**：操作码，4 bits。0 = 标准查询，1 = 方向查询，2 = 服务器状态请求
- **AA**：Authoritative answer，是否是权威回答，1 bit
- **TC**：Truncated，是否被截断，1 bit，不常见
- **RD**：Recursion desired，是否期望递归

???+ info "RD 字段详解"
    查询报中设置，请求 DNS 服务器帮我"递归"解析出最终 IP 地址，而不是只给我下一级服务器信息。

    RD = 0 时，名字服务器不会递归处理查询。如果它不是权威，它会告诉你"你可以去问谁"，并提供下一跳 DNS 服务器的名字/IP，你要自己去一层一层问到底。

- **RA**：Recursion Available，递归是否可用。服务器响应报中设置，告诉客户端"我是否支持递归解析"
- **Z**：保留字段，3 bits
- **RCODE**：响应码，4 bits（仅用于响应报）。0 = 没有出错，3 = 名字差错（从权威名字服务器中返回，表示查询中指定域名不存在）
- **QDCOUNT** / **ANCOUNT** / **NSCOUNT** / **ARCOUNT**：Question / Answer / Authority / Additional 区的记录数

#### Question Section Format

| **字段名** | **含义** |
| --- | --- |
| QNAME | 要查询的域名（如 `www.bupt.edu.cn`，以"标签"+结束 0 字节表示） |
| QTYPE | 查询类型（如 A=1, MX=15, AAAA=28） |
| QCLASS | 查询类（通常是 IN=1，表示 Internet） |

#### Resource Record Format

| **字段名** | **含义** |
| --- | --- |
| NAME | 域名 |
| TYPE | 类型（A, AAAA, CNAME, MX 等） |
| CLASS | 类（通常是 IN = 1，表示 Internet） |
| TTL | 生存时间，单位秒，确定了客户端 DNS Cache 可以缓存该记录的时间 |
| RDLENGTH | RDATA 字段的长度 |
| RDATA | 资源数据（如 A 记录是 IP 地址，MX 记录是多个邮件地址） |

## 电子邮件系统与协议

### 电子邮件系统的组成

<figure markdown="span">
  ![电子邮件系统组成](https://webp-pic.yokumi.cn/2026/01/20260101170719633.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![电子邮件系统组成示意](https://webp-pic.yokumi.cn/2026/01/20260101170722111.png){ loading=lazy width="70%" }
</figure>

SMTP
: 简单邮件传输协议，用于将邮件从发送方客户端传输到服务器，或者从一个邮件服务器传输到另一个邮件服务器

    - 工作在应用层
    - 使用 TCP 端口 25
    - 负责发送邮件
    - 邮件客户端 $\rightarrow$ SMTP 邮件服务器
    - SMTP 邮件服务器 $\rightarrow$ 收件方的邮件服务器

POP3
: 邮局协议第 3 版，用于从邮件服务器上接收（拉取）邮件到客户端

    - 工作在应用层
    - 使用 TCP 端口 110
    - 只负责接收邮件

UA
: User Agent，e.g. Outlook, Gmail

MTA
: Message Transfer Agent，即邮件服务器，用于发/收邮件

### 邮件格式

- **Message Envelope**：消息信封，用于实现邮件在邮件服务器之间的可靠传输，并不是正文的一部分
- **Message Content**：消息内容
    - Headers：from, to, subject, date, postmarks 等
    - Blank Line：空行，用于区分 Header 和 Body
    - Body：邮件正文

<figure markdown="span">
  ![邮件格式](https://webp-pic.yokumi.cn/2026/01/20260101170738979.png){ loading=lazy width="70%" }
</figure>

```
 ┌─────────────┐     ← Envelope（信封部分）—— 用于传输控制
 │ MAIL FROM: sender@example.com
 │ RCPT TO:   receiver@example.com
 └─────────────┘
        ↓
 ┌──────────────────────────────┐
 │ Subject: Hello               │
 │ From: sender@example.com     │
 │ To: receiver@example.com     │
 │                              │
 │ Dear receiver, ...           │
 └──────────────────────────────┘
         ↑
     Message content（邮件内容/正文）
```

### MIME 多用途互联网邮件扩展

MIME（Multipurpose Internet Mail Extensions，多用途互联网邮件扩展）

: 主要用来解决传统 SMTP + ASCII 传输的局限性。由于 ASCII 只有 7 bits 二进制编码，只能表示英文字符，无法表示汉字以及其他多媒体文件。它最初是为电子邮件设计的，但现在也被广泛应用于 HTTP 等

MIME 主要通过在 Header 中新增字段来进行编码：

<figure markdown="span">
  ![MIME](https://webp-pic.yokumi.cn/2026/01/20260101170745331.png){ loading=lazy width="70%" }
</figure>

???+ example "带有附件的 MIME 那件"
    ```
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary="abc123"

    --abc123
    Content-Type: text/plain; charset="utf-8"

    这是邮件正文部分。

    --abc123
    Content-Type: image/png
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename="logo.png"

    iVBORw0KGgoAAAANSUhEUgAAAAUA...

    --abc123--
    ```

    - Header 部分：`multipart/mixed` 表示邮件内容由多个部分组成，每一部分用 boundary（即 `abc123`）分隔
    - Body 部分：一段文本 + 一个 Base64 编码的 PNG 图片

### SMTP 协议

#### 基本模型

<figure markdown="span">
  ![SMTP 基本模型](https://webp-pic.yokumi.cn/2026/01/20260101170751861.png){ loading=lazy width="70%" }
</figure>

#### 基本传输过程

```
S: 220 mail.example.com SMTP server ready
C: HELO client.example.com
S: 250 Hello client.example.com
C: MAIL FROM:<alice@example.com>
S: 250 OK
C: RCPT TO:<bob@example.net>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: 整封邮件内容
C: .
S: 250 Message accepted
C: QUIT
S: 221 Bye
```

- 前三步是建立连接的过程
- `MAIL FROM` 和 `RCPT TO` 是 Message Envelope 部分
- `DATA` 之后就是邮件的内容（Header + Body）
- 最后三步是释放连接的过程

### POP3 协议

#### 基本模型

<figure markdown="span">
  ![POP3 基本模型](https://webp-pic.yokumi.cn/2026/01/20260101170755343.png){ loading=lazy width="70%" }
</figure>

Store-and-Forward：邮件服务器接收到其他邮件服务器发来的邮件后，先存储在服务器上，当客户端连接上服务器后，再转发给客户端；其通常是单连接，一次下载所有邮件。

#### 基本传输过程

```
S: +OK mail.example.com POP3 server ready

C: USER alice@example.com
S: +OK User accepted

C: PASS alice_password
S: +OK Password accepted

C: STAT
S: +OK 2 1536
        ↑ ↑
        | └─ 总字节数
        └── 有 2 封邮件

C: LIST
S: +OK 2 messages (1536 octets)
S: 1 768
S: 2 768
S: .

C: RETR 1
S: +OK 768 octets
S: [第一封邮件的原始内容]
S: .

C: DELE 1
S: +OK Message 1 marked for deletion

C: QUIT
S: +OK Goodbye
```

#### POP3 的缺陷

POP3 协议存在缺陷：邮件下载到本地后，服务器上可删除。如果用户有多台设备，每个客户端邮件内容独立，无法同步。因此 IMAP 应运而生并代替了 POP3 协议。

### IMAP 协议

IMAP（Internet Message Access Protocol，互联网邮件访问协议）

: 目前最常用的邮件读取协议之一，相比早期的 POP3，它更强大、更灵活，特别适合**多设备、多客户端同步查看邮件**的场景。IMAP 服务器监听 TCP 端口 143

<figure markdown="span">
  ![IMAP vs POP3](https://webp-pic.yokumi.cn/2026/01/20260101170802642.png){ loading=lazy width="70%" }
</figure>

| **特性** | **IMAP** | **POP3** |
| --- | --- | --- |
| 邮件存储 | 保存在服务器上（默认） | 下载到本地，服务器上可删除 |
| 邮件阅读 | 在线 | 离线 |
| 多设备访问 | 支持，状态实时同步 | 不支持，每个客户端独立 |
| 文件夹 | 支持，用户可管理收件夹/发件夹等 | 不支持，只处理"收件箱" |
| 部分下载 | 支持（如只获取邮件头） | 不支持，必须整封下载 |
| 同步状态 | 可同步"是否已读/标星/删除等状态" | 本地行为，不影响服务器 |
| 协议端口 | 默认端口 143（非加密），993（SSL） | 默认端口 110，995（SSL） |

简单来说，POP3 实现简单但局限，IMAP 功能强大，具有同步功能，但对服务器的资源需求更高。

### Web Mail

Web Mail（网页邮件）是一种通过网页浏览器使用电子邮件服务的方式，不依赖本地邮件客户端（如 Outlook、Thunderbird）。e.g. [北京邮电大学邮件系统](http://mail.bupt.edu.cn)

本质上就是基于 HTTP/HTTPS 协议与后台的邮件服务器（通过 IMAP/SMTP）通信的前端界面。

<figure markdown="span">
  ![Web Mail](https://webp-pic.yokumi.cn/2026/01/20260101170804992.png){ loading=lazy width="70%" }
</figure>

## 万维网（WWW）

### 概述

WWW（World Wide Web，万维网）是运行在互联网上的一个信息访问系统，它让用户能通过浏览器访问分布在全球各地的网页资源。

- 目标：将分布在整个互联网不同设备上的资源组织起来
- 内容分布在互联网上，存储在 Web Server 中
- 通过 hyperlinks（超链接）进行访问
- 资源格式包括 HTML、CSS、JavaScript、图片、视频等
- 使用 C/S 模式，客户端为浏览器
- 通过 **URL（Uniform Resource Locator，统一资源定位符）** 定位网络资源
- Web Document（也称 Web Page），由 **HTML（HyperText Markup Language，超文本标记语言）** 编写
- 客户端与服务器通过 **HTTP（Hyper-Text Transfer Protocol，超文本传输协议）** 通信

### Web Client: Browser

<figure markdown="span">
  ![Web Client: Browser](https://webp-pic.yokumi.cn/2026/01/20260101170809088.png){ loading=lazy width="70%" }
</figure>

### Web Server

<figure markdown="span">
  ![Web Server](https://webp-pic.yokumi.cn/2026/01/20260101170818113.png){ loading=lazy width="70%" }
</figure>

### 网页分类

Web Document/Web Page（网页），用 HTML 编写，分为三种：

Static Web Page（静态网页）
: 内容是事先写好并存储在服务器上的 HTML 文件，用户访问时，服务器直接将这些文件发送给客户端

<figure markdown="span">
  ![静态网页](https://webp-pic.yokumi.cn/2026/01/20260101170824145.png){ loading=lazy width="70%" }
</figure>

Dynamic Web Page（动态网页）
: 内容是由服务器在用户请求时动态生成的，通常通过后端脚本语言（如 PHP、Python、Node.js 等）结合数据库生成 HTML 页面；每次访问内容可变

<figure markdown="span">
  ![动态网页](https://webp-pic.yokumi.cn/2026/01/20260101170827890.png){ loading=lazy width="70%" }
</figure>

Active Web Page（活动网页）
: 客户端具有交互能力和动态行为的网页，主要依赖 JavaScript、AJAX、DOM 操作等技术在浏览器端运行。不需要依赖服务器处理，程序运行在浏览器端

<figure markdown="span">
  ![活动网页](https://webp-pic.yokumi.cn/2026/01/20260101170833062.png){ loading=lazy width="70%" }
</figure>

### URL 统一资源定位符

<figure markdown="span">
  ![URL 格式](https://webp-pic.yokumi.cn/2026/01/20260101170838273.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![URL 示例](https://webp-pic.yokumi.cn/2026/01/20260101170840683.png){ loading=lazy width="70%" }
</figure>

## HTTP 超文本传输协议

### 概述

<figure markdown="span">
  ![HTTP 概述](https://webp-pic.yokumi.cn/2026/01/20260101170846162.png){ loading=lazy width="70%" }
</figure>

### 工作流程

1. 浏览器分析 URL
2. 浏览器通过 DNS 获得 IP 地址
3. 浏览器根据 IP 地址，和服务器建立 TCP 连接
4. 浏览器发送 HTTP Request 请求
5. 服务器发送一个响应的 Web Page 给浏览器
6. 释放 TCP 连接
7. 浏览器呈现前端页面

<figure markdown="span">
  ![HTTP 工作流程](https://webp-pic.yokumi.cn/2026/01/20260101170852741.png){ loading=lazy width="70%" }
</figure>

### 请求方式

<figure markdown="span">
  ![HTTP 请求方式](https://webp-pic.yokumi.cn/2026/01/20260101170855590.png){ loading=lazy width="70%" }
</figure>

### 消息头

<figure markdown="span">
  ![HTTP 消息头](https://webp-pic.yokumi.cn/2026/01/20260101170859999.png){ loading=lazy width="70%" }
</figure>

### 状态码

<figure markdown="span">
  ![HTTP 状态码](https://webp-pic.yokumi.cn/2026/01/20260101170904918.png){ loading=lazy width="70%" }
</figure>

### HTTP/1.1 vs. HTTP/1.0

<figure markdown="span">
  ![HTTP/1.1 vs HTTP/1.0](https://webp-pic.yokumi.cn/2026/01/20260101170909192.png){ loading=lazy width="70%" }
</figure>

!!! abstract "HTTP/1.1 相比 HTTP/1.0 的提升"
    - **支持持久连接**：默认启用 Keep-Alive，多个 HTTP 请求可以复用同一个 TCP 连接，减少连接开销
    - **支持流水线（Pipelining）**：客户端在收到响应前连续发送多个请求，服务器按顺序响应；将多个请求打包到一个 TCP/IP 包
    - **增强了缓存控制**
    - **支持压缩**
