# 1G · 可扩展价值学习（算法基础）

> 所属报告：[Sergey Levine 近期研究趋势分析](../Sergey_Levine.md) · 类别 ID：`scalable-value-learning` · 论文数：6（2024: 2 / 2025: 4 / 2026: 0）  
> 所有链接均为 arXiv 摘要页，已通过 `verify_links.py` 核对。

---

## 1. 这个方向在研究什么

这是纯 RL 算法研究，不直接涉及机器人硬件。它回答一个根本问题：**价值函数能否像语言模型那样，随着数据、算力和模型规模的增加而可预测地变好？**

背景知识：RL 中的价值函数（V 或 Q）估计"从这个状态（采取这个动作）出发，未来能拿到多少回报"。它用**时序差分（TD）**学习——用自己对下一步的估计来更新当前估计（bootstrapping）。这带来两个众所周知的麻烦：目标是非平稳的（自己在变），误差会沿时间步累积。社区长期认为价值学习"不稳定、难扩展"，与监督学习形成鲜明对比。

这一类论文逐一拆解这个"传说"：

1. 损失函数：用分类交叉熵替代回归 MSE 是否就能扩展（Stop Regressing）？
2. 算力分配：数据与更新次数（UTD）之间的 Pareto 前沿是否可预测（Value-Based RL Scales Predictably）？模型大小、batch size 与 UTD 如何配合（Compute-Optimal Scaling）？
3. 问题结构：长 horizon 是否是离线 RL 扩展的根本障碍（Horizon Reduction）？能否用分治代替逐步回传（Transitive RL）？
4. 基准：需要什么样的基准来暴露算法差异（OGBench）？

**为什么重要**：1C 和 1D 类别中所有"用价值函数改进 generalist"的方法（V-GPS、QGF、RL Token、OGPO…）都建立在"价值函数可以在大模型、大数据上可靠训练"这一前提上。这一类别为该前提提供证据和配方。它在 2025Q4 之后没有新论文——个人推断：核心结论已给出，后续以被引用的形式出现在应用类别中。

---

## 2. 论文逐篇分析（按时间）

### 2024

