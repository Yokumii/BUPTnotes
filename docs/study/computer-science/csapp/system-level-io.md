# 系统级 I/O

## 概述

Linux 的设计哲学是"一切皆文件"：

- Linux 中的文件都是二进制比特串
- 所有的 I/O 设备在系统中都以文件形式呈现：
    - `/dev/sda2`（磁盘设备）
    - `/dev/tty2`（终端设备）
- 内核也以文件形式呈现：
    - `/boot/vmlinuz-3.13.0-55-generic`（内核映像）
    - `/proc`（内核数据结构）

用户程序可通过调用特定的 I/O 函数提出 I/O 请求。在 UNIX/Linux 系统中，可以是 **C 标准 I/O 库函数**或**系统调用的封装函数**：

- 标准 I/O 库函数：如文件 I/O 函数 `fopen()`、`fread()`、`fwrite()`、`fclose()`，或控制台 I/O 函数 `printf()`、`putc()`、`scanf()`、`getc()` 等
- 系统调用封装函数：如 `open()`、`read()`、`write()`、`close()` 等

标准 I/O 库函数比系统调用封装函数抽象层次高，后者属于系统级 I/O 函数。前者是基于后者实现的。

## 文件分类

### 普通文件（Regular Files）

- 文本文件（Text files）：用 ASCII 或 Unicode 字符编码的文件
- 二进制文件（Binary files）：可执行目标文件、图片等

!!! note
    **内核不能区分文本文件与二进制文件**——对内核而言，它们都是字节序列。

### 目录（Directories）

目录是包含一组文件链接的文件。常用命令：

- `mkdir`：创建文件夹
- `ls`：查看文件夹内容
- `rmdir`：删除文件夹（文件夹必须为空）
- `.`：链接自身，`..`：链接父文件夹，`cd ..` 可返回上一级目录

Linux 文件系统**以 `/`（根目录）为起点**，所有文件和目录都组织在树状层次结构下。

## 文件操作

### 打开文件

打开文件时，内核会返回一个小的非负整数，称为**描述符（Descriptor）**。

```c
// 成功则返回新文件描述符，失败返回 -1
int open(char *filename, int flags, mode_t mode);
```

返回的是进程中当前没有被打开的最小描述符。由于进程开始时都会创建三个文件：

- 0：`stdin`（标准输入）
- 1：`stdout`（标准输出）
- 2：`stderr`（标准错误）

所以文件描述符一般从 3 开始。

#### 文件共享

