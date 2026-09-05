# 1C · 通用策略的 RL 后训练（真实机器人）

> 所属报告：[Sergey Levine 近期研究趋势分析](../Sergey_Levine.md) · 类别 ID：`rl-posttraining` · 论文数：11（2024: 4 / 2025: 3 / 2026: 4）  
> 所有链接均为 arXiv 摘要页，已通过 `verify_links.py` 核对。带 † 为 Physical Intelligence 团队大型系统工作。

---

## 1. 这个方向在研究什么

用示范数据训练（行为克隆 BC，或 1A 类别的 VLA 预训练）得到的策略通常"会做但不够好"：不够精确、太慢、遇到示范里没出现的情况不会恢复，而且它会继承示范者的噪声和次优习惯。**RL 后训练（RL post-training / fine-tuning）** 指在预训练之后，让策略在真实机器人上通过试错继续改进。

这一类论文的难点与问题：

1. **样本效率**：真实机器人每小时只能采集几百次尝试；算法必须在 1–几小时内见效。
2. **稳定性**：在大型 VLA 或 diffusion / flow 策略上直接做 actor–critic 极易崩溃或遗忘预训练能力。
3. **在哪个空间做 RL**：原始动作、diffusion 的潜噪声、一个紧凑的读出表征、还是语言 prompt？空间越小越结构化，RL 越高效。
4. **奖励从哪里来**：稀疏的成功 / 失败信号如何变成稠密的过程奖励？
5. **预训练与微调的接口**：怎样的预训练策略才是好的 RL 初始化？微调后如何不丢通用能力？

**为什么重要**：这是"generalist 能不能在部署中变得可靠"的决定性问题。2024 年的 HIL-SERL 证明真实机器人 RL 可以在小时级达到近乎完美；2025–2026 年的工作则把 RL 搬到 VLA 上，并系统研究预训练—微调之间的接口。它是 Levine 组 2026 年论文最集中的方向之一（4 篇）。

---

## 2. 论文逐篇分析（按时间）

### 2024

