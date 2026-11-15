# Inputs 与参数清单

> 这份文档回答：**AI 用了哪些输入、设了哪些参数、哪些是论文值、哪些是 toy 假设、哪些还没有。**
>
> 一句话：**没有 Belle/Belle II 原始数据**；`figures/` 里的图是基于公开论文产额/分辨率的 toy 复现，不是数据拟合结果。

---

## 1. 人类提供的输入

| 输入 | 位置/形式 | 用途 | 状态 |
|---|---|---|---|
| Belle 2003 $D_{sJ}$ 论文 | `references/0307052v2.pdf` | 简化路线的主要依据：cut、产额、质量、分支比 | 已使用 |
| LHCb 2025 论文 | `references/1-s2.0-S2095927325001872-main.pdf` | 完整 B 衰变/Dalitz 路线的物理动机 | 已使用 |
| 师兄/群里发的 cut 表截图 | 图片，已转录到 `docs/10_dsj_analysis.md` | 2003 Belle 选择条件 | 已使用 |
| Belle II 公开软件文档 | `software.belle2.org` | basf2 模块、变量、skim | 已使用 |
| `b2luigi` 公开文档 | `b2luigi.belle2.org` | 批量任务 | 已使用 |
| 用户口头/截图要求 | 对话 | 先做简化路线、生成图像 | 已使用 |
| 群聊里的 GitHub token | 截图 | **未使用，也不应使用** | 已暴露，需 revoke |

---

## 2. 论文物理输入（Belle 2003）

### 2.1 质量与宽度

| 参数 | 值 | 来源/说明 |
|---|---|---|
| $m_{D_{sJ}(2317)}$ | $2317.2\pm0.5\pm0.9\ \mathrm{MeV}$ | Belle 2003 |
| $m_{D_{sJ}(2457)}$（$D_s^*\pi^0$） | $2456.5\pm1.3\pm1.3\ \mathrm{MeV}$ | Belle 2003 |
| $m_{D_{sJ}(2457)}$（$D_s\gamma$） | $2459.5\pm1.3\pm1.0\ \mathrm{MeV}$ | Belle 2003 |
| $\Gamma(D_{sJ}(2317))$ | $<4.6\ \mathrm{MeV}$（90% CL） | Belle 2003 |
| $\Gamma(D_{sJ}(2457))$ | $<5.5\ \mathrm{MeV}$（90% CL） | Belle 2003 |

### 2.2 产额

| 模式 | 产额 | 效率 |
|---|---|---|
| $D_{sJ}(2317)\to D_s^+\pi^0$ | $761\pm44\pm30$ | 8.2% |
| $D_{sJ}(2457)\to D_s^{*+}\pi^0$ | $126\pm25\pm12$ | 4.7% |
| $D_{sJ}(2457)\to D_s^+\gamma$ | $152\pm18$ | 10.2% |
| $D_{sJ}(2457)\to D_s^+\pi^+\pi^-$ | $59.7\pm11.5$ | 15.8% |
| $D_{s1}(2536)\to D_s^+\pi^+\pi^-$ | $56.5\pm13.4$ | 14.3% |

### 2.3 分支比与上限

| 量 | 值 |
|---|---|
| $\mathcal B(D_{sJ}(2457)\to D_s\gamma)/\mathcal B(D_{sJ}(2457)\to D_s^*\pi^0)$ | $0.55\pm0.13\pm0.08$ |
| $\mathcal B(D_{sJ}(2457)\to D_s\pi\pi)/\mathcal B(D_{sJ}(2457)\to D_s^*\pi^0)$ | $0.14\pm0.04\pm0.02$ |
| $\mathcal B(D_{sJ}(2317)\to D_s\gamma)/\mathcal B(D_{sJ}(2317)\to D_s\pi^0)$ | $<0.18$（90% CL） |
| $\mathcal B(D_{sJ}(2317)\to D_s\pi\pi)/\mathcal B(D_{sJ}(2317)\to D_s\pi^0)$ | $<4\times10^{-3}$（90% CL） |

### 2.4 拟合分辨率（用于 toy 图）

