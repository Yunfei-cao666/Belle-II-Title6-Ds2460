# 粒子重建与事件筛选

> 这一章是“怎么在 basf2 里把 $D_s,D^0,D^*,D_{s1},B$ 组合出来”。  
> 所有 cut 都是**初始值**，必须用 MC 优化；不要照抄到生产。

---

## 1. 基线通道

| 通道 | 衰变链 | 用途 |
|---|---|---|
| **A（基线，$B^+$）** | $B^+\to\bar D^{*0}D_{s1}^+$，$\bar D^{*0}\to\bar D^0\gamma$，$\bar D^0\to K^+\pi^-$ | 最干净，$\gamma$ 软但可重建 |
| **B（$B^+$，无 $D^*$）** | $B^+\to\bar D^0D_{s1}^+$，$\bar D^0\to K^+\pi^-$ | 归一化/交叉检验 |
| **C（基线，$B^0$）** | $B^0\to D^{*-}D_{s1}^+$，$D^{*-}\to\bar D^0\pi^-$ | 软 $\pi^-$ 容易，统计可能更好 |
| **D（$B^0$，无 $D^*$）** | $B^0\to D^-D_{s1}^+$，$D^-\to K^+\pi^-\pi^-$ | 归一化/交叉检验 |
| **可选** | $\bar D^{*0}\to\bar D^0\pi^0$；$D_s^+\to K^{*0}K^+$；$D_s^+\to K_S^0K^+$ | 增加统计/系统误差交叉检验 |

信号：

$$
D_{s1}^+\to D_s^+\pi^+\pi^-,
\qquad
D_s^+\to\phi\pi^+,\quad \phi\to K^+K^-.
$$

> 电荷共轭默认自动重建。写 $B^+$ 即可，不要手动再写 $B^-$。

---

## 2. 工作流

```text
uDST/mDST
  │
  ├─ fillParticleList: pi+, K+, gamma, pi0, K_S0
  │
  ├─ D_s+ → φπ+ (φ→K+K−)          [基线]
  ├─ D0bar → K+π−                  [基线]
  ├─ D*0bar → D0bar γ              [通道 A]
  ├─ D*− → D0bar π−               [通道 C]
  ├─ D− → K+π−π−                  [通道 D]
  │
  ├─ D_s1+ → D_s+ π+ π−           [信号]
  │
  ├─ B+ → D*0bar D_s1+ / D0bar D_s1+
  ├─ B0 → D*− D_s1+ / D− D_s1+
  │
  ├─ TreeFitter: 顶点 + 可选 B 质量约束
  ├─ Mbc / ΔE / χ²_prob / flight significance
  ├─ BestCandidateSelection
  │
  ├─ buildRestOfEvent + buildContinuumSuppression
  ├─ MVAExpert (FastBDT)
  │
  └─ variablesToNtuple → RooFit / zfit
```

---

## 3. 基础粒子列表

```python
import basf2 as b2
import modularAnalysis as ma
import variables.utils as vu
import vertex as vx
from variables import variables as vm
from stdV0s import stdKshorts

main = b2.Path()

ma.inputMdstList(
    environmentType="default",
    filelist=["/path/to/your/mdst_or_udst.root"],
    path=main,
)

ma.fillParticleList(
    "pi+:good",
    "thetaInCDCAcceptance and dr < 0.5 and abs(dz) < 2.0 "
    "and pionID > 0.5 and p > 0.08 and pt > 0.05",
    path=main,
)
ma.fillParticleList(
    "K+:good",
    "thetaInCDCAcceptance and dr < 0.5 and abs(dz) < 2.0 "
    "and kaonID > 0.5 and p > 0.10 and pt > 0.05",
    path=main,
)
ma.fillParticleList(
    "gamma:good",
    "E > 0.05 and inCDCAcceptance and abs(clusterTiming) < 200 "
    "and clusterE1E9 > 0.4",
    path=main,
)
ma.reconstructDecay(
    "pi0:good -> gamma:good gamma:good",
    "0.11 < M < 0.15",
    path=main,
)
stdKshorts(path=main)
```

