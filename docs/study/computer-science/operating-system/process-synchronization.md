# 进程同步

## 临界区问题

考虑 $n$ 个进程竞争共享数据的场景。每个进程中访问共享资源的代码段称为**临界区（critical section）**。问题的关键在于：如何确保当某个进程在其临界区内执行时，其他进程不能同时进入各自的临界区。

### 临界区结构

每个进程的通用结构如下：

```c
do {
    // entry section    —— 进入区：请求进入临界区
    // critical section —— 临界区：访问共享资源
    // exit section     —— 退出区：释放临界区
    // remainder section—— 剩余区：其他代码
} while (true);
```

### 三个必要条件

互斥（Mutual Exclusion）
: 如果进程 $P_i$ 在其临界区内执行，则其他任何进程都不能进入各自的临界区。

前进（Progress）
: 如果没有进程处于临界区内，且有若干进程需要进入临界区，则只有那些不在剩余区内执行的进程可参与选择，且这种选择不能无限期推迟。

有限等待（Bounded Waiting）
: 从一个进程做出进入临界区的请求，到该请求被允许为止，其他进程进入其临界区的次数有上限——即不会发生饥饿。

### 软件解决方案

#### Peterson 算法（两进程）

Peterson 算法适用于**两个进程**交替执行临界区的场景。核心思想是结合 `flag[]` 数组（表示进入意愿）和 `turn` 变量（表示轮到谁）来解决互斥与前进问题。

共享变量声明：

```c
bool flag[2];  // flag[i] = true 表示进程 Pi 想进入临界区
int turn;      // 表示轮到哪个进程进入临界区
```

进程 $P_i$ 的完整伪代码（$j = 1 - i$）：

```c
do {
    flag[i] = true;          // 声明自己想进入
    turn = j;                // 让给对方优先
    while (flag[j] && turn == j)
        ;                    // 忙等待：对方想进且轮到对方
    // --- critical section ---
    flag[i] = false;         // 退出临界区，声明不再想进
    // --- remainder section ---
} while (true);
```

???+ info "Peterson 算法正确性分析"
    - **互斥**：若两个进程同时想进入，`turn` 值决定了只有一个进程能通过 `while` 循环
    - **前进**：若对方不想进入（`flag[j] == false`），则 `while` 条件不满足，当前进程立即进入
    - **有限等待**：对方最多进入一次临界区后就会将 `turn` 让出

#### Bakery 算法（n 个进程）

Bakery 算法将 Peterson 算法推广到 $n$ 个进程，思想类似面包店取号排队：每个进程取一个号，号最小的先进入临界区。

共享变量声明：

```c
bool choosing[n];   // choosing[i] = true 表示进程 Pi 正在取号
int number[n];      // number[i] 表示进程 Pi 的号码，0 表示未取号
```

进程 $P_i$ 的完整伪代码：

```c
do {
    // --- 取号 ---
    choosing[i] = true;
    number[i] = max(number[0], number[1], ..., number[n-1]) + 1;
    choosing[i] = false;

    // --- 等待 ---
    for (int j = 0; j < n; j++) {
        while (choosing[j])
            ;    // 等待 Pj 取完号
        while (number[j] != 0 && (number[j], j) < (number[i], i))
            ;    // 存在号比自己小的进程，等待
    }

    // --- critical section ---
    number[i] = 0;    // 退出，释放号码
    // --- remainder section ---
} while (true);
```

其中 `(number[j], j) < (number[i], i)` 的比较规则为：先比较号码，号码小者优先；号码相同则比较进程编号，编号小者优先。

!!! warning "忙等待的缺点"
    上述两种软件方案均采用**忙等待（busy waiting）**：等待的进程持续占用 CPU 执行循环判断，浪费处理器时间。这在单处理器系统中尤其严重，因为忙等待的进程占用了本可分配给临界区进程的 CPU 时间。

### 硬件解决方案

#### TestAndSet 指令