| 模式 | $\Delta M$ 峰位 | 分辨率 $\sigma$ |
|---|---|---|
| $D_{sJ}(2317)\to D_s\pi^0$ | 348.7 MeV | 7.1 MeV（论文报告 7.6±0.5） |
| $D_{sJ}(2457)\to D_s^*\pi^0$ | 344.1 MeV | 5.8 MeV |
| $D_{sJ}(2457)\to D_s\gamma$ | 491.0 MeV | 8.0 MeV（toy 取值） |
| $D_{sJ}(2457)\to D_s\pi\pi$ | 491.4 MeV | 5.8 MeV（toy 取值） |
| $D_{s1}(2536)\to D_s\pi\pi$ | 570.0 MeV | 6.0 MeV（toy 取值） |

> 表中标“toy 取值”的分辨率不是论文的精确拟合值；用于生成示意分布。  
> 论文值以 `docs/10_dsj_analysis.md` 的文字为准。

---

## 3. 选择条件（2003 Belle）

| 对象 / 变量 | 条件 |
|---|---|
| $\phi\to K^+K^-$ | 两条异号径迹；一条 $P(K/\pi)>0.5$，另一条 $>0.2$ |
| $\phi$ 质量窗 | $\lvert M(K^+K^-)-m_\phi\rvert<10\ \mathrm{MeV}$ |
| $\phi$ 螺旋角 | $\lvert\cos\theta_H\rvert>0.35$ |
| bachelor $\pi^+$ | $P(K/\pi)<0.9$ |
| $D_s^+$ 质量窗 | $\lvert M(\phi\pi^+)-m_{D_s}\rvert<10\ \mathrm{MeV}$ |
| $D_{sJ}$ 质心系动量 | $p^*(D_s\pi\pi)>3.5\ \mathrm{GeV}$ |
| $D_{sJ}$ 的两条 pion | 至少一条 $p^*>0.300\ \mathrm{GeV}$ |
| 两条 pion 的 PID | 一条 $P(K/\pi)<0.1$，另一条 $<0.9$ |
| $K_S^0$ veto | $\lvert M(\pi^+\pi^-)-m_{K_S^0}\rvert\ge15\ \mathrm{MeV}$ |
| 多候选 | 保留多个，不作唯一选择 |

---

## 4. Toy 图参数（`code/figures/make_dsj_figures.py`）

### 4.1 四联图/单图

| 面板 | mean (GeV) | sigma (GeV) | $N_{\rm sig}$ | $N_{\rm bkg}$ | x 范围 (GeV) | bins | seed |
|---|---:|---:|---:|---:|---|---:|---:|
| (a) $D_s\pi^0$ | 0.3487 | 0.0071 | 761 | 1500 | 0.10–0.60 | 50 | 11 |
| (b) $D_s^*\pi^0$ | 0.3441 | 0.0058 | 126 | 520 | 0.10–0.60 | 50 | 12 |
| (c) $D_s\gamma$ | 0.4910 | 0.0080 | 152 | 420 | 0.35–0.65 | 50 | 13 |
| (d) $D_s\pi\pi$ | 0.4914 | 0.0058 | 59.7 | 480 | 0.35–0.65 | 50 | 14 |

额外峰（panel d）：

| 参数 | 值 |
|---|---|
| $D_{s1}(2536)$ mean | 0.5700 GeV |
| $\sigma$ | 0.0060 GeV |
| $N$ | 56.5 |

本底模型：

- 截断指数，`bkg_scale = 0.10 GeV`；
- 本底产额 $N_{\rm bkg}$ 是**示意值**，不是论文公布值；
- 数据点用 Poisson 误差；
- 拟合曲线是“高斯 + 指数”的示意，不是对 toy 数据的正式拟合。

### 4.2 其他图

| 图 | 输入 |
|---|---|
| `fig_yields.png` | 论文产额和效率（见 §2.2） |
| `fig_chain.png` | 纯示意图，无数值输入 |

---

## 5. basf2 方案参数（尚未运行）

> 这些是 `code/steering/steering_ntuple.py` 和 docs 里的**初始值**，不是优化后的生产 cut。

### 5.1 输入

| 参数 | 值 | 状态 |
|---|---|---|
| 输入文件 | `"/path/to/your/mdst_or_udst.root"` | 占位符，未提供真实数据 |
| `environmentType` | `"default"` | 待确认 |
| release / globaltag | 未设置 | 待确认 |
| 数据/MC campaign | 未设置 | 待确认 |

### 5.2 基础粒子

