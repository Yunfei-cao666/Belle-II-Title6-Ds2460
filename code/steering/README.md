# Steering skeleton

`steering_ntuple.py` 是本项目的 basf2 ntuple 骨架。

## 状态

- **未在 KEKCC 上验证**；
- cut 是初始值，必须用 MC 优化；
- 代码里的 `Bc:all` / `Bn:all` 是 charged/neutral B 的合并列表；
- 默认只做 $D_s\to\phi\pi$ 基线。

## 运行

```bash
basf2 -n 1000 steering_ntuple.py
```

批量运行时，由 `b2luigi` 传入输入文件列表，不要手改路径。

## 输出

- `ntuple_Bc.root`，tree `Bc`；
- `ntuple_Bn.root`，tree `Bn`。

## 先检查什么

1. log 没有 `ERROR`；
2. `D_s`、`D^0`、$D^*$ 质量峰；
3. $D_{s1}$ 在 MC 中有峰；
4. `Mbc`、`deltaE` 在信号区；
5. `R2`、`cosTBTO` 不是 NaN。

## 已知 TODO

- [ ] 用 `b2help` 核对每个模块参数；
- [ ] 用 MC 优化所有 cut；
- [ ] 加 `MVAExpert`；
- [ ] 加 `b2luigi` 输入；
- [ ] 加数据/MC 对比；
- [ ] 加 `nTracks`、`R2`、`cosTBTO` 的 cut；
- [ ] 处理多候选；
- [ ] 加系统误差权重。

> 不要直接把这个脚本当生产代码跑全数据。先控制道，再信号。
