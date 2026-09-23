# 线程

## 线程概述

!!! abstract "进程与线程的本质区别"
    **进程**是资源分配的基本单位，**线程**是 CPU 使用的基本单位（即轻量级进程 LWP）。

### 线程的组成

线程包含以下组成部分：

- **线程 ID**（Thread ID）
- **程序计数器 PC**
- **寄存器集合**（Register Set）
- **栈**（Stack）

<figure markdown="span">
  ![单线程与多线程进程对比](https://webp-pic.yokumi.cn/2025/10/20251021151346462.png){ loading=lazy width="70%" }
</figure>

### 线程共享与私有资源

同一进程中的线程**共享**：

- 代码段（Code Section）
- 数据段（Data Section）
- 堆（Heap）
- 打开的文件（Open Files）
- 信号（Signals）

每个线程**私有**：

- 栈（Stack）
- 寄存器（Registers）
- 程序计数器（PC）

### 引入线程的动机

- 创建进程开销大，多线程节省资源
- 线程切换比进程切换快（无需切换地址空间）
- 线程可调度到不同处理器上并行执行
- 线程间通信更方便（共享进程地址空间）

### 线程的状态

线程与进程类似，具有三种基本状态：

- **运行态**（Running）：线程正在 CPU 上执行
- **就绪态**（Ready）：线程已准备好，等待被调度
- **等待态**（Waiting）：线程等待某个事件完成

## 线程模型

### 用户线程与内核线程

用户线程（User Thread）
: 由**用户级线程库**管理的线程，内核对其不可见。线程的创建、调度、同步均在用户空间完成。

内核线程（Kernel Thread）
: 由**操作系统内核**直接管理的线程。内核负责线程的创建、调度和管理，能感知每个内核线程的存在。

两者之间的关系形成了不同的线程模型。

### 多对一模型（Many-to-One）

<figure markdown="span">
  ![多对一模型](https://webp-pic.yokumi.cn/2025/10/20251021154018103.png){ loading=lazy width="70%" }
</figure>

多个用户线程映射到一个内核线程。

- 线程管理在用户空间完成，效率高
- 一个线程阻塞将导致**整个进程阻塞**
- 无法利用多核处理器实现真正的并行
- 线程库负责线程间的调度

### 一对一模型（One-to-One）

<figure markdown="span">
  ![一对一模型](https://webp-pic.yokumi.cn/2025/10/20251021154641490.png){ loading=lazy width="70%" }
</figure>

每个用户线程对应一个内核线程。

- 一个线程阻塞**不影响**其他线程
- 可以在多核处理器上实现真正的并行
- 创建内核线程开销较大，线程数量受内核限制
- 典型系统：Windows、Linux、Solaris 9+

### 多对多模型（Many-to-Many）

<figure markdown="span">
  ![多对多模型](https://webp-pic.yokumi.cn/2025/10/20251021155047909.png){ loading=lazy width="70%" }
</figure>

$M$ 个用户线程映射到 $N$ 个内核线程（$M \ge N$）。

- 动态映射，灵活性高
- 既可避免一个线程阻塞整个进程，也可控制内核线程数量
- 实现复杂
- 变体：**两层模型**（Two-level Model），允许部分用户线程绑定到特定内核线程

### 三种模型对比

| 特性 | 多对一 (M:1) | 一对一 (1:1) | 多对多 (M:N) |
|------|-------------|-------------|-------------|
| 线程阻塞影响 | 整个进程阻塞 | 仅阻塞自身 | 仅阻塞自身 |
| 多核并行 | 不支持 | 支持 | 支持 |
| 线程数量 | 不受限 | 受内核限制 | 不受限 |
| 创建开销 | 小 | 大 | 适中 |
| 实现复杂度 | 低 | 中 | 高 |
| 典型系统 | Green Threads | Windows, Linux | Solaris (早期) |

## 线程库

线程库为开发者提供创建和管理线程的 API。主要实现方式有两种：

- **用户级库**：在用户空间实现，内核不感知线程存在
- **内核级库**：由操作系统内核直接支持的 API

### Pthreads

Pthreads 是 **POSIX 标准**定义的线程 API，广泛应用于 UNIX/Linux 系统。

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

int sum; /* this data is shared by the thread(s) */

void *runner(void *param); /* the thread */

int main(int argc, char *argv[])
{
    pthread_t tid; /* the thread identifier */
    pthread_attr_t attr; /* set of thread attributes */

    if (argc != 2) {
        fprintf(stderr, "usage: a.out <integer value>\n");
        return -1;
    }

    if (atoi(argv[1]) < 0) {
        fprintf(stderr, "%d must be >= 0\n", atoi(argv[1]));
        return -1;
    }

    /* get the default attributes */
    pthread_attr_init(&attr);
    /* create the thread */
    pthread_create(&tid, &attr, runner, argv[1]);
    /* wait for the thread to exit */
    pthread_join(tid, NULL);

    printf("sum = %d\n", sum);

    return 0;
}

/* The thread will begin control in this function */
void *runner(void *param)
{
    int i, upper = atoi(param);
    sum = 0;

    for (i = 1; i <= upper; i++)
        sum += i;

    pthread_exit(0);
}
```

???+ info "关键函数说明"
    - `pthread_create()`：创建新线程，指定线程 ID、属性、起始函数和参数
    - `pthread_join()`：等待指定线程结束
    - `pthread_exit()`：线程主动退出

### Java 线程

<figure markdown="span">
  ![Java 线程管理方式](https://webp-pic.yokumi.cn/2025/10/20251021163831162.png){ loading=lazy width="70%" }
</figure>

Java 线程的创建和管理由 JVM 负责，通常采用以下两种方式：

- 继承 `Thread` 类并重写 `run()` 方法
- 实现 `Runnable` 接口并传入 `Thread` 构造函数

Java 线程在底层映射到操作系统内核线程（1:1 模型），由 JVM 负责与操作系统的交互。

## 线程的常见问题

### fork() 与 exec()

当多线程进程调用 `fork()` 时，存在两种语义：

- **复制所有线程**：子进程获得父进程所有线程的副本
- **仅复制调用线程**：子进程只包含调用 `fork()` 的那个线程

???+ warning "实践建议"
    如果 `fork()` 之后紧接着调用 `exec()`，则仅复制调用线程即可（因为 `exec()` 会替换整个进程地址空间）。如果不会调用 `exec()`，则应复制所有线程。

### 线程取消

线程取消（Thread Cancellation）指在线程完成之前终止其执行。目标线程称为**可取消线程**（target thread），分为两种方式：

异步取消（Asynchronous Cancellation）
: 一个线程立即终止目标线程，目标线程可能处于任意执行点，可能导致资源未释放或共享数据不一致

延迟取消（Deferred Cancellation）
: 目标线程定期检查自身是否应被取消，只有在安全的取消点（cancellation point）才执行取消操作

延迟取消更安全，是 Pthreads 的默认取消方式。

### 信号处理

信号（Signal）在 UNIX 系统中用于通知进程发生了某个事件。在多线程环境中的信号处理：

- 信号可分为**同步信号**（由进程自身产生，如除零）和**异步信号**（由外部产生，如 Ctrl+C）
- 每个线程可以有自己的信号掩码
- 某些信号可被定向到特定线程
- 未指定目标线程的信号可被任意线程处理

### 线程池

线程池（Thread Pool）在进程启动时预先创建一定数量的工作线程，放入池中等待任务分配。

!!! tip "线程池的优势"
    - 避免频繁创建和销毁线程的开销
    - 限制并发线程数量，防止系统过载
    - 任务提交与线程创建解耦，响应更快

工作流程：

1. 预先创建 $N$ 个工作线程
2. 任务到达时，从池中取出空闲线程执行
3. 任务完成后，线程归还池中等待下一个任务
4. 若无空闲线程，任务在队列中等待

### 线程特定数据

线程特定数据（Thread-Specific Data, TSD）允许每个线程拥有某个"全局变量"的私有副本。

- 对外表现为全局变量，但每个线程拥有独立的值
- 典型应用：`errno` 变量——每个线程需要自己的错误码
- Pthreads 提供了 `pthread_key_create()`、`pthread_setspecific()`、`pthread_getspecific()` 等 API

### 调度器激活与 LWP

<figure markdown="span">
  ![调度器激活机制](https://webp-pic.yokumi.cn/2025/10/20251021170441139.png){ loading=lazy width="70%" }
</figure>

调度器激活（Scheduler Activations）是 Many-to-Many 模型的一种优化机制，通过**轻量级进程（LWP）**作为用户线程与内核线程之间的中间层：

- 每个 LWP 附着在一个内核线程上
- 内核向用户级线程库提供 LWP（即虚拟处理器）
- 用户级线程库将用户线程调度到 LWP 上执行
- 当内核线程阻塞时，内核通知用户级线程库（通过 **upcall**），由线程库决定下一步调度
- 当阻塞事件完成时，内核再次 upcall 通知线程库

!!! abstract "LWP 的核心作用"
    LWP 使得用户级线程库可以在内核不知晓具体用户线程的情况下，灵活地进行线程调度，同时避免一个线程阻塞导致整个进程停滞的问题。