> `stdPi0s`、`stdPhotons`、`stdCharged` 的部分 list 在 `light-2604` 之后已被标记为 deprecated。  
> 新分析优先用 `stdCharged("base")`、`stdPhotons("base")`，或者像上面这样直接写。

---

## 4. $D_s^+\to\phi\pi^+$

```python
ma.reconstructDecay(
    "phi:good -> K+:good K-:good",
    "1.00 < M < 1.04",
    path=main,
)

ma.reconstructDecay(
    "D_s+:phi -> phi:good pi+:good",
    "1.93 < M < 2.00",
    path=main,
)

vx.treeFit("D_s+:phi", conf_level=0.001, updateAllDaughters=True, path=main)

ma.applyCuts(
    "D_s+:phi",
    "[p* > 1.2] and [chiProb > 0.001] and [significanceOfDistance > 2.0]",
    path=main,
)
```

**为什么：**

- $\phi$ 质量 1.019 GeV，宽 4 MeV；`1.00–1.04` 保留 $\pm20$ MeV。
- $D_s$ 质量 1.968 GeV；初期用 `1.93–2.00`，优化后可收到 $\pm15$ MeV。
- $p^*>1.2$：B 衰变产生的 $D_s$ 在 CM 系动量通常 1.2–1.7 GeV；**不要卡到 1.6 以上**。
- `chiProb > 0.001`：顶点质量；不要用 0.1 这种过紧 cut。
- `significanceOfDistance > 2.0`：$D_s$ 的 $c\tau\sim150\ \mu\mathrm{m}$，有可测位移，能压 prompt 组合。

其他 $D_s$ 道（先各自做，不要混）：

```python
# D_s+ -> K*0 K+
ma.reconstructDecay("K*0:good -> K+:good pi-:good", "0.82 < M < 0.98", path=main)
ma.reconstructDecay("D_s+:kst -> K*0:good K+:good", "1.93 < M < 2.00", path=main)

# D_s+ -> K_S0 K+
ma.reconstructDecay("D_s+:ksk -> K_S0:merged K+:good", "1.92 < M < 2.01", path=main)
```

---

## 5. $\bar D^0$ 与 $D^*$

```python
ma.reconstructDecay(
    "anti-D0:kp -> K+:good pi-:good",
    "1.83 < M < 1.90",
    path=main,
)
vx.treeFit("anti-D0:kp", conf_level=0.001, updateAllDaughters=True, path=main)
ma.applyCuts(
    "anti-D0:kp",
    "[p* > 1.0] and [chiProb > 0.001] and [significanceOfDistance > 2.0]",
    path=main,
)

ma.reconstructDecay(
    "anti-D*0:g -> anti-D0:kp gamma:good",
    "0.130 < M - daughter(0, M) < 0.155",
    path=main,
)
vx.treeFit("anti-D*0:g", conf_level=0.001, updateAllDaughters=True, path=main)

ma.reconstructDecay(
    "D*-:pi -> anti-D0:kp pi-:good",
    "0.140 < M - daughter(0, M) < 0.150",
    path=main,
)
vx.treeFit("D*-:pi", conf_level=0.001, updateAllDaughters=True, path=main)
```

- `M - daughter(0, M)` 是 mother 质量减第一个 daughter 质量，即 $\Delta M=M(D^*)-M(D^0)$。
- $D^{*0}$：约 142 MeV；$D^{*-}$：约 145.4 MeV。
- 用质量差而不是直接卡 $D^*$ 质量，能抵消一部分 $D^0$ 质量分辨率。
- 软光子 $E>0.05$ 要保留；不要用 0.2 砍掉 $D^{*0}\to D^0\gamma$。

---

## 6. $D_{s1}^+\to D_s^+\pi^+\pi^-$

```python
ma.reconstructDecay(
    "D_s1+:sig -> D_s+:phi pi+:good pi-:good",
    "2.42 < M < 2.50",
    path=main,
)
vx.treeFit("D_s1+:sig", conf_level=0.001, updateAllDaughters=True, path=main)
ma.applyCuts(
    "D_s1+:sig",
    "[p* > 1.0] and [chiProb > 0.001]",
    path=main,
)
```

