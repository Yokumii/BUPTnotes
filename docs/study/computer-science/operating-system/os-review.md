# 操作系统复习

## 核心概念与定义

系统调用（System Call）
: 操作系统为应用程序提供的编程接口，是用户态请求内核服务的唯一途径。

特权指令（Privileged Instructions）
: 只能在内核态下执行的指令，用户态试图执行将触发陷阱（trap）。

陷阱（Trap）
: 由软件产生的中断，包括程序错误（如除零）或系统调用请求。

中断向量表（Interrupt Vector Table）
: 存放各类中断服务例程入口地址的表，中断发生时硬件根据中断号查表跳转。

进程（Process）
: 程序被加载到内存后的执行实例。程序是静态的，进程是动态的。

PCB（Process Control Block）
: 操作系统内核中用于描述和管理进程的数据结构，是进程存在的唯一标识。

多道程序度（Degree of Multiprogramming）
: 内存中同时驻留的进程数量，由长期调度器控制。

!!! abstract "操作系统核心要点"
    - 操作系统是**中断驱动**的：所有 CPU 切换和系统服务都由中断触发
    - **引导（Booting）**：开机时将操作系统内核从磁盘加载到内存并启动执行的过程
    - **分时操作系统（Time-sharing OS）**：允许多个用户交互式使用计算机
    - **实时系统（Real-time System）**：在限定时间内对外部事件做出响应

### 进程的五种状态

| 状态 | 说明 |
|------|------|
| 新建（New） | 进程正在被创建 |
| 就绪（Ready） | 进程已准备好，等待分配 CPU |
| 运行（Running） | 进程正在 CPU 上执行 |
| 等待（Waiting） | 进程等待某个事件（如 I/O） |
| 终止（Terminated） | 进程执行完毕 |

### 进程状态转换图

