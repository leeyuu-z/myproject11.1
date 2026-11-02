# myproject11.1

商业银行数字化转型与经营效率研究

金融学本科毕业论文的数据筹备与可复现分析项目。

拟研究题目：《数字化转型对商业银行经营效率的影响研究——基于中国上市银行的实证分析》。

## 当前状态

**BLOCKED：缺少真实数据，尚未运行正式实证分析。**

- 北大商业银行数字化转型指数已邮件申请，尚未收到回复。
- 学校没有可用CSMAR授权，财务数据候选来源改为银行官方年报。
- 当前没有真实银行年度观测、回归结果或论文结论。
- 官方网页核验存在环境访问限制，来源说明中已区分附件线索与独立核验证据。

## 项目结构

- `data/raw/`：原始数据；保持不变，不上传受限文件。
- `data/interim/`、`data/processed/`：后续处理数据。
- `src/`：可复现处理脚本。
- `analysis/`：后续实证分析。
- `docs/`：来源清单、变量字典、申请邮件、采集方案与映射模板。
- `reports/`：可行性汇报与数据质量记录。
- `literature/`：后续文献资料。
- `outputs/`：后续表格与图形。
- `tests/`：后续必要验证。

## 本地盘点

使用Python 3.11及以上，在项目根目录运行：

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/01_inventory.py --root data/raw --output reports/raw_inventory.json
```

原始目录为空时脚本报告BLOCKED，不生成示例数据。安装步骤为依赖复现说明；当前环境已验证盘点脚本运行，未声称在全新环境完整重装验证。

先阅读 `docs/next_actions.md`、`docs/annual_report_fallback.md` 和 `reports/给曾老师的数据来源与可行性汇报.md`。取得真实数据并通过质量检查、确认模型设计后才开展双向固定效应回归。

## 数据使用

代码仓库不包含数据库原始数据。北大指数、CSMAR及其他受限资料的使用与共享须遵守授权；`.gitignore`默认排除数据及图表内容，仅保留目录标记。来源日志与空表头模板不是银行观测数据。
