# MC production skeleton

## 文件

- `signal_decay_DsJ.dec`：EvtGen decay-file 骨架；
- 每个信号模式单独生成，不要把所有模式混在一个样本里。

## 五个样本

1. \(D_{sJ}(2317)^+\to D_s^+\pi^0\)
2. \(D_{sJ}(2457)^+\to D_s^{*+}\pi^0\)
3. \(D_{sJ}(2457)^+\to D_s^+\gamma\)
4. \(D_{sJ}(2457)^+\to D_s^+\pi^+\pi^-\)
5. \(D_{s1}(2536)^+\to D_s^+\pi^+\pi^-\)（对照）

## 产生方式

- 优先用官方 MC 生产工具/生产请求；
- 如果官方 generic \(c\bar c\) 含 \(D_{sJ}\) 且统计足够，可 truth-match 使用；
- 否则生成 dedicated signal MC；
- 用官方 detector simulation + reconstruction；
- 保存 truth 信息。

## 不要做

- 不要把 Belle 2003 MC 当 Belle II MC；
- 不要把 generic inclusive 全部事件当信号效率分母；
- 不要把四个模式混在一个样本里做 cross-feed；
- 不要在没有 truth matching 的情况下用 generic MC 当 signal。

## 下一步

- [ ] 确认官方 generic \(c\bar c\) 是否含 \(D_{sJ}\)；
- [ ] 确认统计量；
- [ ] 生成/申请五个 dedicated samples；
- [ ] 做 truth matching 和效率；
- [ ] 填 cross-feed 矩阵。

详细说明见 `docs/12_mc_production_plan.md`。
