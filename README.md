# Belle II Title 6: $D_{s1}(2460)^+ \to D_s^+ \pi^+\pi^-$

> **公开分析方案与可执行骨架**  
> 目标：在 Belle II 的 $\Upsilon(4S)\to B\bar B$ 数据中，重建
> $B\to \bar D^{(*)}D_{s1}(2460)$、$D_{s1}(2460)^+\to D_s^+\pi^+\pi^-$，
> 先测产额/分支比，再做 Dalitz 振幅分析。
>
> **状态**：方案与代码骨架（planning / skeleton）。代码尚未在 KEKCC 上完整验证，cut 为初始值，必须用 MC 优化。

---

## 1. 这个仓库是什么

这是一个**公开**的 Belle II 分析项目仓库，面向初次接触 Belle II 物理分析的同学。它包含：

- 一份面向师兄/导师的 **执行摘要**；
- 按主题拆分的详细方案（物理、数据生产、重建、本底、拟合、执行计划）；
- 给后续 agent 使用的 **basf2 文档检索协议**；
- 一套**可读、可改、待验证**的 basf2 代码骨架；
- 公开文献与官方文档的入口。

> **公开边界**：本仓库只包含公开文献、公开软件文档、官方示例，以及本项目自己写的文字和代码。  
> **不包含** Belle II 内部未公开数据、内部 ntuple、他人私有 GitLab 仓库、合作组内部会议材料、任何 token/密码。  
> 详见 [`docs/08_access_policy.md`](docs/08_access_policy.md)。

---

## 2. 先看哪几页

| 顺序 | 文件 | 给谁看 | 内容 |
|---|---|---|---|
| 1 | [`docs/00_summary.md`](docs/00_summary.md) | 师兄/导师 | 执行摘要：目标、数据、重建、本底、拟合、计划 |
| 2 | [`docs/01_physics.md`](docs/01_physics.md) | 全组 | 物理动机、LHCb 结果、Belle II 策略 |
| 3 | [`docs/02_data_production.md`](docs/02_data_production.md) | 做数据的人 | Data Production、skim、uDST/mDST、MC |
| 4 | [`docs/03_reconstruction.md`](docs/03_reconstruction.md) | 做重建的人 | $D_s,D^0,D^*,D_{s1},B$ 的模块与 cut |
| 5 | [`docs/04_background_mva.md`](docs/04_background_mva.md) | 做本底/MVA 的人 | ROE/CS、FastBDT、FEI、sideband |
| 6 | [`docs/05_fitting.md`](docs/05_fitting.md) | 做拟合的人 | RooFit 产额、Dalitz、效率、系统误差 |
| 7 | [`docs/06_execution.md`](docs/06_execution.md) | 全组 | 阶段、里程碑、分工、第一周任务 |
| 8 | [`docs/07_search_protocol.md`](docs/07_search_protocol.md) | 后续 agent | 如何查 basf2 wiki / Data Production / 历史版本 |
| 9 | [`docs/08_access_policy.md`](docs/08_access_policy.md) | 全组 | 公开资料边界、token 安全、引用规则 |
| 10 | [`docs/09_agent_brief.md`](docs/09_agent_brief.md) | 后续 agent | 写代码时的任务、约束、验收标准 |
| 11 | [`docs/SEARCH_LOG.md`](docs/SEARCH_LOG.md) | 后续 agent | 已查过的公开资料、待验证项 |

> 执行摘要的 PDF 版本：[`docs/00_summary.pdf`](docs/00_summary.pdf)。  
> GitHub 上直接点 `.md` 也能看，公式用 `$...$` 渲染。

---

## 3. 物理图像一句话

$D_{s1}(2460)^+$ 是 charmed-strange 的 $P$-波态（$J^P=1^+$，质量约 2459.5 MeV，宽度 $<3.5$ MeV）。

在 Belle II 的 $\Upsilon(4S)$ 数据中，它主要来自 B 介子衰变：

