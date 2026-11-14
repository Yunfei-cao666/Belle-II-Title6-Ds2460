# 本底抑制与多变量分析

> 这一章回答：本底从哪里来、用什么变量、怎么训练 FastBDT、怎么避免把信号拟合变量 sculpt 掉。

---

## 1. 主要本底

### 1.1 连续本底

$$
e^+e^-\to q\bar q,\qquad q=u,d,s,c.
$$

- 事件形状是“喷注状”的，和 $\Upsilon(4S)\to B\bar B$ 的“球状”不同；
- $c\bar c$ 会产生 $D_s,D^*$，是最危险的部分；
- 用 ROE（Rest of Event）变量：$R_2$、`cosTBTO`、thrust、Fox-Wolfram、CLEO cones、KSFW；
- 用 FastBDT 组合。

### 1.2 $B\bar B$ 本底

| 来源 | 拓扑 | 为什么危险 | 处理 |
|---|---|---|---|
| $B\to\bar D^{(*)}D_s^{(*)}\pi$ | 多一个 $\pi$ | 软 $\pi$ 漏掉可能落在 $D_{s1}$ 窗 | $M_{\rm bc}$、$\Delta E$、$D_{s1}$ sideband |
| $B\to\bar D^{(*)}D_s\pi\pi$ 非共振 | 四体 | 与信号同末态 | Dalitz 拟合里作为本底 PDF |
| $B\to\bar D^{(*)}D_{s1}(2536)$ | $D_{s1}(2536)\to D^*K$ | $K$ 误认为 $\pi$ | $D_{s1}$ 质量窗；PID |
| $B\to\bar D^{(*)}D_s^*\pi$ | $D_s^*\to D_s\gamma/\pi^0$ | $\gamma/\pi^0$ 漏掉 | 重建 $D_s^*$ 做 veto/控制 |
| $D_s$ 组合本底 | $D_s$ sideband | 随机组合 | $D_s$ 质量窗 + 顶点 |
| $B^+\leftrightarrow B^0$ 交叉 | $D^{*0}$ vs $D^{*-}$ | 误判 B 类型 | 分开拟合；PID |
| $\tau^+\tau^-$ | 低多重数 | 通过松 cut | $n_{\rm tracks}$、B 质量 |

### 1.3 组合本底

- $D_s$ sideband：1.80–1.90、2.02–2.12 GeV；
- $D^0$ sideband：1.75–1.82、1.91–1.98 GeV；
- 随机 $\pi^+\pi^-$ 对；
- 用 $D_{s1}$ sideband 估计。

---

## 2. ROE 与连续本底变量

```python
ma.buildRestOfEvent("Bc:all", path=main)
ma.buildContinuumSuppression("Bc:all", "all", path=main)

ma.buildRestOfEvent("Bn:all", path=main)
ma.buildContinuumSuppression("Bn:all", "all", path=main)
```

> 必须先 `buildRestOfEvent`，再 `buildContinuumSuppression`；否则 ROE 变量为 0/NaN。

| 变量 | 含义 | 典型 cut |
|---|---|---|
| `R2` | Fox-Wolfram 比，越接近 0 越“球” | $<0.4$ |
| `cosTBTO` | B thrust 与 ROE thrust 的夹角余弦 | $\lvert\cdot\rvert<0.8$ |
| `thrust` | 事件 thrust | 配合 BDT |
| `foxWolframR2` | 另一套 Fox-Wolfram | 配合 BDT |
| `cleoConeThrust0..8` | CLEO cones | 配合 BDT |
| `KSFWVariables(hso00)` 等 | KSFW moments | 配合 BDT |
| `nTracks` | 事件径迹数 | $>4$ |

> 变量名是 **`cosTBTO`**，不是 `cosThetaT`。`cosThetaT` 是老 Belle 分析里的叫法。

---

## 3. FastBDT 训练

### 3.1 训练样本

| 样本 | 选择 | 标签 |
|---|---|---|
| Signal MC | $B\to\bar D^{(*)}D_{s1}$，$D_{s1}\to D_s\pi\pi$，truth-matched | `isSignal=1` |
| $B\bar B$ generic | 通过同样重建，truth 不是信号 | `isSignal=0` |
| $q\bar q$ generic | 通过同样重建 | `isSignal=0` |

> 信号和本底分别用 `basf2_mva_merge_mc` 合并；训练/测试按 8:2 或 k-fold 切分。不要用同一批 MC 事件同时训练和测试。

### 3.2 输入变量

第一版推荐：

```text
R2, cosTBTO, thrust, foxWolframR2,
cleoConeThrust0, cleoConeThrust1, cleoConeThrust2,
KSFWVariables(hso00), KSFWVariables(hso02), KSFWVariables(hso04),
nTracks,
B_pstar, B_cosTheta,
Ds1_pstar, Ds1_chiProb,
Ds_sigDist, Ds_pstar,
D0_pstar, Dst_pstar
```

