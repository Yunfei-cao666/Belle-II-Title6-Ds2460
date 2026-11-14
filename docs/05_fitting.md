# 拟合：产额与 Dalitz 振幅

> 这一章分两部分：先用 RooFit 提取产额，再做 $D_{s1}\to D_s\pi\pi$ 的 Dalitz 振幅。  
> 不要一开始就写复杂的振幅拟合；先把产额、本底、效率搞明白。

---

## 1. 产额拟合

### 1.1 拟合变量

| 变量 | 信号 | 本底 | 用途 |
|---|---|---|---|
| $m(D_s\pi\pi)$ | Voigtian / BW $\otimes$ Gaussian | 指数 / Chebychev | 主拟合变量 |
| $M_{\rm bc}$ | Gaussian / Crystal Ball | ARGUS | B 质量 |
| $\Delta E$ | Gaussian / Crystal Ball | 指数 / Chebychev | B 能量 |
| $m(\pi\pi)$ | 不是产额拟合变量 | — | 留给振幅分析 |

推荐策略：

1. 先在 $M_{\rm bc}$ 信号区做 $m(D_s\pi\pi)$ 一维拟合，拿初始产额；
2. 再做 $M_{\rm bc}$ vs $\Delta E$ 二维拟合，约束本底；
3. 最后做 $B^+$ 和 $B^0$ 同时拟合，共享分辨率参数。

### 1.2 RooFit 代码骨架

```python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

f = ROOT.TFile.Open("ntuple_Bc.root")
tree = f.Get("Bc")

x = ROOT.RooRealVar("Ds1_M", "m(D_{s}#pi#pi)", 2.40, 2.52, "GeV")
x.setBins(60)

# 信号：Voigtian = BW ⊗ Gaussian
mean = ROOT.RooRealVar("mean", "mean", 2.4595, 2.450, 2.470)
width = ROOT.RooRealVar("width", "natural width [GeV]", 0.0015, 0.0001, 0.005)
sigma = ROOT.RooRealVar("sigma", "resolution [GeV]", 0.004, 0.001, 0.020)
width.setConstant(True)  # 初版固定 1.5 MeV；统计量大再放开
sig = ROOT.RooVoigtian("sig", "signal", x, mean, width, sigma)

# 本底：指数
tau = ROOT.RooRealVar("tau", "tau", -8.0, -50.0, -0.1)
bkg = ROOT.RooExponential("bkg", "background", x, tau)

# 产额
nsig = ROOT.RooRealVar("nsig", "N_{sig}", 100, 0, 1e6)
nbkg = ROOT.RooRealVar("nbkg", "N_{bkg}", 1000, 0, 1e6)

model = ROOT.RooAddPdf(
    "model", "sig+bkg",
    ROOT.RooArgList(sig, bkg),
    ROOT.RooArgList(nsig, nbkg),
    ROOT.kTRUE,  # 扩展似然：系数是产额
)

data = ROOT.RooDataSet("data", "data", tree, ROOT.RooArgSet(x))
model.fitTo(data, ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))

frame = x.frame(ROOT.RooFit.Title("B^{+} #rightarrow #bar{D}^{*0} D_{s1}^{+}"))
data.plotOn(frame, ROOT.RooFit.Name("data"))
model.plotOn(frame, ROOT.RooFit.Name("fit"))
frame.Draw()

c = ROOT.TCanvas("c", "c", 800, 600)
frame.Draw()
c.SaveAs("fit_Ds1_M.pdf")

print("N_sig =", nsig.getVal(), "+/-", nsig.getError())
```

> `RooVoigtian` 的 `width` 是自然宽度，单位必须和 `x` 一样是 GeV。  
> $D_{s1}$ 的 $\Gamma<3.5$ MeV，初版固定为 1.5 MeV；`sigma` 是探测器分辨率。

### 1.3 $M_{\rm bc}$ 拟合

