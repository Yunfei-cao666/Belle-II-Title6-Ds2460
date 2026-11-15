# 关于 $D_{sJ}$ 分析中 signal MC 的说明

> **用途**：给师兄/组会解释“这个过程的 signal MC 到底怎么产生、能不能直接用 generic MC”。  
> **结论先说**：**可以先拿 inclusive $c\bar c$ generic MC 看峰和本底；但正式的效率、线形和 cross-feed，最好用 dedicated signal MC，或者至少用高统计、truth-matched 的 generic MC。**

---

## 1. 先把三个东西分开

| 名称 | 是什么 | 主要用途 |
|---|---|---|
| **数据** | Belle/Belle II 的 $e^+e^-\to c\bar c$ inclusive 数据 | 最终测量 |
| **generic MC** | 包含所有成分的蒙特卡洛：$c\bar c$、$B\bar B$、$uds$、$\tau\tau$ 等 | 本底、成分、data/MC 对比 |
| **signal MC** | 指定产生 $D_{sJ}$，并指定它衰变到某个末态的 MC | 效率、分辨率、线形、cross-feed |

> 杨昊中说“文献用的是 $ee\to cc$ 的样本”，这说的是**数据**。  
> 但 signal MC 是另一件事：它要模拟 $D_{sJ}$ 的产生和衰变，才能算效率。

---

## 2. 2003 Belle 是怎么做的

2003 Belle 的论文：

> Y. Mikami et al. (Belle), *Measurements of the $D_{sJ}$ resonance properties*, arXiv:hep-ex/0307052.

它的分析是：

- 数据：$86.9\ \mathrm{fb}^{-1}$ 的 $e^+e^-\to c\bar c$；
- 重建 $D_s^+\to\phi\pi^+$，$\phi\to K^+K^-$；
- 重建 $D_{sJ}^+\to D_s^+\pi^0$、$D_s^{*+}\pi^0$、$D_s^+\gamma$、$D_s^+\pi^+\pi^-$；
- 拟合 $\Delta M$ 得到产额、质量、宽度。

论文明确说：

> 他们用 MC 模拟，把 $D_{sJ}(2317)$ 当作标量、把 $D_{sJ}(2457)$ 当作轴矢量，衰变到 $D_s^{(*)}\pi^0$，零自然宽度，用来研究信号形状、效率和两个态之间的 cross-feed。

所以：

- **数据**是 inclusive $c\bar c$；
- **信号形状/效率**来自含 $D_{sJ}$ 的 MC；
- **generic MC** 主要用于本底和成分。

---

## 3. 能不能直接拿 generic MC 用？

可以，但要分用途：

| 用途 | 直接用 generic inclusive $c\bar c$ MC？ | 说明 |
|---|---|---|
| 先看 $\Delta M$ 有没有峰 | ✅ 可以 | 用 truth 匹配出 $D_{sJ}$，先做 sanity check |
| 估本底形状 | ✅ 可以 | generic MC 的强项 |
| 用 `mctruth` 拆成分 | ✅ 可以 | 后面再拆 $c\bar c$、$B\bar B$、$uds$、$\tau\tau$ |
| 估信号效率 | ⚠️ 有条件 | 分母必须是“generated $D_{sJ}$”，不是全部 inclusive 事件 |
| 拟合线形/分辨率 | ⚠️ 有条件 | 统计要够，且 truth matching 要干净 |
| 研究 feed-down / feed-up | ❌ 不够 | 最好每个衰变模式单独生成 signal MC |
| 最终系统误差 | ❌ 不够 | dedicated signal MC + 数据控制样本 |

### 一句话

> **generic MC 可以先用来“看峰”和“估本底”；但不要拿“所有 inclusive 事件”当信号效率的分母。**

---

## 4. 正确的效率算法

$$
\varepsilon =
\frac{N_{\text{重建且 truth-matched 的信号}}}
{N_{\text{生成器里真实产生的 }D_{sJ}}}
$$