**[SERL: A Software Suite for Sample-Efficient Robotic RL](https://arxiv.org/abs/2401.16013)**（2024-01）  
论点：机器人 RL 之所以难用，是因为实现细节常常比算法选择更重要，而高质量实现不可得。SERL 提供精心实现的样本高效离策略 RL、奖励计算与环境重置方法、一个主流机器人的高质量控制器和一组示例任务。结果：PCB 装配、线缆布线、物体搬运平均每个策略只需 25–50 分钟训练，成功率完美或接近完美，对扰动极其鲁棒，并出现**涌现的恢复与纠正行为**。**意义**：把"真实机器人 RL 可行"从个案变成可复现的工具，是本类别后续所有真实实验的软件基础。

**[HIL-SERL: Precise and Dexterous Robotic Manipulation via Human-in-the-Loop RL](https://arxiv.org/abs/2410.21845)**（2024-10，Science Robotics 2025）  
人在环的视觉 RL 系统：整合示范、人工纠正、高效 RL 算法与系统级设计，在动态操作、精密装配、双臂协调等任务上 **1–2.5 小时内**达到接近完美成功率与快速周期。比模仿学习基线成功率平均高 2 倍、执行快 1.8 倍；学到的策略同时具备反应式与预测式控制。**意义**：Scholar 引用 285 次，是"RL 能在实际训练时间内学会真实世界复杂视觉操作"的最强证据，也是 RL Token、OGPO 等后续工作的对照基准。

**[WSRL: Efficient Online RL Fine-Tuning Need Not Retain Offline Data](https://arxiv.org/abs/2412.07762)**（2024-12）  
现代范式是离线 RL 预训练 → 在线 RL 微调，多数方法要求微调时继续在离线数据上训练以保持稳定，但这既慢又限制性能上限。分析发现：保留离线数据主要是为了防止微调开始时价值函数因分布不匹配而**突然发散**（导致遗忘预训练收益）。WSRL 用一个 warmup 阶段——用预训练策略采集极少量 rollout 来"重新校准"离线 Q 函数——之后**完全丢弃离线数据**也能稳定微调，且学得比保留数据的方法更快更好。**意义**：拆掉了"微调必须带着全部预训练数据"的假设，让在大型数据集上预训练的策略可以轻量地在线改进。

**[RLDG: Robotic Generalist Policy Distillation via RL](https://arxiv.org/abs/2412.09858)**（2024-12）  
generalist 的性能取决于训练数据质量。RLDG 用任务专用 RL **生成高质量训练数据**，再用它微调 generalist。在连接器插入、装配等精密任务上，用 RL 数据微调的 generalist 比用人类示范微调的成功率高最多 40%，且对新任务泛化更好；分析表明收益来自更优的动作分布和更好的状态覆盖。**意义**：RL 与 generalist 的另一种结合方式——不直接在 generalist 上做 RL，而是让 RL 当"更好的示范者"。

### 2025

**[DSRL: Steering Your Diffusion Policy with Latent Space RL](https://arxiv.org/abs/2506.15799)**（2025-06）  
BC 策略在新场景表现不佳时通常要再收集示范。DSRL 在 diffusion 策略的**潜噪声空间**上运行 RL 来调整 BC 策略：样本效率高、只需黑盒访问 BC 策略、无需修改基础策略权重，从而避开微调 diffusion 策略的种种困难。在仿真、真实机器人任务以及调整预训练 generalist 上验证。**意义**：Scholar 引用 157 次。它开创了"在一个更小、更结构化的空间做 RL"的思路——噪声空间维度低、且任何噪声都被 BC 策略映射为"合理"动作，探索天然安全。

**[Robust Finetuning of VLA Robot Policies via Parameter Merging](https://arxiv.org/abs/2512.08333)**（2025-12）  
用少量示范微调 generalist 到新任务时会过拟合：既丢掉原有通用能力，又不能在新任务内部泛化。解法极简：**把微调模型的权重与预训练模型的权重插值**。大量仿真与真实实验表明合并模型同时继承通用能力并鲁棒地学会新任务，在新任务的分布外变体上超过预训练模型和微调模型；合并效果随预训练数据量扩展，并支持终身学习中持续加技能而不丢旧能力。**意义**：解决了 RL / BC 后训练的副作用——遗忘。

**[Posterior Behavioral Cloning: Pretraining BC Policies for Efficient RL Finetuning](https://arxiv.org/abs/2512.16911)**（2025-12）  
反向提问：大家都在改进微调算法，但没人问预训练策略是否是好的 RL 初始化。理论上，标准 BC（直接拟合示范动作）**可能无法保证覆盖示范者的动作**——这是有效 RL 微调的最低条件。如果改为建模"给定示范数据集下示范者行为的后验分布"，就能保证覆盖，且预训练性能不差于 BC。PostBC 可用现代生成模型仅靠监督学习实现，在机器人控制基准与真实操作任务上显著改善 RL 微调效果。**意义**：把"为 RL 而预训练"变成一个独立的研究问题。

### 2026

**[RL Token: Bootstrapping Online RL with VLA Models](https://arxiv.org/abs/2604.23073)** †（2026-04）  
VLA 开箱能做很多技能，但精度与速度需要 RL 微调；直接在大型 VLA 上做 RL 太贵。方法：(1) 让 VLA 暴露一个 **"RL token"**——紧凑的读出表征，保留任务相关的预训练知识、同时作为在线 RL 的高效接口；(2) 在其上训练小型 actor–critic 头修正动作，并把学到的策略锚定在 VLA 上。四个真实任务（拧螺丝、扎带、充电器插入、网线插入）：最难阶段速度最多提升 3 倍，成功率在数分钟到数小时内显著提高，部分任务**超过人类遥操作速度**。**意义**：把 HIL-SERL 级别的效率带到了 VLA 上，且不需要更新 VLA 主干。

**[OGPO: Sample Efficient Full-Finetuning of Generative Control Policies](https://arxiv.org/abs/2605.03065)**（2026-05，17 位作者）  
对 diffusion / flow 生成式策略做**全参数**微调：维护离策略 critic 以最大化数据复用，用改进的 PPO 目标把策略梯度传过完整生成过程、以 critic 作为终端奖励。在多任务、高精度插入、灵巧控制上达到 SOTA；据其所知是**唯一**能把初始化很差的 BC 策略在线微调到接近全成功且 replay buffer 中无专家数据的方法，任务特定超参调整很少。附带稳定技巧（success-buffer 正则、双侧保守优势、Q 方差降低）以抑制 critic 被过度利用，并系统研究了生成式策略微调的稳定机制与失败模式。**意义**：与 DSRL / RL Token 的"不动主干"路线相对，OGPO 证明全参数微调也可以做到样本高效——代价是大量稳定性工程。

**[Success Visitation Matching: Learning Process Rewards for Efficient RL](https://arxiv.org/abs/2606.23640)**（2026-06）  
稀疏的 0/1 结果奖励让信用分配很难。方法：训练一个判别器区分过去的成功与失败 episode，用它激励 RL 策略**匹配成功 episode 的状态—动作访问分布、回避失败的**。因为对所有状态都给出反馈（而非只在成功时），它提供"是否在朝完成推进"的稠密信号，并可证明**不改变最优策略**。在仿真与真实操作任务的 RL 微调上显著加速。**意义**：把失败数据变成奖励塑形的来源，与 1F 类别的 RoboReward 形成互补（一个学通用奖励模型，一个从本任务的成败历史里现学）。

**[SARL: Adapting Generalist Robot Policies with Semantic RL](https://arxiv.org/abs/2606.31958)**（2026-06）  
标准 RL 直接优化机器人动作，要求基础策略的动作分布一开始就接近好策略——对超出预训练分布的复杂长时域任务不成立。关键洞见：对足够强的 generalist，**语言 prompt 是另一个可优化的空间**——调节语言输入能唤起策略已有的技能，并组合它们解决零样本做不到的任务。SARL 通过在线交互优化 prompt 空间，把 generalist 当作可控的技能先验；利用已有技能而非从零学新技能带来结构化、语义有意义的探索和高效在线改进。在真实与仿真中解锁了"让 VLA 解决复杂长时域任务"的新能力，显著超过现有部署改进方法。**意义**：RL 的动作空间从"连续控制量"抬升到了"语义技能选择"，这是层级 RL 与 VLA 的一次自然结合。

---

## 3. 演进脉络

```
2024-01  SERL          真实机器人 RL 可复现的软件栈
2024-10  HIL-SERL      1–2.5 小时近乎完美（Science Robotics）       ← 可行性里程碑
2024-12  WSRL          微调不必保留离线数据
2024-12  RLDG          RL 当示范者，蒸馏进 generalist
2025-06  DSRL          在 diffusion 潜噪声空间做 RL                  ← "换空间"路线开端
2025-12  Param Merging 权重插值防遗忘
2025-12  PostBC        为 RL 微调而设计的预训练
2026-04  RL Token      VLA 紧凑读出表征 + 小 actor–critic 头
2026-05  OGPO          生成式策略的全参数离策略微调
2026-06  Visitation    成败判别器 → 稠密过程奖励
2026-06  SARL          在语言 prompt 空间做 RL                        ← 空间抬升到语义层
```

---

## 4. 深度分析

### 4.1 核心变量：RL 在哪个空间进行

| 空间 | 论文 | 维度 / 结构 | 优点 | 局限 |
|---|---|---|---|---|
| 原始动作 | SERL、HIL-SERL、OGPO | 高维连续 | 表达力最强，可精修每一步 | 需要强稳定性工程；大模型上昂贵 |
| 潜噪声 | DSRL | 与动作同维但被 BC 策略"过滤" | 黑盒、任何噪声都映射到合理动作 | 上限受 BC 策略支撑集限制 |
| 读出表征 | RL Token | 低维、任务相关 | 不动 VLA 主干，分钟级见效 | 需要事先改造 VLA 暴露该 token |
| 语言 prompt | SARL | 离散、语义化 | 探索结构化，可组合已有技能解决新任务 | 只能唤起已有技能，不能学新的低层技能 |

趋势很清楚：**空间越小、越贴近预训练先验，RL 越高效**；代价是可改进的范围被先验限制。个人推断：实际系统会分层——SARL 式的语义层 RL 决定"用哪个技能"，RL Token / DSRL 式的低层 RL 精修"怎么执行"。

### 4.2 预训练—微调接口被拆成三个独立问题

- **微调时要不要带旧数据**（WSRL：不必，只需 warmup 重校准）。
- **微调后怎么不遗忘**（Parameter Merging：权重插值）。
- **预训练怎样才是好的初始化**（PostBC：建模后验而非点估计，保证动作覆盖）。

这三个问题在 LLM 领域各有对应（continual pretraining、model merging、SFT-for-RL），本组把它们逐一搬到机器人上并给出理论。

### 4.3 RL 与 generalist 的四种结合方式

1. RL 产生数据，蒸馏进 generalist（RLDG）。
2. RL 在 generalist 外部套一层（DSRL、RL Token）。
3. RL 全参数微调 generalist（OGPO）。
4. RL 进入 generalist 的预训练（1A 类别的 π\*0.6 / RECAP）。

四种方式在 2024–2026 年都被尝试，目前没有单一胜者。它们对"generalist 主干可否被修改"的假设不同，这可能取决于组织形态：学术组更倾向 1、2（黑盒、便宜），工业组有能力做 3、4。

### 4.4 奖励是下一块短板

HIL-SERL 依赖人工纠正与任务专用奖励；RL Token 的任务（插入、拧螺丝）成败易判定。要把 RL 后训练推广到开放任务，需要通用奖励：Success Visitation Matching 从本任务成败历史中学稠密奖励；1F 类别的 RoboReward 学通用 VLM 奖励模型；1D 类别的价值函数则直接在测试时引导。这三条线在 2026 年同时活跃，说明"奖励从哪里来"仍是开放问题。

---

## 5. 与其他类别的连接

- ← **1A**：π\*0.6 / RECAP 是 RL 进入基础模型的版本；RL Token、SARL 以 π 系列为改进对象。
- ↔ **1B**：ARLI 指出 RL 后训练大型 VLA 必须延迟感知；Q-chunking 是 RL 算法层面的分块。
- ↔ **1D**：DSRL / RL Token 是"训练时 RL 但不动主干"，QGF / V-GPS 是"测试时不训练"，两者是同一光谱的两端。
- ← **1F**：RoboReward、ViVa 提供奖励与价值来源。
- ← **1G**：WSRL、PostBC 的理论基础来自价值学习的稳定性研究。
- ↔ **1H**：SFT Memorizes / RL Generalizes 在 LLM 侧得到相同的"RL 后训练更泛化"结论；NLAC 在语言空间做 actor–critic 与 SARL 在 prompt 空间做 RL 互为镜像。

---

## 6. 与我的研究方向的连接

- **SARL 的"技能先验 + 语义层 RL"** 与我设想的"VLA 提出候选技能、world model 评估、value 排序"结构高度一致；区别在于 SARL 通过真实交互学 prompt 选择，而 skill-level world model 可以在想象中先筛掉明显不可行的技能，减少真实交互次数。
- **Success Visitation Matching** 的判别器本质是一个"进度估计器"；skill-level world model 预测的任务进度 \(y_{t+k}\) 可以作为同类的稠密信号，且在执行前就可用。
- **PostBC 的"后验建模保证覆盖"** 与 uncertainty-aware prediction 的思路同源：保留分布而非点估计，为后续决策留出探索空间。
- **RL Token 的紧凑读出表征**提示：world model 也可以只消费 VLA 的一个低维接口 token，而不需要访问完整的视觉特征——这大幅降低模块化集成的成本。

---

## 7. 待追踪问题

- 语义层 RL（SARL）与低层 RL（RL Token）能否在同一系统中叠加？
- OGPO 的全参数微调在 π 级别的 VLA（数十亿参数）上是否可行？
- RL Token 需要"改造 VLA 暴露 token"，这会否成为基础模型发布的标准接口？
- Success Visitation Matching 与 RoboReward 这类学到的奖励，在长时域开放任务上的可靠性如何？
- HIL-SERL 式的人工纠正在 VLA 时代的角色：是数据来源（RECAP 的专家干预），还是会被自动奖励取代？
