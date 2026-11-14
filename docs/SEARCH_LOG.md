# SEARCH LOG

> 记录本方案在编写时查过的公开资料。  
> 具体 release 参数以 KEKCC 上的 `b2help` 为准。

## 2026-11-15

| 主题 | 来源 | 结论 | 置信度 |
|---|---|---|---|
| `reconstructDecay` / `variablesToNtuple` | <https://software.belle2.org/development/sphinx/analysis/doc/MAWrappers.html> | 组合用 `ParticleCombiner`；ntuple 用 `VariablesToNtuple` | 高 |
| `TreeFitter` | <https://software.belle2.org/development/sphinx/analysis/doc/TreeFitter.html> | `massConstraint`、`updateAllDaughters`、`conf_level`；不要对 MC truth 粒子 fit | 高 |
| 变量 `Mbc` / `deltaE` | <https://software.belle2.org/development/sphinx/analysis/doc/Variables.html> | `Mbc` 是 beam-constrained mass；`deltaE = E - E_beam` | 高 |
| 连续本底变量 | 同上 | `R2`、`cosTBTO`、`thrust`、`foxWolframR2`、CLEO cones、KSFW | 高 |
| `buildContinuumSuppression` | MAWrappers | 必须先 `buildRestOfEvent`；mask 用 `all` | 高 |
| `MVAExpert` | <https://software.belle2.org/development/sphinx/mva/doc/index-01-mva.html> | `identifier` 可以是本地 `.root` 或数据库名；变量名必须一致 | 高 |
| FastBDT 训练 | 同上 | `basf2_mva_merge_mc` → `basf2_mva_teacher` → `basf2_mva_evaluate.py` | 高 |
| Skim `B0toDs1D` | <https://software.belle2.org/development/sphinx/skim/doc/02-physics.html> | code 14160200；选 $D_{s1}\to D_s^*\pi^0$，**不包含** $D_{s1}\to D_s\pi\pi$ | 高 |
| Skim `BtoDsDsst_Kpi_KK` | 同上 | code 14121403；用于 $D_s\to\phi\pi/K^{*0}K/K_S^0K$，不是本 B 拓扑 | 高 |
| `b2luigi` | <https://b2luigi.belle2.org/starterkit/Ex07_basf2_analysis.html> | `Basf2PathTask` 新 import 路径；版本间会变 | 中 |
| LHCb 论文 | <https://doi.org/10.1016/j.scib.2025.02.025> | 9 fb$^{-1}$，约 800 事件，$\pi\pi$ 双峰 | 高 |

## 待验证

- [ ] 当前 release 的 `b2help ParticleCombiner` / `TreeFitter` / `MVAExpert`；
- [ ] `B0toDs1D` 在当前 campaign 的 skim 名称；
- [ ] `b2luigi` 的 `Basf2PathTask` import 路径；
- [ ] `MVAExpert` 的 `identifier` 参数名；
- [ ] `VariablesToNtuple` 的 `storeEventType` 是否可用。

> 未使用任何私人 GitLab/GitHub 仓库、内部 ntuple 或 token。
