# b2luigi skeleton

`tasks.py` 是一个最小任务骨架：一个输入文件 → 一对 ntuple。

## 使用

```bash
python tasks.py
```

或在 Python 里：

```python
from tasks import Ds1NtupleTask
Ds1NtupleTask(input_file="/path/to/file.root").run()
```

## 注意

- `Basf2PathTask` 的 import 路径在 b2luigi 版本间变过：
  - 新版本：`from b2luigi.contrib.basf2 import Basf2PathTask`
  - 旧版本：`from b2luigi.basf2_helper import Basf2Task`
- `batch_system` 可选 `"local"`、`"kekcc"`、`"lsf"`、`"htcondor"`，以你的环境为准。
- 大批量时，每个 job 只处理一个文件，输出唯一文件名。
- 不要把 `results/`、`*.root` 提交到 Git。

## 下一步

- [ ] 用真实文件列表替换 `input_file`；
- [ ] 加 `requires()` 依赖；
- [ ] 加合并 ntuple 的 task；
- [ ] 把 `release`、`globaltag` 写进配置。