<figure markdown="span">
  ![文件共享示意图——描述符表与打开文件表的关系](https://webp-pic.yokumi.cn/2026/01/20260101164548543.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![文件共享示意图——父子进程共享打开文件表](https://webp-pic.yokumi.cn/2026/01/20260101164553743.png){ loading=lazy width="70%" }
</figure>

### 读写文件

```c
ssize_t read(int fd, void *buf, size_t n);  // 返回成功读取的字节数，失败为 -1
ssize_t write(int fd, const void *buf, size_t n);  // 同上
```

!!! note "ssize_t 与 size_t"
    `ssize_t` 被定义为 `signed long` 类型，因为它需要返回 $-1$；而 `size_t` 是 `unsigned long` 类型。

### Short Count

Short count
: 执行 I/O 操作（如 `read` 或 `write`）时，实际读取或写入的字节数**小于请求的字节数**的情况。

Short count 通常在以下场景出现：

- 遇到文件末尾（EOF）
- 从终端读取文本行
- 从网络套接字读取或写入

!!! note
    当向磁盘读取或写入时，一般不会发生 short count。

## 创建进程

### Fork 语句

```c
pid_t Fork();
```

返回值为进程编号：

- $0$：子进程
- $> 0$：父进程（返回值为子进程 PID）
- $-1$：Fork 失败

<figure markdown="span">
  ![Fork 创建进程示意图](https://webp-pic.yokumi.cn/2026/01/20260101164558074.png){ loading=lazy width="70%" }
</figure>

Fork 会复制 Fork 之后的所有代码来创建子进程。其执行过程如下：

<figure markdown="span">
  ![Fork 执行过程示意图](https://webp-pic.yokumi.cn/2026/01/20260101164602708.png){ loading=lazy width="70%" }
</figure>

!!! warning
    进程的调度规则不定，父子进程哪个先执行完都有可能。

## I/O 重定向

如果希望将当前进程的 `stdout` 改为另一个文件，即更改描述符表，可通过 `dup2` 来实现：

```c
int dup2(int oldfd, int newfd);
```

如果原来 fd1 指向文件 A，调用 `dup2(4, 1)` 后：

<figure markdown="span">
  ![dup2 重定向示意图](https://webp-pic.yokumi.cn/2026/01/20260101164604991.png){ loading=lazy width="70%" }
</figure>

### 一个读的例子

<figure markdown="span">
  ![读文件示例代码](https://webp-pic.yokumi.cn/2026/01/20260101164610158.png){ loading=lazy width="70%" }
</figure>

需要明确子进程和父进程共享同一打开文件表：

- `s = getpid() & 0x1` 决定了进程的执行顺序：若 $s = 0$，则父进程先执行；若 $s = 1$，则子进程先执行
- Fork 前的 `Read(fd1, &c1, 1)` 已经从打开文件中读取一个字符 `a` 到 `c1`，打开文件表中的文件位置++
- 执行 Fork 后，父子中先执行的进程执行 `Read(fd2, &c2, 1)`，即 $c_2 = \text{b}$，同时文件位置++，并输出结果
- 后执行的进程执行 `Read(fd2, &c2, 1)`，即 $c_2 = \text{c}$，同时文件位置++，并输出结果

结果有 2 种可能：

```
Parent: c1 = a, c2 = b
Child: c1 = a, c2 = c

Child: c1 = a, c2 = b
Parent: c1 = a, c2 = c
```

### 一个写的例子

<figure markdown="span">
  ![写文件示例代码](https://webp-pic.yokumi.cn/2026/01/20260101164612758.png){ loading=lazy width="70%" }
</figure>

首先明确一些标志的含义：

- `O_CREAT`：如果文件不存在，创建文件
- `O_TRUNC`：如果文件存在，则清空文件内容
- `O_RDWR`：文件以读写方式打开
- `O_APPEND`：每次写操作都会将数据追加到文件末尾
- `O_WRONLY`：仅允许写操作

`dup(fd1)` 复制文件描述符 fd1 到 fd2，新描述符 fd2 与 fd1 共享相同的文件表项。

逐步分析：

1. `Write(fd1, "pqrs", 4)`：将 `"pqrs"` 写入文件
2. `Write(fd3, "jklmn", 5)`：将 `"jklmn"` 写入文件末尾
3. `Write(fd2, "wxyz", 4)`：将 `"wxyz"` 写入文件——注意 fd1 的文件位置为 4（写入 pqrs 后），所以此时文件内容为 `"pqrswxyz"`
4. `Write(fd3, "ef", 2)`：将 `"ef"` 写入文件末尾

最终结果为 `"pqrswxyzef"`。

## 标准 I/O

标准 I/O 库将一个打开的文件模型化为一个**流（Stream）**。对于程序员而言，一个流就是一个指向 `FILE` 类型的结构的指针。每个 ANSI C 程序开始时都有三个打开的流 `stdin`、`stdout` 和 `stderr`，分别对应于标准输入、标准输出和标准错误。

<figure markdown="span">
  ![标准 I/O 流示意图](https://webp-pic.yokumi.cn/2026/01/20260101164614990.png){ loading=lazy width="70%" }
</figure>

## Unix I/O vs. 标准 I/O

<figure markdown="span">
  ![Unix I/O 与标准 I/O 对比图](https://webp-pic.yokumi.cn/2026/01/20260101164622556.png){ loading=lazy width="70%" }
</figure>

## 系统调用与 API

- **应用编程接口（API）**与**系统调用**两者在概念上不完全相同：它们都是系统提供给用户程序使用的编程接口，但前者指的是功能更广泛、抽象程度更高的函数，后者仅指通过软中断（自陷）指令向内核态发出特定服务请求的函数
- 系统调用封装函数是 API 函数中的一种
- API 函数最终通过调用系统调用实现 I/O。一个 API 可能调用多个系统调用，不同 API 可能会调用同一个系统调用。但并不是所有 API 都需要调用系统调用
- API 在用户态执行，系统调用封装函数也在用户态执行，但具体服务例程在内核态执行

!!! abstract "API vs 系统调用"
    API 是面向程序员的高层接口，系统调用是面向内核的低层接口。一个 API 函数可能封装一个或多个系统调用，也可能完全不涉及系统调用（如纯数学计算函数）。

## I/O 类型

### 程序控制 I/O（Programmed I/O）

无条件传统方式，又称查询方式，效率低。处理器需要不断查询设备状态，等待 I/O 操作完成。

<figure markdown="span">
  ![程序控制 I/O 示意图](https://webp-pic.yokumi.cn/2026/01/20260101164626576.png){ loading=lazy width="70%" }
</figure>

### 中断驱动 I/O（Interrupt Driven I/O）

处理器启动 I/O 操作后无需等待，可以执行其他任务，直到设备通过**中断信号**通知处理器数据传输完成。

### DMA（Direct Memory Access）

由 DMA 模块负责在 I/O 单元和主存之间**直接传输数据**，无需处理器干预。处理器只需在传输开始和结束时介入，传输期间可执行其他任务。

## 总结

<figure markdown="span">
  ![系统级 I/O 总结图](https://webp-pic.yokumi.cn/2026/01/20260101164629280.png){ loading=lazy width="70%" }
</figure>

