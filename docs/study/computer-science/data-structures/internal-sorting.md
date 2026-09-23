# 内部排序

内部排序是指待排序的数据全部存放在内存中的排序算法。按策略可分为**基于比较的排序**和**基于分配的排序**两大类。

!!! abstract "排序分类概览"
    - **插入排序**：直接插入排序、希尔排序
    - **交换排序**：冒泡排序、快速排序
    - **选择排序**：简单选择排序、堆排序
    - **归并排序**：2-路归并排序
    - **分配排序**：桶排序、计数排序、基数排序

## 基本数据结构

以下所有排序算法共用此顺序表结构，`r[0]` 用作哨兵或辅助空间：

???+ details "SqList 定义与输入输出"
    ```cpp linenums="1"
    #define MAXSIZE 20

    typedef int KeyType;

    typedef struct {
        KeyType r[MAXSIZE+1];  // r[0] 闲置或作哨兵
        int length;
    } SqList;

    void CinList(SqList &L) {
        cin >> L.length;
        for (int i = 1; i <= L.length; i++) {
            cin >> L.r[i];
        }
    }

    void CoutList(SqList L) {
        for (int i = 1; i <= L.length; i++) {
            cout << L.r[i] << " ";
        }
    }
    ```

## 基于比较的排序

### 直接插入排序

将待排序元素逐个插入到已排好序的子序列中，类似于整理扑克牌。

!!! info "关键性质"
    - **稳定性**：稳定
    - **最好时间**：$O(n)$（仅需比较 $n-1$ 次，移动 0 次）
    - **最坏时间**：$O(n^2)$（比较 $\frac{(n+2)(n-1)}{2}$ 次，移动 $\frac{(n+4)(n-1)}{2}$ 次）
    - **平均时间**：$O(n^2)$

???+ tip "特点与优化"
    - 排序过程中前一部分逐渐有序，但可能出现最后一趟之前数据均未在最终位置（如最后一个数据为最小值时）
    - 优化：**折半插入排序**——在查找插入位置时采用二分查找，减少比较次数，但移动次数不变

???+ details "直接插入排序实现"
    ```cpp linenums="1"
    void InsertSort(SqList &L) {
        for (int i = 2; i <= L.length; i++) {  // 循环 n-1 次
            if (L.r[i] < L.r[i - 1]) {
                L.r[0] = L.r[i];  // 用作监视哨
                L.r[i] = L.r[i - 1];  // 算一次移动
                int j;
                for (j = i - 2; L.r[0] < L.r[j]; j--) {
                    L.r[j + 1] = L.r[j];  // 后移一位
                }
                L.r[j + 1] = L.r[0];  // 算一次移动
            }
        }
    }
    ```

### 希尔排序

按间隔步长 $d$ 分组进行直接插入排序，逐步缩小步长直至 $d=1$。

!!! info "关键性质"
    - **稳定性**：不稳定
    - **最好/最坏时间**：与直接插入排序相同
    - **平均时间**：$O(n^{1.3})$

???+ details "希尔排序实现"
    ```cpp linenums="1"
    void ShellSort(SqList &L) {
        // 间隔步长 d 选点作为一组子表进行插排
        // 不断缩小步长，代码略
    }
    ```

### 冒泡排序

相邻元素逐对比较，将最大元素逐步"下沉"至尾部。

!!! info "关键性质"
    - **稳定性**：稳定
    - **最好时间**：$O(n)$（仅需比较 $n-1$ 次，无需移动）
    - **最坏时间**：$O(n^2)$（比较 $\frac{n(n-1)}{2}$ 次，移动 $\frac{3n(n-1)}{2}$ 次）
    - **平均时间**：$O(n^2)$

???+ tip "特点"
    每一趟排序后，最大的元素逐渐下沉至尾部，即放置在最终位置上。通过 `isSorted` 标志优化，若某趟无交换则提前终止。

???+ details "冒泡排序实现"
    ```cpp linenums="1"
    void BubbleSort(SqList &L) {
        bool isSorted = true;
        for (int i = 0; i < L.length - 1 && isSorted; i++) {  // 最多排 n-1 趟
            isSorted = false;
            for (int j = 1; j < L.length - i; j++) {
                if (L.r[j] > L.r[j + 1]) {  // 下沉
                    L.r[0] = L.r[j];
                    L.r[j] = L.r[j + 1];
                    L.r[j + 1] = L.r[0];  // 交换，记为 3 次移动
                    isSorted = true;  // 标志进行了交换
                }
            }
        }
    }
    ```

### 快速排序

选取支点（pivot），将序列划分为小于和大于支点的两部分，递归处理。