分母是**生成器里真实产生的 $D_{sJ}$ 数**，不是全部 inclusive 事件数。

如果你用 generic MC，必须：

1. 在 truth 里找到 $D_{sJ}$；
2. 定义它是否在探测器接受度内；
3. 只对这一部分做分母；
4. 检查统计量是否足够。

如果 generic MC 里只有几十个 $D_{sJ}$，效率误差会很大，尤其是 $D_{sJ}(2457)\to D_s\gamma$、$D_s\pi\pi$ 这种稀有模式。

---

## 5. signal MC 怎么产生

### 5.1 先查官方 generic MC

先确认：

- Belle II 官方 generic $c\bar c$ MC 里有没有 $D_{sJ}$；
- 有哪些衰变模式；
- 统计量多少；
- decay table 是否包含 $D_{sJ}(2317)$、$D_{sJ}(2457)$。

如果官方 generic 已经包含且统计足够，可以直接 truth-match 用。

### 5.2 如果不够，就生成 dedicated signal MC

产生链：

```text
e+e- -> c cbar
  -> 产生 D_sJ+（强制或包含）
  -> D_sJ+ -> D_s+ pi0 / D_s*+ pi0 / D_s+ gamma / D_s+ pi+ pi-
  -> D_s*+ -> D_s+ gamma
  -> D_s+ -> phi pi+
  -> phi -> K+ K-
  -> pi0 -> gamma gamma
  -> 探测器模拟 + 重建
```

EvtGen decay file 骨架（粒子名以你的版本为准）：

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

### 5.3 每个模式单独生成

至少四组：

1. $D_{sJ}(2317)^+\to D_s^+\pi^0$
2. $D_{sJ}(2457)^+\to D_s^{*+}\pi^0$
3. $D_{sJ}(2457)^+\to D_s^+\gamma$
4. $D_{sJ}(2457)^+\to D_s^+\pi^+\pi^-$

另外加一组：

5. $D_{s1}(2536)^+\to D_s^+\pi^+\pi^-$（对照/本底）

不要把所有模式混在一个样本里，否则 cross-feed 和效率不好拆。

---

## 6. 建议的执行顺序

1. 先拿官方 inclusive $c\bar c$ generic MC，truth-match $D_{sJ}$，看 $\Delta M$ 有没有峰；
2. 统计够：先用 generic 做一版效率和线形；
3. 统计不够：生成 dedicated signal MC（每个模式单独）；
4. 用 signal MC 算效率、分辨率、cross-feed；
5. 用 generic MC + 数据 sideband 估本底；
6. 最后用 `mctruth` 拆 $c\bar c$、$B\bar B$、$uds$、$\tau\tau$ 成分。

---

## 7. 给师兄的 5 句话

1. 2003 Belle 的**数据**是 $e^+e^-\to c\bar c$ inclusive，但**signal MC** 要模拟 $D_{sJ}$ 的产生和衰变。
2. generic $c\bar c$ MC 可以先用来“看峰”和估本底，但不能拿全部 inclusive 事件当信号效率的分母。
3. 正式效率、线形和 cross-feed 最好用 dedicated signal MC，每个衰变模式单独生成。
4. 如果官方 generic MC 里 $D_{sJ}$ 统计足够，也可以 truth-match 来用；不够就得自己生成。
5. 后面再用 `mctruth` 拆 $c\bar c$、$B\bar B$、$uds$、$\tau\tau$ 成分。

---

## 8. 需要确认的三件事

- [ ] Belle II 官方 generic $c\bar c$ MC 是否包含 $D_{sJ}(2317)$ 和 $D_{sJ}(2457)$？
- [ ] 每个衰变模式的统计量是多少？
- [ ] 如果不够，是否有现成的 dedicated signal MC，还是需要自己生成？

> 这三个问题确认后，才能决定“直接用 generic”还是“必须生成 signal MC”。
