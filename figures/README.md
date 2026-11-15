# Figures

这些图是 **Belle 2003 $D_{sJ}$ 分析的玩具复现（toy reproduction）**，用于方案/组会，不是对 Belle 或 Belle II 原始数据的重新分析。

- 产额、质量、分辨率来自 Belle 2003 公开论文；
- 本底形状和统计涨落是 toy；
- 每张图都带有 “toy reproduction / not raw data” 标注；
- **不要**去掉标注后当成真实测量结果发表。

## 生成

```bash
python code/figures/make_dsj_figures.py
```

输出：

- `fig_dm_dspi0.png`
- `fig_dm_dsstpi0.png`
- `fig_dm_dsgamma.png`
- `fig_dm_dspipi.png`
- `fig_combined.png`
- `fig_yields.png`
- `fig_chain.png`

## 真实分析需要

- Belle/Belle II 的 ntuple；
- data/MC 对比；
- 拟合结果和系统误差；
- 不能直接用这些 toy 图代替。