!!! info "关键性质"
    - **稳定性**：不稳定
    - **最好时间**：$O(n\log n)$（划分为等长子序列，排序趟数 $\leq \lceil\log_2 n\rceil$）
    - **最坏时间**：$O(n^2)$（初始完全逆序，每次划分只能移动支点到最后）
    - **平均时间**：$O(n\log n)$，是同数量级中**平均性能最好**的比较排序
    - **空间**：理想 $O(\log n)$，最坏 $O(n)$（递归层数 = 二叉树深度）

???+ tip "特点"
    每一趟排完后，支点的位置就在最终位置。划分操作时间复杂度 $O(n)$，移动次数固定为 4 次。

???+ details "快速排序实现"
    ```cpp linenums="1"
    // 快速排序的划分过程
    int Partition(SqList &L, int low, int high) {
        KeyType pivotkey = L.r[low];
        L.r[0] = L.r[low];  // 选择 low 作为支点，移到辅助空间
        while (low < high) {
            while (low < high && L.r[high] >= pivotkey) {  // 从后往前找小于支点的元素
                high--;
            }
            L.r[low] = L.r[high];
            while (low < high && L.r[low] <= pivotkey) {  // 从前往后找大于支点的元素
                low++;
            }
            L.r[high] = L.r[low];
        }
        L.r[low] = L.r[0];  // 将支点移回去
        return low;  // 返回支点位置
    }

    // 快速排序递归的辅助函数
    void Qsort(SqList &L, int low, int high) {
        if (low < high) {
            int pivotloc = Partition(L, low, high);
            Qsort(L, low, pivotloc - 1);
            Qsort(L, pivotloc + 1, high);
        }
    }

    // 快速排序
    void QuickSort(SqList &L) {
        Qsort(L, 1, L.length);
    }
    ```

### 选择排序

每趟从剩余元素中选出最小的，放到已排序序列末尾。

!!! info "关键性质"
    - **稳定性**：不稳定（选择的是下标最大的最小值）
    - **时间复杂度**：$O(n^2)$
    - **比较次数**：$\frac{n(n-1)}{2}$（不受初始序列影响）
    - **移动次数**：$3(n-1)$ 次（每趟最多交换 1 次）

???+ tip "特点"
    排序过程中前一部分数据逐渐有序，且放置在最终位置上。当 $n$ 较小时，简单选择排序通常记录移动次数少于直接插入排序。

???+ details "选择排序实现"
    ```cpp linenums="1"
    void SelectSort(SqList &L) {
        for (int i = 1; i <= L.length - 1; i++) {  // n-1 趟
            int k = i;  // 记录待替换的元素位置
            for (int j = i + 1; j <= L.length; j++) {
                if (L.r[j] < L.r[k]) {
                    k = j;  // 找到最小元素的下标
                }
            }
            if (i != k) {
                L.r[0] = L.r[i];
                L.r[i] = L.r[k];
                L.r[k] = L.r[0];  // 交换元素，记为 3 次移动
            }
        }
    }
    ```

### 堆排序

利用完全二叉堆的性质进行排序。先建大顶堆，再反复取出堆顶元素与堆底交换后调整堆。

!!! info "关键性质"
    - **稳定性**：不稳定
    - **时间复杂度**：$O(n\log n)$
    - **空间**：$O(1)$

???+ tip "堆的基本概念"
    - **小顶堆**：每个节点的值都 $\leq$ 左右孩子的值
    - **大顶堆**：每个节点的值都 $\geq$ 左右孩子的值
    - 堆的构建：从最后一个非叶子节点（序号 $n/2$）开始，从下往上逐步调整
    - 筛选（调整堆）：将堆底元素移到堆顶，与左右孩子中较大的交换，直至满足堆性质

???+ details "堆排序实现"
    ```cpp linenums="1"
    // 筛选（调整堆）
    void HeapAdjust(SqList &L, int root, int end) {
        // root 是待调整子树根节点序号，end 是子树最后一个节点
        L.r[0] = L.r[root];  // 存储当前堆顶元素
        for (int j = 2 * root; j <= end && j + 1 <= end; j *= 2) {
            if (L.r[j] < L.r[j + 1]) {
                j++;  // j 表示左右孩子中较大的节点
            }
            if (L.r[0] >= L.r[j]) {
                break;  // 父节点大于左右孩子，满足大顶堆性质
            }
            L.r[root] = L.r[j];  // 孩子节点换到根节点
            root = j;  // 根节点指向交换下去的节点
        }
        L.r[root] = L.r[0];
    }

    // 堆排序
    void HeapSort(SqList &L) {
        // 建立大顶堆
        for (int i = L.length / 2; i > 0; i--) {
            HeapAdjust(L, i, L.length);
        }
        // 每次取出最大元素（堆顶），与堆底交换，重新调整堆
        for (int i = L.length; i > 1; i--) {
            L.r[0] = L.r[1];
            L.r[1] = L.r[i];
            L.r[i] = L.r[0];  // 交换堆顶和堆底
            HeapAdjust(L, 1, i - 1);  // 调整剩余部分 1 ~ i-1
        }
    }
    ```

