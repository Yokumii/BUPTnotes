# Verilog 编程

## 标识符

标识符
: Verilog 中用于命名模块、端口、信号等的字符串

    命名规则与 C 语言相同；关键字必须小写。

!!! warning "存盘文件名"
    **存盘文件名应与设计的模块名相同**，否则可能导致编译或仿真时找不到对应模块。

## 概述

Verilog 采用 **四值逻辑** 体系：

逻辑值
: Verilog 信号可取的四种状态

    | 值 | 含义 |
    |---|------|
    | `0` | 逻辑低 |
    | `1` | 逻辑高 |
    | `X` | 不定（未知或冲突） |
    | `Z` | 高阻（浮空） |

模块
: Verilog 设计的基本单元，由两部分构成：**描述接口** 与 **描述功能**

<figure markdown="span">
  ![模块结构示意图](https://webp-pic.yokumi.cn/2026/01/20260101154505244.png){ loading=lazy width="70%" }
</figure>

## 数据类型

### 数据 I/O 类型

<figure markdown="span">
  ![数据 I/O 类型](https://webp-pic.yokumi.cn/2026/01/20260101154510724.png){ loading=lazy width="70%" }
</figure>

!!! warning "reg 类型的使用约束"
    - **`always` 中被赋值的信号必须用 `reg` 类型**
    - 输入和双向端口**不能声明为 `reg` 型**

`parameter`
: 符号常量，其定义只在本模块内有效

## 运算符

位连接运算符 `{ }`
: 将两个或多个信号的某些位拼接起来。**不允许连接非定长常数**。

???+ details "位宽自动调整规则"
    - **运算表达式结果的长度**由最长的操作数决定（自动调整位宽）
    - **操作结果的长度**由赋值左端目标长度决定

## 功能描述语句

!!! note "并发语句"
    `assign`、`always`、元件例化均为**并发语句**——它们在仿真时并行执行，不存在顺序依赖。

### assign

<figure markdown="span">
  ![assign 语句](https://webp-pic.yokumi.cn/2026/01/20260101154516046.png){ loading=lazy width="70%" }
</figure>

### always

<figure markdown="span">
  ![always 语句](https://webp-pic.yokumi.cn/2026/01/20260101154523078.png){ loading=lazy width="70%" }
</figure>

### 敏感信号表

敏感信号表
: 列出能够启动 `always` 进程的信号列表；**只有敏感信号的变化才能启动进程**。

!!! warning "组合逻辑的敏感信号"
    组合逻辑中，**所有输入都必须作为敏感信号**，否则仿真结果和综合结果会不一致。

### 注意点

!!! danger "关键禁忌"
    - **不要在一个 `always` 中同时使用 `=` 和 `<=` 赋值**
    - `if`、`case`、`for` 语句**必须在 `always` 块中使用**

## 设计组合电路

### 要求

<figure markdown="span">
  ![组合电路设计要求](https://webp-pic.yokumi.cn/2026/01/20260101154529042.png){ loading=lazy width="70%" }
</figure>

## 设计时序电路

### 要求

<figure markdown="span">
  ![时序电路设计要求](https://webp-pic.yokumi.cn/2026/01/20260101154535650.png){ loading=lazy width="70%" }
</figure>

### 注意点

!!! warning "时序电路敏感信号"
    - **异步信号必须放在敏感信号表中**；必须都是**边沿**触发
    - 锁存器的所有输入都放在敏感信号表中；锁存器敏感信号都是**电平**

## 元件例化

元件例化
: 将一个结构完整的 `module` 模块作为子元件引用到当前设计中

!!! danger "元件例化禁忌"
    **不能在 `always` 语句内部引用子模块**。元件例化是并发语句，应与 `always`、`assign` 处于同一层级。


