"""第9天零基础版成果检查。"""
from pathlib import Path
import re
import sys
import nbformat
import numpy as np
import pandas as pd

def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors, warnings = [], []
    notebook_path = next((root / "notebooks" / name for name in (
        "day09_ml_preparation_student.ipynb", "day09_ml_preparation_teacher_reference.ipynb")
        if (root / "notebooks" / name).is_file()), None)
    if notebook_path is None:
        errors.append("缺少第9天Notebook")
    else:
        nb = nbformat.read(notebook_path, as_version=4)
        source = "\n".join(cell.get("source", "") for cell in nb.cells)
        compact = source.replace(" ", "")
        for token in ("train_test_split", "stratify=STRATIFY_TARGET", "ColumnTransformer", "OneHotEncoder", "DummyClassifier"):
            if token.replace(" ", "") not in compact:
                errors.append(f"Notebook未发现关键步骤：{token}")
        if "STRATIFY_TARGET = None" in source:
            warnings.append("尚未将STRATIFY_TARGET改为y")
        if "TODO 9-" in source:
            warnings.append("Notebook中仍有任务TODO")

    outputs = {name: root / "output" / name for name in (
        "feature_schema.csv", "split_summary.csv", "model_matrix_preview.csv", "baseline_metrics.csv")}
    for name, path in outputs.items():
        if not path.is_file():
            errors.append(f"缺少成果文件：output/{name}")
    if outputs["split_summary.csv"].is_file():
        summary = pd.read_csv(outputs["split_summary.csv"])
        if set(summary.get("split", [])) != {"train", "test"} or int(summary["rows"].sum()) != 5630:
            errors.append("split_summary.csv的划分规模不正确")
        if float(summary["churn_rate"].max() - summary["churn_rate"].min()) > 0.01:
            errors.append("训练集与测试集流失比例差异过大")
    if outputs["model_matrix_preview.csv"].is_file():
        matrix = pd.read_csv(outputs["model_matrix_preview.csv"])
        numeric = matrix.select_dtypes(include=[np.number])
        if matrix.shape != (20, 36) or numeric.shape[1] != 36 or not np.isfinite(numeric.to_numpy()).all():
            errors.append("模型矩阵预览应为20行、36列有限数值")
    if outputs["baseline_metrics.csv"].is_file():
        metrics = pd.read_csv(outputs["baseline_metrics.csv"])
        required = {"accuracy", "churn_recall", "predicted_churn_count"}
        if not required.issubset(set(metrics.get("metric", []))):
            errors.append("baseline_metrics.csv缺少零基础版三项结果")
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for label in ("姓名", "学号", "班级"):
        if re.search(rf"{label}：\s*TODO", readme):
            warnings.append(f"README中的“{label}”尚未填写")
    for message in errors:
        print(f"[失败] {message}")
    for message in warnings:
        print(f"[提醒] {message}")
    if not errors:
        print("[通过] 第9天零基础版成果检查通过")
    print(f"\n结论：{len(errors)}项失败，{len(warnings)}项提醒。")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