???+ warning "堆排序的细节"
    - 树高 $k = \lfloor\log_2 n\rfloor + 1$
    - 每次筛选最多比较 $2(k-1)$ 次，最多移动 $3k$ 次
    - 排序过程中序列后面部分逐渐有序，且在最终位置
    - 对记录数较大的文件很有效

### 2-路归并排序

将含有 1 个元素的子表（天然有序）逐对合并，逐步生成更长的有序表，直至表长 = $n$。

!!! info "关键性质"
    - **稳定性**：稳定（合并时先判断 `<` 条件保证稳定性）
    - **时间复杂度**：$O(n\log n)$（归并 $\lceil\log_2 n\rceil$ 趟，每趟移动 $n$ 次）
    - **空间复杂度**：$O(n)$

???+ details "2-路归并排序实现"
    ```cpp linenums="1"
    // 合并两张子表
    // left 表示第一张表的开头，mid 表示第一张表的结尾
    // mid+1 表示第二张表的开头，right 表示第二张表的结尾
    void Merge(int Source[], int* Dest, int left, int mid, int right) {
        int i = left, j = mid + 1, k = left;
        while (i <= mid && j <= right) {
            if (Source[i] < Source[j]) {  // 先判断 < 条件，保证稳定性
                Dest[k] = Source[i];
                i++;
            } else {
                Dest[k] = Source[j];
                j++;
            }
            k++;
        }
        // 将剩余元素放入 Dest
        while (i <= mid) {
            Dest[k] = Source[i];
            k++, i++;
        }
        while (j <= right) {
            Dest[k] = Source[j];
            k++, j++;
        }
    }

    // 归并排序的递归辅助函数
    void MSort(int Source[], int* Dest, int start, int end) {
        if (start == end) {  // 数组长度为 1，已有序
            Dest[start] = Source[start];
        } else {
            int mid = (start + end) / 2;
            int Temp[MAXSIZE];  // 辅助数组
            MSort(Source, Temp, start, mid);
            MSort(Source, Temp, mid + 1, end);
            Merge(Temp, Dest, start, mid, end);
        }
    }

    // 归并排序
    void MergeSort(SqList &L) {
        MSort(L.r, L.r, 1, L.length);
    }
    ```

## 基于分配的排序

### 桶排序

将元素按值域范围分配到若干桶中，每个桶内部排序后再依次收集。

!!! info "关键性质"
    - **稳定性**：稳定
    - **空间复杂度**：$O(n + k)$，其中 $n$ 为元素数量，$k$ 为桶的数量
    - **平均时间**：$O(n + k\log k)$
    - **最坏时间**：$O(n^2)$（所有元素落在同一个桶中）
    - **适用场景**：待排序数据值域较大但分布比较均匀

???+ details "桶排序实现"
    ```cpp linenums="1"
    void BucketSort(SqList &L) {
        // 找到数组中的最大值和最小值
        KeyType maxVal = L.r[1], minVal = L.r[1];
        for (int i = 2; i <= L.length; i++) {
            if (L.r[i] > maxVal) maxVal = L.r[i];
            if (L.r[i] < minVal) minVal = L.r[i];
        }
        // 计算桶的数量和范围
        int bucketCount = L.length;
        vector<vector<KeyType>> buckets(bucketCount);
        // 将元素分配到对应的桶中
        double range = (double)(maxVal - minVal + 1) / bucketCount;
        for (int i = 1; i <= L.length; i++) {
            int index = (L.r[i] - minVal) / range;
            if (index >= bucketCount) index = bucketCount - 1;
            buckets[index].push_back(L.r[i]);
        }
        // 对每个桶内部进行排序
        for (int i = 0; i < bucketCount; i++) {
            sort(buckets[i].begin(), buckets[i].end());
        }
        // 将排序后的数据从桶中取出，放回原数组
        int idx = 1;
        for (int i = 0; i < bucketCount; i++) {
            for (KeyType val : buckets[i]) {
                L.r[idx++] = val;
            }
        }
    }
    ```

### 计数排序

统计每个值出现的次数，直接按计数输出有序序列。

!!! info "关键性质"
    - **稳定性**：稳定（完整实现需使用前缀和反向填充，上述简化版未体现）
    - **时间复杂度**：$O(n + k)$，其中 $k$ 为值域范围
    - **空间复杂度**：$O(n + k)$
    - **适用场景**：$k$ 不大且序列比较集中时非常高效；$k > n$ 时效率下降

