# 1B · 动作分块与实时执行（Action chunking / real-time execution）

> 所属报告：[Sergey Levine 近期研究趋势分析](../Sergey_Levine.md) · 类别 ID：`chunking-realtime` · 论文数：8（2024: 0 / 2025: 5 / 2026: 3）  
> 所有链接均为 arXiv 摘要页，已通过 `verify_links.py` 核对。带 † 为 Physical Intelligence 团队大型系统工作。

---

## 1. 这个方向在研究什么

**Action chunking（动作分块）** 指策略一次预测未来一段动作序列（例如接下来 50 个控制周期的动作），然后逐个执行或执行一部分后再重新预测，而不是每个时间步只看一次观测、输出一个动作。它最早在 ALOHA / ACT 等模仿学习工作中流行，是让 diffusion / flow 策略在高频控制中表现平滑的关键技巧。

这一类论文把它从"技巧"变成了研究对象，问三个问题：

1. **为什么有效**：流行解释有"时间一致性""缩短有效 horizon""更好的表征"。哪一个是真的？
2. **能不能带进 RL**：RL 的价值函数按单步动作定义，把动作换成"chunk"之后 TD 学习、探索和策略提取会怎样变化？
3. **大模型延迟怎么办**：VLA 推理一次要几百毫秒甚至更久，机器人不能停下来等。如何边执行当前动作段、边生成下一段，并保证两段之间平滑？如果还要在这种延迟下做 RL，马尔可夫假设还成立吗？

**为什么重要**：模型越大越聪明，也越慢；真实机器人需要 10–50 Hz 的连续控制。动作分块和异步执行是目前唯一在实践中被证明能调和这一矛盾的机制，因此它决定了 VLA 能否走出实验室。这一类别在 2025Q2 之前一篇都没有，之后连续出现 8 篇——它是随着 π 系列真正部署才浮现的问题。

---

## 2. 论文逐篇分析（按时间）

### 2025

