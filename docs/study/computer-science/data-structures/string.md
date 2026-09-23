# 串

## 串的基本操作

串（String）是由零个或多个字符组成的有限序列。以下是串的常见基本操作：

`Concat(&T, S1, S2)`
: 用 T 返回由 S1 和 S2 连接而成的新串。

`SubString(&Sub, S, pos, len)`
: 用 Sub 返回 S 字符串第 pos 个位置开始的长度为 len 的子串。

`StrCompare(S, T)`
: 两串比较——S > T 返回值 > 0；S = T 返回值 = 0；S < T 返回值 < 0。

`Index(S, T, pos)`
: 在 S 中第 pos 个位置开始后的部分找到与 T 相同的子串，返回第一次出现的位置；未找到则返回 0。

`Replace(&S, T, V)`
: 用 V 替换 S 中与 T 相等的不重叠子串。

`StrInsert(&S, pos, T)`
: 在 S 的第 pos 个位置前插入 T。

`StrDelete(&S, pos, len)`
: 在 S 中的第 pos 个位置开始删除长度为 len 的子串。

```c
Concat(&T, S1, S2); // 用T返回由S1和S2连接而成的新串两串
SubString(&Sub, S, pos, len); // 用Sub返回S字符串第pos个位置开始的长度为len的子串
StrCompare(S, T); // 两串比较S > T，返回值 > 0；S = T，返回值 = 0；S < T，返回值 < 0；
Index(S, T, pos); // 在S中第pos个位置开始后的部分找到与T相同的子串，返回第一次出现的位置，未找到则返回 0
Replace(&S, T, V); // 用V替换S中与T相等的不重叠子串
StrInsert(&S, pos, T); // 在S的第pos个位置前插入T
StrDelete(&S, pos, len); // 在S中的第pos个位置开始删除长度为len的子串
```

## 串的模式匹配算法

### 简单模式匹配算法（Brute Force）

逐个遍历字符串的每个字母，并逐个检查从它开始的长为 len 个的字符是否匹配。

```c
int Index(SString S, SString T, int pos) {
    i = pos;  j = 1;
    while (i <= S[0] && j <= T[0]) {
        if (S[i] == T[j]) {
            ++i;
            ++j;
        }
        // 继续比较后继字符
        else {
            i = i-j+2;
            j = 1;
        }
        // 指针后退重新开始匹配
    }
    if (j > T[0])
        return i-T[0];
    else return 0;
} // Index
```

!!! note "时间复杂度分析"
    - **最好情况**：每次匹配都在第一个字符就成功或失败，平均时间复杂度为 $O(m + n)$
    - **最坏情况**：每次匹配都在最后一个字符才失败，需要回溯重新匹配，时间复杂度为 $O(m \times n)$

### KMP 算法

KMP 算法通过预处理模式串构建 next 数组，在匹配失败时利用已匹配信息避免回溯，将时间复杂度优化到 $O(m + n)$。

#### next 数组

`next[j]=k`：k 是当模式串中第 j 个字符与主串中相应字符"失配"时，在模式串中需重新和主串中该字符进行比较的字符的位置。

$$
\left.{next[j]=}\left\{\begin{array}{ll}
\mathbf{0} & \text{当 $j=1$ 时(代表下一趟比较$\mathrm{i=i+1,j=1}$)}\\
\mathbf{max\{k\mid1<k<j}\text{且前k - 1个元素和后k-1个元素一致}\}&\text{此集合不为空时,下一趟比较 $i = i,j = k$}\\
\mathbf{1}&\text{其它情況(即 $j \ne 1$ 且上述集合为空)}\end{array}\right.\right.
$$

???+ tip "快速填写记法"
    1. 字符串从 1 开始标号
    2. next[1] 默认为 0
    3. next[i] = 前 i-1 位字符串公共前后缀的长度 + 1

    !!! warning "注意"
        前缀：除最后一个字符外，一个字符串的全部头部组合；后缀：除第一个字符外，一个字符串全部的尾部组合。所以 `"aaa"` 的公共前后缀长度为 2。

```c
void GetNext(const char *T, int *next) {
    int j = 1, k = 0; // j 表示模式串位置, k 是前缀长度
    next[1] = 0;      // 初始化 next 数组
    while (j < strlen(T)) {
        if (k == 0 || T[j] == T[k]) {
            j++;
            k++;
            next[j] = k; // 更新 next[j]
        } else {
            k = next[k]; // 回退
        }
    }
}
```

#### nextval 数组

**引入原因**：next 数组中，前后两个相邻的字母如果相同，在匹配过程中遇到需要回退的情况，可以跳过回退到该字母。

$$
\begin{array}{ll}
nextval[i] & = 1\\
nextval[i] & = \left\{\begin{array}{ll}
nextval[i] = nextval[next[i]] & \text{当$Pattern_i = Pattern_{next[i]}$时}\\
nextval[i] = next[i] & \text{当$Pattern_i \ne Pattern_{next[i]}$时}\end{array}\right.
\end{array}
$$

<figure markdown="span">
  ![next 与 nextval 数组示例](https://webp-pic.yokumi.cn/2026/01/20260101154456076.png){ loading=lazy width="70%" }
</figure>

???+ details "KMP 完整代码"
    ```c
    #include <stdio.h>
    #include <string.h>

    void GetNextVal(const char *T, int *nextval) {
        int j = 1, k = 0; // j 表示模式串位置, k 是前缀长度
        nextval[1] = 0;   // 初始化 nextval 数组

        while (j < strlen(T)) {
            if (k == 0 || T[j] == T[k]) {
                j++;
                k++;
                if (T[j] != T[k]) {
                    nextval[j] = k; // 当 T[j] ≠ T[next[j]] 时，直接赋值
                } else {
                    nextval[j] = nextval[k]; // 当 T[j] == T[next[j]] 时，优化跳跃
                }
            } else {
                k = nextval[k]; // 回退
            }
        }
    }

    int Index_KMP(const char *S, const char *T, int pos) {
        int nextval[100]; // 假设模式串长度不超过 100
        GetNextVal(T, nextval); // 生成 nextval 数组

        int i = pos; // 主串的当前指针
        int j = 1;   // 模式串的当前指针

        while (i <= strlen(S) && j <= strlen(T)) {
            if (j == 0 || S[i - 1] == T[j - 1]) {
                i++;
                j++;
            } else {
                j = nextval[j]; // 模式串向右移动
            }
        }

        if (j > strlen(T)) {
            return i - strlen(T); // 匹配成功，返回匹配位置
        } else {
            return 0; // 匹配失败
        }
    }
    ```
