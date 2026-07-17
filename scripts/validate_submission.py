from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_NOTEBOOKS = [
    "notebooks/day03_pandas_product_analysis.ipynb",
    "notebooks/day04_pm_user_cleaning_project.ipynb",
    "notebooks/day05_pm_student_project.ipynb",
    "notebooks/day06_pm_student_visualization.ipynb",
]

REQUIRED_OUTPUTS = [
    "output/day03_analysis/category_summary.csv",
    "output/day03_analysis/province_summary.csv",
    "output/day04_project/ecommerce_customer_cleaned.csv",
    "output/day04_project/data_quality_before.csv",
    "output/day04_project/data_quality_after.csv",
    "output/day04_project/cleaning_log.csv",
    "output/day04_project/outlier_report.csv",
    "output/day04_project/business_rule_report.csv",
    "output/day05_analysis/overall_metrics.csv",
    "output/day05_analysis/segment_analysis.csv",
    "output/day05_analysis/cross_analysis.csv",
    "output/day06_visualization/chart_manifest.csv",
]

REQUIRED_IMAGES = [
    "output/day06_visualization/01_category_bar.png",
    "output/day06_visualization/02_behavior_scatter.png",
    "output/day06_visualization/03_ordered_line.png",
    "output/day06_visualization/04_composition_chart.png",
    "output/day06_visualization/day06_visualization_summary.png",
]

MANIFEST_COLUMNS = [
    "chart_id",
    "file_name",
    "business_question",
    "chart_type",
    "key_finding",
    "limitation",
]


def check_notebook(relative_path):
    path = ROOT / relative_path
    if not path.exists():
        return False, "文件不存在"

    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"JSON读取失败：{exc}"

    if nb.get("nbformat") != 4:
        return False, "不是nbformat 4"
    if not nb.get("cells"):
        return False, "没有单元格"

    error_outputs = []
    for index, cell in enumerate(nb["cells"]):
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                error_outputs.append(index)

    if error_outputs:
        return False, f"存在错误输出单元格：{error_outputs}"

    return True, f"cells={len(nb['cells'])}"


def check_csv(relative_path):
    path = ROOT / relative_path
    if not path.exists():
        return False, "文件不存在"

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        return False, f"CSV读取失败：{exc}"

    unnamed = [col for col in df.columns if str(col).startswith("Unnamed")]
    if unnamed:
        return False, f"包含多余索引列：{unnamed}"
    if df.empty:
        return False, "CSV为空"

    if relative_path.endswith("chart_manifest.csv"):
        if list(df.columns) != MANIFEST_COLUMNS:
            return False, f"图表清单字段应为：{MANIFEST_COLUMNS}"
        if len(df) != 5:
            return False, "图表清单必须包含5行"
        expected_names = {Path(path).name for path in REQUIRED_IMAGES}
        if set(df["file_name"]) != expected_names:
            return False, "图表清单中的文件名与5张必交图片不一致"
        if df.astype(str).apply(lambda col: col.str.contains("请填写").any()).any():
            return False, "图表清单仍包含“请填写”"

    return True, f"shape={df.shape}"


def check_png(relative_path):
    path = ROOT / relative_path
    if not path.exists():
        return False, "文件不存在"

    if path.stat().st_size < 5_000:
        return False, "图片文件过小，可能为空或导出失败"

    try:
        with path.open("rb") as file:
            signature = file.read(8)
    except Exception as exc:
        return False, f"图片读取失败：{exc}"

    if signature != b"\x89PNG\r\n\x1a\n":
        return False, "不是有效的PNG文件"

    return True, f"size={path.stat().st_size:,} bytes"


def main():
    rows = []

    for path in REQUIRED_NOTEBOOKS:
        passed, note = check_notebook(path)
        rows.append({"类型": "Notebook", "文件": path, "通过": passed, "说明": note})

    for path in REQUIRED_OUTPUTS:
        passed, note = check_csv(path)
        rows.append({"类型": "CSV", "文件": path, "通过": passed, "说明": note})

    for path in REQUIRED_IMAGES:
        passed, note = check_png(path)
        rows.append({"类型": "PNG", "文件": path, "通过": passed, "说明": note})

    report = pd.DataFrame(rows)
    print(report.to_string(index=False))

    missing_or_failed = report.loc[~report["通过"]]
    print("\n通过：", int(report["通过"].sum()), "/", len(report))

    if not missing_or_failed.empty:
        raise SystemExit("提交检查未通过，请完成或修正以上文件。")

    print("提交结构检查通过。请继续人工复核代码、指标和结论。")


if __name__ == "__main__":
    main()
