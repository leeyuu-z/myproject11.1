# 第一阶段复现

在现有隔离环境使用/workspace/finance-paper，不新建Git worktree。

```bash
cd /workspace/finance-paper
python3 src/01_inventory.py --root data/raw --output reports/raw_inventory.json
```

脚本只读原始文件，输出每文件SHA256、大小、实际行数/字段/缺失数及错误。CSV按UTF-8-sig/GB18030尝试；XLSX每张表读取，XLS需另装并固定xlrd，ZIP仅列成员不解压，PDF只盘点不声称已提取表格。无文件时状态BLOCKED，不生成示例数据。未来大文件应分块读取，手工复核字段与缺失码。

当前pandas/openpyxl/numpy/matplotlib版本已记录requirements.txt；statsmodels、linearmodels尚未安装，第一阶段不需要。绘图时设置MPLCONFIGDIR=/tmp/finance-paper-matplotlib。实证阶段确认后单独固定所需依赖。未创建02—08阶段占位脚本，避免把未实现流程标成完成。

目录：data/raw为不可修改的原始数据（脚本不写入），interim/processed为将来输出；src处理脚本；analysis后续模型；literature文献；docs来源与方法；reports研究报告；outputs表图；tests后续必要验证。

不要提交受限原始数据。gitignore已排除全部data与outputs内容（保留目录标记）。后续盘点报告含文件名及字段，公开前也应检查许可与隐私。字段模板只有表头，不是观测数据。
