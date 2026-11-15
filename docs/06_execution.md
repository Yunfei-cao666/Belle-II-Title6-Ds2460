# 逐步执行计划

> 这一章把“大计划”拆成可执行的小阶段。  
> 原则：**先控制道，再信号；先产额，再振幅；每一步都有交付物和 gate。**

> **2026-11-15 更新**：根据黄仪伟/杨昊中的建议，先走**简化路线**——直接重建 continuum $e^+e^-\to c\bar c$ 中的 $D_{sJ}$，复现 Belle 2003 的 $\Delta M$ 分析（见 `docs/10_dsj_analysis.md`）。  
> 完整 B 衰变/Dalitz 路线保留为长期目标。

---

## 0. 总览

| 阶段 | 时间 | 目标 | 交付物 | Gate |
|---|---|---|---|---|
| 0 准备 | 2 周 | 环境、账号、文档 | 能跑官方示例 | `basf2` 能启动 |
| 1 控制道 | 6 周 | $B\to\bar D^*D_s$ | 质量峰 + cutflow | 控制道干净 |
| 2 信号 ntuple | 3 个月 | $D_{s1}\to D_s\pi\pi$ | ntuple + BDT | MC 有峰 |
| 3 产额/分支比 | 6 个月 | 信号产额 | 拟合图 + $R$ | 显著度/上限 |
| 4 振幅 | 9–12 个月 | Dalitz | fit fractions | closure 通过 |
| 5 系统误差/发表 | 12–18 个月 | 论文 | draft | review 通过 |

---

## 0.1 先做简化路线（2–4 周）

在进入 B 衰变重建前，先做：

- [ ] 找 Belle II 的 continuum/charm skim；
- [ ] 复现 $D_s^+\to\phi\pi^+$ 质量峰；
- [ ] 加 $\pi^0$、$\gamma$、$D_s^{*+}$；
- [ ] 画 $\Delta M(D_s^+\pi^0)$、$\Delta M(D_s^{*+}\pi^0)$、$\Delta M(D_s^+\gamma)$、$\Delta M(D_s^+\pi^+\pi^-)$；
- [ ] 用 Gaussian + polynomial 拟合；
- [ ] 先看 $D_{sJ}(2317)$，再看 $D_{sJ}(2457)$。

参考：`docs/10_dsj_analysis.md`。

---

## 1. 阶段 0：准备（第 0–2 周）

**目标**：能跑通 basf2，知道数据在哪里。

- [ ] 加入 Belle II 合作组，拿到 KEKCC 账号；
- [ ] 配环境：

  ```bash
  ssh <user>@kekcc.kek.jp
  source /cvmfs/belle.kek.jp/setup/default/setup.sh
  b2setup
  b2help-recommendation
  ```

- [ ] 跑官方第一个 steering file；
- [ ] 读 Online Book 的 Analysis / ROE / CS / Vertex / b2luigi；
- [ ] 在 GitHub 建公开仓库 `Belle-II-Title6-Ds2460`；
- [ ] 确认只使用公开资料，不把内部数据/他人代码放公开库。

**Gate**：`basf2` 能启动；官方示例能跑；仓库能 push。

---

## 2. 阶段 1：控制道（第 2–6 周）

**目标**：跑通 $B^+\to\bar D^{*0}D_s^+$，$D_s^+\to\phi\pi^+$。

这个道和信号共享：

- $D_s\to\phi\pi$；
- $D^0\to K\pi$；
- $D^{*0}\to D^0\gamma$；
- B 顶点、$M_{\rm bc}$、$\Delta E$；
- ROE/CS。

但没有 $D_{s1}\to D_s\pi\pi$，所以是完美的“重建验证”。

任务：

- [ ] 用 1 个 uDST 文件、`basf2 -n 1000` 跑通；
- [ ] 画 $D_s$、$D^0$、$D^*$、$M_{\rm bc}$、$\Delta E$；
- [ ] 写 cutflow 表；
- [ ] 数据/MC 对比；
- [ ] 多候选率；
- [ ] 写 1 页控制道报告。

**Gate**：控制道在数据和 MC 中都有干净峰；cutflow 合理。

---

## 3. 阶段 2：信号 ntuple（第 6–12 周）

**目标**：跑通 $D_{s1}\to D_s\pi\pi$，输出 ntuple。

任务：

- [ ] 用 `code/steering/steering_ntuple.py` 骨架；
- [ ] 先 100 个事件，检查 log；
- [ ] 用 `b2luigi` 批量跑 skim 文件；
- [ ] 画 $D_{s1}$、$m(\pi\pi)$、$M_{\rm bc}$、$\Delta E$；
- [ ] 训练第一版 FastBDT；
- [ ] 画 ROC、overtraining、变量重要度；
- [ ] 在数据 sideband 上看 BDT 分布；
- [ ] 估计信号产额。

