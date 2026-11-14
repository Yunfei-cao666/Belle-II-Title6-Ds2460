# 数据生产、Skim 与 MC

> 这一章回答：数据从哪里来、用什么格式、选哪个 skim、MC 怎么准备。  
> 原则：**先确认数据和 skim，再写重建代码**；不要拿一个不知道版本的样本直接跑。

---

## 1. Belle II 数据生产的基本概念

Belle II 的数据不是每个分析者从 raw data 开始重建，而是由合作组集中生产：

| 层级 | 内容 | 谁生产 | 分析者怎么用 |
|---|---|---|---|
| raw | 探测器原始数据 | 数据获取 | 一般不直接碰 |
| mdst | 重建后的 tracks、ECL clusters、KLM、V0 等 | 集中 production | 用 `RootInput` / `inputMdstList` 读 |
| uDST | 在 mdst 上预置 Particle、顶点、ROE/CS 等信息 | 集中 production / skim | 推荐，分析更快 |
| ntuple | 你自己选的变量 | 你的 steering file | RooFit / pandas / uproot |

> **不要自己重跑 detector reconstruction**，除非你是做重建/校准的专家。物理分析从 mdst/uDST 开始。

### 1.1 `mdst` 和 `uDST` 的区别

- **mdst**：更底层，包含 track、cluster、V0 等；适合调试和查重建问题。
- **uDST**：在 mdst 基础上加了 Particle 对象、顶点、ROE/CS 等信息；文件更小、分析更快。
- 两者都可以用：

  ```python
  import modularAnalysis as ma
  ma.inputMdstList(environmentType="default", filelist=[...], path=main)
  ```

- 不要假设 uDST 里一定有你要的 ParticleList；仍然要自己 `fillParticleList` / `reconstructDecay`。

---

## 2. 数据量级

2026 年中 Belle II 已积累约 $757\ \mathrm{fb}^{-1}$ 的 $\Upsilon(4S)$ 数据。按 $0.75\ \mathrm{ab}^{-1}$ 保守估算：

$$
N_{B\bar B}\approx \mathcal L\times \sigma_{b\bar b}
\approx 0.75\ \mathrm{ab}^{-1}\times 1.05\ \mathrm{nb}
\approx 8\times10^8.
$$

所以 $1\ \mathrm{ab}^{-1}\approx10^9$ 个 $B\bar B$ 对。这个量级是后面产额估算的基石。

> 具体亮度、run 范围、数据质量以官方 luminosity 页面和 Data Production 页面为准。

---

## 3. Skim 选择

### 3.1 通用 hadronic B skim

数据量太大，不可能每个分析都从全部 mdst 开始。官方 skim 把事例分成若干类，每类只保留一小部分。

对本课题：

- 推荐先用**通用 hadronic B skim**；
- 不同 campaign 的 skim 名称可能不同（例如 `Hadronic`、`BHadronic`、`SystematicsCombinedHadronic` 等）；
- **具体名称以 DataSetDBS / 生产页面的 campaign 为准**，不要照抄旧文档。

### 3.2 `B0toDs1D` skim：能参考，但不能直接用

官方有一个专门的 skim：

```text
Skim name: B0toDs1D
Skim LFN code: 14160200
Category: physics, hadronic B to charm
```

它重建的是：

$$
B^0\to D^-D_{s1}^+,\qquad
D_{s1}^+\to D_s^{*+}\pi^0,\qquad
D_s^{*+}\to D_s^+\gamma,
$$

并要求 $\pi^0$ 和 $\gamma$。  
**它不会保留 $D_{s1}\to D_s\pi\pi$**，因为末态没有 $\pi^0/\gamma$ 的要求。

所以：

- 它是很好的**代码模板**：可以看 B 顶点、$M_{\rm bc}$、$\Delta E$、$D_{s1}-D_s^*$ 质量差怎么写；
- 但它**不是**本课题的数据样本；
- 不要因为名字里有 `Ds1D` 就直接用它。

### 3.3 自定义 skim

长期最省 CPU 的方案是申请一个专用 skim，例如：

```text
B0toDs1D_DsPiPi
```

在 `B0toDs1D` 的基础上：

- 把 $D_{s1}\to D_s^*\pi^0$ 换成 $D_{s1}\to D_s\pi\pi$；
- 加 $B^+\to\bar D^{*0}D_{s1}^+$；
- 保留 $M_{\rm bc}$、$\Delta E$、$D_s$ 质量、$D^0$ 质量等基本 cut；
- 输出 uDST/mdst。

> 定制 skim 需要 skim 联系人/生产团队配合，不要自己改 central production。

---

## 4. MC 样本

### 4.1 需要哪些 MC

