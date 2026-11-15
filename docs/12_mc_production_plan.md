# $D_{sJ}$ 分析的 MC 生产与使用方案

> **状态**：确认版（decision note）  
> **结论**：**最终分析必须用 dedicated signal MC；generic inclusive $c\bar c$ MC 只用于 first look、本底和成分。**
>
> 这份文档把“signal MC 到底怎么产生、generic MC 怎么用、效率怎么算、cross-feed 怎么处理”一次写清楚。

---

## 0. 确认结论

| 问题 | 确认答案 |
|---|---|
| 2003 Belle 的数据是什么？ | $e^+e^-\to c\bar c$ inclusive 数据 |
| 能不能只用 generic MC 做最终信号效率？ | **不能**，除非 generic 里 $D_{sJ}$ 统计足够且 truth matching 干净；最终建议 dedicated signal MC |
| generic MC 用来做什么？ | first look、本底形状、成分拆分（`mctruth`） |
| signal MC 用来做什么？ | 效率、分辨率、线形、feed-down/feed-up、cross-feed |
| 每个衰变模式要不要分开生成？ | **要**，四个模式 + $D_{s1}(2536)$ 对照分别生成 |
| 效率分母是什么？ | **generated $D_{sJ}$ 数**，不是全部 inclusive 事件数 |

**一句话：**

> **generic MC 可以先跑；但论文级结果必须用 dedicated signal MC。**

---

## 1. 样本清单

### 1.1 数据

- Belle II（或 Belle 2003 对照）的 $e^+e^-\to c\bar c$ inclusive 数据；
- 用 continuum/charm skim；
- 不用 hadronic B skim。

### 1.2 Generic MC

| 样本 | 用途 |
|---|---|
| $c\bar c$ inclusive | 信号 first look、本底、成分 |
| $B\bar B$ generic | $B\bar B$ 本底 |
| $uds$ generic | 轻夸克连续本底 |
| $\tau^+\tau^-$ | 低多重数本底 |

> generic MC 先不拆成分；后面用 `mctruth` 拆 $c\bar c$、$B\bar B$、$uds$、$\tau\tau$。

### 1.3 Dedicated signal MC

每个模式单独生成：

1. $D_{sJ}(2317)^+\to D_s^+\pi^0$
2. $D_{sJ}(2457)^+\to D_s^{*+}\pi^0$
3. $D_{sJ}(2457)^+\to D_s^+\gamma$
4. $D_{sJ}(2457)^+\to D_s^+\pi^+\pi^-$
5. $D_{s1}(2536)^+\to D_s^+\pi^+\pi^-$（对照/本底）

建议每个模式至少 $10^5$ 个生成事件；如果要做 cross-feed 矩阵，建议 $5\times10^5$ 到 $10^6$。

---

## 2. 产生链

```text
e+e- -> c cbar
  -> 产生 D_sJ+（强制或包含）
  -> D_sJ+ -> D_s+ pi0 / D_s*+ pi0 / D_s+ gamma / D_s+ pi+ pi-
  -> D_s*+ -> D_s+ gamma
  -> D_s+ -> phi pi+
  -> phi -> K+ K-
  -> pi0 -> gamma gamma
  -> 探测器模拟
  -> 重建
```

### 2.1 产生 $D_{sJ}$

两种做法：

**A. 官方 generic $c\bar c$ MC**

- 先查官方 production 是否包含 $D_{sJ}(2317)$、$D_{sJ}(2457)$；
- 如果包含且统计足够，用 truth matching 选出来；
- 适合 first look 和本底。

**B. Dedicated signal MC**

- 在 $e^+e^-\to c\bar c$ 产生器中强制 $c$ 夸克碎裂到 $D_{sJ}$；
- 或用 exclusive $e^+e^-\to D_{sJ}^+X$ 产生；
- 每个衰变模式单独生成；
- 用 EvtGen 指定衰变；
- 用官方 detector simulation + reconstruction。

> 不要用 Belle 2003 的 MC 代替 Belle II MC；能量、探测器和重建都不同。

---

## 3. EvtGen decay file

`code/mc/signal_decay_DsJ.dec` 是骨架。核心内容：

```text
Decay D_sJ+
1.0  D_s+  pi0;
Enddecay

Decay D_sJ+
1.0  D_s*+  pi0;
Enddecay

Decay D_sJ+
1.0  D_s+  gamma;
Enddecay

Decay D_sJ+
1.0  D_s+  pi+  pi-;
Enddecay

Decay D_s*+
1.0  D_s+  gamma;
Enddecay

Decay D_s+
1.0  phi  pi+;
Enddecay

Decay phi
1.0  K+  K-;
Enddecay

Decay pi0
1.0  gamma  gamma;
Enddecay
```

> 粒子名和语法以你的 EvtGen 版本为准。  
> 每个模式单独一个 decay file，避免混在一起。

---

## 4. basf2 分析：truth matching

### 4.1 需要定义的 truth 标志

在 ntuple 里保存：