- 质量窗 `2.42–2.50` 是宽松窗；优化后可收到 `2.445–2.475`，两侧留 sideband。
- **不要在这一步卡 $m(\pi\pi)$**，否则 Dalitz 分析有偏。
- $D_{s1}$ 寿命极短，不要硬要求它有显著 flight distance；`TreeFitter` 会自动合并顶点。

---

## 7. B 组合

```python
ma.reconstructDecay(
    "B+:dstDs1 -> anti-D*0:g D_s1+:sig",
    "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
    path=main,
)
ma.reconstructDecay(
    "B+:dDs1 -> anti-D0:kp D_s1+:sig",
    "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
    path=main,
)
ma.reconstructDecay(
    "B0:dsDs1 -> D*-:pi D_s1+:sig",
    "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
    path=main,
)

ma.reconstructDecay(
    "D-:kpipi -> K+:good pi-:good pi-:good",
    "1.85 < M < 1.89",
    path=main,
)
vx.treeFit("D-:kpipi", conf_level=0.001, updateAllDaughters=True, path=main)

ma.reconstructDecay(
    "B0:dDs1 -> D-:kpipi D_s1+:sig",
    "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
    path=main,
)
```

合并电荷共轭：

```python
ma.copyLists(
    "Bc:all",
    ["B+:dstDs1", "B+:dDs1", "B-:dstDs1", "B-:dDs1"],
    path=main,
)
ma.copyLists(
    "Bn:all",
    ["B0:dsDs1", "B0:dDs1", "anti-B0:dsDs1", "anti-B0:dDs1"],
    path=main,
)

vx.treeFit("Bc:all", conf_level=0.001, updateAllDaughters=True, path=main)
vx.treeFit("Bn:all", conf_level=0.001, updateAllDaughters=True, path=main)

for name in ["Bc:all", "Bn:all"]:
    ma.applyCuts(
        name,
        "[chiProb > 0.001] and [dr < 1.0] and [abs(dz) < 2.0] "
        "and [p* < 0.6] and [abs(cosTheta) < 0.9]",
        path=main,
    )
    ma.rankByHighest(name, "chiProb", numBest=1, path=main)
```

### 7.1 $M_{\rm bc}$ 和 $\Delta E$

$$
M_{\rm bc}=\sqrt{E_{\rm beam}^2-|\vec p_B|^2},
\qquad
\Delta E=E_B-E_{\rm beam},
\qquad
E_{\rm beam}=\frac{\sqrt{s}}{2}.
$$

- 正确 B：$M_{\rm bc}\approx5.28\ \mathrm{GeV}$，$\Delta E\approx0$。
- $M_{\rm bc}$ 对 B 动量误差不敏感。
- 分辨率：$M_{\rm bc}$ 几个 MeV，$\Delta E$ 几十 MeV。
- `abs(deltaE) < 0.10` 是初始值；$D^{*0}\to D^0\gamma$ 可先放到 0.15。

> **B 质量约束的坑**：  
> `treeFit(..., massConstraint=["B+"], updateAllDaughters=True)` 会改变 daughter 动量。  
> 做 Dalitz 分析时，不要用质量约束后的 daughter 4-momenta 去算 Dalitz 变量；用无约束的版本，或保存约束前/后两套变量。

---

## 8. 初始 cut 表

