# 链接

## 链接概述

源程序的编译 `gcc -Og -o prog main.c swap.c` 可以分为以下四个阶段：

Pre-Processor 预处理 (cpp)
: `cpp -o main.i main.c` 或 `gcc -E -o main.i main.c`，`-E` 为限制 gcc 只做预处理工作

Compiler 编译 (ccl)
: `cc -S -o main.s main.i` 或 `gcc -S -o main.s main.i`，`-S` 表示只做编译

Assembler 汇编 (as)
: `as -o main.o main.s`，这步得到的是**可重定位文件**

Linker 链接 (ld)
: `ld -static -o prog main.o sum.o` 以及其他库文件，`-static` 表示静态编译

<figure markdown="span">
  ![编译的四个阶段](https://webp-pic.yokumi.cn/2026/01/20260101164359701.png){ loading=lazy width="70%" }
</figure>

链接动作在编译、加载和运行时都可以被执行。

## 静态链接器的任务

### 1. 符号解析（Symbol Resolution）

将**引用符号和定义符号建立关联**。定义的实质是被分配了存储空间：为函数名指定其代码所在区，为变量名指定其所占的静态数据区。需要掌握如何区分定义符号和引用符号。

### 2. 重定位（Relocation）

- 合并相同的节：例如，所有 `.text` 节合并作为可执行文件中的 `.text` 节
- 对定义符号进行重定位，确定地址：例如，为函数确定首地址，进而确定每条指令的地址，为变量确定首地址
- 对引用符号进行重定位，确定地址：需要用到在 `.rel_data` 和 `.rel_text` 节中保存的重定位信息

## 符号解析

### 三类符号

Global symbol（全局符号）
: 自定他用，全局可见，跨模块使用，在链接时进行符号解析

External symbol（外部符号）
: 他定自用，与 Global symbol 相对，链接时在其他模块中查找

Local symbol（局部符号）
: 自定自用，局部符号通常由 `static` 修饰，限制其作用域

!!! warning "区分 Local non-static variables 与 Local static variables"

    ```c
    static int x = 15;

    int f() {
        static int x = 17;
        return x++;
    }

    int g() {
        static int x = 19;
        return x += 14;
    }

    int h() {
        return x += 27;
    }
    ```

    函数 $f$ 和 $g$ 中的 $x$ 都是作用域在函数内的**局部静态变量**，最外面的 $x$（即函数 $h$ 引用的）是**文件范围内的静态变量**。

### 全局符号的多重定义

如果存在多个同名全局变量，需要区分强符号与弱符号：

强符号
: **函数以及初始化的全局变量**

弱符号
: **未初始化的全局变量**

<figure markdown="span">
  ![强符号与弱符号的规则](https://webp-pic.yokumi.cn/2026/01/20260101164404714.png){ loading=lazy width="70%" }
</figure>

规则如下：

1. 不许有多个同名的强符号，否则 Linker error
2. 如果有一个同名的强符号和多个弱符号，则取强
3. 如果有多个同名的弱符号，随机选择

!!! danger "链接器不做类型检查"

    <figure markdown="span">
      ![链接器不做类型检查导致的问题](https://webp-pic.yokumi.cn/2026/01/20260101164408558.png){ loading=lazy width="70%" }
    </figure>

    引用 double 类型的 $x$ 变量（8 bytes）时可能会覆盖 $y$ 的空间。

## 目标文件（Object Files）

可重定位目标文件（.o file）
: 包含代码和数据，可与其他可重定位目标文件合并生成可执行目标文件

可执行目标文件（a.out file）
: 可重定位目标文件经过链接得到的产物，可以直接复制到内存中并执行

共享目标文件（.so file）
: 特殊的可重定位目标文件，可以在程序加载或运行时被动态地加载进内存并链接

## ELF 可重定位目标文件格式

<figure markdown="span">
  ![ELF可重定位目标文件格式](https://webp-pic.yokumi.cn/2026/01/20260101164411802.png){ loading=lazy width="70%" }
</figure>

ELF header
: 16 字节的序列，包括字的大小等信息

`.text` section
: 代码段

`.rodata` section
: 只读数据，比如 switch 的跳转表、printf 的格式字符串

`.data`
: 初始化的全局变量和静态 C 变量

`.bss`
: 未初始化以及初始化为 0 的全局变量和静态 C 变量。实际上不占用任何存储空间，仅是一个占位符（Better Save Space）。运行时自动分配这些变量的初始值为 0

!!! note ".bss 与 COMMON 的区别"

    `.bss` 存放未被初始化的静态变量以及初始化为 0 的全局或静态变量；COMMON 存放未被初始化的全局变量。

`.symtab`
: 符号表

`.rel.text` / `.rel.data`
: 占位符，即引用别的模块中定义的全局变量和函数的指令的占位符

<figure markdown="span">
  ![rel节中的占位符](https://webp-pic.yokumi.cn/2026/01/20260101164415045.png){ loading=lazy width="70%" }
</figure>

`.debug`
: 调试信息（需要加上 `gcc -g`）

Section header table
: 每个节的大小信息

## 可执行目标文件格式

<figure markdown="span">
  ![可执行目标文件格式](https://webp-pic.yokumi.cn/2026/01/20260101164421100.png){ loading=lazy width="70%" }
</figure>

与可重定位目标文件相比：

- **多了**程序头表：包含第一条指令的地址
- **少了** `.rel.text` 和 `.rel.data`，因为已经链接完毕，无需再重定位

## 重定位

### 重定位信息

<figure markdown="span">
  ![重定位信息](https://webp-pic.yokumi.cn/2026/01/20260101164424700.png){ loading=lazy width="70%" }
</figure>

### R_386_PC32 重定位方式

<figure markdown="span">
  ![R_386_PC32重定位示例](https://webp-pic.yokumi.cn/2026/01/20260101164431238.png){ loading=lazy width="70%" }
</figure>

根据重定位前的 `.o` 文件，能得到哪些信息？

- `main` 在 `.text` 节中偏移为 0 处开始，占 $0x12$ bytes
- `e8 fc ff ff ff` 中，`e8` 是 `call` 的机器码，后面应该存放 `swap` 函数的地址，但目前未重定位，所以没有意义，是占位符
- 下一行的 `7: R_386_PC32 swap` 也是占位符，用于重定位：7 表示需要在地址 7（$6 + 1$，`call` 的机器码占一个字节）处进行重定位，`R_386_PC32` 表示需要计算的是 PC 相对地址

<figure markdown="span">
  ![R_386_PC32重定位计算过程](https://webp-pic.yokumi.cn/2026/01/20260101164435560.png){ loading=lazy width="70%" }
</figure>

???+ example "重定位计算详解"

    <figure markdown="span">
      ![重定位计算问题](https://webp-pic.yokumi.cn/2026/01/20260101164440630.png){ loading=lazy width="70%" }
    </figure>

    `main` 函数从 $0x8048380$ 开始，占 $0x12$ bytes，`swap` 紧跟 `main` 后，所以其起始地址为 $0x8048380 + 0x12 = 0x8048392$，由于机器代码首地址需要按 4 字节边界对齐，所以应该是 $0x8048394$。

    **重定位后，call 指令的机器代码应该是什么？**

    1. 由于采用 `R_386_PC32` 相对地址法，转移目标地址 $= \text{PC} + \text{偏移地址（重定位值）}$
    2. 在执行 `call` 时，PC 指向 `call` 指令的下一条地址，即 $0x8048380 + 0x7 = 0x8048387$
    3. 但是，由于一开始有一个占位的初始偏移值 `fc ff ff ff`（即 $-4$），链接器在进行重定位之前，会先减掉这个临时的偏移量，所以正确的 PC 地址应该是 $0x8048387 - (-4) = 0x804838b$
    4. 事实上，这个 PC 地址就是 `call` 指令的下一条语句的地址
    5. 重定位值 $= \text{转移目标地址} - \text{PC} = 0x8048394 - 0x804838b = 0x9$
    6. 链接器将 `call` 指令的机器代码修正为 `e8 09 00 00 00`（小端法）

### R_386_32 重定位方式

<figure markdown="span">
  ![R_386_32重定位方式](https://webp-pic.yokumi.cn/2026/01/20260101164444553.png){ loading=lazy width="70%" }
</figure>

## 静态库链接（Static Libraries）

将所有相关的目标文件模块打包成一个单独的文件，称为静态库。使链接器构造可执行文件时，只要复制静态库里被程序引用的目标模块，相比于链接整个模块，减少了可执行文件在磁盘和内存中的大小。

```Shell
# 创建静态库
unix> ar rs libc.a \
  atoi.o printf.o ... random.o
```

<figure markdown="span">
  ![静态库的创建与使用](https://webp-pic.yokumi.cn/2026/01/20260101164448410.png){ loading=lazy width="70%" }
</figure>

```Shell
# 与静态库链接
unix> gcc -static -o prog2r \
  main2.o -L. -lvector
```

<figure markdown="span">
  ![与静态库链接的过程](https://webp-pic.yokumi.cn/2026/01/20260101164452332.png){ loading=lazy width="70%" }
</figure>

### 自定义创建静态库

```Shell
gcc -c myproc1.c myproc2.c
ar rcs mylib.a myproc1.o myproc2.o

gcc -c main.c
gcc -static -o myproc main.o ./mylib.a  # 标准的静态库无需显式给出
```

### 符号解析的完整过程

在进行符号解析的过程中，按从左往右的顺序进行链接，并将符号分为三个集合：

- **E**：合并以组成可执行文件的所有目标文件集合
- **U**：当前所有未解析的引用符号
- **D**：当前所有定义的符号的集合，来更新 U 和 E

???+ example "符号解析示例"

    <figure markdown="span">
      ![符号解析完整过程](https://webp-pic.yokumi.cn/2026/01/20260101164455104.png){ loading=lazy width="70%" }
    </figure>

    1. 扫描到 `main.o` 并加入 E
    2. 把 `main.o` 中未解析的引用 `myfunc` 加入 U，把 `main` 加入 D
    3. 扫描到静态库文件 `mylib.a`，将 U 中的符号与 `mylib.a` 中所有目标模块依次匹配，将 `myfunc` 从 U 中删除移到 D，将 `myproc1.o` 加入 E
    4. 此时 `myproc1.o` 中发现未定义 `printf` 符号，将其加入到 U
    5. 不断扫描静态库文件，直至 U、D 不变
    6. 扫描默认的库文件 `libc.a` 时，找到 `printf.o` 定义，将 `printf.o` 加入到 E，并将 `printf` 从 U 移动到 D，此时 U 一定是空的，否则就报错了
    7. 由于未引用 `myproc2.o` 的内容，它并不在 E 中，被丢弃

!!! warning "静态库链接的顺序扫描问题"

    <figure markdown="span">
      ![静态库顺序扫描导致的问题](https://webp-pic.yokumi.cn/2026/01/20260101164500525.png){ loading=lazy width="70%" }
    </figure>

    好的做法是**将静态库放在命令行最后**。如果静态库之间并不相互独立，静态库需要重复出现：

    <figure markdown="span">
      ![静态库需要重复出现](https://webp-pic.yokumi.cn/2026/01/20260101164505173.png){ loading=lazy width="70%" }
    </figure>

### 静态库的缺陷

- 主存资源浪费
- 磁盘空间浪费
- 更新困难，使用不便

## 动态链接的共享库（Shared Libraries）

共享库是一个目标文件（Linux：`.so` 文件；Windows：`.dll` 文件），从程序中分离出来，磁盘和内存中都只有一个备份。可以**在程序运行或加载时，加载到内存的任意位置，并和一个内存中的程序链接起来，称为动态链接**。

<figure markdown="span">
  ![动态链接示意图](https://webp-pic.yokumi.cn/2026/01/20260101164508248.png){ loading=lazy width="70%" }
</figure>

`ldd prog` 可以打印出可执行文件需要的动态链接库。

### 自定义创建动态链接库

```Shell
unix> gcc -Og -c test1.c test2.c
unix> gcc -shared -fpic -o test.so \
  test1.o test2.o

unix> gcc -c main.c
unix> gcc -o test main.o ./test.so
```

`-fpic` 是生成位置无关的共享库代码文件。

### 加载时的动态链接过程

<figure markdown="span">
  ![加载时的动态链接过程](https://webp-pic.yokumi.cn/2026/01/20260101164513174.png){ loading=lazy width="70%" }
</figure>

1. 在静态链接器 `ld` 链接的过程中，生成重定位和符号表信息
2. 加载可执行程序时，加载器发现在程序表中的 `.interp` 段，其中包含了动态链接器路径名 `ld-linux.so`，因而加载器根据指定路径加载并启动动态链接器运行
3. 完成重定位后，将控制权交给可执行文件，开始执行程序

### 运行时的动态链接过程

```c
#include <dlfcn.h>

/* Dynamically load the shared library that contains addvec() */
handle = dlopen("./libvector.so", RTLD_LAZY);

/* Get a pointer to the addvec() function we just loaded */
addvec = dlsym(handle, "addvec");

/* Now we can call addvec() just like any other function */
addvec(x, y, z, 2);

/* Unload the shared library */
dlclose(handle);
```

<figure markdown="span">
  ![运行时的动态链接过程](https://webp-pic.yokumi.cn/2026/01/20260101164518116.png){ loading=lazy width="70%" }
</figure>

### 延迟绑定（Lazy Binding）

上述过程也被称为**延迟绑定**，它将函数地址的绑定推迟到**函数第一次被调用时**，而不是在程序加载到内存时立即完成所有函数地址的绑定。

延迟绑定依赖两种关键的数据结构：**GOT（全局偏移表）** 和 **PLT（过程链接表）**。

GOT（全局偏移表）
: 一个包含地址的表，存放在程序的数据段中（`.data` 或 `.bss`）。每个引用的全局对象（包括全局变量和动态链接函数）在 GOT 中占据一个条目（8 字节）。每个目标模块（目标文件或共享库）都会有自己的独立 GOT。在程序加载时，动态链接器计算全局变量或函数的绝对地址，将每个 GOT 条目更新为对应全局对象的**绝对地址**。

PLT（过程链接表）
: 一段可执行代码，用来间接调用动态链接的函数。每个动态链接的函数在 PLT 中都有一个对应的条目，**每个条目大小为 16 字节**。在程序中，所有对动态函数的调用都会先跳转到对应的 PLT 条目，而不是直接调用函数地址。每个动态函数在 GOT 中都有一个对应的条目，初始状态下，该条目指向动态链接器的解析代码。当动态链接器解析了目标函数地址后，会更新对应的 GOT 条目为函数的实际地址。

???+ info "PLT/GOT 的调用流程"

    **第一次调用函数**：

    1. PLT 条目先访问 GOT，发现 GOT 中的地址是动态链接器的入口
    2. 动态链接器解析函数的实际地址，并更新 GOT 条目

    **后续调用函数**：

    - PLT 条目直接跳转到 GOT 条目中存储的函数地址，避免重复解析

<figure markdown="span">
  ![GOT与PLT的工作机制](https://webp-pic.yokumi.cn/2026/01/20260101164522129.png){ loading=lazy width="70%" }
</figure>

