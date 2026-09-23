# CSAPP 习题解答

本文收录《Computer Systems: A Programmer's Perspective》（CSAPP）课后习题的个人解答，涵盖第2、3、7、10章，侧重信息表示、机器级表示、链接与系统级 I/O 等核心主题。

## 第2章：信息的表示与处理

### 练习 2.21

<figure markdown="span">
  ![练习2.21题图](https://webp-pic.yokumi.cn/2026/01/20260101153934267.png){ loading=lazy width="70%" }
</figure>

### 练习 2.23

<figure markdown="span">
  ![练习2.23题图](https://webp-pic.yokumi.cn/2026/01/20260101153945718.png){ loading=lazy width="70%" }
</figure>

### 练习 2.24

<figure markdown="span">
  ![练习2.24题图](https://webp-pic.yokumi.cn/2026/01/20260101153953784.png){ loading=lazy width="70%" }
</figure>

???+ details "解答要点"
    两种类型都是先截断（对对应的无符号数取模操作），补码的话再进行一次 U2T 转化。

### 练习 2.33

<figure markdown="span">
  ![练习2.33题图](https://webp-pic.yokumi.cn/2026/01/20260101154000966.png){ loading=lazy width="70%" }
</figure>

### 练习 2.40

<figure markdown="span">
  ![练习2.40题图](https://webp-pic.yokumi.cn/2026/01/20260101154013807.png){ loading=lazy width="70%" }
</figure>

### 练习 2.44

<figure markdown="span">
  ![练习2.44题图](https://webp-pic.yokumi.cn/2026/01/20260101154024764.png){ loading=lazy width="70%" }
</figure>

???+ details "逐项解答"
    **A.** 反例：$x = -1$，此时 $x - 1 = 0$，不满足条件。

    **B.** $x \& 0111_2 \ne 0111_2$ 当 $x$ 的低3位有1位等于0时即可成立；$x \ll 29 < 0$ 将 $x$ 的低3位移到高3位。低三位如果全为1则后者为真，有0则前者为真，因此表达式恒为真。

    **C.** 反例：$x$ 为一个比较大的正数，平方后超过 $2^{31} - 1$。

    **D.** 真：当 $x = \text{TMin}$ 时 $-x = \text{TMin}$；其余情况若 $x$ 为负数，$-x$ 必为非负数。

    **E.** 反例：$x = \text{TMin}$，此时 $-x = \text{TMin}$，二者相等。

    **F.** 真：比较类型为无符号数比较，加法都按补码运算，两边二进制结果显然一致。

    **G.** 真：$-y = \sim y + 1 \Rightarrow \sim y = -y - 1 \Rightarrow x \cdot \sim y + u_y \cdot u_x = x \cdot (-y + y - 1) = -x$。全部按二进制表示理解即可。

### 练习 2.45

<figure markdown="span">
  ![练习2.45题图](https://webp-pic.yokumi.cn/2026/01/20260101154035971.png){ loading=lazy width="70%" }
</figure>

### 练习 2.47

<figure markdown="span">
  ![练习2.47题图](https://webp-pic.yokumi.cn/2026/01/20260101155959429.png){ loading=lazy width="70%" }
</figure>

### 练习 2.54

<figure markdown="span">
  ![练习2.54题图](https://webp-pic.yokumi.cn/2026/01/20260101154117861.png){ loading=lazy width="70%" }
</figure>

???+ details "逐项解答"
    **A.** 真：`double` 范围和精度比 `int` 大。

    **B.** 假：`int` 转化为 `float` 可能会发生舍入。

    **C.** 假：`double` 转化为 `float` 会截断。

    **D.** 真：`double` 范围和精度比 `float` 大。

    **E.** 真：只需改变符号位即可。

    **F.** 真：两边都先转化为 `double` 类型再运算。

    **G.** 真：即使溢出到正无穷也大于0。

    **H.** 假：浮点数运算不满足结合律。

### 练习 2.60

<figure markdown="span">
  ![练习2.60题图](https://webp-pic.yokumi.cn/2026/01/20260101154123278.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```c
    unsigned replace_byte(unsigned x, int i, unsigned char b) {
        int i_times_8 = i << 3; // 将字节单位转化为位
        unsigned mask = 0xFF << i_times_8; // 0xFF 左移 i 个字节，得到第 i 个字节为 FF，其余全为 0
        // x & ~mask 可以将 x 的第 i 个字节清 0
        // b << i_times_8 将 b 移动到第 i 个字节上
        // 两者进行或运算即可实现替换
        return (x & ~mask) | (b << i_times_8);
    }
    ```

### 练习 2.65

<figure markdown="span">
  ![练习2.65题图](https://webp-pic.yokumi.cn/2026/01/20260101154129633.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```c
    int odd_ones(unsigned x) {
        // 高位和低位进行异或：1对0得1，1对1或0对0得0
        // 高位有奇数个1还是偶数个1的信息被转移到低位中
        x = x ^ (x >> 16); // 将 x 的高16位与低16位异或
        x = x ^ (x >> 8);
        x = x ^ (x >> 4);
        x = x ^ (x >> 2);
        x = x & 1;
        return x;
    }
    ```

### 练习 2.67

<figure markdown="span">
  ![练习2.67题图](https://webp-pic.yokumi.cn/2026/01/20260101154133033.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    **A.** C 标准中，在32位机器上，移位32位是一种未定义的行为。

    **B.** 先移31位，再移一位即可：

    ```c
    int beyond_msb = 1 << 32;
    // 改为
    int beyond_msb = set_msb << 1;
    ```

    **C.** 类似地（16位机器上，移动 $n + 16$ 位和移动 $n$ 位效果一样）：

    ```c
    int set_msb = 1 << 15;
    int beyond_msb = set_msb << 1;
    ```

### 练习 2.68

<figure markdown="span">
  ![练习2.68题图](https://webp-pic.yokumi.cn/2026/01/20260101154136769.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```c
    int lower_one_mask(int n) {
        unsigned Part = -1; // 各位全1
        unsigned len = sizeof(int) * 8 - n; // 右移位数
        return (int)(Part >> len);
    }
    ```

## 第3章：机器级表示

### 练习 3.1

<figure markdown="span">
  ![练习3.1题图](https://webp-pic.yokumi.cn/2026/01/20260101154141184.png){ loading=lazy width="70%" }
</figure>

### 练习 3.2

<figure markdown="span">
  ![练习3.2题图](https://webp-pic.yokumi.cn/2026/01/20260101154151421.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```asmx86
    movl %eax, (%rsp)
    movw (%rax), %dx
    movb $0xFF, %bl
    movb (%rsp, %rdx, 4), %dl
    movq (%rdx), %rax
    movw %dx, (%rax)
    ```

    !!! tip "判断技巧"
        别管 Src 和 Dest，看哪个对涉及对寄存器取值了。

### 练习 3.3

<figure markdown="span">
  ![练习3.3题图](https://webp-pic.yokumi.cn/2026/01/20260101154154036.png){ loading=lazy width="70%" }
</figure>

???+ details "逐条分析"
    1. **`%ebx` 不能用来存放内存地址！**（此题存了立即数 `0xF` 在内存中的地址）
    2. `%rax` 配 `movq`，`movl` 配 `%eax`
    3. Src 和 Dest 都在引用内存
    4. `%sl` 不存在
    5. 立即数不能作为 Dest
    6. `%rdx` 和 `movl` 不匹配
    7. `%si` 配 `movw`

### 练习 3.4

<figure markdown="span">
  ![练习3.4题图](https://webp-pic.yokumi.cn/2026/01/20260101154159534.png){ loading=lazy width="70%" }
</figure>

### 练习 3.5

<figure markdown="span">
  ![练习3.5题图](https://webp-pic.yokumi.cn/2026/01/20260101154203712.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```c
    void decode1(long *xp, long *yp, long *zp) {
        long x = *xp;
        long y = *yp;
        long z = *zp;
        *yp = x;
        *zp = y;
        *xp = z;
        return;
    }
    ```

### 练习 3.6

<figure markdown="span">
  ![练习3.6题图](https://webp-pic.yokumi.cn/2026/01/20260101154207736.png){ loading=lazy width="70%" }
</figure>

!!! warning "易错点"
    `lea` 是直接取寄存器值，不是取内存地址！

### 练习 3.7

<figure markdown="span">
  ![练习3.7题图](https://webp-pic.yokumi.cn/2026/01/20260101154214788.png){ loading=lazy width="70%" }
</figure>

### 练习 3.9

<figure markdown="span">
  ![练习3.9题图](https://webp-pic.yokumi.cn/2026/01/20260101154221531.png){ loading=lazy width="70%" }
</figure>

### 练习 3.15

<figure markdown="span">
  ![练习3.15题图](https://webp-pic.yokumi.cn/2026/01/20260101154237472.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    **A.** `4003fc + 0x02 = 4003fe`

    **B.** `400431 + 0xf4 = 400425`

    **C.** `ja` 跳转地址为 `400547`；`pop` 指定的地址 $+ 0x02 = \text{ja}$ 的跳转地址，所以 `pop` 地址为 `400545`

    **D.** $4005\text{ed} + 0\text{x}\,\text{ffff ff73} = 400560$

### 练习 3.18

<figure markdown="span">
  ![练习3.18题图](https://webp-pic.yokumi.cn/2026/01/20260101154241726.png){ loading=lazy width="70%" }
</figure>

### 练习 3.20

<figure markdown="span">
  ![练习3.20题图](https://webp-pic.yokumi.cn/2026/01/20260101154244374.png){ loading=lazy width="70%" }
</figure>

### 练习 3.26

<figure markdown="span">
  ![练习3.26题图](https://webp-pic.yokumi.cn/2026/01/20260101154249861.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    **A.** 中间翻译法（Jump-to-middle）：

    ```c
    goto Test;
    Loop:
        body;

    Test:
        t = test;
        if (t) goto Loop;
    end;
    ```

    **B.** 对应 C 代码：

    ```c
    while (x != 0) {
        val = x ^ val;
        x = x >> 1;
    }
    ```

    **C.** 从一个无符号长整数 $x$ 的最高有效位开始，逐位移除最低有效位，直到剩下最后一个有效的非零位。然后检查该值的最低有效位是否为1，并返回结果——即判断 $x$ 的奇偶性。

### 练习 3.27

<figure markdown="span">
  ![练习3.27题图](https://webp-pic.yokumi.cn/2026/01/20260101154253088.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    **Jump-to-middle 版本：**

    ```c
    // Jump-to-middle
    init:
        int result = 1;
        int i = 2;
        goto test;
    loop:
        result *= i;
        i++;

    test:
        if (i <= n)
            goto loop;
    done;
    ```

    **Guarded-do 版本：**

    ```c
    // guarded-do
    init:
        int result = 1;
        int i = 2;
        if (n < 1) goto end;
    loop:
        result *= i;
        i++;
        if (t) goto loop;
    end;
    ```

### 练习 3.31

<figure markdown="span">
  ![练习3.31题图](https://webp-pic.yokumi.cn/2026/01/20260101154304256.png){ loading=lazy width="70%" }
</figure>

### 练习 3.32

<figure markdown="span">
  ![练习3.32题图](https://webp-pic.yokumi.cn/2026/01/20260101154309481.png){ loading=lazy width="70%" }
</figure>

### 练习 3.33

<figure markdown="span">
  ![练习3.33题图](https://webp-pic.yokumi.cn/2026/01/20260101154314078.png){ loading=lazy width="70%" }
</figure>

### 练习 3.36

<figure markdown="span">
  ![练习3.36题图](https://webp-pic.yokumi.cn/2026/01/20260101154325051.png){ loading=lazy width="70%" }
</figure>

### 练习 3.37

<figure markdown="span">
  ![练习3.37题图](https://webp-pic.yokumi.cn/2026/01/20260101154329382.png){ loading=lazy width="70%" }
</figure>

### 练习 3.38

<figure markdown="span">
  ![练习3.38题图](https://webp-pic.yokumi.cn/2026/01/20260101154343675.png){ loading=lazy width="70%" }
</figure>

### 练习 3.44

<figure markdown="span">
  ![练习3.44题图](https://webp-pic.yokumi.cn/2026/01/20260101154354430.png){ loading=lazy width="70%" }
</figure>

???+ details "各结构体内存布局"

    **P1**（共占16字节）：

    | 偏移 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | i | i | i | i | c | X | X | X |

    | 偏移 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | j | j | j | j | d | X | X | X |

    **P2**（共占16字节）：

    | 偏移 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | i | i | i | i | c | d | X | X |

    | 偏移 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | j | j | j | j | j | j | j | j |

    **P3**（共占10字节）：

    | 偏移 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | w[0] | w[0] | w[1] | w[1] | w[2] | w[2] | c[0] | c[1] |

    | 偏移 | 8 | 9 |
    | --- | --- | --- |
    | 内容 | c[2] | X |

    **P4**（共占40字节）：

    | 偏移 | 0 | 1 | ... | 7 |
    | --- | --- | --- | --- | --- |
    | 内容 | w | w | ... | w |

    | 偏移 | 8 | 9 | 10 | ... | 15 |
    | --- | --- | --- | --- | --- | --- |
    | 内容 | w | w | X | X | X |

    | 偏移 | 16 | ... | 23 |
    | --- | --- | --- | --- |
    | 内容 | c | c | ... | c |

    | 偏移 | 24 | ... | 31 |
    | --- | --- | --- | --- |
    | 内容 | c | c | ... | c |

    | 偏移 | 32 | ... | 39 |
    | --- | --- | --- | --- |
    | 内容 | c | c | ... | c |

    **P5**（共占40字节）：

    | 偏移 | 0 | 1 | ... | 7 |
    | --- | --- | --- | --- | --- |
    | 内容 | a | a | ... | a |

    | 偏移 | 8 | 9 | 10 | ... | 15 |
    | --- | --- | --- | --- | --- | --- |
    | 内容 | a | X | a | a | a |

    | 偏移 | 16 | ... | 23 |
    | --- | --- | --- | --- |
    | 内容 | a | a | a | X |

    | 偏移 | 24 | ... | 31 |
    | --- | --- | --- | --- |
    | 内容 | t | t | ... | t |

    | 偏移 | 32 | ... | 39 |
    | --- | --- | --- | --- |
    | 内容 | t | t | ... | t |

### 练习 3.45

<figure markdown="span">
  ![练习3.45题图](https://webp-pic.yokumi.cn/2026/01/20260101154357296.png){ loading=lazy width="70%" }
</figure>

???+ details "结构体内存布局"

    **原始 rec**（共占56字节）：

    | 偏移 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | a | a | a | a | a | a | a | a |

    | 偏移 | 8 | 9 |
    | --- | --- | --- |
    | 内容 | b | b |

    | 偏移 | 16 | ... | 23 |
    | --- | --- | --- | --- |
    | 内容 | c | c | ... | c |

    | 偏移 | 24 | ... | 27 | 28 | ... | 31 |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | d | ... | d | e | e | ... | e |

    | 偏移 | 32 | 33 |
    | --- | --- | --- |
    | 内容 | f | f |

    | 偏移 | 40 | ... | 47 |
    | --- | --- | --- | --- |
    | 内容 | g | g | ... | g |

    | 偏移 | 48 | ... | 51 | 52 | ... | 55 |
    | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | h | h | h | h | X | X |

    **重排 rec'**（共占40字节）：

    | 偏移 | 0 | 1 | ... | 7 |
    | --- | --- | --- | --- | --- |
    | 内容 | a | a | ... | a |

    | 偏移 | 8 | ... | 15 |
    | --- | --- | --- | --- |
    | 内容 | c | c | ... | c |

    | 偏移 | 16 | ... | 23 |
    | --- | --- | --- | --- |
    | 内容 | g | g | ... | g |

    | 偏移 | 24 | ... | 27 | 28 | ... | 31 |
    | --- | --- | --- | --- | --- | --- | --- |
    | 内容 | e | e | ... | e | h | h | ... | h |

    | 偏移 | 32 | 33 | 34 | 35 |
    | --- | --- | --- | --- | --- |
    | 内容 | b | b | d | f |

## 第7章：链接

### 练习 7.1

<figure markdown="span">
  ![练习7.1题图](https://webp-pic.yokumi.cn/2026/01/20260101154405589.png){ loading=lazy width="70%" }
</figure>

### 练习 7.2

<figure markdown="span">
  ![练习7.2题图](https://webp-pic.yokumi.cn/2026/01/20260101154423813.png){ loading=lazy width="70%" }
</figure>

### 练习 7.4

<figure markdown="span">
  ![练习7.4题图](https://webp-pic.yokumi.cn/2026/01/20260101154426603.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    **A.** `4004de + 1 = 4004df`（`callq` 的机器码 `e8` 占一个字节）

    **B.** 引用值为 `0x 00 00 00 05`，注意小端法！

### 练习 7.5

<figure markdown="span">
  ![练习7.5题图](https://webp-pic.yokumi.cn/2026/01/20260101154435313.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    重定位条目包含以下信息：

    * `R_X86_64_PC32` 表示采用 PC 相对寻址法
    * `offset` 表示偏移量为 $0xa = 10$
    * `addend` 可以修正偏移量

    计算引用值：

    $$r_{ptr} = 0x4004e8 - (0x4004d0 + 0xa) + (-4) = 10 = 0x0a$$

    所以引用的值是 `0x 00 00 00 0a`；在汇编代码中被更新为 `e8 0a 00 00 00`。

## 第10章：系统级I/O

### 练习 10.1

<figure markdown="span">
  ![练习10.1题图](https://webp-pic.yokumi.cn/2026/01/20260101154443142.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```
    fd2 = 3
    ```

    !!! info "原因"
        `Close(fd1)` 后，文件描述符被释放，下一次 `Open` 分配到最小的可用描述符编号3。

### 练习 10.2

<figure markdown="span">
  ![练习10.2题图](https://webp-pic.yokumi.cn/2026/01/20260101154445532.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```
    c = f
    ```

    !!! info "原因"
        `fd1` 读取一个字节后，文件位置确实 $+1$ 了，但 `fd1` 和 `fd2` 分两次打开，对应不同的描述符，从而对应不同的打开文件表，所以互不影响。

### 练习 10.3

<figure markdown="span">
  ![练习10.3题图](https://webp-pic.yokumi.cn/2026/01/20260101154449314.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```
    c = o
    ```

    !!! info "原因"
        父子进程共享同一个打开文件表，因此子进程的读取会影响父进程的文件位置。

### 练习 10.5

<figure markdown="span">
  ![练习10.5题图](https://webp-pic.yokumi.cn/2026/01/20260101154451989.png){ loading=lazy width="70%" }
</figure>

???+ details "解答"
    ```
    c = o
    ```

    !!! info "原因"
        `dup2` 将 `fd1` 重定向到 `fd2`，因此通过 `fd1` 读取时实际读取的是 `fd2` 对应文件的内容。