```python
mbc = ROOT.RooRealVar("B_Mbc", "M_{bc}", 5.20, 5.30, "GeV")
mean_b = ROOT.RooRealVar("mean_b", "mean", 5.279, 5.275, 5.283)
sigma_b = ROOT.RooRealVar("sigma_b", "sigma", 0.0025, 0.001, 0.006)
sig_b = ROOT.RooGaussian("sig_b", "signal", mbc, mean_b, sigma_b)

m0 = ROOT.RooRealVar("m0", "endpoint", 5.2897)
c = ROOT.RooRealVar("c", "c", -20.0, -100.0, -1.0)
p = ROOT.RooRealVar("p", "p", -1.0)
p.setConstant(True)
bkg_b = ROOT.RooArgusBG("bkg_b", "argus", mbc, m0, c, p)

nsig_b = ROOT.RooRealVar("nsig_b", "N_{sig}", 100, 0, 1e6)
nbkg_b = ROOT.RooRealVar("nbkg_b", "N_{bkg}", 1000, 0, 1e6)
model_b = ROOT.RooAddPdf(
    "model_b", "sig+bkg",
    ROOT.RooArgList(sig_b, bkg_b),
    ROOT.RooArgList(nsig_b, nbkg_b),
    ROOT.kTRUE,
)
```

> 如果 $B^+$ 和 $B^0$ 的 $M_{\rm bc}$ 分辨率不同，分别拟合，或加一个共享的 `sigma` 比例参数。

### 1.4 显著性

- 用 `RooStats::ProfileLikelihoodCalculator` 或 `RooStats::HypoTestInverter`；
- 不要用“产额除以误差”手算显著性；
- 如果信号不显著，给 90% CL 上限。

---

## 2. Dalitz 振幅分析

### 2.1 运动学变量

三体衰变 $D_{s1}\to D_s(p_1)\pi^+(p_2)\pi^-(p_3)$ 只有两个独立变量：

$$
m^2(\pi^+\pi^-),\qquad m^2(D_s^+\pi^-).
$$

以及 helicity 角：

- $\theta_1$：在 $\pi\pi$ 静止系中，$\pi^+$ 与 $D_{s1}$ 方向的夹角；
- $\phi_1$：$D_{s1}\to D_s(\pi\pi)$ 与 $(\pi\pi)\to\pi\pi$ 两个衰变平面的夹角。

### 2.2 Isobar 模型

$$
\mathcal A(s_{12},s_{13})=\sum_i c_i\,A_i(s_{12})\,Y_{1m_i}(\theta_1,\phi_1).
$$

- $A_i$：共振线形（BW、Flatté、K-matrix）；
- $c_i$：复耦合；
- $Y_{1m}$：自旋 1 的角分布；对 scalar isobar（$f_0$），角因子是 $\cos\theta_1$；
- fit fraction：

$$
F_i=\frac{\int |c_i A_i|^2\,d\Phi}{\int |\sum_j c_j A_j|^2\,d\Phi}.
$$

### 2.3 建议的模型集合

1. **基线**：$f_0(500)+f_0(980)+f_2(1270)$（复现 LHCb 的常规 $\pi\pi$ 拟合）；
2. **K-matrix** $\pi\pi$ S-wave；
3. **加入 $T_{c\bar s}$**（标量、同位旋 1）和它的 isospin partner；
4. **模型无关矩**：不拟合，直接测 $\langle Y_{lm}\rangle$ 随 $m(\pi\pi)$ 的变化。

> LHCb 自己指出：$f_0(980)$、$f_2(1270)$ 的峰远在 $D_{s1}\to D_s\pi\pi$ 的运动学上限之外，所以“常规共振”拟合的物理可信度有限。  
> Belle II 不应只复现这个拟合，而应同时给出模型无关的 $m(\pi\pi)$ 双峰结构和多模型比较。

### 2.4 效率图

