"""只读盘点真实原始文件；不推断数据来源，不自动清洗或回归。"""
import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

SUPPORTED = {'.csv', '.xls', '.xlsx', '.dta', '.zip', '.pdf'}

def summarize(frame):
    return {'rows': len(frame), 'columns': [str(x) for x in frame.columns],
            'missing': {str(k): int(v) for k, v in frame.isna().sum().items()},
            'note': '缺失按pandas默认规则；数据库特殊缺失码需结合元数据另查。'}

def inspect_file(path, root):
    result = {'file': str(path.relative_to(root)), 'bytes': path.stat().st_size,
              'source': 'UNVERIFIED', 'sha256': None}
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    result['sha256'] = h.hexdigest()
    try:
        suffix = path.suffix.lower()
        if suffix == '.csv':
            for encoding in ('utf-8-sig', 'gb18030'):
                try:
                    frame = pd.read_csv(path, encoding=encoding, dtype=str)
                    result.update(encoding=encoding, **summarize(frame))
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError('无法按UTF-8或GB18030解码，请明确实际编码')
        elif suffix in ('.xlsx', '.xls'):
            with pd.ExcelFile(path) as book:
                result['sheets'] = {sheet: summarize(pd.read_excel(book, sheet_name=sheet, dtype=str))
                                    for sheet in book.sheet_names}
        elif suffix == '.dta':
            result.update(summarize(pd.read_stata(path, convert_categoricals=False)))
        elif suffix == '.zip':
            with zipfile.ZipFile(path) as archive:
                result['members'] = [{'name': x.filename, 'bytes': x.file_size} for x in archive.infolist()]
            result['note'] = '只列成员，未解压或统计内部表格。'
        else:
            result['note'] = 'PDF仅登记文件，未提取表格或核验内容。'
    except Exception as exc:
        result['inspection_error'] = f'{type(exc).__name__}: {exc}'
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('data/raw'))
    parser.add_argument('--output', type=Path, default=Path('reports/raw_inventory.json'))
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f'原始数据目录不存在：{root}')
    if args.output.resolve().is_relative_to(root):
        parser.error('盘点报告不得写入原始数据目录')
    files = sorted(x for x in root.rglob('*') if x.is_file() and x.suffix.lower() in SUPPORTED)
    records = [inspect_file(x, root) for x in files]
    report = {'generated_at_utc': datetime.now(timezone.utc).isoformat(), 'root': str(root),
              'data_status': 'BLOCKED' if not files else 'PENDING_QUALITY_REVIEW',
              'file_count': len(files), 'files': records,
              'note': '文件存在不代表数据真实、来源已核验或可以回归。空目录不能计算样本量。'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'盘点完成：{len(files)}个候选数据文件；状态{report["data_status"]}；{args.output}')
    if any('inspection_error' in x for x in records):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
