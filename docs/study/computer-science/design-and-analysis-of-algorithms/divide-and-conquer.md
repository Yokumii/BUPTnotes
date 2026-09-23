# 分治法

分治法（Divide and Conquer）是一种重要的算法设计策略，其核心思想是将一个规模较大的问题分解为若干个规模较小、形式相同的子问题，递归地求解子问题，再将子问题的解合并为原问题的解。

!!! abstract "Divide-Conquer-Combine 三步框架"

    Divide（分解）
    : 将规模为 $n$ 的问题分成若干个**规模较小、形式相同**的子问题

    Conquer（解决）
    : 递归地解决这些子问题（或直接解决小规模问题）

    Combine（合并）
    : 将子问题的解合并成原问题的解

适用条件：

- 问题可以分解为若干个形式相同、规模更小的子问题
- 子问题的解可以合并为原问题的解
- 子问题相互独立，不包含公共子问题（否则更适合动态规划）


## 二分搜索

### 基本思想

- **Divide**：取中点 $\text{mid}$
- **Conquer**：只在一侧子数组递归/迭代查找（规模减半）
- **Combine**：无需合并

### 代码实现

???+ details "二分搜索实现"
    ```c linenums="1"
    int binarySearch(int a[], int n, int x) {
        int left = 0, right = n - 1;
        while (left <= right) {
            int mid = (left + right) / 2;
            if (x == a[mid]) return mid;
            else if (x < a[mid]) right = mid - 1;
            else left = mid + 1;
        }
        return -1;
    }
    ```

### 时间复杂度分析

每次将问题规模缩小一半，最多循环 $\lceil \log_2 n \rceil$ 次，循环体内复杂度为 $O(1)$：

- **最好**：一次命中中点 $\Rightarrow O(1)$
- **最坏**：查到空区间 $\Rightarrow O(\log n)$
- **平均**：$O(\log n)$

也可用递归式求解：$T(n)=T(n/2)+O(1) \Rightarrow O(\log n)$。

### 解题示例

输入：$a=[3,5,7,8,9,12,15]$，找 $x=9$。

1. $l=0, r=6 \rightarrow \text{mid}=3, a[3]=8 < 9 \rightarrow l=4$
2. $l=4, r=6 \rightarrow \text{mid}=5, a[5]=12 > 9 \rightarrow r=4$
3. $l=4, r=4 \rightarrow \text{mid}=4, a[4]=9$ 命中 $\rightarrow$ 返回 4

### 拓展：分治求最大最小值

- **Divide**：将数组分成左右两半
- **Conquer**：递归地在左右子数组中分别求最大值和最小值
- **Combine**：全局最小值 $= \min(\text{左最小}, \text{右最小})$，全局最大值 $= \max(\text{左最大}, \text{右最大})$

???+ details "分治求最大最小值实现"
    ```c linenums="1"
    // 返回 (max, min)
    MaxMin(A, l, r) {
        if (l == r) return A[l], A[l];         // 只有一个元素
        else if (r == l + 1) {                  // 两个元素
            if (A[l] > A[r]) return A[l], A[r];
            else return A[r], A[l];
        }
        else {
            int mid = (l + r) / 2;
            maxl, minl = MaxMin(A, l, mid);
            maxr, minr = MaxMin(A, mid + 1, r);
            return max(maxl, maxr), min(minl, minr);
        }
    }
    ```

表面上是二分，实际上底层是元素成对比较。共有 $\lfloor n/2 \rfloor$ 对，内部比较一次，然后与全局的 min/max 分别比较一次，每对共 3 次比较。时间复杂度和直接遍历一样均为 $O(n)$，不过比较次数会少一些。


## 快速幂

问题：求解 $X^N$。

核心思路：

- 若 $N$ 为偶数：$X^N = (X^2)^{N/2}$
- 若 $N$ 为奇数：$X^N = (X^2)^{(N-1)/2} \cdot X$

???+ details "快速幂实现"
    ```c linenums="1"
    int pow(int x, int n) {
        if (n == 0) return 1;                   // 递归边界
        else if (n % 2 == 0) return pow(x * x, n / 2);
        else return pow(x * x, n / 2) * x;
    }
    ```

任何情况下时间复杂度均为 $O(\log n)$。


## 合并排序

### 基本思想

- **Divide**：把数组分成左右两半
- **Conquer**：递归分别排序左右半
- **Combine**：把两个有序序列线性合并成一个有序序列

### 代码实现

???+ details "合并排序（递归写法）"
    ```c linenums="1"
    void mergeSort(Comparable a[], int left, int right) {
        if (left < right) {                     // 至少有 2 个元素
            int mid = (left + right) / 2;
            mergeSort(a, left, mid);
            mergeSort(a, mid + 1, right);
            merge(a, left, mid, right);
        }
    }

    void merge(int arr[], int left, int mid, int right) {
        int i = left, j = mid + 1, k = 0;
        int *tmp = new int[right - left + 1];

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) tmp[k++] = arr[i++];
            else tmp[k++] = arr[j++];
        }
        while (i <= mid) tmp[k++] = arr[i++];
        while (j <= right) tmp[k++] = arr[j++];

        for (int t = 0; t < k; t++) arr[left + t] = tmp[t];
        delete[] tmp;
    }
    ```

