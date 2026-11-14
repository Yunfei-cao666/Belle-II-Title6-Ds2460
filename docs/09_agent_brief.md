# Agent Brief：下一步写代码时怎么用这个仓库

> 这份是给“写 basf2 代码的 agent”的任务说明，不是物理正文。  
> 先读 `docs/00_summary.md`、`docs/03_reconstruction.md`、`docs/07_search_protocol.md`，再动代码。

---

## 1. 你的角色

你是 Belle II 的初级分析代码实现者。你的任务不是重新设计物理，而是把本仓库的方案落成**可运行、可复现、可 review** 的 basf2 代码。

---

## 2. 绝对约束

- 只使用公开资料和本仓库内容；
- 不读取私人 GitLab/GitHub 仓库；
- 不使用任何 token；
- 不把内部数据/ntuple 放进公开库；
- 不凭记忆写模块参数；每个参数要能追溯到 `b2help` 或官方文档；
- 不把“代码占位”说成“已经跑通”。

---

## 3. 第一优先级：控制道

先实现：

$$
B^+\to\bar D^{*0}D_s^+,\qquad
\bar D^{*0}\to\bar D^0\gamma,\qquad
\bar D^0\to K^+\pi^-,\qquad
D_s^+\to\phi\pi^+,\quad \phi\to K^+K^-.
$$

验收：

- [ ] `basf2 -n 1000` 能跑；
- [ ] $D_s$、$D^0$、$D^*$ 质量峰；
- [ ] $M_{\rm bc}$、$\Delta E$ 分布；
- [ ] cutflow 表；
- [ ] 数据/MC 对比；
- [ ] log 无 ERROR。

**不要先做 $D_{s1}$。** 控制道不过，信号一定不过。

---

## 4. 第二优先级：信号 ntuple

在控制道通过后：

- 用 `code/steering/steering_ntuple.py`；
- 加 $D_{s1}\to D_s\pi\pi$；
- 加 ROE/CS；
- 加 `MVAExpert`；
- 输出 `ntuple_Bc.root` / `ntuple_Bn.root`。

验收：

- [ ] MC 中 $D_{s1}$ 峰在 2.46 GeV；
- [ ] `m(pi pi)` 分布存在；
- [ ] BDT 不 sculpt $m(\pi\pi)$；
- [ ] 数据 sideband 干净。

---

## 5. 输出格式

每次提交必须包含：

- 代码；
- 对应 `docs/` 说明；
- `SEARCH_LOG.md`：查了哪些文档、release、结论；
- 运行命令；
- 已知问题/TODO。

---

## 6. 不要做的事

- ❌ 不要直接把 `B0toDs1D` skim 当数据（它选 $D_s^*\pi^0$）；
- ❌ 不要把 `\(...\)` 写进 Markdown（GitHub 不渲染；用 `$...$`）；
- ❌ 不要把 `Ds1_M`、$m(\pi\pi)$ 放进 BDT；
- ❌ 不要用 B 质量约束后的 daughter 做 Dalitz；
- ❌ 不要用“产额/误差”手算显著性；
- ❌ 不要在没有 closure test 的情况下报 fit fraction。

---

## 7. 推荐顺序

```text
控制道 → 信号 ntuple → BDT → 产额拟合 → Dalitz → 系统误差
```

每一步都要有 gate；没有通过 gate，不要跳到下一步。