- 用**平 Dalitz（PHSP）**信号 MC 重建；
- 得到二维效率图 $\varepsilon(m^2_{\pi\pi},m^2_{D_s\pi})$；
- 用直方图或 `RooNDKeysPdf` 平滑；
- 在拟合 PDF 里乘上效率；
- 检查 Dalitz 边界附近效率是否太低；低效率区域要做系统误差。

### 2.5 拟合工具

- **RooFit**：适合产额拟合和不太复杂的自定义 PDF；
- **zfit**：Python 原生、灵活，适合复杂振幅和扫描；
- 建议：产额用 RooFit，Dalitz 用 zfit（或 RooFit + `RooFit::Minuit`）。

伪代码：

```python
for event in data:
    m2_pp, m2_Dspi = event.m2_pp, event.m2_Dspi
    amp = sum(c[i] * lineshape[i](m2_pp) * angular[i](m2_pp, m2_Dspi)
              for i in range(n_terms))
    pdf = abs(amp)**2 * efficiency(m2_pp, m2_Dspi)
    nll -= log(pdf / normalization)
```

### 2.6 背景

- 用 sideband 或 `RooStats::SPlot` 估计本底；
- 拟合时作为背景 PDF 或权重；
- 不要把 sideband 本底直接减掉而不传播误差。

### 2.7 Closure test

在拟合数据前，必须先用 MC 做 closure test：

1. 用已知模型生成 toy/MC；
2. 用同一模型拟合；
3. 检查是否能还原输入 fit fraction；
4. 再用不同模型拟合，检查偏差。

---

## 3. 结果与解释

| 结果 | 怎么读 |
|---|---|
| $N_{\rm sig}$ | 信号产额；用 $N_{\rm sig}/(\varepsilon\mathcal L)$ 或相对归一化道得到分支比 |
| $m(\pi\pi)$ 双峰 | 与 LHCb 比较；看峰位、相对高度、干涉 |
| fit fractions | 各分量占比；注意干涉项，fit fraction 之和可以小于 1 |
| $\Delta$NLL | 模型比较；不要只看 $\chi^2$ |
| $B^+$ vs $B^0$ | 同位旋一致性 |
| 系统误差 | 见 §4 |

---

## 4. 系统误差

| 来源 | 估计方法 | 初始量级 |
|---|---|---|
| Tracking | 控制样本 | 1–2% / track |
| PID | `PIDCalibrationWeights` | 1–3% |
| $\gamma/\pi^0$ | $e^+e^-\to\gamma\gamma$、$\pi^0\to\gamma\gamma$ | 2–5% |
| BDT | 变 cut、data/MC 重加权 | 2–5% |
| 本底模型 | 变 PDF、sideband 范围 | 3–10% |
| 信号模型 | 变 BW 参数、分辨率 | 2–5% |
| 振幅模型 | 变共振集合、K-matrix、$T_{c\bar s}$ | 主导（10–30%） |
| MC 统计 | bootstrap | 1–5% |
| 亮度 | 官方 | 0.7%（绝对分支比）；比值抵消 |

> 做比值 $R$ 时，luminosity、tracking、PID 的很多误差会抵消。

---

## 5. 盲分析

- 在 cut 和 BDT 优化完成前，blind $M_{\rm bc}$ 信号区（5.27–5.29）和 $D_{s1}$ 质量信号区（2.45–2.47）；
- 用 sideband 和 MC 做所有优化；
- 冻结选择后再 unblind；
- 振幅分析可以先 blind fit fraction，等效率/本底模型 review 后再打开。

---

## 6. 检查清单

- [ ] 产额拟合的 `width` 单位正确（GeV）；
- [ ] `RooAddPdf` 用扩展似然；
- [ ] 信号/本底 PDF 都有 sideband 约束；
- [ ] 振幅效率图来自 PHSP MC；
- [ ] 有 closure test；
- [ ] 有模型无关矩；
- [ ] 系统误差表完整；
- [ ] 盲分析流程已定义。