**[Stop Regressing: Training Value Functions via Classification for Scalable Deep RL](https://arxiv.org/abs/2403.03950)**（2024-03，12 位作者）  
价值函数通常用 MSE 回归拟合 bootstrapped 目标，但把回归式价值 RL 扩展到 Transformer 等大网络很难；监督学习靠交叉熵分类损失却可靠扩展到巨大网络。论文研究：**把回归换成分类**是否同样能改善 RL 的可扩展性。结果：分类交叉熵训练的价值函数在多个领域显著提升性能与可扩展性——Atari 单任务（SoftMoE）、Atari 多任务（大型 ResNet）、**Q-transformer 机器人操作**、无搜索下棋、语言 agent Wordle，均达 SOTA。分析表明收益主要来自缓解价值 RL 固有的问题：噪声目标与非平稳性。**意义**：一个几乎零成本的改动，把"价值学习不能扩展"的第一块基石撬松。

**[OGBench: Benchmarking Offline Goal-Conditioned RL](https://arxiv.org/abs/2410.20092)**（2024-10）  
离线目标条件 RL（GCRL）是从无奖励标注数据中获取多样行为与表征的简单、无监督、领域无关的方式，却缺少标准基准。OGBench 包含 8 类环境、85 个数据集、6 个代表性算法的参考实现，专门设计来探测**stitching、长时域推理、高维输入与随机性**等能力。在旧基准上排名相近的算法，在 OGBench 上暴露出鲜明的强弱差异。**意义**：Scholar 引用 253 次。它成为本组后续几乎所有价值学习论文（FQL、Horizon Reduction、Transitive RL、Decoupled Q-Chunking）的评测标准。

### 2025

**[Value-Based Deep RL Scales Predictably](https://arxiv.org/abs/2502.04327)**（2025-02）  
扩展需要可预测性：不仅要在更多算力 / 数据下表现好，还要能从小规模实验预测大规模结果。论文证明**离策略价值 RL 尽管"名声不好"，其实是可预测的**：(1) 达到某性能所需的数据与算力位于一条由 **UTD 比**控制的 Pareto 前沿上，估计该前沿即可预测"给更多算力需要多少数据"或反之；(2) 可以确定总预算在数据与算力之间的最优分配，并据此选超参；(3) 这种可预测性依赖先估计超参之间的可预测关系，以管理 RL 特有的过拟合与可塑性丢失。在 SAC、BRO、PQL 三种算法、DeepMind Control / Gym / IsaacGym 上验证外推。**意义**：第一次给价值 RL 画出类似语言模型的 scaling law。

**[Horizon Reduction Makes RL Scalable](https://arxiv.org/abs/2506.04168)**（2025-06）  
一个真正可扩展的离线 RL 算法应能在足够数据、算力与容量下解决任何问题。用**比典型大 1000 倍**的数据集在多样、困难、此前未解决的任务上检验，发现许多现有算法扩展性差，远低于最大性能就饱和。假设：**horizon 是主因**。多组分析实验证实长 horizon 确实是离线 RL 扩展的根本障碍；多种 horizon reduction 技术显著提升可扩展性。提出极简但可扩展的 SHARSA，取得最佳渐近性能与扩展行为。**意义**：把"扩展失败"从算法细节归因到问题结构，并给出可操作的解法方向——这直接支撑 1B 类别的 Q-chunking、Decoupled Q-Chunking（chunk 就是 horizon reduction）。

**[Compute-Optimal Scaling for Value-Based Deep RL](https://arxiv.org/abs/2508.14881)**（2025-08）  
语言模型的 compute-optimal 扩展研究充分，RL 很少。在线价值 RL 有两个算力分配轴：模型容量与 UTD 比。固定算力预算下如何划分以最大化样本效率？分析揭示模型大小、batch size、UTD 之间微妙的相互作用，特别是 **TD-overfitting** 现象：增大 batch 会迅速损害小模型的 Q 函数精度，但大模型没有这一效应——所以大规模时可以有效使用大 batch。给出理解这一现象的心智模型与选择 batch size / UTD 的指南。**意义**：与 Value-Based RL Scales Predictably 一起，构成价值 RL 的"Chinchilla"式分析。

**[Transitive RL: Value Learning via Divide and Conquer](https://arxiv.org/abs/2510.22512)**（2025-10）  
面向离线 GCRL（任意状态到任意状态最短步数）。TRL 把 GCRL 中的**三角不等式**结构转化为实用的分治式价值更新规则。相比 TD：偏差累积更少——原则上处理长度 T 的轨迹只需 \(O(\log T)\) 次递归而非 \(O(T)\)；相比蒙特卡洛：因做动态规划而方差更低。在困难的长时域基准任务上取得离线 GCRL 最佳性能。**意义**：这是对 Horizon Reduction 结论的算法回应——既然 horizon 是障碍，就用 \(\log T\) 的递归结构绕开它。

---

## 3. 演进脉络

```
2024-03  Stop Regressing    损失函数：回归 → 分类                       ← 撬动第一块基石
2024-10  OGBench            基准：暴露 stitching / 长时域 / 高维差异
2025-02  Scales Predictably 算力—数据 Pareto 前沿由 UTD 控制             ← scaling law
2025-06  Horizon Reduction  问题结构：horizon 是根本障碍；SHARSA
2025-08  Compute-Optimal    模型大小 × batch × UTD；TD-overfitting
2025-10  Transitive RL      分治式价值更新，O(log T) 递归
```

一条清晰的逻辑链：先证明价值学习**可以**扩展（Stop Regressing）→ 证明它**可预测地**扩展（Scales Predictably、Compute-Optimal）→ 找出**阻碍**扩展的结构因素（Horizon Reduction）→ 给出针对该因素的**新算法**（Transitive RL）。OGBench 贯穿其中作为标尺。

---

## 4. 深度分析

### 4.1 把 RL 的"传说"逐条证伪

社区对价值 RL 的三个成见——不稳定、不可预测、不能上大模型——分别被 Stop Regressing（分类损失稳定训练）、Scales Predictably（Pareto 前沿可外推）、Compute-Optimal（大模型反而能用大 batch）针对性回应。这一系列工作的方法论是**借用监督学习的扩展研究工具**（scaling law、compute-optimal 分析、损失函数选择），而不是发明新的 RL 理论。

### 4.2 Horizon 是贯穿多个类别的核心变量

Horizon Reduction 的结论在本报告其他类别中反复出现：

- 1B：Q-chunking 在 chunk 空间做 RL（缩短有效 horizon）；Decoupled Q-Chunking 让 critic 用长 chunk（更少的回传步数）。
- 1C：SARL 在语义 prompt 空间做 RL——每个"语义动作"覆盖很多低层步，有效 horizon 大幅缩短。
- 1E：层级控制本身就是 horizon reduction。
- 1G：Transitive RL 用 \(\log T\) 递归。

个人推断：这是 Levine 组 2025–2026 年最具统一性的技术主题——"让价值在更粗的时间尺度上回传"，无论是通过 chunk、技能、语义动作还是分治。

### 4.3 与生成式策略研究的分工

本类别关心 critic（价值函数）如何扩展；1D 类别关心 actor（flow / diffusion 策略）如何被 critic 改进。两者组合起来才是完整的 actor–critic 系统。QGF 的论点——测试时引导避开 actor–critic 训练的不稳定从而随规模扩展更好——可以看作本类别结论在 actor 侧的延伸：**critic 可以稳定扩展，actor 的不稳定性可以通过不训练 actor 来绕开**。

---

## 5. 与其他类别的连接

- → **1B**：Horizon Reduction 是 Q-chunking / Decoupled Q-Chunking / MAC 的理论动机。
- → **1C**：WSRL 的价值发散分析、PostBC 的覆盖理论属于同一算法传统。
- → **1D**：FQL 在 OGBench 上评估；QGF 的可扩展性论点依赖 critic 可稳定训练。
- → **1F**：ViVa 的视频价值函数是价值学习向被动数据的扩展。
- ↔ **1H**：Digi-Q（在冻结 VLM 特征上做 TD 学习）、VIMPO（critic-free 的策略隐式价值）是 LLM 侧的价值学习变体。

---

## 6. 与我的研究方向的连接

- **Horizon 结论直接支持 skill-level world model 的动机**：如果 horizon 是价值学习和模型预测（MAC）的共同障碍，那么在技能时间尺度上建模就是最自然的 horizon reduction——一个技能覆盖数十到数百个控制步，把 \(T\) 缩小一到两个数量级。
- **Transitive RL 的三角不等式**对目标条件的 humanoid 任务有直接意义：技能级 world model 可以预测"执行技能后离目标还有多远"，与 GCRL 的距离结构天然兼容。
- **Stop Regressing 的分类损失**可用于 world model 的 outcome 头：把 success / failure / progress 预测建成分类而非回归，可能更稳定，也便于输出校准的不确定性。
- **TD-overfitting 的警示**：在小模型上增大 batch 会伤害价值精度——设计轻量的 skill-level value / world model 时需要注意这一点。

---

## 7. 待追踪问题

- 这一类别 2025Q4 之后是否会有新论文，还是已转入应用？
- Scaling law 是否会从仿真控制扩展到真实机器人数据集？
- Transitive RL 的分治更新能否用于非目标条件（有奖励）的任务？
- 价值函数的可扩展性结论在数十亿参数的 VLA critic 上是否成立？