**不要放：**

- `Ds1_M`
- $m(\pi\pi)$
- $m(D_s\pi)$
- `Mbc`
- `deltaE`

原因：这些是拟合变量；如果 BDT 用它们训练，会把信号/本底形状 sculpt 掉，拟合模型不自洽。

### 3.3 训练命令

```bash
# 1) 合并信号/本底，并切训练/测试
basf2_mva_merge_mc \
  -s signal_ntuple.root \
  -b bkg_ntuple.root \
  -o train.root \
  --ftest 0.2

# 2) 训练 FastBDT
basf2_mva_teacher \
  --datafiles train_train.root \
  --treename tree \
  --identifier Ds1_BDT.root \
  --variables R2 cosTBTO thrust foxWolframR2 nTracks \
              B_pstar B_cosTheta Ds1_pstar Ds1_chiProb \
              Ds_sigDist Ds_pstar D0_pstar Dst_pstar \
  --target_variable isSignal \
  --method FastBDT

# 3) 评估（ROC、重要度、overtraining）
basf2_mva_evaluate.py \
  -id Ds1_BDT.root \
  -data train_test.root \
  -tree tree \
  -out bdt_report.zip
```

> 参数名以你环境里的 `basf2_mva_teacher --help` 为准。

### 3.4 在 basf2 中应用

```python
mva = b2.register_module("MVAExpert")
mva.param("listNames", ["Bc:all", "Bn:all"])
mva.param("extraInfoName", "BDT")
mva.param("identifier", "Ds1_BDT.root")
main.add_module(mva)
```

**常见坑**：训练和应用变量名必须完全一致；release/globaltag 不一致可能直接 segfault。用同一个 release 训练和应用。

### 3.5 BDT cut 优化

- 扫 `BDT > x`；
- 目标函数：$S/\sqrt{S+B}$（先），或 Punzi（低统计）；
- 在数据 sideband 上检查本底抑制；
- 不要用数据信号区选 cut；
- 报告：信号效率、$B\bar B$ 剩余、$q\bar q$ 剩余、$S/B$、$S/\sqrt{S+B}$。

---

## 4. FEI / tag side

FEI（Full Event Interpretation）可以重建另一个 B，提供 tag-side 信息。

- 优点：压连续本底、判断 B 味道；
- 缺点：效率低、CPU 高；
- 对本分析，信号 B 已全重建，**基线不需要 FEI**；
- 建议把 FEI 作为系统误差/交叉检验，而不是默认要求。

Flavor Tagger 也不需要：B 的电荷由 $D_{s1}$ 和 $\bar D$ 的电荷直接决定。

---

## 5. 数据驱动本底估计

- $D_{s1}$ sideband：2.40–2.44、2.48–2.52（避开 2.536 的 $D_{s1}(2536)$）；
- $M_{\rm bc}$ sideband：5.20–5.26；
- $\Delta E$ sideband：$0.10<\lvert\Delta E\rvert<0.20$；
- 用 sideband 拟合本底形状，再外推到信号区；
- 对 $B\bar B$ 本底，用 MC 归一化 + 数据 sideband 修正；
- 对 peaking background（例如 $B\to\bar D^*D_s^*\pi$），在拟合里加 Gaussian/模板，或做 veto。

---

## 6. 系统误差

| 来源 | 估计方法 | 初始量级 |
|---|---|---|
| Tracking | 控制样本 $D_s\to\phi\pi$、$D^0\to K\pi$ | 1–2% / track |
| PID | `PIDCalibrationWeights` / 数据控制样本 | 1–3% |
| $\gamma/\pi^0$ | $e^+e^-\to\gamma\gamma$、$\pi^0\to\gamma\gamma$ | 2–5% |
| BDT | 变 cut、data/MC 重加权、不同训练样本 | 2–5% |
| 本底模型 | 变 PDF、sideband 范围 | 3–10% |
| 信号模型 | 变 BW 参数、分辨率、B 质量约束 | 2–5% |
| MC 统计 | bootstrap / 子样本 | 1–5% |
| 亮度 | 官方 | 0.7%（绝对分支比）；比值抵消 |

> 做比值 $R$ 时，luminosity、tracking、PID 的很多误差会抵消；这是为什么推荐先测相对分支比。

---

## 7. 检查清单

- [ ] ROE 在 `buildContinuumSuppression` 之前构建；
- [ ] BDT 输入没有拟合变量；
- [ ] 训练/测试样本独立；
- [ ] 有 ROC、overtraining、变量重要度；
- [ ] 数据 sideband 上检查 BDT 分布；
- [ ] BDT cut 用 MC + sideband 优化；
- [ ] 系统误差表包含 BDT、PID、$\gamma/\pi^0$、本底模型。
