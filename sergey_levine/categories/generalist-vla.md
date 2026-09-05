# 1A · 通用机器人基础模型（Generalist policy / VLA）

> 所属报告：[Sergey Levine 近期研究趋势分析](../Sergey_Levine.md) · 类别 ID：`generalist-vla` · 论文数：13（2024: 5 / 2025: 7 / 2026: 1）  
> 所有链接均为 arXiv 摘要页，已通过 `verify_links.py` 核对。带 † 为 Physical Intelligence 团队大型系统工作。

---

## 1. 这个方向在研究什么

**VLA（Vision-Language-Action model）** 是一种把摄像头图像和自然语言指令直接映射为机器人动作的神经网络。它通常以一个在互联网图文数据上预训练好的视觉语言模型（VLM，如 PaliGemma、Llama + SigLIP）为主干，再接一个"动作头"输出连续的关节 / 末端控制量。"Generalist policy"（通用策略）是更宽的说法：一个策略控制很多机器人、做很多任务，不一定含语言。

这一类论文回答的问题包括：

1. **数据从哪里来**：多机器人数据集（Open X-Embodiment、DROID）、网络图文数据、人类视频，能否混在一起训练一个策略？
2. **动作如何表示**：把连续动作离散成 token 让 Transformer 自回归预测（OpenVLA、FAST），还是用 diffusion / flow-matching 直接生成连续动作块（π0）？
3. **如何不破坏预训练知识**：加一个随机初始化的动作头会不会让 VLM 的语义能力退化（Knowledge Insulation）？
4. **泛化到什么程度**：新物体、新房间、没见过的机器人（π0.5、π0.7、CrossFormer）？
5. **能否从经验中学习**：预训练之后，模型能否用自己部署时收集的数据继续变好（π\*0.6）？

**为什么重要**：如果这条路走得通，机器人学习就能像语言模型那样进入"预训练 + 微调"的范式——不用为每个任务从零训练，而是下载一个基础模型、用少量数据适配。Levine 组（与 Physical Intelligence）的 π 系列是这条路线上迭代最快、最完整的公开谱系。

---

## 2. 论文逐篇分析（按时间）

### 2024

