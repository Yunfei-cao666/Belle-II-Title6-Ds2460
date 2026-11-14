# Fit skeleton

`fit_yield.py` 是 $m(D_s\pi\pi)$ 的 RooFit 产额拟合骨架。

## 运行

```bash
python fit_yield.py
```

需要 `ntuple_Bc.root`，tree 名 `Bc`，分支 `Ds1_M`。

## 模型

- Signal: `RooVoigtian`（BW $\otimes$ Gaussian）；
- Background: `RooExponential`；
- Extended likelihood。

## 注意

- `RooVoigtian` 的 `width`/`sigma` 单位是 **GeV**，不是 MeV；
- `Ds1_M` 分支来自 `steering_ntuple.py` 的别名；
- 初版把 `width` 固定为 1.5 MeV；统计量大再放开；
- 真实分析还要加 $M_{\rm bc}$、$\Delta E$ 二维拟合和 sideband 约束；
- 不要用“产额/误差”手算显著性，用 RooStats。

## 下一步

- [ ] 加 $M_{\rm bc}$ / $\Delta E$ 二维模型；
- [ ] 加 $B^+$/$B^0$ 同时拟合；
- [ ] 加系统误差；
- [ ] 加 Dalitz 振幅（另写 `fit_dalitz.py`）。