<figure markdown="span">
  ![进程状态转换图](https://webp-pic.yokumi.cn/2025/10/20251007173620406.png){ loading=lazy width="70%" }
</figure>

### 死锁的四个必要条件

| 条件 | 说明 |
|------|------|
| 互斥（Mutual Exclusion） | 资源不能共享，一次只能被一个进程使用 |
| 占有并等待（Hold and Wait） | 进程持有至少一个资源，同时等待其他资源 |
| 非抢占（No Preemption） | 已分配的资源不能被强制剥夺 |
| 循环等待（Circular Waiting） | 存在进程的循环链，每个进程都在等待下一个进程持有的资源 |

### 临界区问题的三个条件

互斥（Mutual Exclusion）
: 若进程 $P_i$ 在其临界区内执行，则其他进程不能进入各自的临界区。

前进（Progress）
: 没有进程在临界区时，需要进入的进程可以进入，且选择不能无限推迟。

有限等待（Bounded Waiting）
: 从请求进入临界区到获准进入，其他进程进入临界区的次数有上限。

### IPC 的两种基本方法

| 方法 | 机制 | 特点 |
|------|------|------|
| 共享内存（Shared Memory） | 进程共享同一块内存区域 | 速度快，需自行同步 |
| 消息传递（Message Passing） | 通过 send/receive 交换消息 | 适用于分布式系统 |

### 调度器分类

| 调度器 | 别称 | 功能 |
|--------|------|------|
| 长期调度器 | 作业调度器 | 从作业队列中选择进程进入内存，控制多道程序度 |
| 短期调度器 | 进程/CPU 调度器 | 从就绪队列中选择进程分配 CPU |
| 中期调度器 | — | 将进程在内存与磁盘之间换入换出 |

### 调度准则

| 准则 | 说明 |
|------|------|
| CPU 利用率（CPU Utilization） | CPU 忙碌时间的比例 |
| 吞吐量（Throughput） | 单位时间内完成的进程数 |
| 周转时间（Turnaround Time） | 从进程创建到终止的总时间 |
| 等待时间（Waiting Time） | 在就绪队列中等待的总时间 |
| 响应时间（Response Time） | 从提交请求到首次响应的时间 |

!!! tip "核心公式"
    $$\text{Waiting Time} + \text{Burst Time} = \text{Turnaround Time}$$

### 信号量的含义

!!! note "信号量 value 的语义"
    - $S \geq 0$：可用资源数量
    - $S < 0$：$|S|$ 为等待队列中的进程数
    - 无忙等待信号量需要**进程等待队列**

### 线程模型

| 模型 | 特点 | 代表系统 |
|------|------|----------|
| 多对一 | 多个用户线程映射到一个内核线程 | — |
| 一对一 | 每个用户线程对应一个内核线程 | Linux、Solaris 10 |
| 多对多 | $m$ 个用户线程映射到 $n$ 个内核线程 | — |


## 简答题要点

### 优先级反转

在实时系统中，**优先级反转**指高优先级进程被低优先级进程阻塞的现象。

**典型场景**：高优先级进程 H 等待低优先级进程 L 持有的资源；此时中等优先级进程 M 抢占了 L 的 CPU，导致 L 无法尽快释放资源，H 被间接地长期阻塞。

!!! warning "优先级反转的本质"
    高优先级进程并非被同等或更高优先级进程阻塞，而是被**低优先级进程**通过资源依赖间接阻塞，且中等优先级进程"插队"使情况恶化。

**解决方案**：

优先级继承（Priority Inheritance）
: 低优先级进程持有高优先级进程所需资源时，**临时提升**其优先级至与高优先级进程相同，使其尽快执行并释放资源，释放后恢复原优先级。

优先级天花板协议（Priority Ceiling Protocol）
: 每个资源被分配一个优先级天花板（等于所有可能访问该资源的进程的最高优先级）；进程获取资源时，其优先级提升至该天花板值。

### 条件变量的两种语义

**Signal and Continue（Hansen 语义）**：

- 发信号（signal）的线程**继续执行**
- 被唤醒的线程进入就绪队列，等待调度
- 被唤醒线程重新运行时需**重新检查条件**（必须用 while 循环）

**Signal and Wait（Hoare 语义）**：

- 发信号的线程**立即挂起**，让出管程
- 被唤醒的线程**立即获得管程**并开始执行
- 被唤醒线程此时条件必然成立，无需重新检查

!!! abstract "实际应用"
    大多数系统（如 POSIX、Java）采用 **Signal and Continue** 语义，因此条件变量必须配合 while 循环使用，防止虚假唤醒。

### 不安全状态 ≠ 死锁

- **安全状态**：存在一个安全序列，所有进程都能按某种顺序获得资源并顺利完成
- **不安全状态**：不存在保证所有进程都能完成的安全序列
- **死锁**：进程已经被循环等待阻塞，无法继续

!!! warning "关键区分"
    不安全状态只是**无法保证**存在完成序列，但某些执行顺序仍可能成功。不安全状态是死锁的**必要条件**，但不是充分条件：不安全 → 可能死锁；安全 → 一定不死锁。

### 多级反馈队列调度原则

1. 设置多个优先级不同的就绪队列，优先级从高到低排列
2. 每个队列有不同长度的时间片：高优先级队列时间片短，低优先级队列时间片长
3. 新进程进入最高优先级队列
4. 进程用完当前队列的时间片后，降级到下一优先级队列
5. 在当前队列中未用完时间片（如因 I/O 阻塞）的进程，回到原队列（或升级）
6. 仅当高优先级队列为空时，才调度低优先级队列中的进程
7. 实现了**老化机制**：长时间等待的进程可被提升到更高优先级队列


## 信号量题型解题技巧

### 通用解题框架

1. **识别角色**：确定有几类进程/线程
2. **识别资源**：确定共享缓冲区/资源的容量和约束
3. **设置信号量**：
    - `mutex = 1`：互斥访问共享资源
    - `empty = N`：空位数量
    - `full = 0`：产品数量
    - 其他同步信号量根据约束设置
4. **编写伪代码**：先 P 同步信号量，再 P 互斥信号量；先 V 互斥信号量，再 V 同步信号量

!!! warning "P 操作顺序"
    同步信号量（empty/full）必须在互斥信号量（mutex）**之前** P 操作，否则可能死锁。V 操作顺序无严格限制。


### 爸爸妈妈儿女水果盘问题

盘容量为 1。爸爸放苹果，妈妈放橘子，女儿吃苹果，儿子吃橘子。

```c
semaphore plate = 1;    // 盘中空位，初始为 1
semaphore apple  = 0;   // 苹果数量
semaphore orange = 0;   // 橘子数量
```

???+ success "解题代码"
    ```c
    // 爸爸
    do {
        prepare_apple();
        wait(plate);       // 等待盘空
        put_apple();
        signal(apple);     // 苹果+1
    } while (true);

    // 妈妈
    do {
        prepare_orange();
        wait(plate);       // 等待盘空
        put_orange();
        signal(orange);    // 橘子+1
    } while (true);

    // 女儿
    do {
        wait(apple);       // 等待苹果
        take_apple();
        signal(plate);     // 盘空+1
        eat_apple();
    } while (true);

    // 儿子
    do {
        wait(orange);      // 等待橘子
        take_orange();
        signal(plate);     // 盘空+1
        eat_orange();
    } while (true);
    ```


### 扩展生产者-消费者（P3/P4 模同步）

缓冲区大小为 N，P1、P2 为生产者，P3、P4 为消费者。要求 P3 只消费 P1 的产品，P4 只消费 P2 的产品。

```c
semaphore mutex  = 1;   // 互斥访问缓冲区
semaphore empty  = N;   // 空位数
semaphore full1  = 0;   // P1 产品数
semaphore full2  = 0;   // P2 产品数
```

???+ success "解题代码"
    ```c
    // P1（生产者1）
    do {
        produce_item1();
        wait(empty);
        wait(mutex);
        put_item1();
        signal(mutex);
        signal(full1);
    } while (true);

    // P2（生产者2）
    do {
        produce_item2();
        wait(empty);
        wait(mutex);
        put_item2();
        signal(mutex);
        signal(full2);
    } while (true);

    // P3（消费者，只消费 P1 产品）
    do {
        wait(full1);
        wait(mutex);
        take_item1();
        signal(mutex);
        signal(empty);
        consume_item1();
    } while (true);

    // P4（消费者，只消费 P2 产品）
    do {
        wait(full2);
        wait(mutex);
        take_item2();
        signal(mutex);
        signal(empty);
        consume_item2();
    } while (true);
    ```


### SWAP 指令实现互斥

使用 SWAP 指令和两个布尔变量实现互斥。

```c
// 共享变量
bool lock = false;
```

???+ success "解题代码"
    ```c
    // 进程 Pi
    do {
        bool key = true;
        while (key == true)
            Swap(&key, &lock);   // lock 为 true 时 key 换回 true
        // --- critical section ---
        lock = false;
        // --- remainder section ---
    } while (true);

    // Swap 原子操作
    void Swap(bool *a, bool *b) {
        bool temp = *a;
        *a = *b;
        *b = temp;
    }
    ```


### 可乐机问题（10 槽，最多 1 人访问）

可乐机有 10 个槽位，同时最多 1 人访问可乐机。

```c
semaphore mutex = 1;    // 互斥访问可乐机
semaphore empty = 10;   // 空槽数
semaphore full  = 0;    // 可乐数
```

???+ success "解题代码"
    ```c
    // 生产者（补货员）
    do {
        wait(empty);
        wait(mutex);
        put_coke();
        signal(mutex);
        signal(full);
    } while (true);

    // 消费者（购买者）
    do {
        wait(full);
        wait(mutex);
        take_coke();
        signal(mutex);
        signal(empty);
    } while (true);
    ```


### 可乐机变体（生产者最多放 4，消费者取 1-2）

可乐机有 10 个槽位。生产者每次最多放 4 瓶，消费者每次取 1 或 2 瓶。同时最多 1 人访问。

```c
semaphore mutex = 1;    // 互斥访问
semaphore empty = 10;   // 空槽数
semaphore full  = 0;    // 可乐数
```

???+ success "解题代码"
    ```c
    // 生产者（每次放 1~4 瓶）
    do {
        int produce_num = rand(1, 4);    // 随机决定放几瓶
        for (int i = 0; i < produce_num; i++)
            wait(empty);                 // 逐个获取空位
        wait(mutex);
        for (int i = 0; i < produce_num; i++)
            put_coke();
        signal(mutex);
        for (int i = 0; i < produce_num; i++)
            signal(full);                // 逐个增加可乐数
    } while (true);

    // 消费者（每次取 1 或 2 瓶）
    do {
        int consume_num = rand(1, 2);    // 随机决定取几瓶
        for (int i = 0; i < consume_num; i++)
            wait(full);                  // 逐个获取可乐
        wait(mutex);
        for (int i = 0; i < consume_num; i++)
            take_coke();
        signal(mutex);
        for (int i = 0; i < consume_num; i++)
            signal(empty);               // 逐个释放空位
    } while (true);
    ```


### 水果盘（1 个苹果或 3 个橘子）

盘容量为 3 个水果位。爸爸放苹果（占 1 位），妈妈放橘子（占 1 位），女儿吃苹果，儿子吃橘子。盘中有苹果时妈妈不放橘子，盘中有橘子时爸爸不放苹果。即：盘中要么全是苹果，要么全是橘子。

```c
semaphore mutex  = 1;   // 互斥访问盘
semaphore empty  = 3;   // 空位数
semaphore apple  = 0;   // 苹果数
semaphore orange = 0;   // 橘子数
semaphore sp     = 1;   // 同步：标记盘的类型（苹果盘/橘子盘）
```

???+ success "解题代码"
    ```c
    // 爸爸（放苹果，每次 1 个，盘中最多 3 个苹果）
    do {
        wait(sp);            // 获取盘类型控制权
        wait(empty);         // 等待空位
        wait(mutex);
        put_apple();
        signal(mutex);
        signal(apple);
        // 放完苹果后不释放 sp，保持"苹果盘"状态
        // 当盘中苹果全被取走后，女儿释放 sp
    } while (true);

    // 但更常见的简化写法是引入 plate_type 变量
    // 下面给出更实用的解法：

    // 改进：使用 plate_type 标记当前盘类型
    // plate_type = 0 表示空/无类型，1 表示苹果盘，2 表示橘子盘
    int plate_type = 0;  // 共享变量
    semaphore mutex  = 1;
    semaphore empty  = 3;
    semaphore apple  = 0;
    semaphore orange = 0;

    // 爸爸
    do {
        wait(empty);
        wait(mutex);
        if (plate_type == 0 || plate_type == 1) {
            plate_type = 1;
            put_apple();
            signal(mutex);
            signal(apple);
        } else {
            signal(mutex);
            signal(empty);  // 放回空位，等待
        }
    } while (true);

    // 妈妈
    do {
        wait(empty);
        wait(mutex);
        if (plate_type == 0 || plate_type == 2) {
            plate_type = 2;
            put_orange();
            signal(mutex);
            signal(orange);
        } else {
            signal(mutex);
            signal(empty);
        }
    } while (true);

    // 女儿
    do {
        wait(apple);
        wait(mutex);
        take_apple();
        if (/* 盘中无苹果了 */)
            plate_type = 0;
        signal(mutex);
        signal(empty);
    } while (true);

    // 儿子
    do {
        wait(orange);
        wait(mutex);
        take_orange();
        if (/* 盘中无橘子了 */)
            plate_type = 0;
        signal(mutex);
        signal(empty);
    } while (true);
    ```


### 狮子与羊笼子问题

笼子容量：1 只狮子或 2 只羊。猎人放狮子，牧羊人放羊，观光者取动物。

```c
semaphore mutex   = 1;   // 互斥访问笼子
semaphore empty   = 2;   // 空位（以羊为单位，狮子占 2 位）
semaphore lion    = 0;   // 狮子数
semaphore sheep   = 0;   // 羊数
semaphore type_ok = 1;   // 控制笼中动物类型一致
```

???+ success "解题代码"
    ```c
    // 猎人（放狮子，占 2 位）
    do {
        wait(empty);        // 先占 1 位
        wait(empty);        // 再占 1 位（狮子占 2 位）
        wait(type_ok);      // 确保类型一致
        wait(mutex);
        put_lion();
        signal(mutex);
        signal(lion);
    } while (true);

    // 牧羊人（放羊，占 1 位）
    do {
        wait(empty);
        wait(type_ok);
        wait(mutex);
        put_sheep();
        signal(mutex);
        signal(sheep);
    } while (true);

    // 观光者（取动物）
    do {
        wait(mutex);
        if (/* 有狮子 */) {
            take_lion();
            signal(lion);      // lion 计数减
            signal(empty);
            signal(empty);     // 狮子释放 2 个空位
            signal(type_ok);   // 取完后释放类型锁
        } else if (/* 有羊 */) {
            take_sheep();
            signal(sheep);
            signal(empty);
            if (/* 笼空了 */)
                signal(type_ok);
        }
        signal(mutex);
    } while (true);
    ```


### 幼儿园老师分水果

盘容量 5 个水果。老师放水果（1 个苹果 + 2 个橘子为一份），男孩吃苹果，女孩吃橘子。

```c
semaphore mutex  = 1;   // 互斥访问盘
semaphore empty  = 5;   // 空位数
semaphore apple  = 0;   // 苹果数
semaphore orange = 0;   // 橘子数
```

???+ success "解题代码"
    ```c
    // 老师（每次放 1 苹果 + 2 橘子）
    do {
        wait(empty);         // 苹果占 1 位
        wait(empty);         // 橘子占第 1 位
        wait(empty);         // 橘子占第 2 位
        wait(mutex);
        put_apple();
        put_orange();
        put_orange();
        signal(mutex);
        signal(apple);       // 苹果 +1
        signal(orange);      // 橘子 +1
        signal(orange);      // 橘子再 +1
    } while (true);

    // 男孩（吃苹果）
    do {
        wait(apple);
        wait(mutex);
        take_apple();
        signal(mutex);
        signal(empty);
        eat_apple();
    } while (true);

    // 女孩（吃橘子）
    do {
        wait(orange);
        wait(mutex);
        take_orange();
        signal(mutex);
        signal(empty);
        eat_orange();
    } while (true);
    ```


### 桥梁过河问题

桥上最多 4 辆车，同方向可连续通行，反方向需等待。

```c
semaphore bridge   = 4;    // 桥上车辆数上限
semaphore mutex_ns = 1;    // 保护南北向计数器
semaphore mutex_sn = 1;    // 保护北南向计数器
semaphore turn     = 1;    // 方向互斥
int count_ns = 0;          // 南→北车辆数
int count_sn = 0;          // 北→南车辆数
```

???+ success "解题代码"
    ```c
    // 南→北方向
    do {
        wait(mutex_ns);
        if (count_ns == 0)
            wait(turn);         // 第一辆车获取方向锁
        count_ns++;
        signal(mutex_ns);

        wait(bridge);           // 获取桥上名额
        cross_bridge_ns();
        signal(bridge);

        wait(mutex_ns);
        count_ns--;
        if (count_ns == 0)
            signal(turn);       // 最后一辆车释放方向锁
        signal(mutex_ns);
    } while (true);

    // 北→南方向
    do {
        wait(mutex_sn);
        if (count_sn == 0)
            wait(turn);
        count_sn++;
        signal(mutex_sn);

        wait(bridge);
        cross_bridge_sn();
        signal(bridge);

        wait(mutex_sn);
        count_sn--;
        if (count_sn == 0)
            signal(turn);
        signal(mutex_sn);
    } while (true);
    ```


### 读者-写者问题（FIFO 公平）

在基本读者优先的基础上增加 FIFO 公平性：使用队列信号量确保先到先服务。

```c
semaphore rw_mutex = 1;   // 读写互斥
semaphore mutex_r  = 1;   // 保护 read_count
semaphore queue    = 1;   // FIFO 公平队列
int read_count = 0;
```

???+ success "解题代码"
    ```c
    // 读者
    do {
        wait(queue);           // 排队
        wait(mutex_r);
        read_count++;
        if (read_count == 1)
            wait(rw_mutex);    // 第一个读者锁住写者
        signal(mutex_r);
        signal(queue);         // 允许下一个人排队

        // --- read ---

        wait(mutex_r);
        read_count--;
        if (read_count == 0)
            signal(rw_mutex);  // 最后一个读者释放
        signal(mutex_r);
    } while (true);

    // 写者
    do {
        wait(queue);           // 排队
        wait(rw_mutex);
        signal(queue);         // 允许下一个人排队

        // --- write ---

        signal(rw_mutex);
    } while (true);
    ```

!!! note "queue 信号量的作用"
    `queue` 确保读者和写者按到达顺序进入。写者到达时先获取 `queue`，后续读者被阻塞在 `wait(queue)` 上，直到写者获取 `rw_mutex` 后释放 `queue`，从而防止写者饥饿。


### 诊所医生/病人问题

诊所有 1 名医生，候诊室有 10 把椅子。病人来时有空椅则坐下等候，否则离开。

```c
semaphore doctor   = 1;    // 医生是否空闲
semaphore chairs   = 10;   // 空椅数
semaphore mutex    = 1;    // 保护 waiting_count
int waiting_count  = 0;
```

???+ success "解题代码"
    ```c
    // 病人
    do {
        wait(mutex);
        if (waiting_count >= 10) {
            signal(mutex);
            leave();           // 没有空椅，离开
            continue;
        }
        waiting_count++;
        signal(mutex);

        wait(chairs);          // 占一把椅子
        wait(doctor);          // 等待医生
        signal(chairs);        // 离开椅子去看病

        see_doctor();

        wait(mutex);
        waiting_count--;
        signal(mutex);
        signal(doctor);        // 看完释放医生
    } while (true);

    // 医生
    do {
        wait(doctor);          // 等待病人
        treat_patient();
        signal(doctor);        // 诊疗完毕
    } while (true);
    ```


### 流水线产品 C 问题

产品 C 需要 4 个 A + 3 个 B。装配台最多放 12 个零件。

```c
semaphore mutex = 1;    // 互斥访问装配台
semaphore slot  = 12;   // 装配台空位
semaphore partA = 0;    // A 零件数
semaphore partB = 0;    // B 零件数
```

???+ success "解题代码"
    ```c
    // A 生产者
    do {
        produce_A();
        wait(slot);
        wait(mutex);
        put_A();
        signal(mutex);
        signal(partA);
    } while (true);

    // B 生产者
    do {
        produce_B();
        wait(slot);
        wait(mutex);
        put_B();
        signal(mutex);
        signal(partB);
    } while (true);

    // C 装配者
    do {
        wait(partA); wait(partA); wait(partA); wait(partA);  // 取 4 个 A
        wait(partB); wait(partB); wait(partB);                // 取 3 个 B
        wait(mutex);
        take_4A_3B();
        signal(mutex);
        for (int i = 0; i < 7; i++)
            signal(slot);       // 释放 7 个空位
        assemble_C();
    } while (true);
    ```


### 水果盘变体（3 个水果，苹果/橘子变体）

盘容量 3。爸爸放苹果，妈妈放橘子，女儿吃苹果，儿子吃橘子。

```c
semaphore mutex  = 1;   // 互斥访问盘
semaphore empty  = 3;   // 空位数
semaphore apple  = 0;   // 苹果数
semaphore orange = 0;   // 橘子数
```

???+ success "解题代码"
    ```c
    // 爸爸
    do {
        prepare_apple();
        wait(empty);
        wait(mutex);
        put_apple();
        signal(mutex);
        signal(apple);
    } while (true);

    // 妈妈
    do {
        prepare_orange();
        wait(empty);
        wait(mutex);
        put_orange();
        signal(mutex);
        signal(orange);
    } while (true);

    // 女儿
    do {
        wait(apple);
        wait(mutex);
        take_apple();
        signal(mutex);
        signal(empty);
    } while (true);

    // 儿子
    do {
        wait(orange);
        wait(mutex);
        take_orange();
        signal(mutex);
        signal(empty);
    } while (true);
    ```


### 士兵过独木桥问题

独木桥同一时间只允许一个方向的士兵通过，无人数上限。

```c
semaphore bridge   = 1;    // 方向互斥
semaphore mutex_lr = 1;    // 保护左→右计数
semaphore mutex_rl = 1;    // 保护右→左计数
int count_lr = 0;
int count_rl = 0;
```

???+ success "解题代码"
    ```c
    // 左→右士兵
    do {
        wait(mutex_lr);
        if (count_lr == 0)
            wait(bridge);         // 第一个士兵锁方向
        count_lr++;
        signal(mutex_lr);

        cross_bridge_lr();

        wait(mutex_lr);
        count_lr--;
        if (count_lr == 0)
            signal(bridge);       // 最后一个士兵释放方向
        signal(mutex_lr);
    } while (true);

    // 右→左士兵
    do {
        wait(mutex_rl);
        if (count_rl == 0)
            wait(bridge);
        count_rl++;
        signal(mutex_rl);

        cross_bridge_rl();

        wait(mutex_rl);
        count_rl--;
        if (count_rl == 0)
            signal(bridge);
        signal(mutex_rl);
    } while (true);
    ```


### 自行车厂问题

车架架最多放 10 个，轮架最多放 20 个。组装工人取 1 车架 + 2 轮子。

```c
semaphore mutex_frame = 1;   // 互斥访问车架架
semaphore mutex_wheel = 1;   // 互斥访问轮架
semaphore frame_slot  = 10;  // 车架架空位
semaphore wheel_slot  = 20;  // 轮架空位
semaphore frame       = 0;   // 车架数
semaphore wheel       = 0;   // 轮子数
```

???+ success "解题代码"
    ```c
    // 车架生产者
    do {
        produce_frame();
        wait(frame_slot);
        wait(mutex_frame);
        put_frame();
        signal(mutex_frame);
        signal(frame);
    } while (true);

    // 轮子生产者
    do {
        produce_wheel();
        wait(wheel_slot);
        wait(mutex_wheel);
        put_wheel();
        signal(mutex_wheel);
        signal(wheel);
    } while (true);

    // 组装工人
    do {
        wait(frame);              // 取 1 车架
        wait(mutex_frame);
        take_frame();
        signal(mutex_frame);
        signal(frame_slot);

        wait(wheel); wait(wheel); // 取 2 轮子
        wait(mutex_wheel);
        take_wheel(); take_wheel();
        signal(mutex_wheel);
        signal(wheel_slot); signal(wheel_slot);

        assemble_bicycle();
    } while (true);
    ```


### 邮箱通信问题

P1 有邮箱 m，P2 有邮箱 n。P1 向 P2 发消息（放入 n），P2 向 P1 发消息（放入 m）。各自邮箱容量有限（m 容量 M，n 容量 N）。

```c
semaphore mutex_m = 1;    // 互斥访问邮箱 m
semaphore mutex_n = 1;    // 互斥访问邮箱 n
semaphore empty_m = M;    // 邮箱 m 空位数
semaphore full_m  = 0;    // 邮箱 m 消息数
semaphore empty_n = N;    // 邮箱 n 空位数
semaphore full_n  = 0;    // 邮箱 n 消息数
```

???+ success "解题代码"
    ```c
    // P1：向 n 发消息，从 m 收消息
    do {
        // 发送
        prepare_msg();
        wait(empty_n);
        wait(mutex_n);
        send_to_n();
        signal(mutex_n);
        signal(full_n);

        // 接收
        wait(full_m);
        wait(mutex_m);
        receive_from_m();
        signal(mutex_m);
        signal(empty_m);
        process_msg();
    } while (true);

    // P2：向 m 发消息，从 n 收消息
    do {
        // 接收
        wait(full_n);
        wait(mutex_n);
        receive_from_n();
        signal(mutex_n);
        signal(empty_n);
        process_msg();

        // 发送
        prepare_msg();
        wait(empty_m);
        wait(mutex_m);
        send_to_m();
        signal(mutex_m);
        signal(full_m);
    } while (true);
    ```


### 电信营业厅问题

100 部手机库存，1 个营业员，营业厅最多 20 人。

```c
semaphore hall      = 20;   // 营业厅容量
semaphore salesman  = 1;    // 营业员
semaphore mutex     = 1;    // 保护库存
int stock           = 100;  // 手机库存
```

???+ success "解题代码"
    ```c
    // 顾客
    do {
        wait(hall);           // 进入营业厅
        wait(salesman);       // 等待营业员
        wait(mutex);
        if (stock > 0) {
            stock--;
            sell_phone();
        } else {
            // 无货
        }
        signal(mutex);
        signal(salesman);
        signal(hall);         // 离开营业厅
    } while (true);
    ```


### 奇偶缓冲区问题

缓冲区 N 个单元。P1 产生数据放入缓冲区，P2 取奇数，P3 取偶数。

```c
semaphore mutex   = 1;   // 互斥访问缓冲区
semaphore empty   = N;   // 空位数
semaphore odd     = 0;   // 奇数个数
semaphore even    = 0;   // 偶数个数
```

???+ success "解题代码"
    ```c
    // P1（生产者）
    do {
        int num = produce();
        wait(empty);
        wait(mutex);
        put(num);
        signal(mutex);
        if (num % 2 == 1)
            signal(odd);
        else
            signal(even);
    } while (true);

    // P2（取奇数）
    do {
        wait(odd);
        wait(mutex);
        take_odd();
        signal(mutex);
        signal(empty);
        process_odd();
    } while (true);

    // P3（取偶数）
    do {
        wait(even);
        wait(mutex);
        take_even();
        signal(mutex);
        signal(empty);
        process_even();
    } while (true);
    ```


### 包饺子问题

3 个爱好者吃饺子，1 个供应者。供应者每次提供 2 种原料（共 3 种：面、馅、佐料），缺哪种爱好者就拿哪种并包饺子。

三种原料组合中，供应者每次放 2 种，缺第 3 种：

```c
semaphore supply_A = 0;   // 有面+馅（缺佐料）
semaphore supply_B = 0;   // 有面+佐料（缺馅）
semaphore supply_C = 0;   // 有馅+佐料（缺面）
semaphore finish   = 0;   // 通知供应者可以继续
semaphore mutex    = 1;   // 互斥访问桌面
```

???+ success "解题代码"
    ```c
    // 供应者
    do {
        wait(finish);
        wait(mutex);
        int choice = rand(1, 3);  // 随机放 2 种
        put_ingredients(choice);
        signal(mutex);
        if (choice == 1) signal(supply_A);
        else if (choice == 2) signal(supply_B);
        else signal(supply_C);
    } while (true);

    // 爱好者 A（缺佐料）
    do {
        wait(supply_A);
        wait(mutex);
        take_and_make_dumplings();
        signal(mutex);
        signal(finish);
    } while (true);

    // 爱好者 B（缺馅）
    do {
        wait(supply_B);
        wait(mutex);
        take_and_make_dumplings();
        signal(mutex);
        signal(finish);
    } while (true);

    // 爱好者 C（缺面）
    do {
        wait(supply_C);
        wait(mutex);
        take_and_make_dumplings();
        signal(mutex);
        signal(finish);
    } while (true);
    ```


### 寺庙打水问题

小和尚打水倒入缸，老和尚从缸取水。井互斥访问，3 个水桶，缸容量 10 桶。

```c
semaphore well    = 1;    // 井互斥
semaphore bucket  = 3;    // 水桶数
semaphore vat     = 10;   // 缸空位
semaphore water   = 0;    // 缸中水量
semaphore vat_mut = 1;    // 缸互斥
```

???+ success "解题代码"
    ```c
    // 小和尚（打水入缸）
    do {
        wait(bucket);          // 取水桶
        wait(vat);             // 等待缸有空位
        wait(well);            // 互斥访问井
        draw_water();
        signal(well);          // 打完释放井
        wait(vat_mut);
        pour_into_vat();       // 倒入缸
        signal(vat_mut);
        signal(water);         // 缸中水+1
        signal(bucket);        // 归还水桶
    } while (true);

    // 老和尚（从缸取水）
    do {
        wait(bucket);          // 取水桶
        wait(water);           // 等待缸中有水
        wait(vat_mut);
        scoop_from_vat();      // 从缸取水
        signal(vat_mut);
        signal(vat);           // 缸空位+1
        drink_water();
        signal(bucket);        // 归还水桶
    } while (true);
    ```

### 工厂货架问题

A 货架容量 10，B 货架容量 10。A 生产者放 A 零件，B 生产者放 B 零件，装配工人取 1 个 A + 1 个 B 组装。

```c
semaphore mutex_A  = 1;   // 互斥访问 A 货架
semaphore mutex_B  = 1;   // 互斥访问 B 货架
semaphore slot_A   = 10;  // A 货架空位
semaphore slot_B   = 10;  // B 货架空位
semaphore partA    = 0;   // A 零件数
semaphore partB    = 0;   // B 零件数
```

???+ success "解题代码"
    ```c
    // A 生产者
    do {
        produce_A();
        wait(slot_A);
        wait(mutex_A);
        put_A();
        signal(mutex_A);
        signal(partA);
    } while (true);

    // B 生产者
    do {
        produce_B();
        wait(slot_B);
        wait(mutex_B);
        put_B();
        signal(mutex_B);
        signal(partB);
    } while (true);

    // 装配工人
    do {
        wait(partA);
        wait(mutex_A);
        take_A();
        signal(mutex_A);
        signal(slot_A);

        wait(partB);
        wait(mutex_B);
        take_B();
        signal(mutex_B);
        signal(slot_B);

        assemble();
    } while (true);
    ```

### 生产者-消费者允许同时 1 生产者 + 1 消费者

缓冲区大小 N，允许 1 个生产者和 1 个消费者同时访问（各自操作不同位置），但不允许多个生产者或多个消费者同时访问。

```c
semaphore mutex_p = 1;   // 生产者互斥
semaphore mutex_c = 1;   // 消费者互斥
semaphore empty   = N;   // 空位数
semaphore full    = 0;   // 产品数
```

???+ success "解题代码"
    ```c
    // 生产者
    do {
        produce_item();
        wait(empty);
        wait(mutex_p);        // 生产者间互斥
        put_item();
        signal(mutex_p);
        signal(full);
    } while (true);

    // 消费者
    do {
        wait(full);
        wait(mutex_c);        // 消费者间互斥
        take_item();
        signal(mutex_c);
        signal(empty);
        consume_item();
    } while (true);
    ```

!!! note "关键区别"
    与标准生产者-消费者问题不同，这里将 `mutex` 拆分为 `mutex_p` 和 `mutex_c`，使得生产者和消费者可以同时访问缓冲区（一个写一个读），但同类之间仍然互斥。


### 仓库 X/Y 约束问题

仓库存放两种产品 X 和 Y，约束：$-N < X - Y < M$（即 Y 比 X 多不超过 N，X 比 Y 多不超过 M）。

```c
semaphore mutex  = 1;   // 互斥访问仓库
semaphore slot_x = M;   // X 可以比 Y 多存放的量
semaphore slot_y = N;   // Y 可以比 X 多存放的量
```

???+ success "解题代码"
    ```c
    // X 入库
    do {
        wait(slot_x);         // 等待 X 的余量（X - Y < M）
        wait(mutex);
        store_X();
        signal(mutex);
        signal(slot_y);       // X 多了一个，Y 的余量增加（Y - X 的上限放宽）
    } while (true);

    // Y 入库
    do {
        wait(slot_y);         // 等待 Y 的余量（Y - X < N）
        wait(mutex);
        store_Y();
        signal(mutex);
        signal(slot_x);       // Y 多了一个，X 的余量增加
    } while (true);
    ```

!!! note "约束分析"
    - `slot_x` 初始为 M：X 最多比 Y 多 M 个
    - `slot_y` 初始为 N：Y 最多比 X 多 N 个
    - X 入库时消耗 `slot_x`，释放 `slot_y`（差值向 X 偏移）
    - Y 入库时消耗 `slot_y`，释放 `slot_x`（差值向 Y 偏移）


### 数据采集系统（3 个缓冲区）

3 个采集进程分别向 3 个缓冲区写入数据，1 个处理进程从 3 个缓冲区各取 1 条数据后处理。

```c
semaphore mutex1 = 1, mutex2 = 1, mutex3 = 1;  // 3 个缓冲区互斥
semaphore empty1 = N, empty2 = N, empty3 = N;   // 各缓冲区空位
semaphore full1  = 0, full2  = 0, full3  = 0;   // 各缓冲区数据数
```

???+ success "解题代码"
    ```c
    // 采集进程 1
    do {
        collect_data1();
        wait(empty1);
        wait(mutex1);
        write_buf1();
        signal(mutex1);
        signal(full1);
    } while (true);

    // 采集进程 2
    do {
        collect_data2();
        wait(empty2);
        wait(mutex2);
        write_buf2();
        signal(mutex2);
        signal(full2);
    } while (true);

    // 采集进程 3
    do {
        collect_data3();
        wait(empty3);
        wait(mutex3);
        write_buf3();
        signal(mutex3);
        signal(full3);
    } while (true);

    // 处理进程
    do {
        wait(full1);
        wait(full2);
        wait(full3);           // 3 个缓冲区都有数据

        wait(mutex1);
        take_buf1();
        signal(mutex1);
        signal(empty1);

        wait(mutex2);
        take_buf2();
        signal(mutex2);
        signal(empty2);

        wait(mutex3);
        take_buf3();
        signal(mutex3);
        signal(empty3);

        process_data();
    } while (true);
    ```


## 死锁计算

### 公式推导

设有 $M$ 个进程，每个最多需要 $k$ 个资源，总资源数为 $R$。

最坏情况：每个进程都已获得 $k - 1$ 个资源，还差 1 个即可完成。此时共占用 $M(k-1)$ 个资源。只需再提供 1 个资源，就能保证至少一个进程完成并释放所有资源。

因此，**无死锁条件**：

$$R \geq (k - 1) \cdot M + 1$$

!!! tip "解题模板"
    1. 识别每个进程的最大需求 $k$
    2. 识别总资源数 $R$
    3. 代入公式求出最大进程数 $M$：$$M \leq \frac{R - 1}{k - 1}$$
    4. 结果取整数部分

### 典型例题

**题目**：系统有 10 台磁带机，每个进程最多需要 3 台，最多允许多少个进程同时运行而不死锁？

**解答**：

$$10 \geq 2M + 1 \implies M \leq \frac{9}{2} = 4.5$$

取整数，最多 **4** 个进程。


## 银行家算法

银行家算法用于**死锁避免**，在分配资源前检查分配后系统是否仍处于安全状态。

### 数据结构

| 名称 | 含义 |
|------|------|
| Available | 各类资源的当前可用数量（向量） |
| Max | 每个进程对每类资源的最大需求（矩阵） |
| Allocation | 每个进程当前已分配的各类资源数量（矩阵） |
| Need | 每个进程尚需的各类资源数量（矩阵），Need = Max - Allocation |

### 安全性算法步骤

1. 初始化 `Work = Available`，`Finish[i] = false`（对所有 $i$）
2. 寻找满足 `Finish[i] == false` 且 `Need[i] <= Work` 的进程 $P_i$
3. 若找到：`Work = Work + Allocation[i]`，`Finish[i] = true`，回到步骤 2
4. 若所有 `Finish[i] == true`，系统处于安全状态；否则不安全

### 例题

| 进程 | Allocation (A B C) | Max (A B C) | Need (A B C) |
|------|---------------------|-------------|--------------|
| P0 | 0 1 0 | 7 5 3 | 7 4 3 |
| P1 | 2 0 0 | 3 2 2 | 1 2 2 |
| P2 | 3 0 2 | 9 0 2 | 6 0 0 |
| P3 | 2 1 1 | 2 2 2 | 0 1 1 |
| P4 | 0 0 2 | 4 3 3 | 4 3 1 |

Available = (3 3 2)

???+ success "安全性检查"
    1. P1: Need(1,2,2) <= Available(3,3,2) → Work = (3,3,2) + (2,0,0) = (5,3,2)，Finish[P1] = true
    2. P3: Need(0,1,1) <= Work(5,3,2) → Work = (5,3,2) + (2,1,1) = (7,4,3)，Finish[P3] = true
    3. P4: Need(4,3,1) <= Work(7,4,3) → Work = (7,4,3) + (0,0,2) = (7,4,5)，Finish[P4] = true
    4. P0: Need(7,4,3) <= Work(7,4,5) → Work = (7,4,5) + (0,1,0) = (7,5,5)，Finish[P0] = true
    5. P2: Need(6,0,0) <= Work(7,5,5) → Work = (7,5,5) + (3,0,2) = (10,5,7)，Finish[P2] = true

    安全序列：`<P1, P3, P4, P0, P2>`，系统处于安全状态。

!!! warning "资源请求处理"
    当进程 $P_i$ 请求资源 Request 时：
    1. 若 Request > Need[i]，出错（请求超过最大需求）
    2. 若 Request > Available，$P_i$ 等待
    3. 试分配：Available -= Request，Allocation[i] += Request，Need[i] -= Request
    4. 执行安全性检查：安全则分配，不安全则回滚试分配