**[DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset](https://arxiv.org/abs/2403.12945)**（2024-03，101 位作者）  
76k 条示范轨迹 / 350 小时，覆盖 564 个场景、84 个任务，由 50 位采集者在北美、亚洲、欧洲用 12 个月采集。摘要指出：此前即便最通用的策略也主要在少数环境上训练，场景与任务多样性有限；用 DROID 训练能提升策略性能与泛化。**意义**：它把"数据多样性"而非"数据量"确立为 generalist 的瓶颈，后续 RoboArena、RoboReward 都建在 DROID 硬件平台与数据上。

**[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)**（2024-05）  
在 Open X-Embodiment 的 800k 轨迹上训练的大型 Transformer 策略，可用语言或目标图像指令，在消费级 GPU 上几小时内微调到有新传感器输入和新动作空间的机器人。在 9 个机器人平台上验证。**意义**：Octo 的关键词是"易于微调的初始化"，它确立了 generalist 的产品形态——不是一个终态模型，而是一个可微调的起点。

**[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)**（2024-06）  
7B 参数的开源 VLA：Llama 2 语言主干 + DINOv2 与 SigLIP 融合的视觉编码器，在 970k 真实示范上训练。在 29 个任务上比 55B 的闭源 RT-2-X 绝对成功率高 16.5%，参数少 7 倍；微调后比从零训练的 Diffusion Policy 高 20.4%；支持 LoRA 微调和量化部署。**意义**：证明了"更小 + 更好的视觉特征 + 更多样数据"胜过"更大"，并且让 VLA 研究第一次对学术界完全开放——后续 ECoT、V-GPS 等都以 OpenVLA 为基座。

**[CrossFormer: Scaling Cross-Embodied Learning](https://arxiv.org/abs/2408.11812)**（2024-08）  
一套 Transformer 权重控制 20 种 embodiment（单臂、双臂、轮式、四旋翼、四足），900K 轨迹，**不需要手工对齐观测或动作空间**。匹配每种机器人的专用策略，并显著超过此前的跨 embodiment 方法。**意义**：回答"一个网络能否跨越操作、导航、运动、飞行"，为 π0.7 的零样本跨 embodiment 埋下伏笔。

**[π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164)** †（2024-10）  
在预训练 VLM 之上加 **flow-matching** 架构生成连续动作，用多种灵巧机器人平台（单臂、双臂、移动操作）的大规模数据训练。评估三方面：预训练后零样本执行、跟随人类或高层 VLM 策略的语言指令、微调获取新技能；任务包括叠衣、清桌、装箱。**意义**：这是 VLA 从"离散 token 自回归"转向"连续生成式动作头"的标志，也是 Physical Intelligence 整条 π 谱系的起点。

### 2025

**[FuSe (Beyond Sight): Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding](https://arxiv.org/abs/2501.04693)**（2025-01）  
问题：generalist 只用视觉 + 本体感知，但伸手进袋子时视觉被遮挡，应该靠触觉和声音。FuSe 用自然语言作为跨模态的共同 grounding，结合多模态对比损失与"传感器 grounded 的语言生成"损失，让 generalist 微调到触觉、音频等缺乏大数据的模态。零样本完成需要跨模态联合推理的任务；同一配方对 diffusion generalist 和大型 VLA 都适用；成功率比所有基线高 20% 以上。**意义**：语言不只是指令接口，也可以是把异构传感器"接入" generalist 的胶水。

**[FAST: Efficient Action Tokenization for VLA Models](https://arxiv.org/abs/2501.09747)** †（2025-01）  
发现按维度、按时间步分箱的动作 tokenization 在高频灵巧数据上表现很差；提出基于离散余弦变换（DCT）的压缩式 tokenization。发布在 1M 真实轨迹上训练的通用 tokenizer FAST+。与 π0 结合可扩展到 10k 小时数据，匹配 diffusion VLA 的性能，训练时间最多减少 5 倍。**意义**：说明自回归路线并没有被 flow 路线淘汰——瓶颈在动作表示，而不在自回归本身。

**[π0.5: a VLA with Open-World Generalization](https://arxiv.org/abs/2504.16054)** †（2025-04）  
基于 π0，用**异构任务联合训练**：多机器人数据、高层语义子任务预测、网络数据等；训练样本是混合多模态的（图像观测、语言指令、物体检测、语义子任务预测、低层动作在同一序列中）。实验表明这种知识迁移对泛化是必需的，并**首次**展示端到端学习系统能在**完全没见过的家庭**里完成清理厨房 / 卧室这类长时域灵巧任务。**意义**：π0.5 是本报告 Scholar 引用最高的近期论文（1352 次）。它把"高层语义预测"直接编进策略的训练目标，模糊了 VLA 与层级系统的边界。

**[Knowledge Insulating VLA Models: Train Fast, Run Fast, Generalize Better](https://arxiv.org/abs/2505.23705)** †（2025-05）  
研究一个被忽视的问题：给 VLM 加一个随机初始化的 diffusion / flow 动作专家，会不会破坏 VLM 的语义知识、拖慢训练？结论是**朴素地加入会显著损害训练速度与知识迁移**；论文系统分析设计选择，并提出在 VLA 训练中"隔离"VLM 主干的技术。**意义**：它解释了为什么 π0.5 要同时保留离散 token 预测和连续动作头——离散路径负责保护语义知识，连续路径负责实时控制。

**[OmniVLA: An Omni-Modal VLA for Robot Navigation](https://arxiv.org/abs/2509.19480)**（2025-09）  
导航策略通常只支持一种目标模态。OmniVLA 用高容量 VLA 主干，通过**随机模态融合**同时训练 2D 位姿、第一视角图像、自然语言三种目标及其组合。结果：对未见环境泛化强、对模态缺失鲁棒、能跟随新语言指令，超过各模态的专用基线。**意义**：把 VLA 思路推广到导航，并把"目标表示的多样性"作为扩大可用数据集的手段。

**[π\*0.6: a VLA That Learns From Experience](https://arxiv.org/abs/2511.14759)** †（2025-11，56 位作者）  
提出 RECAP（RL with Experience and Corrections via Advantage-conditioned Policies）：先用**离线 RL** 预训练一个 generalist VLA（π\*0.6），再通过机器人上的数据采集特化到下游任务。可纳入异构数据：示范、on-policy 采集数据、自主执行期间的专家遥操作干预。成果：在真实家庭叠衣、可靠装箱、用专业咖啡机做咖啡；在最难任务上吞吐量翻倍以上、失败率约减半。**意义**：这是 π 系列第一次把 RL 放进基础模型本身（而非作为下游微调），也是 1C 类别"RL 后训练"与 1A 类别的交汇点。

**[Emergence of Human to Robot Transfer in VLA Models](https://arxiv.org/abs/2512.22414)**（2025-12）  
人类视频多样且易得，但人与机器人之间的映射难以手工建立。论文提出简单的联合训练配方，发现**当 VLA 在足够多的场景、任务和 embodiment 上预训练后，人→机器人迁移会涌现**；分析认为原因是多样预训练产生了 embodiment 无关的表征。在只在人类数据中出现的泛化设置上，性能几乎翻倍。**意义**：为"用人类视频扩大机器人数据"提供了一个不需要手工对齐的路线，其前提是 1A 类别中其他工作已经把机器人数据多样性做上去。

### 2026

**[π0.7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](https://arxiv.org/abs/2604.15483)** †（2026-04，88 位作者）  
核心思想：训练时使用**多样化的上下文条件化**。prompt 中不只有"做什么"的语言指令，还有描述"怎么做、做得多好"的多模态信息——任务表现元数据、子目标图像等。这使模型能利用非常多样的数据：示范、可能次优的自主数据（包括失败）、非机器人数据。能力：在未见环境跟随多样指令（含多阶段厨房电器任务）、零样本跨 embodiment（从未见过叠衣任务的机器人能叠衣）、开箱即用操作咖啡机的水平**匹配专门 RL 微调的模型**。**意义**：π0.7 把"可操控性（steerability）"写进标题——通用性不再只由参数承载，而由 prompt 中的多模态条件共同决定。它也吸收了 1C 类别（用表现标签学失败数据）和 1E 类别（子目标图像作为接口）的成果。

---

## 3. 演进脉络

```
2024-03  DROID           数据多样性是瓶颈
2024-05  Octo            开源 generalist，易微调
2024-06  OpenVLA         7B 开源 VLA，小而强
2024-08  CrossFormer     一套权重跨 20 种 embodiment
2024-10  π0              VLM + flow 动作头                       ← 架构转折
2025-01  FAST / FuSe     动作 tokenization；异构传感器接入
2025-04  π0.5            异构联合训练，未见家庭泛化               ← 泛化里程碑
2025-05  Knowledge Ins.  加动作头如何不破坏 VLM 知识
2025-09  OmniVLA         多模态目标的导航 VLA
2025-11  π*0.6 / RECAP   离线 RL 预训练 + 部署经验                ← RL 进入基础模型
2025-12  Human→Robot     人类视频迁移随规模涌现
2026-04  π0.7            多样上下文条件化 → 可操控                ← 接口转折
```

三个转折点：**架构**（π0：离散 → 连续生成）、**泛化**（π0.5：实验室 → 未见家庭）、**接口**（π0.7：指令 → 多模态条件）。夹在中间的 FAST、Knowledge Insulation、FuSe 是为这些转折清障的"基础设施论文"。

---

## 4. 深度分析

### 4.1 离散 token 与连续生成的路线之争并未结束

π0 用 flow matching，看似宣告自回归路线失败；但三个月后的 FAST 表明，自回归 VLA 失败的原因是 tokenization 太粗糙，换成 DCT 压缩后能匹配 diffusion VLA 且训练快 5 倍。Knowledge Insulation 又指出连续动作头会损害 VLM 知识迁移。π0.5 的最终方案是**两者共存**：离散 token 路径承担语义与知识保护，连续路径承担实时控制。个人推断：未来 VLA 的动作表示会是"混合的"，而不是二选一。

### 4.2 "泛化"的定义在三年内被不断抬高

- 2024（Octo、OpenVLA）：泛化 = 微调到新机器人 / 新任务后表现好。
- 2025（π0.5）：泛化 = 零样本进入未见家庭完成长时域任务。
- 2026（π0.7）：泛化 = 零样本跨 embodiment 完成从未在该机器人上见过的任务，且性能接近专门 RL 微调的模型。

每一次抬高都伴随数据源的扩展：机器人数据 → + 网络数据与语义预测 → + 失败数据与非机器人数据。

### 4.3 数据的"质量"从筛选对象变成条件变量

早期 generalist 只用成功示范。π\*0.6 通过 advantage conditioning 吃下 on-policy 数据与专家干预；π0.7 直接把"任务表现元数据"放进 prompt，把次优与失败数据也变成训练信号。这意味着**数据质量不再是过滤标准，而是模型的一个输入维度**——训练时告诉模型这条数据好不好，推理时要求它按"好"的方式做。

### 4.4 大团队化

π0（24 人）→ π0.5（36 人）→ π\*0.6（56 人）→ π0.7（88 人）。作者规模的增长说明基础模型的构建已经是工程组织问题，学术实验室能贡献的位置在于：动作表示（FAST）、知识保护（Knowledge Insulation）、数据扩展（Human→Robot）、异构传感器（FuSe）这类"配件"研究，以及 1B–1G 类别中围绕基础模型的改进方法。

---

## 5. 与其他类别的连接

- → **1B 动作分块与实时执行**：π0 的 flow 动作块直接引出 RTC 系列的延迟问题。
- → **1C RL 后训练**：π\*0.6 / RECAP 是两类的交汇点；RL Token、SARL 都以 π 系列为被改进对象。
- → **1E 推理与层级**：π0.5 的语义子任务预测、π0.7 的子目标图像条件，与 Hi Robot、Steerable Policies 是同一问题的两端。
- → **1F 评估**：DROID 平台是 RoboArena、RoboReward 的基础；SC3-Eval 评估的正是这类 VLA。

---

## 6. 与我的研究方向的连接

- π0.7 把**子目标图像**作为条件接口，与 skill-level world model 预测"技能执行后的状态"天然对接：world model 的预测可直接作为 π0.7 类模型的子目标条件输入。
- Knowledge Insulation 提示：在 VLA 与低层控制器之间插入任何新模块（包括 world model）时，都要关心它是否破坏主干的预训练知识；模块化（不反传到主干）可能比端到端更稳妥。
- Human→Robot Transfer 的"embodiment 无关表征随规模涌现"结论，对 physics-grounded human-motion prediction 有直接意义：人类运动数据可以成为 humanoid 策略预训练的一部分，而映射不必手工设计。

---

## 7. 待追踪问题

- π0.7 之后是否会把 RL Token / SARL 式的部署后 RL 直接融入基础模型发布？
- 混合动作表示（离散 + 连续）是否会成为标准，还是某一路线最终胜出？
- 人类视频在 π 系列预训练中占比多少、带来多少泛化增益？
- 88 人规模的系统论文之后，学术界在 1A 类别的贡献空间会收窄到哪些"配件"？
