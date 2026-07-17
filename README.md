# 电商用户数据分析实训种子项目

本项目用于第3～5天个人实训。每名学生从种子项目开始，独立完成Notebook和输出成果，并推送到自己的GitHub仓库。

## 学习路径

```text
Day03 Pandas商品数据探索
        ↓
Day04 电商用户数据清洗与预处理
        ↓
Day05 电商用户多维分析
```

Day03使用淘宝商品数据，训练Pandas基础。Day04和Day05使用电商用户数据：Day04生成清洗结果，Day05必须读取Day04的输出。

## 项目结构

```text
.
├── data/
│   ├── 淘宝全品类全国数据.csv
│   └── E Commerce Dataset.xlsx
├── docs/
│   ├── day03_task.md
│   ├── day04_task.md
│   └── day05_student_manual.md
├── notebooks/
│   ├── day03_pandas_product_analysis.ipynb
│   ├── day04_pm_user_cleaning_project.ipynb
│   └── day05_pm_student_project.ipynb
├── output/
│   ├── day03_analysis/
│   ├── day04_project/
│   └── day05_analysis/
├── scripts/
│   └── validate_submission.py
├── .gitignore
├── requirements.txt
└── SUBMISSION_CHECKLIST.md
```

## 环境准备

建议使用Python 3.10或更高版本。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Windows PowerShell激活环境：

```powershell
.venv\Scripts\Activate.ps1
```

## 完成顺序

### Day03

打开`notebooks/day03_pandas_product_analysis.ipynb`，完成检查点1～6，并输出：

```text
output/day03_analysis/category_summary.csv
output/day03_analysis/province_summary.csv
```

### Day04

打开`notebooks/day04_pm_user_cleaning_project.ipynb`，完成清洗流程，并输出：

```text
output/day04_project/ecommerce_customer_cleaned.csv
output/day04_project/data_quality_before.csv
output/day04_project/data_quality_after.csv
output/day04_project/cleaning_log.csv
output/day04_project/outlier_report.csv
output/day04_project/business_rule_report.csv
```

### Day05

只有Day04清洗结果生成后，才能运行`notebooks/day05_pm_student_project.ipynb`。最终输出：

```text
output/day05_analysis/overall_metrics.csv
output/day05_analysis/segment_analysis.csv
output/day05_analysis/cross_analysis.csv
```

## 自检

克隆项目后、开始任务前运行：

```bash
python scripts/validate_seed.py
```

完成全部任务后运行：

```bash
python scripts/validate_submission.py
```

验证脚本只检查文件结构、Notebook格式和CSV基本质量，不能替代教师对代码、指标与结论的评价。

## 提交到个人GitHub仓库

教师发布种子仓库后，每名学生执行：

```bash
git clone <教师提供的种子仓库地址>
cd ecommerce-user-analysis-seed
git remote rename origin upstream
git remote add origin <你的个人GitHub仓库地址>
git push -u origin main
```

完成每日任务后：

```bash
git add notebooks output
git commit -m "complete day03 pandas analysis"
git push
```

建议Day03、Day04和Day05分别提交，提交信息应准确描述本次完成的内容。

## 学术诚信

- 每名学生独立完成代码、结果和结论；
- 可以讨论方法，但不得复制他人的Notebook或输出文件；
- 教师会通过口头提问检查字段含义、指标分母和结论边界；
- 不要把教师演示Notebook或教师参考答案加入个人仓库。

## 数据提醒

本项目数据仅用于课程实训。教师在将种子项目发布到公开GitHub仓库前，应确认数据文件的再分发许可；许可不明确时建议使用私有仓库。
