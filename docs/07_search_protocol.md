# 给后续 Agent 的 basf2 文档检索协议

> 这一章是写给“下一步写代码的 agent”看的，不是物理分析正文。  
> 目标：让 agent 在**公开、可引用、可版本化**的 basf2 文档中查找模块、参数、skim、Data Production 和示例，而不是凭记忆写代码。

---

## 1. 原则

1. **只查公开资料**：公开 basf2 文档、公开 GitHub/GitLab 的 basf2 代码、公开论文、官方示例。
2. **不查私人库**：不读取其他分析者的私有 GitLab/GitHub 仓库、内部 ntuple、内部会议材料，除非项目负责人明确授权，并在私有环境使用。
3. **不把 token 写进任何文件**：不使用别人的 personal access token。
4. **每条结论要有来源**：URL、release、日期、模块名、参数名。
5. **版本必须记录**：basf2 的 `release`、`globaltag`、skim campaign、文档版本。
6. **找不到就写 TODO**：不要猜模块参数；在代码里用 `TODO(agent): verify` 标记。

---

## 2. 信息来源优先级

| 优先级 | 来源 | 用途 | 备注 |
|---|---|---|---|
| 1 | 当前 release 的 Sphinx 文档 | 模块、参数、变量、示例 | 最权威 |
| 2 | `b2help` / `b2help-recommendation` | 本机安装版本的模块参数、推荐 cut | 必须在 KEKCC 上跑 |
| 3 | 公开 `basf2` GitLab/GitHub 源码 | 模块实现、默认参数 | 只读；不复制他人分析代码 |
| 4 | Online Book / tutorial | 入门、示例 | 可能滞后 |
| 5 | `questions.belle2.org` | 具体报错、经验 | 公开问答 |
| 6 | 公开论文 / PDG | 物理输入 | 引用 DOI |
| 7 | 内部 Data Production / Analysis 页面 | 数据、skim、校准 | **需要权限；不要在公开库复制内容** |

> 如果第 1–3 条能回答，就不要用第 7 条。  
> 公开库只写“入口”和“检索方法”，不复制内部页面正文。

---

## 3. 标准检索流程

### Step 1：确定对象和关键词

例如：

```text
对象：D_s1 -> D_s pi pi
关键词：
  D_s1, Ds1, D_s1(2460), Ds2460
  D_s -> phi pi, D_s -> K* K, D_s -> K_S K
  B -> D* D_s1, B -> D D_s1
  Mbc, deltaE, TreeFitter, ParticleCombiner
  ContinuumSuppression, ROH, R2, cosTBTO
  MVAExpert, FastBDT
```

### Step 2：查当前 release 文档

- 先查 `analysis/doc/MAWrappers.html`：`reconstructDecay`、`applyCuts`、`variablesToNtuple`、`buildRestOfEvent`、`buildContinuumSuppression`。
- 再查 `analysis/doc/Variables.html`：变量名、定义、是否依赖其他 module。
- 再查 `analysis/doc/TreeFitter.html`：`massConstraint`、`updateAllDaughters`、`conf_level`。
- 再查 `mva/doc/`：`MVAExpert`、`basf2_mva_teacher`、weightfile identifier。
- 再查 `skim/doc/`：skim 名称、code、重建模式。

### Step 3：查本机 `b2help`

在 KEKCC 上：

```bash
b2help ParticleCombiner
b2help TreeFitter
b2help MVAExpert
b2help-recommendation
```

`b2help` 给出的是**当前安装版本**的参数，优先级高于网页旧文档。

### Step 4：查公开源码

- 只读公开的 `basf2` 仓库；
- 搜索模块名、参数名；
- 看默认值和单位；
- 不复制其他分析仓库的代码。

### Step 5：交叉验证

同一个参数至少在两个来源确认：

- Sphinx 文档；
- `b2help`；
- 源码；
- 公开 tutorial。

如果冲突，以**当前 release 的 `b2help` + 源码**为准，并记录冲突。

### Step 6：写入记录

每个模块/参数记录：

```yaml
topic: TreeFitter mass constraint
source: https://software.belle2.org/development/sphinx/analysis/doc/TreeFitter.html
release: light-2604-jellyfish
module: TreeFitter
parameter: massConstraint
value: ["B+"]
why: constrain B mass; do not use for Dalitz daughters
confidence: high
todo: verify on KEKCC
```

---

## 4. Data Production / b2luminosity / skim 的检索

### 4.1 Data Production

需要查：

- mdst/uDST 的生产 campaign；
- skim 的生产列表；
- run 范围、数据质量；
- 校准/globaltag；
- 亮度（b2luminosity）。

公开入口：

- <https://software.belle2.org/development/sphinx/>
- <https://software.belle2.org/development/sphinx/skim/doc/>
- <https://software.belle2.org/development/sphinx/online_book/>

内部页面（需权限）：

- Data Production；
- b2luminosity；
- skim 运行/校准；
- Performance recommendations。

> 公开库只记录“怎么查”，不复制内部页面正文。

### 4.2 Skim

检索关键词：

```text
skim B0toDs1D
skim Ds1
skim BtoDsDsst
skim Hadronic
skim BHadronic
skim SystematicsCombinedHadronic
```

需要确认：

- skim 的重建模式是否包含 $D_{s1}\to D_s\pi\pi$；
- 是否要求 $\pi^0$ / $\gamma$；
- skim code / LFN；
- 适用于哪个 campaign。

**已知坑**：`B0toDs1D`（14160200）选的是 $D_{s1}\to D_s^*\pi^0$，不包含 $D_{s1}\to D_s\pi\pi$。不要因为它名字像就直接用。

### 4.3 Analyses 包

- `Analyses` 里是分析者上传的包；
- 公开库不复制别人的分析代码；
- 如果要用，先确认 license/作者许可；
- 内部笔记只在私有环境使用，并记录授权。

---

## 5. 历史版本

Belle II 软件更新很快。检索时必须记录：

```text
release: light-2604-jellyfish
globaltag: ...
date: 2026-...
```

规则：

1. 不要混用不同 release 的模块参数；
2. 如果网上文档是 `development`，而本机是 `light-2503`，以本机 `b2help` 为准；
3. 历史版本用于理解 API 变化，不用于生产；
4. 在 `docs/` 里记录“这个参数在哪个 release 改过”。

---

## 6. 给 Agent 的输出格式

Agent 写完代码后，必须同时写：

- `docs/` 里对应的说明；
- 代码里的 `TODO(agent): verify`；
- 一个 `SEARCH_LOG.md`（可放在 `docs/` 下），记录：

```text
日期：
release：
查询：
来源：
结论：
置信度：
未解决：
```

没有 `SEARCH_LOG.md` 的代码，不算完成。

---

## 7. 禁止事项

- ❌ 不使用别人的 GitHub/GitLab token；
- ❌ 不把 token、cookie、proxy 密码写进仓库；
- ❌ 不读取私人 GitLab 仓库；
- ❌ 不复制其他分析者的内部笔记到公开库；
- ❌ 不把 Belle II 内部 ntuple/数据上传到公开 GitHub；
- ❌ 不凭记忆写模块参数；
- ❌ 不把“网上示例”当成当前 release 的保证。

---

## 8. 一句话

**Agent 的任务不是“背 basf2 API”，而是“在公开、版本化的文档里找到证据，并把证据写进代码和文档”。**