| 对象 | 变量 | 初始 cut | 为什么 |
|---|---|---|---|
| 径迹 | `thetaInCDCAcceptance` | true | CDC 接受度 |
| 径迹 | `dr` | $<0.5\ \mathrm{cm}$ | 压坏径迹 |
| 径迹 | `abs(dz)` | $<2.0\ \mathrm{cm}$ | 压坏径迹 |
| 径迹 | `pionID`/`kaonID` | $>0.5$ | 基本 PID |
| 径迹 | `p` | $>0.08\ \mathrm{GeV}$ | 软 $\pi$ |
| 光子 | `E` | $>0.05\ \mathrm{GeV}$ | 保留软 $\gamma$ |
| 光子 | `clusterE1E9` | $>0.4$ | 光子形状 |
| 光子 | `abs(clusterTiming)` | $<200\ \mathrm{ns}$ | 压 beam background |
| $\pi^0$ | $M(\gamma\gamma)$ | $0.11–0.15\ \mathrm{GeV}$ | $\pi^0$ 窗 |
| $\phi$ | $M(K^+K^-)$ | $1.00–1.04\ \mathrm{GeV}$ | $\phi$ 窗 |
| $D_s$ | $M$ | $1.93–2.00\ \mathrm{GeV}$ | 初期宽窗 |
| $D_s$ | `p*` | $>1.2\ \mathrm{GeV}$ | B daughter |
| $D_s$ | `significanceOfDistance` | $>2.0$ | 位移 |
| $D^0$ | $M$ | $1.83–1.90\ \mathrm{GeV}$ | $D^0$ 窗 |
| $D^0$ | `p*` | $>1.0\ \mathrm{GeV}$ | B daughter |
| $D^*$ | $M-M(D^0)$ | 0.130–0.155 / 0.140–0.150 | 质量差 |
| $D_{s1}$ | $M$ | $2.42–2.50\ \mathrm{GeV}$ | 信号窗 |
| $D_{s1}$ | `p*` | $>1.0\ \mathrm{GeV}$ | B daughter |
| B | `Mbc` | $5.20–5.30\ \mathrm{GeV}$ | 信号区 |
| B | `abs(deltaE)` | $<0.10\ \mathrm{GeV}$ | 信号区 |
| B | `chiProb` | $>0.001$ | 顶点 |
| B | `dr`/`abs(dz)` | $<1.0/2.0\ \mathrm{cm}$ | B 顶点 |
| B | `p*` | $<0.6\ \mathrm{GeV}$ | B 近乎静止 |
| Event | `nTracks` | $>4$ | 压多重数 |
| Event | `R2` | $<0.5$ | 连续本底预选 |
| Event | `abs(cosTBTO)` | $<0.9$ | 连续本底预选 |

---

## 9. 验证清单

- [ ] $D_s\to\phi\pi$ 质量峰：数据/MC 峰位差 $<5\ \mathrm{MeV}$；
- [ ] $\phi\to K^+K^-$ 峰位 1.019 GeV；
- [ ] $D^0\to K^+\pi^-$ 峰位 1.865 GeV；
- [ ] $D^{*0}\to D^0\gamma$、$D^{*-}\to D^0\pi^-$ 的 $\Delta M$ 峰；
- [ ] $D_{s1}\to D_s\pi\pi$ 在 MC 中看到 2.46 GeV 峰；
- [ ] B 的 $M_{\rm bc}$ 在 5.28 GeV、$\Delta E$ 在 0；
- [ ] cutflow 表：信号效率、$B\bar B$ 本底、$q\bar q$ 本底；
- [ ] 多候选率：`rankByHighest("chiProb")` vs 随机选，确认不引入偏差。

---

## 10. 常见错误

| 错误 | 现象 | 解决 |
|---|---|---|
| `Mbc` 未定义 | `Variable 'Mbc' not found` | `Mbc` 只对 B 候选有意义 |
| `ParticleList` 不存在 | `B-:... does not exist` | 检查电荷共轭名；`summaryOfLists` |
| 候选太多 | 内存爆 | `candidate_limit`；加 $p^*$、顶点 cut |
| `TreeFitter` 效率低 | 信号效率 <95% | 协方差初始化；不要对 MC truth 粒子 fit；先 `conf_level=-1` |
| 软光子效率低 | $D^{*0}\to D^0\gamma$ 少 | 放宽 `E>0.05`；用 $D^{*0}\to D^0\pi^0$ 补充 |
| $D_{s1}$ 质量窗太宽 | 本底大 | 优化到 $\pm15$ MeV；留 sideband |
