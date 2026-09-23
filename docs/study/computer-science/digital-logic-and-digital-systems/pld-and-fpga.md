# PLD 与 FPGA

## 概述

现代数字系统由三种核心积木块构成：

CPU
: 中央处理器，负责通用计算与控制。

PLD
: 可编程逻辑器件（Programmable Logic Device），提供可由用户自定义的逻辑功能。

RAM
: 随机存取存储器，用于数据存储与缓存。

!!! note "PLD 的定位"
    PLD 填补了通用 CPU 与专用 ASIC 之间的空白——它既不像 CPU 那样依赖软件指令流，也不像 ASIC 那样制造后功能完全固定，而是允许用户在硬件层面灵活配置逻辑功能。

## 编程部位

PLD 的可编程部位决定了用户可以在哪些环节自定义逻辑：

<figure markdown="span">
  ![PLD 编程部位](https://webp-pic.yokumi.cn/2026/01/20260101154557334.png){ loading=lazy width="70%" }
</figure>

## 编程方法

不同的 PLD 采用不同的编程技术，决定了配置数据的写入方式与可擦写性：

<figure markdown="span">
  ![PLD 编程方法](https://webp-pic.yokumi.cn/2026/01/20260101154600897.png){ loading=lazy width="70%" }
</figure>

## CPLD

CPLD（Complex Programmable Logic Device）是复杂可编程逻辑器件，通常由多个 PAL/GAL 模块通过可编程互连矩阵组成，适合实现组合逻辑和中等规模的状态机：

<figure markdown="span">
  ![CPLD 结构](https://webp-pic.yokumi.cn/2026/01/20260101154603559.png){ loading=lazy width="70%" }
</figure>

## FPGA

FPGA（Field Programmable Gate Array）是现场可编程门阵列，基于查找表（LUT）和可编程互连资源实现逻辑配置，适合大规模、高密度的数字系统设计：

<figure markdown="span">
  ![FPGA 结构 1](https://webp-pic.yokumi.cn/2026/01/20260101154607650.png){ loading=lazy width="70%" }
</figure>

<figure markdown="span">
  ![FPGA 结构 2](https://webp-pic.yokumi.cn/2026/01/20260101154611454.png){ loading=lazy width="70%" }
</figure>

### 在系统可编程 ISP

传统的 PLD 在用于生产时，是**先编程后装配**——即器件在焊接到电路板之前就必须完成配置。

ISP（In-System Programmability）打破了这一限制：

!!! warning "ISP 的关键意义"
    isp 则可以在装配之前、装配过程中和装配之后再编程。这意味着：
    
    - 产线上无需专用编程器，直接通过板载接口配置
    - 设计迭代无需更换器件，在板上进行现场修改
    - 支持远程升级与功能更新，大幅降低维护成本