| 样本 | 用途 | 备注 |
|---|---|---|
| Signal MC $B^+\to\bar D^{*0}D_{s1}^+$ | 效率、分辨率、BDT 信号 | 产额拟合用物理模型 |
| Signal MC $B^0\to D^{*-}D_{s1}^+$ | 同上 | 注意 $D^{*-}\to\bar D^0\pi^-$ |
| Signal MC $B^0\to D^-D_{s1}^+$ | 同上 | 无 $D^*$ |
| Generic $B\bar B$ | $B\bar B$ 本底 | 至少 $B^+B^-$ 和 $B^0\bar B^0$ |
| Generic $q\bar q$（$u,d,s,c$） | 连续本底 | $c\bar c$ 最重要 |
| $\tau^+\tau^-$ | 低多重数本底 | 通常被 $n_{\rm tracks}$ 和 B 质量压低 |
| Flat Dalitz signal MC | 振幅效率图 | 用 PHSP，不用共振模型 |
| Control MC $B\to\bar D^*D_s$ | 验证重建/BDT | 已知分支比 |

### 4.2 Signal MC 的 EvtGen decay file 骨架

```text
Decay B+
1.0  anti-D*0  D_s1+;
Enddecay

Decay anti-D*0
1.0  anti-D0  gamma;
Enddecay

Decay D_s1+
1.0  D_s+  pi+  pi-  PHSP;
Enddecay

Decay D_s+
1.0  phi  pi+;
Enddecay

Decay phi
1.0  K+  K-;
Enddecay

End
```

> 粒子名和语法以你使用的 EvtGen 版本为准。  
> **做振幅分析时保留 `PHSP`**；否则效率图会带进生成模型，拟合有偏。

### 4.3 MC 生产注意事项

- 记录 **campaign、release、globaltag、decay file、生成时间**；
- 信号 MC 和 generic MC 要用同一套 reconstruction/globaltag；
- 做 data/MC 对比时，必须知道 MC 的 pile-up/beam background 设置；
- 不要用 private MC 混在 official MC 里而不记录。

---

## 5. 数据访问与工作流

### 5.1 本地/KEKCC

- 小样本：`basf2 -n 1000 steering.py`；
- 大样本：`b2luigi` + KEKCC batch；
- grid：`gbasf2` + proxy。

### 5.2 `b2luigi` 的任务流

```text
输入文件列表
  → Basf2PathTask（每个文件一个 job）
  → ntuple 输出
  → MergeTask（合并）
  → 拟合/画图
```

- 每个 job 输出唯一文件名；
- 把 `release`、`globaltag`、输入文件列表写入配置；
- 不要在一个 job 里跑全部数据。

### 5.3 数据记录

建议每个数据集记录：

```yaml
dataset: data_2024_run2
campaign: MC16
release: light-2604-jellyfish
globaltag: ...
skim: Hadronic
files: [...]
luminosity_fb: ...
notes: ...
```

没有这些信息，后面系统误差无法复现。

---

## 6. `b2luminosity`、校准与 Data Production

师兄提到的 `Data Production` 不只是“生产 mdst”，还包括：

- **b2luminosity**：亮度测量、run-by-run 亮度；
- **skim 的运行**：哪些 skim 在哪些 campaign 生产；
- **校准**：tracking、ECL、PID、beam background 等；
- **数据质量**：run 范围、坏 run、trigger 变化。

做分析时至少要确认：

- [ ] 数据是哪一年/哪个 campaign；
- [ ] 用的 skim 是否包含我的信号；
- [ ] 亮度误差是多少；
- [ ] tracking/PID/$\gamma$ 的推荐 globaltag 是什么；
- [ ] 是否有 data quality 问题。

> 这些信息通常在 Belle II 内部 Data Production / Performance 页面。**公开仓库只写公开入口和检索方法**，不复制内部页面内容。

---

## 7. 本章检查清单

- [ ] 数据和 MC 的 campaign/release/globaltag 已记录；
- [ ] 用的 skim 确认包含 $D_{s1}\to D_s\pi\pi$；
- [ ] 没有误用 `B0toDs1D`（它选的是 $D_s^*\pi^0$）；
- [ ] signal MC 的 $D_{s1}\to D_s\pi\pi$ 是 PHSP（做振幅时）；
- [ ] generic $B\bar B$ 和 $q\bar q$ 都有；
- [ ] 亮度、run 范围、数据质量已确认；
- [ ] 所有文件路径和版本写进了配置。

---

## 8. 参考入口

- Belle II 软件文档：<https://software.belle2.org/development/sphinx/>
- Skim 文档：<https://software.belle2.org/development/sphinx/skim/doc/>
- Online Book：<https://software.belle2.org/development/sphinx/online_book/>
- `b2luigi`：<https://b2luigi.belle2.org/>
- 数据生产/亮度/校准：以 Belle II 内部 Data Production 页面为准（公开仓库只记录入口，不复制内容）。
