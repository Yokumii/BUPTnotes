# 信息的表示与处理

## 信息的表示

### 字长

: 32 位机器的字长为 4 Bytes（$32/8$），寻址空间为 $2^{32} = 4 \times 2^{30} = 4\text{GB}$。

    内存中，32 位机器最小连续字间隔 4 Byte，64 位机器最小连续字间隔 8 Byte，字节 Byte 是最基本的存储单元。

<figure markdown="span">
  ![内存管理方式示意图](https://webp-pic.yokumi.cn/2026/01/20260101164631896.png){ loading=lazy width="70%" }
</figure>

### 数据表示

不同数据类型在不同平台下的字长不同：`int` 可以跨平台兼容，而 `long` 和 `pointer` 在 32 位与 64 位平台下字长不同。

<figure markdown="span">
  ![不同平台下的数据类型字长](https://webp-pic.yokumi.cn/2026/01/20260101164634863.png){ loading=lazy width="70%" }
</figure>

### 字节序

数据在内存中的存放顺序分为两种：

- **大端法**（Big Endian）：最高有效字节放在最低地址
- **小端法**（Little Endian）：最低有效字节放在最低地址

以 `int x = 0x01234567, &x = 0x100` 为例：

| Address       | 0x100 | 0x101 | 0x102 | 0x103 |
| ------------- | ----- | ----- | ----- | ----- |
| Big Endian    | 01    | 23    | 45    | 67    |
| Little Endian | 67    | 45    | 23    | 01    |

???+ example "字节序验证程序"
    ```c
    #include <stdio.h>

    typedef unsigned char *pointer;

    void show_bytes(pointer start, size_t len) {
        // 从数据的指针开始打印数据，即从低地址开始打印
        size_t i;
        for (i = 0; i < len; i++)
            printf("%p\t0x%.2x\n", start + i, start[i]);
        printf("\n");
    }

    int main(void) {
        int a = 15213; // 15213 = 00 00 3b 6d;
        printf("int a = 15213;\n");
        show_bytes((pointer) &a, sizeof(int));

        int b = -15213;
        printf("int b = -15213;\n");
        show_bytes((pointer) &b, sizeof(int));

        char s[6] = "18213";
        printf("string s = \"18213\"\n");
        show_bytes((pointer) &s, sizeof(s));
        return 0;
    }
    ```

    !!! tip "字符数组的字节序"
        对于字符数组，每个字符按照小端法存储，因此整个字符串在大端法和小端法下的表现完全相同。

### 数据的存储排列

<figure markdown="span">
  ![数据的存储排列练习题](https://webp-pic.yokumi.cn/2026/01/20260101164638996.png){ loading=lazy width="70%" }
</figure>

???+ success "解答"
    0x08000100

### 边界对齐

: 按边界对齐（以 32 位机器为例，按字节编址，4 个字节同时读写）：

    - 字地址：4 的倍数
    - 半字地址：2 的倍数
    - 字节地址：任意

    按边界对齐浪费了一些空间，但减少了访存次数。

<figure markdown="span">
  ![边界对齐示意图](https://webp-pic.yokumi.cn/2026/01/20260101164641207.png){ loading=lazy width="70%" }
</figure>

### 运算

#### 布尔运算

按位与、按位取反等操作，对每一位独立运算：

- $\sim 0x41(01000001) \rightarrow 10111110 = 0xBE$
- $\sim 0x00 \rightarrow 0xFF$
- $0x69 \& 0x55 \rightarrow 01101001 \& 01010101 = 01000001$

#### 逻辑运算

`||`、`&&`、`!`：运算结果只有 0 或 1（只要不为 0 即为 1）。注意与布尔运算区分——逻辑运算是对整体真假的判断，而非逐位操作。

#### 移位运算

- 逻辑左移/右移：空位补 0
- 算术右移：左侧填充符号位（正数补 0，负数补 1）

???+ warning "算术右移的符号位填充"
    算术右移的左边填充符号位，这是保证负数右移后仍为负数的关键。

### 无符号数与有符号数的比较

运算时，有符号数优先转化为无符号数。数据类型只决定读取方式，不改变存储方式（01 串本身不变）。

| 关系表达式                                          | 运算类型   | 结果    | 说明                                                                           |
| :------------------------------------------------- | :------- | :----- | :---------------------------------------------------------------------------- |
| $0 == 0U$                                          | unsigned | True   |                                                                               |
| $-1 < 0$                                           | signed   | True   |                                                                               |
| $-1 < 0U$                                          | unsigned | False  | $-1 = 1\cdots1_2 = U_{max} > 0$                                               |
| $2147483647(2^{31}-1) > -2147483637-1$             | signed   | True   |                                                                               |
| $2147483647U > -2147483637-1$                      | unsigned | False  | $-2147483637-1 = T_{min} \rightarrow 1\cdots0U = 2^{31} > 2^{31}-1$           |
| $2147483647 > (int)2147483648U$                    | signed   | True   | $(int)2147483648U = 1\cdots0 = -2^{31}$                                       |
| $-1 > -2$                                          | signed   | True   |                                                                               |
| $(unsigned)-1 > -2$                                | unsigned | True   | $(unsigned)-1 = U_{max}$                                                      |

???+ danger "`sizeof()` 返回 `unsigned int`"
    `sizeof()` 的返回类型为 `unsigned int`，以下代码会导致死循环：

    <figure markdown="span">
      ![sizeof导致死循环的代码示例](https://webp-pic.yokumi.cn/2026/01/20260101164651221.png){ loading=lazy width="70%" }
    </figure>

    因为 `i` 与 `sizeof()` 的返回值做比较时，`i` 被转换为无符号数，负数变为大正数，条件始终为真。

<figure markdown="span">
  ![无符号数与有符号数比较注意事项](https://webp-pic.yokumi.cn/2026/01/20260101164644799.png){ loading=lazy width="70%" }
</figure>

### 位扩展与位截断

#### 符号扩展（Sign Extension）

: 根据最高位（符号位）决定补 0 或补 1。正数高位补 0，负数高位补 1，保证扩展后数值不变。

#### 位截断（Sign Truncation）

: 无符号数截断：

    $$B2U_k(x_{k-1}\cdots x_0) = B2U_w(x_{w-1}\cdots x_0) \bmod 2^k$$

    有符号数截断：

    $$B2T_k(x_{k-1}\cdots x_0) = U2T_w(B2U_w(x_{w-1}\cdots x_0) \bmod 2^k)$$

    即先截断再重新解释。

???+ example "位扩展与截断示例"
    <figure markdown="span">
      ![位扩展与截断练习题](https://webp-pic.yokumi.cn/2026/01/20260101164653537.png){ loading=lazy width="70%" }
    </figure>

    解答：
    ```c
    short si = 0x8000 = -32768;
    unsigned short usi = 0x8000 = 32768;
    int i = 0xFFFF8000 = -32768;
    unsigned ui = 0x00008000 = 32768;
    ```

    <figure markdown="span">
      ![截断后再扩展的练习题](https://webp-pic.yokumi.cn/2026/01/20260101164656766.png){ loading=lazy width="70%" }
    </figure>

    解答：
    ```c
    int i = 0x00008000 = 32768;
    short si = (short)i = 0x8000 = -32768;
    int j = si = 0xFFFF8000 = -32768;
    ```

## 整数运算

### 加法

#### 无符号数加法

$$s = UAdd_w(u, v) = (u + v) \bmod 2^w$$

结果寄存器会截断溢出的最高位。

!!! warning "无符号数加法溢出"
    溢出时，结果一定小于任何一个加数。

#### 有符号数加法

$$s = (int)((unsigned)u + (unsigned)v)$$

- **正溢出**：$x + y \ge 2^{w-1}$，截断后结果为 $x + y - 2^w$
- **负溢出**：$x + y < -2^{w-1}$，截断后结果为 $x + y + 2^w$
- 正数 + 负数：不可能溢出

### 减法

用加法实现减法：

$$[A - B]_{\text{补}} = [A]_{\text{补}} + [-B]_{\text{补}}$$

求 $[-B]_{\text{补}}$ 的推导：

$$[B]_{\text{补}} + [-B]_{\text{补}} = 11\cdots1$$

$$\sim[B]_{\text{补}} + [B]_{\text{补}} + 1 = 11\cdots1 + 1 = 0$$

$$[-B]_{\text{补}} = \sim[B]_{\text{补}} + 1$$

???+ tip "补码求负的要点"
    已知 $B$ 的补码，求 $-B$ 的补码：按位取反再加 1 即可。

### 加法逆元

- **无符号数**：$-x = 2^w - x$（$x \ne 0$），0 的逆元是 0
- **有符号数**：$x + (-x) = 0$；特例 $T_{min}$：$10\cdots0 + 10\cdots0 = 0$，即 $-T_{min} = T_{min}$

???+ warning "$T_{min}$ 的加法逆元是其自身"
    由于补码表示的不对称性（$T_{min}$ 的绝对值比 $T_{max}$ 大 1），$-T_{min}$ 无法在有符号数范围内表示，因此 $-T_{min} = T_{min}$。

### 加法器与条件码

<figure markdown="span">
  ![加法器电路与条件码](https://webp-pic.yokumi.cn/2026/01/20260101164700031.png){ loading=lazy width="70%" }
</figure>

条件码的定义：

- **CF**（Carry Flag）：当做减法（Sub = 1）或产生进位（Co = 1）时 $CF = 1$，表示发生借位或进位
- **SF**（Sign Flag）：运算结果的符号位
- **ZF**（Zero Flag）：$ZF = 1$ 当 Sum = 0
- **OF**（Overflow Flag）：$OF = 1$ 当两个加数同号但与 Sum 异号（即发生溢出的情形）

<figure markdown="span">
  ![条件码练习题](https://webp-pic.yokumi.cn/2026/01/20260101164706562.png){ loading=lazy width="70%" }
</figure>

???+ example "条件码计算示例"
    ```c
    unsigned int x = 1000 0110;
    unsigned int y = 1111 0110; // -y_补 = 00001010

    int m = x = 1000 0110 = -122;
    int n = y = 1111 0110 = -10;
    ```

    **减法运算**：

    ```c
    // CF = 1（减法有借位），OF = 0（并没有溢出），SF = 1
    unsigned int z1 = x - y = 1000 0110 + 00001010 = 10010000 = 144;
    int k1 = m - n = 10010000 = -112 = -112 - (-10);
    ```

    **加法运算**：

    ```c
    // CF = 1（有进位），OF = 1（发生溢出），SF = 0
    unsigned int z2 = x + y = 1000 0110 + 11110110 = 01111100 = 124 = (134 + 246) % 256;
    int k2 = m + n = 01111100 = 124 = -122 - 10 + 256;
    ```

### 乘法

1. **无符号数乘法**：和加法类似进行截断，即 $(u \times v) \bmod 2^w$
2. **补码乘法**：先按无符号数进行乘法运算截断，然后将结果转化为有符号数
3. **变量与常数之间的乘运算**（左移实现）：

<figure markdown="span">
  ![乘法与左移的关系](https://webp-pic.yokumi.cn/2026/01/20260101164709364.png){ loading=lazy width="70%" }
</figure>

### 除法

1. **变量与常数之间的除运算**（算术右移实现）：

<figure markdown="span">
  ![除法与算术右移的关系](https://webp-pic.yokumi.cn/2026/01/20260101164716773.png){ loading=lazy width="70%" }
</figure>

2. **负数向 0 取整的偏移量**：负数做算术右移时需要加偏移量以保证向 0 取整：

$$x = (x + (1 << k) - 1) >> k$$

## 浮点数

### 二进制表示方法

引入负指数即可表示小数部分。其缺陷是无法同时平衡整数部分的范围和小数部分的精度。

### IEEE 754 标准

<figure markdown="span">
  ![IEEE 754 浮点数格式](https://webp-pic.yokumi.cn/2026/01/20260101164723330.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![IEEE 754 浮点数格式详细说明](https://webp-pic.yokumi.cn/2026/01/20260101164728208.png){ loading=lazy width="70%" }
</figure>

浮点数的组成：

- **exp**：阶码（exponent）
- **frac**：尾数（fraction）

#### 规格化数（Normalized）

: exp 不全为 0 且不全为 1。

    $$E = exp - Bias = exp - (2^{k-1} - 1)$$

    - 32 bits：$Bias = 2^7 - 1 = 127$, $exp \in [1, 254] \rightarrow E \in [-126, 127]$
    - 64 bits：$Bias = 2^{10} - 1 = 1023$, $exp \in [1, 2046] \rightarrow E \in [-1022, 1023]$

    尾数：$M = 1.frac_{(2)}$（隐含的整数部分 1 不存储）

#### 非规格化数（Denormalized）

: exp 全为 0。

    $$E = 1 - Bias$$

    $$M = frac$$

    ???+ info "非规格化数的阶码偏置"
        非规格化数的阶码使用 $1 - Bias$ 而非 $0 - Bias$，是为了保证从非规格化数到规格化数的平滑过渡。

#### 特殊值（Special Values）

: exp 全为 1。

    - exp 全为 1，frac 全为 0：$s = 0$ 表示正无穷 $+\infty$，$s = 1$ 表示负无穷 $-\infty$
    - exp 全为 1，frac 不为 0：表示 NaN（Not a Number）

<figure markdown="span">
  ![浮点数各类值的分布](https://webp-pic.yokumi.cn/2026/01/20260101164731925.png){ loading=lazy width="70%" }
</figure>

???+ info "浮点数分布特点"
    在 0 附近均匀分布，向外逐渐扩大（呈指数分布）。

### 舍入规则

IEEE 754 采用**向偶数舍入**（round to even）：四舍六入五向偶——当舍入位恰好为 5 时，向最近的偶数方向舍入。

### 类型转换

| 转换方向                    | 说明                                                                   |
| :------------------------- | :------------------------------------------------------------------- |
| $double/float \rightarrow int$ | 直接对实际存储的二进制串进行位截断；体现为向 0 舍入；超界的情况转化为 $T_{min}$ |
| $int \rightarrow float$        | 位数相同，不会截断，但可能会发生舍入                                     |
| $int/float \rightarrow double$ | double 的有效位数更多，能保留精确度                                      |
| $double \rightarrow float$     | 能表达的范围变小，可能溢出为 $\infty$，并且精度降低，可能发生舍入         |

???+ example "类型转换练习题"
    <figure markdown="span">
      ![类型转换练习题](https://webp-pic.yokumi.cn/2026/01/20260101164734519.png){ loading=lazy width="70%" }
    </figure>

    解答：

    1. $x$ 如果很大，`(float)x` 会发生舍入
    2. `double` 表示范围大于 `int`，所以能精确表示
    3. 同理 2
    4. `(float)d` 会发生溢出或舍入
    5. 没有问题，`-f` 或 `-d` 就是符号位取反即可

???+ warning "浮点数加法不满足结合律"
    由于精度限制和舍入的存在，浮点数加法运算不满足结合律，即 $(a + b) + c \ne a + (b + c)$ 在某些情况下可能成立。