`TestAndSet` 是一条原子指令：读取 `lock` 的旧值，并将其设为 `true`，然后返回旧值。

```c
bool TestAndSet(bool *lock) {
    bool old = *lock;
    *lock = true;
    return old;
}
```

基于 `TestAndSet` 的互斥锁实现：

```c
// 共享变量
bool lock = false;

// 进程 Pi
do {
    while (TestAndSet(&lock))
        ;    // lock 为 true 时忙等待
    // --- critical section ---
    lock = false;
    // --- remainder section ---
} while (true);
```

???+ tip "满足有限等待的 TestAndSet 方案"
    上述简单实现不满足有限等待。改进方案需引入 `waiting[]` 数组：

    ```c
    // 共享变量
    bool lock = false;
    bool waiting[n];

    // 进程 Pi
    do {
        waiting[i] = true;
        bool key = true;
        while (waiting[i] && key)
            key = TestAndSet(&lock);
        waiting[i] = false;
        // --- critical section ---

        // 退出时选择下一个等待进程
        int j = (i + 1) % n;
        while (j != i && !waiting[j])
            j = (j + 1) % n;

        if (j == i)
            lock = false;       // 没有其他等待者
        else
            waiting[j] = false; // 唤醒 Pj
        // --- remainder section ---
    } while (true);
    ```

#### Swap 指令

`Swap` 是一条原子指令：交换两个布尔变量的值。

```c
void Swap(bool *a, bool *b) {
    bool temp = *a;
    *a = *b;
    *b = temp;
}
```

基于 `Swap` 的互斥锁实现：

```c
// 共享变量
bool lock = false;

// 进程 Pi
do {
    bool key = true;
    while (key == true)
        Swap(&key, &lock);    // lock 为 true 时 key 换回 true，继续等待
    // --- critical section ---
    lock = false;
    // --- remainder section ---
} while (true);
```

#### 互斥锁（Mutex Lock）

互斥锁是对硬件原子操作的封装，提供 `acquire()` 和 `release()` 两个操作：

```c
// 互斥锁结构
typedef struct {
    bool available;  // true 表示锁可用
} mutex_lock;

acquire(mutex_lock *lock) {
    while (!TestAndSet(&lock->available))
        ;    // 忙等待
}

release(mutex_lock *lock) {
    lock->available = false;
}

// 使用方式
do {
    acquire(&mutex);
    // --- critical section ---
    release(&mutex);
    // --- remainder section ---
} while (true);
```

## 信号量

信号量 $S$ 是一个整型变量，只能通过两个**原子操作** `wait()` 和 `signal()` 访问：

```c
wait(S) {       // aka. P 操作
    while (S <= 0)
        ;       // 忙等待
    S--;
}

signal(S) {     // aka. V 操作
    S++;
}
```

### 信号量的类型

二值信号量（Binary Semaphore）
: $S$ 的值只能为 0 或 1，功能类似于互斥锁。

    ```c
    // 二值信号量使用示例
    semaphore mutex = 1;    // 初始值为 1

    // 进程 Pi
    wait(mutex);
    // --- critical section ---
    signal(mutex);
    ```

计数信号量（Counting Semaphore）
: $S$ 的值可以大于 1，用于控制对具有多个实例的资源访问。$S$ 的初始值等于可用资源的数量。

### 无忙等待的实现

忙等待浪费 CPU 资源。改进方案在信号量结构中增加**等待队列**，使等待进程进入阻塞状态而非忙等：

```c
typedef struct {
    int value;             // 信号量值
    struct process *list;  // 等待队列
} semaphore;
```

改进后的 `wait()` 和 `signal()` 实现：

```c
wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        // 将当前进程加入 S->list
        add(S->list, current_process);
        block();    // 阻塞当前进程，交出 CPU
    }
}

signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        // 从等待队列中唤醒一个进程
        process *P = remove(S->list);
        wakeup(P);
    }
}
```

!!! note "value 的含义"
    在无忙等待实现中，`S->value` 的**负值**的绝对值等于等待队列中的进程数量。例如 `S->value == -3` 表示有 3 个进程正在等待该信号量。