$$
B^+\to \bar D^{*0}D_{s1}^+,\qquad
B^0\to D^{*-}D_{s1}^+,\qquad
B^0\to D^-D_{s1}^+ .
$$

然后：

$$
D_{s1}^+\to D_s^+\pi^+\pi^-,\qquad
D_s^+\to \phi\pi^+,\ \phi\to K^+K^- .
$$

LHCb 在 9 fb$^{-1}$ 的 $pp$ 数据中看到约 800 个信号事例，并在 $m(\pi^+\pi^-)$ 谱中看到双峰结构。Belle II 的优势是干净、可全重建、可分 $B^+/B^0$，可以用不同系统误差独立检验。

---

## 4. 仓库结构

```text
.
├── README.md
├── docs/
│   ├── 00_summary.md
│   ├── 01_physics.md
│   ├── 02_data_production.md
│   ├── 03_reconstruction.md
│   ├── 04_background_mva.md
│   ├── 05_fitting.md
│   ├── 06_execution.md
│   ├── 07_search_protocol.md
│   ├── 08_access_policy.md
│   ├── 09_agent_brief.md
│   └── SEARCH_LOG.md
├── code/
│   ├── steering/
│   │   ├── README.md
│   │   └── steering_ntuple.py
│   ├── b2luigi/
│   │   ├── README.md
│   │   └── tasks.py
│   ├── mva/
│   │   ├── README.md
│   │   └── train_bdt.sh
│   └── fit/
│       ├── README.md
│       └── fit_yield.py
├── references/
│   └── README.md
└── .gitignore
```

---

## 5. 当前状态与下一步

**已经有的：**

- 物理目标、LHCb 结果与 Belle II 策略；
- 数据/MC/skim 的选择建议；
- $D_s,D^0,D^*,D_{s1},B$ 的重建链与初始 cut；
- ROE/CS + FastBDT 的本底抑制方案；
- RooFit 产额拟合与 Dalitz 振幅分析框架；
- 18 个月执行计划与团队分工；
- 代码骨架与后续 agent 的检索协议。

**还没有的：**

- 在 KEKCC 上跑通的完整 steering file；
- 用真实 MC 优化后的 cut；
- 数据/MC 对比图、cutflow、BDT ROC；
- 真实的信号产额与拟合结果；
- 系统误差表。

**下一步（按顺序）：**

1. 在 KEKCC 上跑通控制道 $B^+\to\bar D^{*0}D_s^+$；
2. 跑通 $D_{s1}\to D_s\pi\pi$ 的 ntuple；
3. 训练第一版 FastBDT；
4. 做 $M_{\rm bc}$ / $\Delta E$ / $m(D_s\pi\pi)$ 的产额拟合；
5. 再做 Dalitz 振幅分析。

---

## 6. 参考文献

- LHCb Collaboration, *Study of $D_{s1}(2460)^+\to D_s^+\pi^+\pi^-$ in $B\to\bar D^{(*)}D_s^+\pi^+\pi^-$ decays*, Science Bulletin **70** (2025) 1432–1444.  
  DOI: [10.1016/j.scib.2025.02.025](https://doi.org/10.1016/j.scib.2025.02.025)
- Belle II 软件文档：<https://software.belle2.org/development/sphinx/>
- Belle II Online Book：<https://software.belle2.org/development/sphinx/online_book/>
- Belle II 软件问答：<https://questions.belle2.org/>

---

## 7. 使用与贡献

- 先读 [`docs/00_summary.md`](docs/00_summary.md)；
- 要改物理/选择，改 `docs/`；
- 要改代码，从 `code/steering/` 开始；
- 所有新增内容必须注明来源（公开文档/公开论文/自己的推导）；
- 不要把内部数据、他人代码、token 放进本仓库。

> 这是一个**公开**仓库，任何内容都可能被合作组外的人看到。提交前请确认没有敏感信息。