**Gate**：MC 中能看到 $D_{s1}$ 峰；数据 sideband 干净；BDT 不 sculpt $m(\pi\pi)$。

---

## 4. 阶段 3：产额与分支比（第 3–6 个月）

任务：

- [ ] 冻结选择（除 BDT cut）；
- [ ] $m(D_s\pi\pi)$ 一维拟合；
- [ ] $M_{\rm bc}$ vs $\Delta E$ 二维拟合；
- [ ] $B^+$ / $B^0$ 同时拟合；
- [ ] 计算相对分支比 $R$；
- [ ] first unblinding；
- [ ] 写 2 页 internal note。

**Gate**：信号显著度 $>3\sigma$，或给出上限；系统误差表初版。

---

## 5. 阶段 4：振幅分析（第 6–12 个月）

任务：

- [ ] 用 PHSP MC 做效率图；
- [ ] 实现 isobar 模型；
- [ ] 先拟合 MC，做 closure test；
- [ ] 拟合数据 sideband 本底；
- [ ] 拟合 $f_0(500)+f_0(980)+f_2(1270)$ 基线；
- [ ] 加 K-matrix、$T_{c\bar s}$；
- [ ] 模型比较、fit fraction、系统误差；
- [ ] 写 paper draft。

**Gate**：closure test 通过；fit fraction 稳定；系统误差可控。

---

## 6. 阶段 5：发表（第 12–18 个月）

- [ ] 内部 review（ARC/物理组）；
- [ ] 合作组 review；
- [ ] 投稿。

---

## 7. 团队分工

| 角色 | 负责 | 第一件交付物 |
|---|---|---|
| 分析负责人 | 物理目标、cut 策略、review、论文 | 2 页 analysis proposal |
| 重建/选择 | $D_s,D^*,D_{s1},B$ 重建、cutflow、控制样本 | 各粒子质量峰 + cutflow |
| 本底/MVA | ROE、CS、FastBDT | BDT ROC、data/MC |
| 拟合/振幅 | RooFit、Dalitz、误差 | 产额拟合图、fit fraction |
| 计算/b2luigi | 数据定位、批量任务、grid | 可复现 workflow |
| 系统误差/论文 | PID、tracking、$\gamma/\pi^0$、模型误差 | 系统误差表 |

---

## 8. 第一周任务（可直接发群里）

- **Day 1**：登录 KEKCC，`source .../setup.sh`，`b2setup`，跑官方第一个 steering file。
- **Day 2**：读 `B0toDs1D`、`BtoDsDsst_Kpi_KK` 的源码；画出 B 拓扑。
- **Day 3**：用 100 个 uDST 重建 $D_s\to\phi\pi$，画质量峰。
- **Day 4**：重建 $D^0\to K\pi$ 和 $D^{*0}\to D^0\gamma$，画 $\Delta M$。
- **Day 5**：重建 $B\to\bar D^*D_s$ 控制道，画 $M_{\rm bc}$、$\Delta E$；写 1 页 cutflow。
- **周末**：组会报告“控制道是否干净；下一步最大风险是什么”。

---

## 9. 里程碑与决策点

| 时间 | 里程碑 | 决策 |
|---|---|---|
| M0（2 周） | 环境跑通 | 能否用 KEKCC？ |
| M1（6 周） | 控制道 | 重建是否可靠？ |
| M2（3 月） | 信号 ntuple | 是否有足够信号？ |
| M3（6 月） | 产额/分支比 | 是否继续振幅？ |
| M4（9 月） | 振幅基线 | 模型是否收敛？ |
| M5（12 月） | 系统误差 | 是否达到发表精度？ |
| M6（18 月） | 论文 | — |

---

## 10. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 信号产额低 | 无法做振幅 | 先做产额/上限；扩大 $D_s$ 道；等更多数据 |
| $B\bar B$ 本底模型不确定 | 产额偏差 | sideband + MC 双估计 |
| 振幅模型依赖 | 物理结论不稳 | 模型无关矩 + 多模型 + closure |
| BDT 系统误差 | 效率不确定 | 变 cut、data/MC 重加权 |
| 软件版本变化 | 代码跑不动 | 固定 release/globaltag；记录版本 |
| 团队经验不足 | 进度慢 | 先控制道；每周 code review |

---

## 11. 阶段 gate 的“完成定义”

每个阶段不是“跑完代码”就结束，而是：

- 有可复现的 steering file；
- 有 cutflow；
- 有数据/MC 对比；
- 有 log/输出记录；
- 有 1 页总结；
- 通过组内 review。

没有这些，不要进入下一阶段。
