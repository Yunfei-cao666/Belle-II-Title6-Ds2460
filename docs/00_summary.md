# 2 页摘要：Belle II 上的 $D_{s1}(2460)^+\to D_s^+\pi^+\pi^-$

> **题目**：Title 6 — $D_{s1}(2460)\to D_s\pi\pi$  
> **参考**：LHCb, Science Bulletin 70 (2025) 1432–1444, [DOI](https://doi.org/10.1016/j.scib.2025.02.025)  
> **状态**：方案与代码骨架，尚未在 KEKCC 上完整验证。

---

## 1. 物理目标

$D_{s1}(2460)^+$ 是 charmed-strange 的 $P$-波态，$J^P=1^+$，质量约 $2459.5\ \mathrm{MeV}$，宽度 $<3.5\ \mathrm{MeV}$。它和 $D_{s0}^*(2317)^+$ 的质量都明显低于朴素夸克模型预期，可能涉及：

- 常规 $c\bar s$ 态与 $D^{(*)}K$ 耦合道；
- $D^*K$ 强子分子态；
- 四夸克态或混合态；
- 与 $T_{c\bar s}(2900)$ 等奇异四夸克候选有关。

LHCb 在 $9\ \mathrm{fb}^{-1}$ 的 $pp$ 数据中，用三个 B 衰变通道得到约 800 个 $D_{s1}\to D_s\pi\pi$ 信号事例，并在 $m(\pi\pi)$ 谱中看到明显的**双峰结构**。常规 $\pi\pi$ 共振拟合需要很大的 $f_0(980)$、$f_2(1270)$ 贡献，但 $D_{s1}\to D_s\pi\pi$ 的 $\pi\pi$ 质量上限只有约 492 MeV，这些峰远在运动学边界之外。因此，LHCb 也讨论了非共振、三角奇点、$T_{c\bar s}$ 等解释。

Belle II 的价值：**独立实验、干净环境、可全重建、可分 $B^+/B^0$、系统误差不同**。我们不一定能立刻超过 LHCb 的统计量，但可以独立检验双峰结构和振幅模型。

---

## 2. 在 Belle II 怎么产生 $D_{s1}$

在 $\Upsilon(4S)$ 数据中，$D_{s1}(2460)$ 主要来自 B 介子衰变，不能直接“$e^+e^-\to D_{s1}$”。基线通道：

$$
\begin{aligned}
B^+ &\to \bar D^{*0}D_{s1}^+, &
\bar D^{*0}&\to \bar D^0\gamma,\quad \bar D^0\to K^+\pi^-,\\
B^0 &\to D^{*-}D_{s1}^+,\quad &D^{*-}&\to \bar D^0\pi^-,\\
B^0 &\to D^-D_{s1}^+,\quad &D^-&\to K^+\pi^-\pi^-.
\end{aligned}
$$

信号衰变：

$$
D_{s1}^+\to D_s^+\pi^+\pi^-,\qquad
D_s^+\to \phi\pi^+,\quad \phi\to K^+K^-.
$$

基线只做 $D_s\to\phi\pi$；$D_s\to K^{*0}K$、$K_S^0K$ 作为交叉检验，不要一上来混在一起。

---

## 3. 数据与 MC

- 2026 年中 Belle II 已积累约 $757\ \mathrm{fb}^{-1}$ 的 $\Upsilon(4S)$ 数据；本方案按 $0.75\ \mathrm{ab}^{-1}$ 保守估算，$1\ \mathrm{ab}^{-1}\approx 10^9\ B\bar B$。
- 数据：优先用官方 **hadronic B skim** 的 uDST/mDST；具体 skim 名称以 campaign 的 DataSetDBS 为准。
- **不要直接用 `B0toDs1D` skim（14160200）**：它重建的是 $D_{s1}\to D_s^*\pi^0$、$D_s^*\to D_s\gamma$，不会保留 $D_{s1}\to D_s\pi\pi$。它可以作为代码模板，但不能当数据样本。
- MC：signal（$B^+\to\bar D^{*0}D_{s1}^+$、$B^0\to D^{*-}D_{s1}^+$、$B^0\to D^-D_{s1}^+$）、generic $B\bar B$、generic $q\bar q$、$\tau\tau$。
- 做振幅分析时，效率图要用**平 Dalitz（PHSP）**信号 MC，不能用共振模型生成，否则效率有偏。

---

## 4. 重建与选择

核心模块：

- `ParticleCombiner` / `reconstructDecay`
- `TreeFitter` / `vertex.treeFit`
- `BestCandidateSelection` / `rankByHighest`
- `VariablesToNtuple`
- `RestOfEventBuilder`、`ContinuumSuppressionBuilder`
- `MVAExpert`

初始 cut（必须用 MC 优化，不要照抄）：

| 对象 | 初始 cut |
|---|---|
| $D_s$ | $1.93<M<2.00\ \mathrm{GeV}$，$p^*>1.2\ \mathrm{GeV}$，$\chi^2_{\rm prob}>0.001$，位移显著性 $>2$ |
| $D^0$ | $1.83<M<1.90\ \mathrm{GeV}$，$p^*>1.0\ \mathrm{GeV}$，$\chi^2_{\rm prob}>0.001$ |
| $D^{*0}$ | $0.130<M(D^{*0})-M(D^0)<0.155\ \mathrm{GeV}$ |
| $D^{*-}$ | $0.140<M(D^{*-})-M(D^0)<0.150\ \mathrm{GeV}$ |
| $D_{s1}$ | $2.42<M<2.50\ \mathrm{GeV}$，$p^*>1.0\ \mathrm{GeV}$，$\chi^2_{\rm prob}>0.001$ |
| B | $M_{\rm bc}>5.20\ \mathrm{GeV}$，$|\Delta E|<0.10\ \mathrm{GeV}$，$\chi^2_{\rm prob}>0.001$ |

$M_{\rm bc}=\sqrt{E_{\rm beam}^2-|\vec p_B|^2}$，$\Delta E=E_B-E_{\rm beam}$。信号在 $M_{\rm bc}\approx5.28\ \mathrm{GeV}$、$\Delta E\approx0$。

---

## 5. 本底与 MVA

主要本底：

- 连续本底 $e^+e^-\to q\bar q$（尤其 $c\bar c$）；
- $B\to\bar D^{(*)}D_s^{(*)}\pi$、非共振 $D_s\pi\pi$；
- $D_{s1}(2536)$ 误重建；
- $D_s$ / $D^0$ 组合本底；
- $B^+\leftrightarrow B^0$ 交叉。

工具：

1. `buildRestOfEvent` + `buildContinuumSuppression`；
2. 变量：$R_2$、`cosTBTO`、thrust、Fox-Wolfram、CLEO cones、KSFW、`nTracks`；
3. FastBDT：`basf2_mva_merge_mc` → `basf2_mva_teacher` → `MVAExpert`；
4. 训练变量**不要**放 $m(\pi\pi)$、$D_{s1}$ 质量、$M_{\rm bc}$、$\Delta E$，避免 sculpting；
5. FEI 可选，不作为基线。

---

## 6. 拟合

### 产额拟合

- 先做 $m(D_s\pi\pi)$ 一维拟合：Voigtian（BW $\otimes$ Gaussian）+ 指数本底；
- 再做 $M_{\rm bc}$ vs $\Delta E$ 二维拟合：Gaussian/Crystal Ball + ARGUS/指数；
- 用 RooFit；$B^+$ 和 $B^0$ 分开或同时拟合。

### Dalitz 振幅

$$
m^2(\pi^+\pi^-),\qquad m^2(D_s^+\pi^-)
$$

以及 helicity 角 $\theta_1,\phi_1$。isobar 模型：

$$
\mathcal A(s_{12},s_{13})=\sum_i c_i A_i(s_{12})Y_{1m_i}(\theta_1,\phi_1).
$$

模型集合：

1. $f_0(500)+f_0(980)+f_2(1270)$（复现 LHCb 的常规拟合）；
2. K-matrix $\pi\pi$ S-wave；
3. 加入 $T_{c\bar s}$（标量、同位旋 1）；
4. 模型无关矩 $\langle Y_{lm}\rangle(m_{\pi\pi})$。

> 不要只报一个 fit fraction；要同时给模型比较、干涉项、系统误差和 $B^+/B^0$ 一致性。

---

## 7. 执行计划

| 阶段 | 时间 | 交付物 |
|---|---|---|
| 0 准备 | 2 周 | 环境、账号、控制道 |
| 1 控制道 | 6 周 | $B\to\bar D^*D_s$ 质量峰 + cutflow |
| 2 信号 ntuple | 3 个月 | $D_{s1}$ 峰、BDT、data/MC |
| 3 产额/分支比 | 6 个月 | 拟合图、相对分支比 |
| 4 振幅 | 9–12 个月 | Dalitz 图、fit fractions |
| 5 系统误差/发表 | 12–18 个月 | 系统误差表、paper draft |

第一周只做一件事：在 KEKCC 上跑通 $B^+\to\bar D^{*0}D_s^+$，$D_s^+\to\phi\pi^+$ 的控制道。

---

## 8. 主要风险

| 风险 | 缓解 |
|---|---|
| 信号产额低 | 先做产额/上限；扩大 $D_s$ 道；等更多数据 |
| $B\bar B$ 本底模型不确定 | sideband + MC 双估计 |
| 振幅模型依赖 | 模型无关矩 + 多模型 + closure test |
| BDT 系统误差 | 变 cut、data/MC 重加权 |
| 软件版本变化 | 固定 release/globaltag；记录版本 |
| 公开库合规 | 只放公开资料；不碰私人库/token |

---

## 9. 一句话结论

**这是一份“先跑通控制道、再做信号、先测产额、再做振幅”的分阶段方案；当前版本是可执行的骨架，不是已经完成的分析结果。**
