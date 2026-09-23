# 机器级表示

## 机器级表示基础

### 指令的概念

微指令
: 微程序级命令，属于**硬件**范畴

伪指令
: 由若干机器指令组成的指令序列，属于**软件**范畴

机器指令
: 介于微指令与伪指令之间，处于硬件和软件的交界面

!!! abstract "本章说明"
    本章提及的"指令"均指**机器指令**。汇编指令是机器指令的汇编表示形式（符号表示），机器指令（二进制串）与汇编指令一一对应，它们都与具体机器结构有关，都属于机器级指令。

编译命令：

```bash
gcc -Og -S test.c    # -Og 为优化选项，得到汇编代码 test.s
```

### 机器代码的组成

机器代码由操作码、源操作数、目的操作数地址（立即数、寄存器编号、存储地址）组成：

<figure markdown="span">
  ![机器代码组成](https://webp-pic.yokumi.cn/2026/01/20260101164739316.png){ loading=lazy width="70%" }
</figure>

通常由以下三部分构成：

程序计数器 PC (Program Counter)
: 即 `%rip`（x86-64），指向当前正在执行指令的**下一条指令**的地址

整数寄存器 Register file
: 分别存储 64 位的值（地址或整数数据）

状态寄存器 Condition codes
: 最近执行的算术或逻辑指令的状态信息

!!! warning "注意"
    机器代码**不区分**无符号整数和有符号整数，也不区分函数和指针。

### ISA 指令集体系结构

<figure markdown="span">
  ![ISA 指令集体系结构](https://webp-pic.yokumi.cn/2026/01/20260101164743448.png){ loading=lazy width="70%" }
</figure>

### 信息访问（保护模式下）

#### 整数寄存器

<figure markdown="span">
  ![x86-64 整数寄存器](https://webp-pic.yokumi.cn/2026/01/20260101164745790.png){ loading=lazy width="70%" }
</figure>

各寄存器用途：

`%rax`
: 函数返回值

`%rdi`
: 函数调用的第 1 个参数

`%rsi`
: 函数调用的第 2 个参数

`%rdx`
: 函数调用的第 3 个参数

`%rcx`
: 函数调用的第 4 个参数

`%r8`
: 函数调用的第 5 个参数

`%r9`
: 函数调用的第 6 个参数（超过 6 个参数放在栈空间中）

`%rsp`
: 栈顶指针

#### 操作数指示符号

寄存器
: 直接调用即可

立即数
: `$ + 整数` 表示

内存引用
: `(%rax)` 直接引用

基址 + 比例变址 + 位移
: `D(Rb, Ri, S)`，表示获取 $Rb + S \times Ri + D$ 地址上的数。其中 $Rb$ 为段基址，$Ri$ 为有效地址（不能是 `%rsp`），$S$ 为比例因子（1、2、4、8），$D$ 为偏移量

<figure markdown="span">
  ![操作数寻址模式](https://webp-pic.yokumi.cn/2026/01/20260101164750702.png){ loading=lazy width="70%" }
</figure>

!!! tip "注意"
    计算时直接拿寄存器做运算得到地址，但最终结果应该是**该地址上的数**。

#### 传送指令

**mov 指令**：`movq src, dest`

- 立即数可以移动到寄存器或内存地址：
    - `movq $0x4, %rax` $\Leftrightarrow$ `temp = 0x4`
    - `movq $-147, (%rax)` $\Leftrightarrow$ `*p = -147`
- 寄存器可以移动到寄存器或内存地址
- 内存只能移动到寄存器，**内存之间不能移动**
- `movl` 指令以寄存器为目的时，不但会更新低 32 位的值，还会将高位 4 字节都设置为 0
- `movs`：符号扩展；`movz`：零扩展

**lea 指令**：加载有效地址，`leaq (%rdi, %rdi, 2), %rax`

!!! warning "lea 与 mov 的区别"
    `lea` 虽然加了括号，但实际上取的是**内存的地址**，且结果也是内存的地址，而非地址的指向。所以 `leaq (%rdi, %rdi, 2), %rax` 等价于 `t = x + x * 2`。

#### 二元运算指令

<figure markdown="span">
  ![二元运算指令](https://webp-pic.yokumi.cn/2026/01/20260101164802509.png){ loading=lazy width="70%" }
</figure>

- `sarq` 为算术右移，`shrq` 为逻辑右移
- **除了乘除，都不区分有符号和无符号**
- **加减影响所有标志**
- **递增递减影响除进位借位 CF 以外的标志**
- **取负 NEG 影响标志：对 0 取负得到 0，CF = 0；其余情况 CF = 1**
- **比较运算：做减法得到标志，不会改变寄存器的值**

#### 一元运算指令

<figure markdown="span">
  ![一元运算指令](https://webp-pic.yokumi.cn/2026/01/20260101164805036.png){ loading=lazy width="70%" }
</figure>

- 逻辑运算中，`not` 不会影响标志，其余 OF = CF = 0，ZF 和 SF 根据结果设置
- **`test` 做"与"操作，但不会改变寄存器的值，仅影响标志位**

### GCC 使用举例

```bash
gcc -Og -S test.c              # 得到汇编代码 test.s
gcc -O1 test.c -o test         # 得到可执行文件 test
objdump -d test.o > test.txt   # 得到反汇编代码
```

!!! note "可重定位目标文件 vs 可执行目标文件"
    可重定位目标文件还没有经过链接器链接：

    <figure markdown="span">
      ![可重定位与可执行目标文件](https://webp-pic.yokumi.cn/2026/01/20260101164810895.png){ loading=lazy width="70%" }
    </figure>

## 控制流

### 条件码

<figure markdown="span">
  ![条件码寄存器](https://webp-pic.yokumi.cn/2026/01/20260101164822790.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![条件码设置指令](https://webp-pic.yokumi.cn/2026/01/20260101164827374.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![条件码读取指令](https://webp-pic.yokumi.cn/2026/01/20260101164831694.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![条件码与跳转](https://webp-pic.yokumi.cn/2026/01/20260101164836182.png){ loading=lazy width="70%" }
</figure>

!!! warning "`cmp` 指令注意"
    `cmp` 实际上做减运算，**后减前**。

### 循环结构

#### do-while 循环

```c
do {
    body;
} while (test);
```

等价于 goto 形式：

```c
Loop:
    body;
    t = test;
    if (t) goto Loop;
```

#### while 循环

```c
while (test) {
    body;
}
```

???+ note "Jump-to-middle 翻译方法（-O2 优化）"
    判断在后面，先跳到末尾进行判断，再返回中间执行整体：

    ```c
    goto test;
    Loop:
        body;

    test:
        t = test;
        if (t) goto Loop;
    ```

???+ note "Guarded-do 翻译方法（-O1 优化）"
    先进行判断，然后转换为 do-while 循环：

    ```c
    t = test;
    if (!t) goto END;
    Loop:
        body;
        t = test;
        if (t) goto Loop;
    END;
    ```

#### for 循环

```c
for (init; test; update) {
    body;
}
```

转化为 while 循环：

```c
init;
while (test) {
    body;
    update;
}
```

写成 goto 形式：

```c
init;
t = test;
Loop:
    body;
    update;
    if (t) goto Loop;
END;
```

### Switch 分支结构

Switch 并非简单的 if 判断，而是通过**跳转表 (Jump Table)** 来实现。每一个分支被视为一个代码块，代码块开头的地址被存放在跳转表中：

<figure markdown="span">
  ![Switch 跳转表结构](https://webp-pic.yokumi.cn/2026/01/20260101164839578.png){ loading=lazy width="70%" }
</figure>

```asm
my_switch:
    movq  %rax, %rcx
    cmpq  $6, %rdi        // x : 6
    ja    .L8              // if x > 6, goto default
    jmp   *.L4(,%rdi, 8)  // *(.L4 + x * 8) 的地址上的值，即间接跳转
```

!!! tip "跳转表的工作原理"
    先计算出跳转表上的索引位置，跳转到该索引上的值处，即**间接跳转**。

## 过程调用

### 过程机制的三要素

1. **Passing control（传递控制）**：记录函数返回地址，跳转到函数开始地址
2. **Passing data（传递参数）**
3. **Memory management（内存管理）**

### 运行时的栈和栈帧

- 习惯性将栈顶画在底部，从下到上地址增大，栈向低地址生长（向下生长）
- `pushq Src`：使 `%rsp` 减小；`popq Dest`：使 `%rsp` 增加
- push/pop 不会改变栈上的内容，只会改变指针的位置

`callq label`
: 将返回地址 push 到栈上，然后跳转到 label。即栈向下生长一格，将函数返回地址放入，`%rsp` 存的是指向该返回地址的指针；然后 `%rip` 变为函数的开始地址

`ret`
: 从栈上 pop 地址，然后跳转到该地址（即将 PC `%rip` 设置为该地址）。此时过程内的一切东西都会被释放（除了动态申请的内存）

!!! note "label 不占位置"

<figure markdown="span">
  ![栈帧结构示意](https://webp-pic.yokumi.cn/2026/01/20260101164844532.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![call 和 ret 操作示意](https://webp-pic.yokumi.cn/2026/01/20260101164847265.png){ loading=lazy width="70%" }
</figure>

### 栈帧 (Stack Frame)

栈帧即**过程活动记录**，每次调用函数分配一段独立的栈帧，`ret` 时释放栈帧。

一个常见的调用过程的栈内容如下（向下生长，往下为低地址）：

| 内容 | 说明 |
| --- | --- |
| Arg n | 调用者栈帧 |
| $\cdots$ | |
| Arg 7 | 调用者栈帧 |
| Return Addr (Caller's %rip) | 调用者栈帧 |
| optional Callee's %rbp | 被调用者栈帧 |
| Saved Registers + Local Variables | 被调用者栈帧 |
| Arg Build (optional) | 被调用者栈帧（如该函数内部还要调用其他函数，需要传递的参数在这里准备） |

### 数据传送与局部存储

!!! note "以下讨论均为整数类型，浮点数有另一套机制"

#### 参数传递

当传递参数超过 6 个时，x86-64 要求**超过寄存器限制的参数按照从右到左的顺序压入栈（后面的参数先进入栈）**：

<figure markdown="span">
  ![超过6个参数的传递方式](https://webp-pic.yokumi.cn/2026/01/20260101164849558.png){ loading=lazy width="70%" }
</figure>

#### 寄存器保存约定

由于寄存器在所有进程之间进行共享，规定 Callee（被调用者）不会覆盖 Caller（调用者）会使用到的寄存器的值：

Caller Saved（调用者保存）
: **调用者负责保存**在函数调用前需要保留的寄存器值。如果调用者需要在函数调用后继续使用某些寄存器中的值，那么它必须在调用函数之前将这些值保存到栈中或其他地方，并在函数返回后再恢复。通过上述操作，Callee 可以在调用过程中使用和改变这些寄存器的值。

    典型的有：`%r10, %r11, %rax, %rdi, %rsi, %rdx, %rcx, %r8, %r9`

    !!! tip "理解"
        即参数基本寄存器和返回寄存器，调用者需要对自己负责，调用子函数时需要确保这些值不被被调用者改变。

Callee Saved（被调用者保存）
: **被调用者负责保存**在函数调用中需要保护的寄存器值，通常通过压栈来进行（即上面画的 Callee 栈帧中 Saved Registers 的部分）。

    典型的有：`%rbx, %rbp, %r12, %r13, %r14, %r15`

    !!! tip "`%rsp` 的特殊性"
        `%rsp` 比较特殊——调用子函数时，栈指针会往下移至子函数栈帧的栈顶，当子函数结束时，显然需要子函数来恢复栈顶指针指向调用者栈帧的栈顶。

#### 寄存器保存示例

???+ example "Callee Saved 的例子"
    <figure markdown="span">
      ![Callee Saved 示例](https://webp-pic.yokumi.cn/2026/01/20260101164851571.png){ loading=lazy width="70%" }
    </figure>

    首先，`%rdi` 作为 Caller Saved，需要由该函数保存。由于 `%rbx` 为 Callee Saved，其值在该函数运行过程中不会发生改变，所以将 `%rdi` 保存在 `%rbx` 中，通过寄存器实现了保存。

    上述操作导致了一个问题：`%rbx` 作为 Callee Saved，而该函数作为其上一层（主函数）的被调用者，该函数作为被调用者需要保存 `%rbx`。所以该函数一开头将 `%rbx` 压入栈，最后又弹回给 `%rbx`，通过在栈上存储实现了保存。

???+ example "递归的例子"
    <figure markdown="span">
      ![递归调用示例](https://webp-pic.yokumi.cn/2026/01/20260101164854197.png){ loading=lazy width="70%" }
    </figure>

    在该函数中递归调用时，作为主调函数，需要保存 `%rdi`，与上面的例子类似保存在 `%rbx` 中；由于 `%rbx` 是 Callee Saved，`pcouter_r` 作为主函数和上一层 `pcounter_r` 的被调用者，所以也需要保存 `%rbx`。

### 函数调用完整示例

<figure markdown="span">
  ![函数调用完整示例](https://webp-pic.yokumi.cn/2026/01/20260101164857675.png){ loading=lazy width="70%" }
</figure>

???+ question "几个关键问题"
    **栈操作为何不使用传统 push/pop，而是直接移动指针？**

    - 功能上相同：两种方式都用于管理栈上的数据
    - 实现上不同：直接调整 `%rsp` 更高效，尤其在需要分配大块连续内存时；而 push/pop 更适合操作单个寄存器或简单的栈保存和恢复

    **为何多申请了一个 8 字节空间？**

    System V ABI 规范了函数调用时的堆栈布局，以确保各函数之间的参数传递和返回地址的存储符合标准。**堆栈以 16 字节对齐的方式操作**，从而在调用指令（如 `CALL` 和 `RET`）时避免对齐问题。

    **何时申请栈中局部空间，何时不需要？**

    需要申请局部空间的情况：
    - 局部变量无法存放在寄存器中（数量超过可用寄存器，或较大如数组、结构体）
    - 指针操作需要实际内存地址（如 `&v1` 需要将变量地址传递给函数）
    - 函数递归或多层嵌套调用（每次调用分配独立栈帧保存局部变量和状态）

    不需要申请局部空间的情况：
    - 变量可以完全存储在寄存器中（编译器优化时会尽可能将局部变量映射到寄存器）
    - 无需持久化变量状态（局部变量只在寄存器中临时使用且不需要在函数调用间共享）

## 数据结构

### 数组 (Array)

`Type A[L]` 会在内存中分配连续的 $L \times \text{sizeof(Type)}$ 个字节。单独的 `A` 表示数组指针；$A + i$ 事实上是 $A + i \times \text{sizeof(Type)}$ 的地址：

<figure markdown="span">
  ![数组内存布局](https://webp-pic.yokumi.cn/2026/01/20260101164902193.png){ loading=lazy width="70%" }
</figure>

```c
int get_digit(int *a, int x) {
    return a[x];
}

// 翻译成汇编代码
// %rdi = a, %rsi = x;
movl (%rdi, %rsi, 4), %eax;  // a + 4 * x
```

#### 数组与指针的区分

数组可以视为首项的指针，对于两者混用的情况，做出以下区分：

| Decl | | A1, A2 | | | \*A1, \*A2 | |
| --- | :-- | :--- | :--- | ---- | ---------- | ---- |
| | Cmp | Bad | Size | Comp | Bad | Size |
| `int A1[3]` | Y | N | 12 | Y | N | 4 |
| `int *A2` | Y | N | 8 | Y | Y | 4 |

其中 `int *A2` 声明了一个指向整型的指针，但它指向的地址未被指定，即指向一个未被分配的内存空间，是一个**坏指针**：

<figure markdown="span">
  ![数组与指针区分](https://webp-pic.yokumi.cn/2026/01/20260101164904746.png){ loading=lazy width="70%" }
</figure>

更复杂的声明对比：

| Decl | | An | | | \*An | | | \*\*An | |
| --- | --- | --- | ---- | --- | ---- | ---- | --- | ------ | ---- |
| | Cmp | Bad | Size | Cmp | Bad | Size | Cmp | Bad | Size |
| `int A1[3]` | Y | N | 12 | Y | N | 4 | N | - | - |
| `int *A2[3]` | Y | N | 24 | Y | N | 8 | Y | Y | 4 |
| `int (*A3)[3]` | Y | N | 8 | Y | Y | 12 | Y | Y | 4 |
| `int (*A4[3])` | Y | N | 24 | Y | N | 8 | Y | Y | 4 |

!!! tip "声明解读规则"
    - `()` 的优先级最高，`[]` 之，然后是 `*`
    - `int *A2[3]` 等价于 `int (*A4[3])`：`[]` 优先级高于 `*`，所以 `A2[3]` 表示 A2 是数组，`int *` 表示数组的每个元素是一个指向 int 的指针
    - `int (*A3)[3]`：`()` 优先级高于 `[]`，所以 `(*A3)` 表示 A3 是一个**指向包含 3 个整型的数组的指针**

<figure markdown="span">
  ![复杂声明内存布局](https://webp-pic.yokumi.cn/2026/01/20260101164907293.png){ loading=lazy width="70%" }
</figure>

#### 二维数组

二维数组按**行优先**存储：

<figure markdown="span">
  ![二维数组存储方式](https://webp-pic.yokumi.cn/2026/01/20260101164909038.png){ loading=lazy width="70%" }
</figure>

要访问 `A[i][j]`，取 $A + (i \times C + j) \times 4$ 即可。

### 结构体 (Structure)

结构体也是一段连续的内存区域：

<figure markdown="span">
  ![结构体内存布局](https://webp-pic.yokumi.cn/2026/01/20260101164910899.png){ loading=lazy width="70%" }
</figure>

#### 对齐 (Alignment)

结构体的某个类型对象的**地址必须是 $k = 2, 4, 8$ 的倍数（对齐）**。原因是：

**内存访问的单位是块**
: 在现代计算机中，内存通常是以**固定大小的块**（如 4 字节或 8 字节，依赖于系统架构）进行访问的。这种对齐方式是硬件设计的结果，因为大多数处理器一次性加载的数据是 4 字节（32 位）或 8 字节（64 位），以提高性能。

**缓存行 (Cache Line) 的作用**
: 缓存行是 CPU 缓存与内存之间传输数据的最小单位，典型大小为 **64 字节**。当 CPU 访问内存时，会将整块缓存行加载到缓存中，以减少后续访问的延迟。

**跨缓存行访问的影响**
: 如果一个数据（如一个结构体或数组元素）跨越了两个缓存行：

    1. CPU 需要加载两个缓存行（额外的内存访问）
    2. 性能下降，因为需要两次读取操作

**对齐的意义**
: 数据对齐可以避免跨缓存行的情况，确保数据操作只涉及单个缓存行，从而提高访问效率。

**虚拟内存的分页 (Page) 机制**
: 现代操作系统的虚拟内存将内存划分为**页 (Page)**，每页通常是 4 KB。页是内存管理的最小单位，每一页可能映射到不同的物理内存区域，或者部分未分配。

    跨页访问的复杂性：如果一个数据块跨越了两个页：

    1. 操作系统需要处理两次页表查找，性能下降
    2. 如果某一页未映射（如缺页错误），会导致额外的开销
    3. 在某些极端情况下（如页权限不同），可能会引发访问冲突或安全问题

    对齐的重要性：避免数据跨页存储可以减少页表查找和缺页错误，简化虚拟内存管理，提高内存操作效率。

!!! tip "优化建议"
    倾向于将占字节数大的对象放在前面，以减小空间浪费。

### 共用体 (Union)

共用体根据最大的类型对象所占字节数分配内存，一次只能使用一个对象：

<figure markdown="span">
  ![共用体内存布局](https://webp-pic.yokumi.cn/2026/01/20260101164913871.png){ loading=lazy width="70%" }
</figure>

???+ question "`(float) u` 与 bit2float 相同吗？"
    **不相同。**

    - `(float) u`：类型转换，将 unsigned 类型的整数 $u$ 转换为 float 类型。转换时 $u$ 的数值会从整数解释为浮点数，改变其表示方式。例如 $u = 42$ 会被转换为浮点数 42.0。
    - `bit2float`：并不改变位模式，而是通过 union 将 unsigned 类型的位模式**解释**为 float 类型。如果传入的 $u$ 并不是有效的浮点数位模式，结果可能是未定义的浮点数。

???+ question "`(unsigned) f` 与 bit2unsigned 相同吗？"
    同理，**不相同**。

## 进阶：内存分配与安全

### 程序运行的内存分配策略

#### 静态存储分配

编译时就能确定每个数据目标在运行时刻的存储空间需求，因而在编译时就可以给他们分配固定的内存空间。

!!! warning "限制"
    程序代码中**不允许有可变数据结构（比如可变数组）的存在，也不允许有嵌套或者递归的结构出现**，因为会导致编译程序无法计算准确的存储空间需求。

#### 栈式存储分配

在编译期间，过程、函数以及嵌套程序块的活动记录大小（最大值）应该是可以确定的（以便进入的时候动态地分配活动记录的空间），这是进行栈式存储分配的**必要条件**。如果不满足则应该使用堆式存储管理。

#### 堆式存储分配

- **数据对象的生存期与创建它的过程/函数的执行期无关**
- 在任意时刻以任意次序从数据段的堆区分配和释放数据对象的运行时存储空间，分配和释放数据对象的操作是应用程序通过向操作系统提出申请来实现

<figure markdown="span">
  ![内存分配策略对比](https://webp-pic.yokumi.cn/2026/01/20260101164916355.png){ loading=lazy width="70%" }
</figure>

### 缓冲区溢出攻击

<figure markdown="span">
  ![缓冲区溢出攻击示例](https://webp-pic.yokumi.cn/2026/01/20260101164918990.png){ loading=lazy width="70%" }
</figure>

应对之道：

- **Stack Randomization**：栈随机化，栈底指针浮动
- **设置金丝雀 Canary**
- **栈区域规定是不可执行的**

### 金丝雀 (Canary)

```asm
40072f:  sub    $0x18,%rsp        # 分配栈空间 24 bytes
400733:  mov    %fs:0x28,%rax     # Get Canary：%fs:0x28 是一个只读的内存区域
40073c:  mov    %rax,0x8(%rsp)    # Place it on stack（Canary 8 bytes）
400741:  xor    %eax,%eax         # 自己和自己做异或，即擦除 Canary
400743:  mov    %rsp,%rdi
400746:  callq  4006e0 <gets>
40074b:  mov    %rsp,%rdi
40074e:  callq  400570 <puts@plt>
400753:  mov    0x8(%rsp),%rax    # Get it again from stack
400758:  xor    %fs:0x28,%rax     # 重新和只读区域上的值做异或
400761:  je     400768 <echo+0x39> # ZF = 0，即说明两者相等，没问题
400763:  callq  400580 <__stack_chk_fail@plt> # 否则说明 stack 上的 Canary 被顶掉，Fail
400768:  add    $0x18,%rsp
40076c:  retq
```

!!! info "Canary 机制原理"
    1. 从只读内存区域 `%fs:0x28` 获取 Canary 值，放入栈中
    2. 函数执行完毕后，将栈上的 Canary 值与只读区域原始值做异或比较
    3. 如果两者相等（ZF = 0），说明 Canary 未被篡改，正常返回
    4. 如果不等，说明栈上的 Canary 被溢出顶掉，调用 `__stack_chk_fail` 失败处理

### 面向返回攻击 (Return-Oriented Programming Attacks, ROP)

利用已有的代码片段（Gadget），跳转到 Gadgets 上逐步执行操作：

<figure markdown="span">
  ![ROP 攻击示意](https://webp-pic.yokumi.cn/2026/01/20260101164920974.png){ loading=lazy width="70%" }
</figure>

!!! warning "ROP 与 Canary"
    ROP 攻击仍然防不了金丝雀机制。

