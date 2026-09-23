# 存储系统

## 寄存器堆

寄存器堆（Register File）
: 由多个寄存器构成的集合，常用于数据寄存。有三组外部信号：地址（短地址）、数据、读/写控制。

???+ note "多端口寄存器堆"
    多端口寄存器堆支持**同时读、写**，可同时输出两个数。这种并行访问能力是 CPU 流水线设计的基础——取指、译码、执行等阶段可能同时需要读取不同寄存器的值。


## 寄存器队列

寄存器队列是一种按 **FIFO（First In First Out，先进先出）** 方式工作的存储部件：

FIFO 队列
: 用若干个移位寄存器构建的小型存储部件，用于指令队列。

### 特点

- 无地址线，双端口存储器，可同时读写
- FIFO 常见应用场景：

    - 两个不同速率系统之间的通信缓冲
    - 数据采集传送
    - 串并转换


## 寄存器栈

寄存器栈是一种按 **LIFO（Last In First Out，后进先出）** 方式工作的存储部件：

LIFO 栈
: 用若干个**双向移位寄存器**构建的小型存储部件。

!!! note "寄存器栈的用途"
    寄存器栈主要用于**减少函数调用时对内存的访问**。通过在栈中保存返回地址、局部变量等，避免了频繁的主存读写开销。


## RAM

### 特性与作用

RAM（Random Access Memory，随机存取存储器）
: 能读能写、易失性存储器，用于存放编写的程序和数据。

### 逻辑结构

<figure markdown="span">
  ![RAM 逻辑结构](https://webp-pic.yokumi.cn/2026/01/20260101154538398.png){ loading=lazy width="70%" }
</figure>

RAM 的逻辑结构包括三个核心部分：

地址译码器
: 将输入的地址信号转换为对应存储单元的选择信号

存储矩阵
: 由大量存储元排列构成的矩阵，是数据存储的主体

读写控制电路
: 控制对存储矩阵的读出或写入操作

### SRAM 与 DRAM

RAM 分为 SRAM（Static RAM）和 DRAM（Dynamic RAM）两种类型：

<figure markdown="span">
  ![SRAM 与 DRAM 对比1](https://webp-pic.yokumi.cn/2026/01/20260101154546215.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![SRAM 与 DRAM 对比2](https://webp-pic.yokumi.cn/2026/01/20260101154550516.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![SRAM 与 DRAM 对比3](https://webp-pic.yokumi.cn/2026/01/20260101154553293.png){ loading=lazy width="70%" }
</figure>


## ROM

### 逻辑构成

ROM（Read Only Memory，只读存储器）的逻辑构成基于门阵列结构：

ROM 逻辑结构
: **与门阵列（地址译码器）＋ 或门阵列（存储矩阵）**

!!! warning "ROM 的编程"
    ROM 写入数据的过程称为对其**编程**。不同类型的 ROM 具有不同的编程和擦除方式。

### 分类

PROM（Programmable ROM）
: 一次可编程只读存储器，写入后不可更改

EPROM（Erasable Programmable ROM）
: 可擦除可编程只读存储器，支持多次编程

???+ info "更多 ROM 类型"
    除了 PROM 和 EPROM，还有 EEPROM（电擦除可编程 ROM）、Flash Memory（闪存）等。关于更详细的 ROM 分类和特性，参见[计组：存储系统](../computer-organization/storage-system.md)。


## 存储器容量计算

存储器容量
: 单元数 $\times$ 每单元的位数，即**字数 $\times$ 字长**

???+ example "容量计算举例"
    若一个存储器有 $2^{10} = 1024$ 个存储单元，每个单元存储 8 位数据，则存储容量为：

    $$1024 \times 8 = 8192\text{ bit} = 1\text{ KB}$$