### 经典同步问题

#### 生产者-消费者问题

一组生产者向缓冲区放入产品，一组消费者从缓冲区取出产品。需要协调：缓冲区满时生产者等待，缓冲区空时消费者等待，对缓冲区的访问必须互斥。

信号量定义：

```c
semaphore mutex = 1;   // 互斥访问缓冲区
semaphore full  = 0;   // 已放入的产品数
semaphore empty = n;   // 空缓冲区数量，n 为缓冲区大小
```

生产者进程：

```c
do {
    // produce an item
    wait(empty);       // 等待空位
    wait(mutex);       // 进入临界区
    // add item to buffer
    signal(mutex);     // 离开临界区
    signal(full);      // 增加产品数
} while (true);
```

消费者进程：

```c
do {
    wait(full);        // 等待产品
    wait(mutex);       // 进入临界区
    // remove item from buffer
    signal(mutex);     // 离开临界区
    signal(empty);     // 增加空位数
    // consume the item
} while (true);
```

!!! warning "wait 操作的顺序"
    `wait(empty)` 和 `wait(mutex)` 的顺序不能颠倒。若生产者先执行 `wait(mutex)` 再执行 `wait(empty)`，当缓冲区已满时，生产者持有 mutex 且等待 empty，而消费者需要 mutex 才能取产品——导致**死锁**。消费者一侧同理。

#### 读者-写者问题（读者优先）

多个读者可以同时读取共享数据，但写者必须独占访问。读者优先策略：只要有读者在读，后续读者可直接进入，写者必须等待所有读者完成。

信号量与变量定义：

```c
semaphore rw_mutex = 1;   // 读写互斥，写者与第一个/最后一个读者使用
semaphore mutex_r  = 1;   // 保护 read_count 的互斥
int read_count = 0;       // 当前正在读的读者数量
```

读者进程：

```c
do {
    wait(mutex_r);
    read_count++;
    if (read_count == 1)
        wait(rw_mutex);   // 第一个读者锁住写者
    signal(mutex_r);

    // --- read shared data ---

    wait(mutex_r);
    read_count--;
    if (read_count == 0)
        signal(rw_mutex); // 最后一个读者释放写者
    signal(mutex_r);
} while (true);
```

写者进程：

```c
do {
    wait(rw_mutex);
    // --- write shared data ---
    signal(rw_mutex);
} while (true);
```

???+ warning "读者优先的饥饿问题"
    在读者优先策略下，如果读者源源不断到来，写者可能被无限期推迟——即**写者饥饿**。解决此问题的方案包括写者优先策略和公平策略。

#### 哲学家就餐问题

5 位哲学家围坐圆桌，每两位之间放一根筷子。哲学家交替思考和进餐，进餐需同时拿到**左右两根**筷子。

信号量定义：

```c
semaphore chopstick[5] = {1, 1, 1, 1, 1};  // 5 根筷子，初始均可用
```

哲学家 $P_i$ 的行为（第 $i$ 位哲学家使用第 $i$ 根和第 $(i+1) \bmod 5$ 根筷子）：

```c
do {
    // think ...

    wait(chopstick[i]);            // 拿左边筷子
    wait(chopstick[(i + 1) % 5]);  // 拿右边筷子

    // eat ...

    signal(chopstick[i]);            // 放左边筷子
    signal(chopstick[(i + 1) % 5]);  // 放右边筷子

    // think ...
} while (true);
```

!!! danger "死锁风险"
    如果 5 位哲学家同时拿起左边的筷子，则每个人都无法拿到右边的筷子——所有哲学家无限等待，形成**死锁**。常见解决策略：

    - 最多允许 4 位哲学家同时拿筷子（引入计数信号量，初值为 4）
    - 奇数号哲学家先拿左再拿右，偶数号哲学家先拿右再拿左（破坏循环等待）
    - 仅当左右筷子均可用时才拿起（原子操作）
