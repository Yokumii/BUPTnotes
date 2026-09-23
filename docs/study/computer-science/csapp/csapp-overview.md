# CSAPP 概述

## 程序的执行过程

<figure markdown="span">
  ![程序从源代码到机器执行的完整过程](https://webp-pic.yokumi.cn/2026/01/20260101164323526.png){ loading=lazy width="70%" }
</figure>

编辑代码
: 使用高级程序语言编写源代码，属于人工可读的文本阶段

编译器 (Compiler)
: 将高级语言源代码翻译为汇编代码，此时指令操作用助记符表示

汇编器 (Assembler)
: 将汇编代码转换为机器指令（01 字符串），即二进制可执行的机器码

!!! tip "关键理解"
    整个流程可概括为：**源代码 → 汇编代码 → 机器代码 → 硬件调度执行**。每一步都是从前一阶段的抽象表示向更底层的具体表示转换。

## 8086 CPU

<figure markdown="span">
  ![8086 CPU 内部寄存器结构示意图](https://webp-pic.yokumi.cn/2026/01/20260101164327505.png){ loading=lazy width="70%" }
</figure>

### 通用寄存器组 (GPRS)

???+ details "数据寄存器"
    AX (Accumulator)
    : 累加器，用于算术运算和 I/O 操作

    BX (Base)
    : 基地址寄存器，用于存储基址

    CX (Counter)
    : 计数寄存器，用于循环和串操作计数

    DX (Data)
    : 数据寄存器，用于 I/O 端口地址和乘除法辅助

???+ details "地址寄存器"
    SP (Stack Pointer)
    : 堆栈指针，指向栈顶

    BP (Base Pointer)
    : 基址指针，用于访问栈中参数和局部变量

    DI (Destination Index)
    : 目标地址寄存器，用于串操作的目标地址

    SI (Source Index)
    : 源地址寄存器，用于串操作的源地址

### 内部寄存器

CS (Code Segment)
: 代码段寄存器；与 IP 组合可得到下一条指令的地址

DS (Data Segment)
: 数据段寄存器

SS (Stack Segment)
: 堆栈段寄存器；函数调用时的返回地址、局部变量和参数等存放在此段

ES (Extra Segment)
: 附加段寄存器

IP (Instruction Pointer)
: 指令指针；总是指向**当前正在执行的指令的下一条指令的偏移地址**

!!! warning "注意"
    CS 和 IP 共同决定指令的执行位置：实际地址 = $CS \times 16 + IP$。

### 标志寄存器

???+ details "标志位详情"
    OF (Overflow)
    : 溢出标志，运算结果超出表示范围时置 1

    DF (Direction)
    : 方向标志，控制串操作的方向（递增或递减）

    IF (Interrupt)
    : 中断允许标志，决定 CPU 是否响应可屏蔽中断

    SF (Sign)
    : 符号标志，等于运算结果的最高位（反映正负）

    ZF (Zero)
    : 零标志，运算结果为 0 时 ZF = 1

    AF (Auxiliary Carry)
    : 辅助进位标志，用于 BCD 运算

    PF (Parity)
    : 奇偶标志，低 8 位满足偶校验时 PF = 1

    CF (Carry)
    : 进位/借位标志，无符号运算产生进位或借位时置 1

!!! info "寻址空间"
    8086 的地址总线为 20 位，总共可寻址空间为 $2^{20} = 1\text{ MB}$（即 $2^{20}$ 字节）。

## 一个完整程序的执行过程

以下以 `hello` 程序为例，描述从输入到输出的完整执行流程。

### 1. 从键盘读取命令

<figure markdown="span">
  ![从键盘读取 hello 命令的数据流向](https://webp-pic.yokumi.cn/2026/01/20260101164331593.png){ loading=lazy width="70%" }
</figure>

用户从键盘上输入 `hello` 命令，数据经由 I/O 中继器传递到 CPU，CPU 将其存入主存中的缓冲区。

### 2. 从磁盘加载可执行文件到主存

<figure markdown="span">
  ![从磁盘加载可执行文件到主存的过程](https://webp-pic.yokumi.cn/2026/01/20260101164340533.png){ loading=lazy width="70%" }
</figure>

CPU 先向主存发送读取指令，随后将磁盘上的可执行文件加载到主存中，准备执行。

### 3. 执行程序并输出结果

<figure markdown="span">
  ![执行程序并将输出字符串从存储器写到显示器](https://webp-pic.yokumi.cn/2026/01/20260101164348751.png){ loading=lazy width="70%" }
</figure>

CPU 从主存获取字符串的地址并存入寄存器，再控制 I/O 设备将字符串输出到显示器上的图形化窗口。

!!! note "整体流程总结"
    完整执行过程可概括为三步：
    
    1. **输入**：键盘 → I/O 中继器 → CPU → 主存
    2. **加载**：磁盘 → 主存（CPU 发出加载指令）
    3. **输出**：CPU 从主存取数据 → 寄存器 → I/O 设备 → 显示器
