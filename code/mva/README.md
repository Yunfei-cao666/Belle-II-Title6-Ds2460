# MVA skeleton

`train_bdt.sh` 是 FastBDT 的训练骨架。

## 输入

- `signal_ntuple.root`：signal MC 的 ntuple，含 `isSignal=1`；
- `bkg_ntuple.root`：generic $B\bar B$ + $q\bar q$，含 `isSignal=0`；
- 两个文件的 tree 名都为 `tree`，变量名一致。

## 运行

```bash
bash train_bdt.sh
```

## 变量

```text
R2 cosTBTO thrust foxWolframR2 nTracks
B_pstar B_cosTheta Ds1_pstar Ds1_chiProb
Ds_sigDist Ds_pstar D0_pstar Dst_pstar
```

**不要**把 `Ds1_M`、$m(\pi\pi)$、$M_{\rm bc}$、`deltaE` 放进去，否则会 sculpt 拟合变量。

## 输出

- `Ds1_BDT.root`：权重文件；
- `bdt_report.zip`：ROC、重要度、overtraining 检查。

## 在 basf2 中应用

在 `steering_ntuple.py` 里取消注释：

```python
mva = b2.register_module("MVAExpert")
mva.param("listNames", ["Bc:all", "Bn:all"])
mva.param("extraInfoName", "BDT")
mva.param("identifier", "Ds1_BDT.root")
main.add_module(mva)
```

## 注意

- 训练和应用必须用同一个 release/globaltag；
- 变量名不一致可能直接 segfault；
- 先用 `basf2_mva_info Ds1_BDT.root` 检查权重文件；
- 不要用数据信号区选 BDT cut。