| 列表 | cut |
|---|---|
| `pi+:good` | `thetaInCDCAcceptance`，`dr<0.5`，`abs(dz)<2.0`，`pionID>0.5`，`p>0.08`，`pt>0.05` |
| `K+:good` | 同上，`kaonID>0.5`，`p>0.10` |
| `gamma:good` | `E>0.05`，`inCDCAcceptance`，`abs(clusterTiming)<200`，`clusterE1E9>0.4` |
| `pi0:good` | `0.11<M<0.15` |
| `K_S0:merged` | `stdKshorts` |

### 5.3 重建 cut

| 对象 | 参数 | 值 |
|---|---|---|
| $\phi$ | 质量窗 | 1.00–1.04 GeV |
| $D_s$ | 质量窗 / $p^*$ / $\chi^2_{\rm prob}$ / 位移 | 1.93–2.00 GeV / $>1.2$ / $>0.001$ / $>2$ |
| $D^0$ | 质量窗 / $p^*$ / $\chi^2_{\rm prob}$ | 1.83–1.90 GeV / $>1.0$ / $>0.001$ |
| $D^{*0}$ | $\Delta M$ | 0.130–0.155 GeV |
| $D^{*-}$ | $\Delta M$ | 0.140–0.150 GeV |
| $D_{s1}$ | 质量窗 / $p^*$ / $\chi^2_{\rm prob}$ | 2.42–2.50 GeV / $>1.0$ / $>0.001$ |
| B | $M_{\rm bc}$ / $\lvert\Delta E\rvert$ / $\chi^2_{\rm prob}$ / $dr$ / $\lvert dz\rvert$ / $p^*$ / $\lvert\cos\theta\rvert$ | 5.20–5.30 GeV / $<0.10$ GeV / $>0.001$ / $<1.0$ cm / $<2.0$ cm / $<0.6$ GeV / $<0.9$ |

### 5.4 模块参数

| 模块 | 参数 | 值 |
|---|---|---|
| `TreeFitter` | `conf_level` | 0.001 |
| `TreeFitter` | `updateAllDaughters` | True |
| `TreeFitter` | `massConstraint` | 基线不加；可选 |
| `MVAExpert` | `identifier` | `Ds1_BDT.root` |
| `MVAExpert` | `extraInfoName` | `BDT` |
| `b2luigi` | `batch_system` | `"kekcc"` |
| `b2luigi` | `workers` | 10（示例） |

### 5.5 RooFit 产额拟合参数

| 参数 | 值 |
|---|---|
| $x$ 范围 | 2.40–2.52 GeV |
| signal mean | 2.4595 GeV |
| natural width | 0.0015 GeV（固定） |
| resolution $\sigma$ | 0.004 GeV（浮动） |
| background | `RooExponential`，初始 `tau=-8` |
| 初始产额 | $N_{\rm sig}=100$，$N_{\rm bkg}=1000$ |
| 似然 | extended |

---

## 6. 还没有的输入（关键）

| 缺什么 | 影响 |
|---|---|
| Belle II 真实数据/MC 文件路径 | 不能跑真实 ntuple |
| Belle II release / globaltag | 不能保证模块参数正确 |
| continuum/charm skim 名称 | 不能定位数据 |
| Belle II 亮度/continuum 比例 | 不能算真实预期产额 |
| Belle II PID/$\pi^0$/$\gamma$ 效率 | 不能把 2003 效率直接搬过来 |
| 真实 data/MC ntuple | 不能做真实拟合 |
| 振幅模型/效率图 | 不能做 Dalitz |

---

## 7. 明确没有使用的东西

- ❌ Belle 的 86.9 fb\(^{-1}\) 原始数据；
- ❌ Belle II 的 ntuple；
- ❌ 私人 GitLab/GitHub 分析库；
- ❌ Analyses 里的他人代码；
- ❌ 群聊中的 GitHub token；
- ❌ 任何内部会议材料/未公开数据。

---

## 8. 复现命令

```bash
# 图
python code/figures/make_dsj_figures.py

# 报告 PDF（需要本地 Markdown -> HTML/PDF 工具）
# 当前仓库已包含 docs/10_dsj_analysis.pdf
```

---

## 9. 一句话

**论文输入是真实的；toy 图的产额/分辨率来自论文，但本底和涨落是假设；basf2 参数是初始值，尚未在 KEKCC 上验证。**