**[RTC: Real-Time Execution of Action Chunking Flow Policies](https://arxiv.org/abs/2506.07339)** †（2025-06）  
问题：action chunking 解决了时间一致性，但没解决延迟——在 chunk 边界会出现停顿或分布外的抖动。RTC 是一个**推理时算法**，对任何 diffusion / flow VLA 开箱可用、无需重训：执行当前 chunk 的同时生成下一个 chunk，把"必然会执行"的动作**冻结**，用 inpainting 补全其余部分。引入 Kinetix 仿真中 12 个高动态任务的基准，并在 6 个真实双臂任务上评估；RTC 对推理延迟独特地鲁棒，显著提高吞吐量，在点火柴这类精细任务上即便有显著延迟也能高成功率。**意义**：把延迟问题正式提上台面，Scholar 引用 175 次，是本类别的拐点。

**[Q-chunking: Reinforcement Learning with Action Chunking](https://arxiv.org/abs/2507.07969)**（2025-07）  
面向 offline-to-online RL 的长时域稀疏奖励任务。关键洞见：把模仿学习中的 action chunking 用到 TD-based RL——**直接在"chunked"动作空间中做 RL**，好处有两点：(1) 利用离线数据中时间一致的行为做更有效的在线探索；(2) 使用无偏的 n 步回传，让 TD 学习更稳定高效。在一系列长时域稀疏奖励操作任务上超过此前最好的 offline-to-online 方法。**意义**：Scholar 引用 100 次，证明动作分块对 RL 的价值不只是"平滑"，而是同时改善探索和价值回传。

**[Training-Time Action Conditioning for Efficient Real-Time Chunking](https://arxiv.org/abs/2512.05964)** †（2025-12）  
RTC 的推理时 inpainting 有计算开销、增加延迟。替代方案：**在训练时模拟推理延迟**，直接条件于动作前缀，推理时零开销。不改模型结构、不改机器人运行时，几行代码即可实现。仿真中在高延迟下超过推理时 RTC；在 π0.6 上的装箱与咖啡任务中保持相同性能与速度但计算更省。**意义**：把一个推理时的 trick 转化为训练目标——这是本组反复出现的模式（同见 1D 类别里 CFGRL 把 guidance 变成训练目标）。

**[MAC: Scalable Offline Model-Based RL with Action Chunks](https://arxiv.org/abs/2512.08108)**（2025-12）  
研究 model-based value expansion 能否成为离线 RL 处理长时域任务的可扩展配方。矛盾：想象 rollout 越长，价值 bootstrapping 偏差越小，但模型误差累积越大。解法：用**动作分块的动力学模型**——从一段动作序列直接预测未来状态，而不是逐步预测——减少复合误差；并用从表达力强的行为分块策略中做拒绝采样代替直接优化策略，防止分布外动作利用模型漏洞。在最多 1 亿 transition 的数据集上取得离线 model-based RL 中最佳表现，尤其在长时域任务上。**意义**：这是本报告中最接近"技能级世界模型"的工作——预测粒度从单步提升到动作块。

**[Decoupled Q-Chunking](https://arxiv.org/abs/2512.10926)**（2025-12）  
chunked critic（估计一段动作序列的价值）能加速价值回传，但从它提取策略很难：策略必须开环输出整段动作，对需要反应性的环境不利，chunk 越长越难建模。关键洞见：**让 critic 的 chunk 长度与 policy 的 chunk 长度解耦**——针对"部分动作块"蒸馏出一个 critic（从原 chunked critic 乐观回传，近似部分块延伸为完整块时的最大价值），策略只需输出较短的块。在长时域离线目标条件任务上稳定超过先前方法。**意义**：把 1B 类别的核心张力（长 chunk 利于价值学习、短 chunk 利于反应性）用架构解耦解决。

### 2026

**[AsyncVLA: An Asynchronous VLA for Fast and Robust Navigation on the Edge](https://arxiv.org/abs/2602.13476)**（2026-02）  
基础模型的计算成本导致高延迟，在动态环境中会破坏控制回路。AsyncVLA 解耦语义推理与反应执行：大模型在远程工作站给高层引导，轻量的 onboard **Edge Adapter** 以高频持续修正动作。为弥合两条异步流之间的域差距，引入端到端微调协议与偏向动态交互的轨迹重加权。在通信延迟最高 6 秒的真实导航任务上比 SOTA 基线成功率高 40%。**意义**：把延迟问题推到极端（秒级），并给出"大模型 + 边缘小模型"的层级方案。

**[Why Does Action Chunking Improve Behavioral Cloning Performance in Robotic Control?](https://arxiv.org/abs/2608.02547)**（2026-08）  
通过仿真与真实的严格实验，**否定**了三种流行解释（时间一致性、horizon 缩短、表征学习）。真正的原因：(a) 相比马尔可夫策略，分块策略有更强的**非马尔可夫表达力**和更低的复合误差——但在很多场景下，这些效果可以完全由"延迟策略"（每步基于 k 步前的观测预测单个动作）获得；(b) 额外的好处是**隐式集成（implicit ensembling）**：分块策略同时学习多种时间关系（a_t|o_t, a_t|o_{t-1}, …），行为类似模型集成，提升鲁棒性与泛化。基于此，可以**不用 action chunking 也匹配其性能**——把分块策略当作随机延迟的策略集成来部署；并提出显式实例化集成的策略类，在许多领域显著超过 action chunking。**意义**：这是一篇"拆解神话"的论文，它把动作分块的价值归结为两个可以单独实现的机制，为设计更好的策略类打开空间。

**[ARLI: Learning to Act While Waiting — RL Finetuning of Generalist Robot Policies Under Inference Latency](https://arxiv.org/abs/2608.23831)** †（2026-08，20 位作者）  
VLA 的严重推理延迟会导致停顿或抖动，从而**改变有效的环境动力学，破坏 RL 依赖的马尔可夫假设，使标准 RL 算法完全失效**。ARLI（Asynchronous RL with Intermediate Information）建立在异步推理之上（交错生成与执行以隐藏延迟），并解决其与 RL 的不兼容：设计低延迟的 RL 策略，在推理窗口内最大化反应性——通过状态增广（纳入已承诺的动作和一次推理中途的观测）恢复近马尔可夫结构。在仿真与真实操作任务上，能在标准 RL 完全失败的延迟条件下有效微调，甚至匹配或超过理想无延迟设置下的标准 RL。**意义**：把 1B（延迟）和 1C（RL 后训练）两个类别正式接上——RL 后训练大型 VLA 必须是延迟感知的。

---

## 3. 演进脉络

```
2025-06  RTC                推理时 inpainting 解决 chunk 边界抖动          ← 问题浮现
2025-07  Q-chunking         RL 直接在 chunk 空间进行
2025-12  Training-time RTC  把 RTC 变成训练目标，推理零开销
2025-12  MAC                动作块级动力学模型减少复合误差
2025-12  Decoupled Q-Chunk  critic 长 chunk / policy 短 chunk 解耦
2026-02  AsyncVLA           秒级延迟：远程大模型 + 边缘适配器
2026-08  Why Chunking       否定流行解释；非马尔可夫表达力 + 隐式集成
2026-08  ARLI               延迟破坏马尔可夫假设；延迟感知 RL           ← 与 RL 后训练汇合
```

两条子线：**执行线**（RTC → Training-time RTC → AsyncVLA → ARLI）解决"怎么在延迟下执行 / 学习"；**算法线**（Q-chunking → MAC → Decoupled Q-Chunking → Why Chunking）解决"chunk 在学习中到底起什么作用"。

---

## 4. 深度分析

### 4.1 延迟不是工程细节，而是改变问题定义的变量

RTC 把延迟当作执行层的平滑问题；ARLI 则指出延迟会改变**环境的有效动力学**——机器人在等待推理时，世界继续运动，"状态"已经不是策略看到的那个状态，马尔可夫性被破坏。这解释了为什么把标准 RL 直接套在异步执行的 VLA 上会完全失败。个人推断：随着 VLA 参数继续增长，延迟感知会成为所有 RL 后训练方法的默认要求，而不是可选项。

### 4.2 "推理时 trick → 训练时目标"的迁移模式

RTC（推理时 inpainting）→ Training-time RTC（训练时模拟延迟）。同一模式在本组其他类别反复出现：V-GPS 的推理时重排序 → CFGRL 把 guidance 写进训练目标；QGF 的测试时引导 → QAM / RQL 把价值梯度纳入训练。这反映一个工程哲学：先用推理时方法快速验证机制有效，再把它固化到训练里换取零推理开销。

### 4.3 chunk 长度的两难与解耦

- 长 chunk：n 步回传偏差小、探索时间一致（Q-chunking）；动力学模型复合误差小（MAC）。
- 短 chunk：策略反应快、容易建模。
- Decoupled Q-Chunking 的答案是让 critic 与 policy 用不同长度。

这与多时间尺度控制的直觉一致：**评价可以在粗时间尺度上进行，执行需要在细时间尺度上进行**。

### 4.4 "为什么有效"的答案改变了设计空间

Why Chunking 的结论——非马尔可夫表达力 + 隐式集成——意味着动作分块并非唯一途径：随机延迟的策略集成可以复现其效果，显式集成还能超过它。对设计者的启示是，可以把"多时间关系的集成"作为一个独立的设计维度，与是否分块解耦。

---

## 5. 与其他类别的连接

- ← **1A 基础模型**：π0 的 flow 动作块是这一切的源头；Training-time RTC 直接在 π0.6 上实验。
- → **1C RL 后训练**：Q-chunking 是 RL 算法；ARLI 是 RL 后训练的前置条件。
- → **1D 测试时引导**：Decoupled Q-Chunking 的"从 chunked critic 蒸馏部分 critic"与 QGF 的"用 critic 引导 flow"共享价值函数视角。
- → **1G 可扩展价值学习**：Q-chunking 与 MAC 都是对 Horizon Reduction 结论（horizon 是扩展障碍）的具体回应——chunk 就是一种 horizon reduction。

---

## 6. 与我的研究方向的连接

- **MAC 是 skill-level world model 的直接先例**：它证明"从动作序列预测未来状态"比逐步预测复合误差更小。把预测粒度从"动作块"进一步提升到"技能"（更长、语义化、带 outcome 标签），是自然的延伸；MAC 用拒绝采样防止模型被分布外动作利用的做法，对应我关于"OOD 时拒绝 imagined rollout 进入 replay buffer"的设想。
- **Decoupled Q-Chunking 的解耦思想**可迁移为：world model / value 在技能时间尺度上评价，低层控制器在高频上执行。
- **ARLI 对 humanoid 尤其相关**：人形机器人平衡控制对延迟极敏感，任何 VLA + RL 方案都必须在设计之初考虑推理窗口内的反应性。
- **Why Chunking 的隐式集成**为不确定性估计提供了一个几乎免费的来源：分块策略内部不同时间关系之间的分歧，可能就是一个可用的 epistemic uncertainty 信号（个人推断，需验证）。

---

## 7. 待追踪问题

- Training-time RTC 与 ARLI 的状态增广能否合并为一个统一的"延迟感知训练"配方？
- Decoupled Q-Chunking 的解耦能否推到"技能级 critic + 动作级 policy"？
- Why Chunking 的显式集成策略类在真实 VLA 规模上是否成立？
- MAC 的动作块动力学模型是否会与 1F 类别的视频世界模型（SC3-Eval）融合？