```text
isSignal          # 重建候选是否匹配 truth D_sJ
isD_sJ            # truth 里是否有 D_sJ
DsJ_mode          # 2317->Ds pi0 / 2457->Ds* pi0 / ...
isFeedDown        # 是否来自另一个 D_sJ 态
isFeedUp          # 是否来自低质量态
true_DsJ_M        # truth 质量
true_DsJ_pstar    # truth 动量
```

### 4.2 匹配条件

建议：

- 重建 $D_s$ 与 truth $D_s$ 的 $\Delta R$、质量窗匹配；
- 重建 $D_{sJ}$ 与 truth $D_{sJ}$ 的 $\Delta R$、电荷匹配；
- 末态 $\pi^0,\gamma,\pi^\pm$ 与 truth  daughters 匹配；
- 记录匹配质量，不要只用 `isSignal` 一个布尔值。

### 4.3 效率

$$
\varepsilon =
\frac{N_{\text{重建且 truth-matched}}}
{N_{\text{generated }D_{sJ}\text{ in acceptance}}}
$$

- 分母是 generated $D_{sJ}$，不是全部 inclusive 事件；
- 如果分母加了 $p^*>3.5$ 的 generator-level cut，要在文档里写清楚；
- 建议同时报告“无 generator cut”和“有 acceptance cut”的效率。

---

## 5. Cross-feed

必须用 dedicated signal MC 做矩阵：

| 生成 \ 重建 | $D_s\pi^0$ | $D_s^*\pi^0$ | $D_s\gamma$ | $D_s\pi\pi$ |
|---|---|---|---|---|
| $D_{sJ}(2317)\to D_s\pi^0$ | 主信号 | feed-up? | feed-up? | feed-up? |
| $D_{sJ}(2457)\to D_s^*\pi^0$ | feed-down? | 主信号 | 光子漏掉/替换 | 软 $\pi^0$ 漏掉 |
| $D_{sJ}(2457)\to D_s\gamma$ | feed-down? | 光子误组合 | 主信号 | — |
| $D_{sJ}(2457)\to D_s\pi\pi$ | feed-down? | — | — | 主信号 |

> 这张表要用 MC 填，不能凭直觉。  
> 特别是 $D_{sJ}(2317)$ 和 $D_{sJ}(2457)$ 之间的 feed-down/feed-up，是 2003 Belle 拟合里明确处理的。

---

## 6. Generic MC 的正确用法

### 6.1 可以

- first look：truth-match $D_{sJ}$，看 $\Delta M$ 峰；
- 本底形状：$c\bar c$、$B\bar B$、$uds$、$\tau\tau$；
- 成分拆分：用 `mctruth` 分类；
- data/MC 对比的起点。

### 6.2 不可以

- 不能拿全部 inclusive 事件当信号效率分母；
- 不能假设 generic 的 $D_{sJ}$ 产生模型和 data 一致；
- 不能用低统计 generic 做稀有模式效率；
- 不能用 generic 代替 cross-feed 专用样本。

---

## 7. 执行顺序

### 第 1 步：确认官方 MC

- [ ] Belle II 官方 generic $c\bar c$ 是否含 $D_{sJ}(2317)$、$D_{sJ}(2457)$？
- [ ] 每个模式统计多少？
- [ ] decay table 是否包含四个衰变模式？
- [ ] 是否有现成 signal MC？

### 第 2 步：generic first look

- [ ] 用 generic $c\bar c$ truth-match $D_{sJ}$；
- [ ] 画 $\Delta M(D_s\pi^0)$、$\Delta M(D_s^*\pi^0)$、$\Delta M(D_s\gamma)$、$\Delta M(D_s\pi\pi)$；
- [ ] 检查本底形状和统计量。

### 第 3 步：dedicated signal MC

- [ ] 每个模式生成 $10^5$–$10^6$ 事件；
- [ ] 用官方 detector simulation + reconstruction；
- [ ] 保存 truth 信息；
- [ ] 做 truth matching。

### 第 4 步：效率与 cross-feed

- [ ] 算每个模式的效率；
- [ ] 填 cross-feed 矩阵；
- [ ] 检查 feed-down/feed-up；
- [ ] 估计 MC 统计误差。

### 第 5 步：数据拟合

- [ ] 用 signal MC 做信号模板/线形；
- [ ] 用 generic MC + sideband 做本底；
- [ ] 同时拟合 $D_{sJ}(2317)$ 和 $D_{sJ}(2457)$；
- [ ] 系统误差。

---

## 8. 验收标准

- [ ] 每个 signal 模式的生成数、重建数、truth-matched 数都有记录；
- [ ] 效率分母定义写清楚；
- [ ] cross-feed 矩阵有 MC 支持；
- [ ] generic MC 只用于本底/成分，不冒充 signal；
- [ ] 所有图带 “MC” 或 “toy” 标注；
- [ ] 不把 Belle 2003 的 MC 当 Belle II MC。

---

## 9. 一句话总结

> **generic MC 是“看”和“估本底”的工具；dedicated signal MC 才是“算效率、线形、cross-feed”的工具。两者不能混。**