???+ details "计数排序实现"
    ```cpp linenums="1"
    void CountSort(SqList &L) {
        int maxVal = L.r[1], minVal = L.r[L.length];
        // 查找最大值和最小值
        for (int i = 2; i <= L.length; i++) {
            if (L.r[i] > maxVal) maxVal = L.r[i];
            if (L.r[i] < minVal) minVal = L.r[i];
        }
        // 计数数组
        int* C = new int[maxVal - minVal + 1]();
        // 计数
        for (int i = 1; i <= L.length; i++) {
            C[L.r[i] - minVal]++;
        }
        // 按计数输出
        int k = 1;
        for (int i = minVal; i <= maxVal; i++) {
            for (int j = 0; j < C[i - minVal]; j++) {
                L.r[k] = i;
                k++;
            }
        }
        delete[] C;
    }
    ```

!!! tip "计数排序的优势"
    排序速度快于任何比较排序算法，但当值域范围 $k$ 过大时，空间和时间效率都会下降。

### 基数排序

按关键字的各位（从低位到高位或反之）逐趟进行分配和收集。

!!! info "关键性质"
    - **稳定性**：稳定
    - **时间复杂度**：$O(d(n + r))$，其中 $d$ 为关键字位数，$r$ 为基数
    - **空间复杂度**：$O(n + r)$（$n$ 个记录游标 + 队头/队尾指针数组）

???+ tip "基数排序细节"
    - 每一趟：分配复杂度 $O(n)$，收集复杂度 $O(r)$
    - 共需 $d$ 趟
    - 当 $r$ 和 $d$ 为常数时，时间复杂度可视为 $O(n)$

???+ details "基数排序实现"
    ```cpp linenums="1"
    void RadixSort(SqList &L) {
        // 基数排序的具体实现按 LSD/MSD 方式逐位分配收集
        // 此处仅列出框架，详细实现略
    }
    ```

## 排序算法总结

### 稳定性

| 稳定排序 | 不稳定排序 |
| --- | --- |
| 直接插入排序 | 希尔排序 |
| 冒泡排序 | 快速排序 |
| 2-路归并排序 | 选择排序 |
| 桶排序 | 堆排序 |
| 计数排序 | |
| 基数排序 | |

### 复杂度与适用场景对比

| 排序算法 | 稳定性 | 最好时间 | 最坏时间 | 平均时间 | 空间 | 适用场景 |
| --- | --- | --- | --- | --- | --- | --- |
| 直接插入排序 | :white_check_mark: | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | $n$ 较小、基本有序 |
| 希尔排序 | :x: | $O(n)$ | $O(n^2)$ | $O(n^{1.3})$ | $O(1)$ | $n$ 中等 |
| 冒泡排序 | :white_check_mark: | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | $n$ 较小、教学演示 |
| 快速排序 | :x: | $O(n\log n)$ | $O(n^2)$ | $O(n\log n)$ | $O(\log n)$ | 关键字随机分布、$n$ 较大 |
| 选择排序 | :x: | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | $n$ 较小、移动次数少 |
| 堆排序 | :x: | $O(n\log n)$ | $O(n\log n)$ | $O(n\log n)$ | $O(1)$ | $n$ 较大、空间受限 |
| 2-路归并排序 | :white_check_mark: | $O(n\log n)$ | $O(n\log n)$ | $O(n\log n)$ | $O(n)$ | $n$ 较大、要求稳定 |
| 桶排序 | :white_check_mark: | $O(n+k\log k)$ | $O(n^2)$ | $O(n+k\log k)$ | $O(n+k)$ | 值域大但分布均匀 |
| 计数排序 | :white_check_mark: | $O(n+k)$ | $O(n+k)$ | $O(n+k)$ | $O(n+k)$ | $k$ 较小、序列集中 |
| 基数排序 | :white_check_mark: | $O(d(n+r))$ | $O(d(n+r))$ | $O(d(n+r))$ | $O(n+r)$ | 关键字可按位分解 |

???+ abstract "选择排序算法的原则"
    - 关键字随机分布时，快速排序平均时间最短，堆排序次之但辅助空间少
    - $n$ 较小时，可采用直接插入或简单选择排序；前者稳定，后者移动次数通常更少
    - $n$ 较大时，应采用 $O(n\log n)$ 的排序（主要为快速排序和堆排序）或基数排序；但基数排序对关键字结构有一定要求
    - 要求稳定性且 $n$ 较大时，2-路归并排序是首选

???+ warning "选出前 k 个最小元素"
    给定 $n$ 个值不同的元素，不经排序选出前 $k$ 个最小元素的方法：

    | 方法 | 比较次数 | 说明 |
    | --- | --- | --- |
    | 选择排序 / 冒泡排序 | $\approx kn$ | 运行 $k$ 趟即可 |
    | 快速排序 | $\approx n + k\log n$ | 每次仅对第一个子序列划分 |
    | 堆排序 | $\approx 4n + (k-1)\log n$ | 先建小根堆，$k-1$ 次堆调整 |

    若要求这 $k$ 个元素有序，需额外对选出的 $k$ 个元素排序。