???+ details "合并排序（非递归写法）"
    ```c linenums="1"
    void mergeSort2(Comparable a[], int n) {
        if (n < 2) return;
        for (int i = 1; i < n; i *= 2) {        // i 表示每组的一半长度
            int left = 0;
            int mid = left + i - 1;               // left~mid 为左半分组，长度为 i
            int right = mid + i;                   // mid+1~right 为右半分组，长度为 i

            while (right < n) {
                merge(a, left, mid, right);
                left = right + 1;
                mid = left + i - 1;
                right = mid + i;
            }

            if (left < n && mid < n) {            // 多余部分
                merge(a, left, mid, n - 1);
            }
        }
    }
    ```

### 时间复杂度分析

每次分成两半 + 合并需要线性时间：

$$T(n)=2T(n/2)+O(n)$$

解得 $T(n)=O(n\log n)$。最坏和平均时间复杂度均为 $O(n\log n)$。

合并排序是**稳定**的：合并时遇到两个元素相等，规定先取左边子序列的元素，保持相等元素在原序列中的相对顺序不变。

### 解题示例

以 $[7,2,9,4,3,8,6,1]$ 为例：

**1. 递归思路**：

<figure markdown="span">
  ![合并排序递归过程](https://webp-pic.yokumi.cn/2025/12/20251228094302286.png){ loading=lazy width="70%" }
</figure>

**2. 非递归思路**：

<figure markdown="span">
  ![合并排序非递归过程](https://webp-pic.yokumi.cn/2025/12/20251228095507164.png){ loading=lazy width="70%" }
</figure>


## 快速排序

### 基本思想

1. **Divide（分解）**：选择一个**基准元素（pivot）**，通过一次划分操作将序列分成两部分：
    - 左子序列：所有元素 $\leq$ pivot
    - 右子序列：所有元素 $>$ pivot
    - 此时 pivot 已处在最终正确位置
2. **Conquer（解决）**：递归地对左右两个子序列分别进行快速排序
3. **Combine（合并）**：不需要额外合并操作——就地排序，递归完成后整体已有序

### 代码实现

???+ details "快速排序实现"
    ```c linenums="1"
    int partition(int A[], int low, int high) {
        int pivot = A[low];
        int i = low, j = high;
        while (i < j) {
            while (i < j && A[j] > pivot) j--;   // 右边第一个小于等于基准
            A[i] = A[j];
            while (i < j && A[i] <= pivot) i++;  // 左边第一个大于基准
            A[j] = A[i];
        }
        A[i] = pivot;
        return i;
    }

    void quickSort(int A[], int low, int high) {
        if (low > high) return;
        int p = partition(A, low, high);
        quickSort(A, low, p - 1);
        quickSort(A, p + 1, high);
    }
    ```

### 时间复杂度分析

**最好情况**：每次 pivot 把数组**几乎均分**，划分复杂度为 $O(n)$：

$$T(n) = 2T(n/2) + O(n) \Rightarrow \boxed{T(n) = O(n\log n)}$$

对应空间复杂度为 $O(\log n)$（递归栈深度）。

**最坏情况**：每次 pivot 都是**最小或最大元素**，子问题规模为 $n-1$ 和 0：

$$T(n) = T(n-1) + O(n) \Rightarrow \boxed{T(n) = O(n^2)}$$

对应空间复杂度为 $O(n)$。

**平均时间复杂度**：$\boxed{O(n\log n)}$。

### 退化分析与解决

退化出现的典型情况：

- 数组**已经有序**（升序或降序）
- 且**总是选择第一个或最后一个元素作为 pivot**

解决的核心思路是改进 pivot 的选择，使划分更加均衡。

!!! tip "改进 pivot 选择"

    **1. 随机基准**：每次划分前随机选择一个元素作为 pivot。

    ??? details "随机基准划分"
        ```c linenums="1"
        int randomPartition(int A[], int low, int high) {
            int p = random(low, high);
            swap(A[p], A[low]);                  // 随机基准交换到最低位
            return partition(A, low, high);
        }
        ```

    **2. 三数取中**：从待划分段的开头、中间、结尾三个数中取中间值作为基准。

    ??? details "三数取中划分"
        ```c linenums="1"
        int mid3Partition(int A[], int low, int high) {
            int mid = (low + high) / 2;
            int a = A[low], b = A[mid], c = A[high];
            if ((b <= a && a <= c) || (c <= a && a <= b)) {
                return partition(A, low, high);
            } else if ((a <= b && b <= c) || (c <= b && b <= a)) {
                swap(A[mid], A[low]);
                return partition(A, low, high);
            } else {
                swap(A[high], A[low]);
                return partition(A, low, high);
            }
        }
        ```

### 改成稳定排序

快排之所以不稳定，根因是 **partition 过程中会把相等元素跨越式交换**，打乱相对次序。

可以采用**三路划分（3-way partition）** + 额外数组的方式：

选 pivot 后，从左到右扫描顺序把元素分到三个序列：

- $L$：所有 $<$ pivot
- $E$：所有 $=$ pivot
- $G$：所有 $>$ pivot

由于从左到右扫描并在序列尾添加，相对顺序不变。

???+ details "稳定快速排序实现"
    ```c linenums="1"
    void stableQuickSort(int A[], int low, int high) {
        if (low > high) return;

        int pivot = A[low];
        int buf[high - low + 1];

        // 统计各段长度
        int cntL = 0, cntE = 0, cntG = 0;
        for (int i = low; i <= high; i++) {
            if (A[i] < pivot) cntL++;
            else if (A[i] == pivot) cntE++;
            else cntG++;
        }
        int pL = 0, pE = cntL, pG = cntL + cntE;

        // 写入
        for (int i = low; i <= high; i++) {
            if (A[i] < pivot) buf[pL++] = A[i];
            else if (A[i] == pivot) buf[pE++] = A[i];
            else buf[pG++] = A[i];
        }

        // 拷贝回原数组
        for (int i = 0; i < high - low + 1; i++) A[low + i] = buf[i];

        stableQuickSort(A, low, low + cntL - 1);
        stableQuickSort(A, low + cntL + cntE, high);
    }
    ```


## 线性时间选择

### 问题描述

选择问题：给定线性序集中 $n$ 个元素和一个整数 $k\ (1 \le k \le n)$，找出这 $n$ 个元素中第 $k$ 小的元素。

朴素方法：先排序再取第 $k$ 个，时间复杂度 $O(n\log n)$。

特殊情况：

- $k=1$：最小值
- $k=n$：最大值
- $k=\lceil n/2 \rceil$：中位数

!!! info "核心思路"
    如果能在线性时间内找到一个划分基准，使得按该基准划分出的两个子数组长度都至少为原数组长度的 $\varepsilon\ (0 < \varepsilon < 1)$ 倍，则可以在最坏情况下用 $O(n)$ 时间完成选择任务。

### 基本步骤

1. **Divide**：把 $n$ 个元素分成若干小组
2. **Conquer**：递归地找一个"好 pivot"（中位数的中位数）
3. **Combine**：用该 pivot 划分数组，只在一边递归查找第 $k$ 小

!!! abstract "中位数的中位数算法步骤"

    **Step 1：分组**
    : 将 $n$ 个元素**按顺序**分成 $\lceil n/5 \rceil$ 组，每组 5 个元素（最后一组不足 5 个也允许）

    **Step 2：组内排序并取中位数**
    : 对每一组用任意简单排序，取每组的**中位数**，得到一个新数组 $M$（长度约 $n/5$）

    **Step 3：递归求中位数的中位数**
    : 在数组 $M$ 中递归求其中位数，该值作为全局 **pivot**

    **Step 4：按 pivot 划分原数组**
    : 用 pivot 对原数组做一次 partition，得到三部分：
    - $L$：小于 pivot
    - $E$：等于 pivot
    - $G$：大于 pivot

    **Step 5：只在一边递归**
    : 若 $k \le |L|$：在 $L$ 中递归找第 $k$ 小
    若 $|L| < k \le |L|+|E|$：pivot 即答案
    否则：在 $G$ 中递归找第 $k - |L| - |E|$ 小

### 代码实现

???+ details "线性时间选择实现"
    ```c linenums="1"
    int selectK(int A[], int low, int high, int k) {
        if (high - low < 75) {                   // 小规模，直接排序解决
            sort(A + low, A + high + 1);
            return A[low + k - 1];
        }

        int idx = low;
        for (int i = low; i + 4 <= high; i += 5) { // 每 5 个一组
            insertionSort(A, i, i + 4);
            swap(A[idx++], A[i + 2]);            // 第 3 小即中位数
        }
        // 此时 A[low..idx-1] 放的是每组的中位数
        // 递归找中位数的中位数
        int m = idx - low;
        int pivot = selectK(A, low, low + m - 1, (m + 1) / 2);

        int p = partition(A, low, high, pivot);  // p 为中位数的中位数位置
        int leftSize = p - low;

        if (k <= leftSize) {
            return selectK(A, low, p - 1, k);
        } else if (k == leftSize + 1) {
            return pivot;
        } else {
            return selectK(A, p + 1, high, k - leftSize - 1);
        }
    }
    ```

### 复杂度分析

采用 5 个一组可以证明：

- pivot **至少大于** $\dfrac{3(n-5)}{10}$ 个元素
- pivot **至少小于** $\dfrac{3(n-5)}{10}$ 个元素

因此最大子问题规模 $\le \dfrac{7n}{10}$：

$$T(n) \le T\!\left(\frac{n}{5}\right) + T\!\left(\frac{7n}{10}\right) + O(n)$$

因为 $\dfrac{n}{5} + \dfrac{7n}{10} = \dfrac{9n}{10} < n$，所以时间复杂度 $\boxed{T(n) = O(n)}$。

