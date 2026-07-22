from pathlib import Path
import json
import sys

import joblib
import nbformat
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
failures = 0
warnings = 0

def check(ok, label, warning=False):
    global failures, warnings
    if ok:
        print("[通过] " + label)
    elif warning:
        print("[提醒] " + label)
        warnings += 1
    else:
        print("[失败] " + label)
        failures += 1

required = {
    "model_comparison.csv", "confusion_matrix_summary.csv",
    "customer_churn_predictions.csv", "high_risk_customers.csv",
    "feature_importance.csv", "selected_model.joblib", "model_metadata.json",
    "model_selection_note.txt", "reflection.txt",
}
actual = {p.name for p in OUT.iterdir() if p.is_file()} if OUT.exists() else set()
check(required.issubset(actual), f"9项成果文件齐全；缺少：{sorted(required-actual)}")

try:
    comparison = pd.read_csv(OUT / "model_comparison.csv")
    expected_models = {"baseline", "logistic_regression", "decision_tree", "random_forest"}
    check(set(comparison["model"]) == expected_models, "模型比较包含基线与三个正式模型")
    check((comparison[["tn", "fp", "fn", "tp"]].sum(axis=1) == 1126).all(), "每个混淆矩阵合计1126人")
    baseline = comparison.set_index("model").loc["baseline"]
    check(abs(float(baseline["churn_recall"])) < 1e-12, "最低参照线流失召回率为0")
    formal = comparison.query("model != 'baseline'")
    check(formal["churn_recall"].max() > 0.80, "至少一个正式模型流失召回率超过80%")
except Exception as exc:
    print("[失败] model_comparison.csv：", exc)
    failures += 1

try:
    predictions = pd.read_csv(OUT / "customer_churn_predictions.csv")
    check(len(predictions) == 1126, "用户预测文件包含1126名测试用户")
    check(predictions["CustomerID"].is_unique, "预测文件CustomerID唯一")
    check(predictions["churn_probability"].between(0, 1).all(), "流失概率位于0到1")
except Exception as exc:
    print("[失败] customer_churn_predictions.csv：", exc)
    failures += 1

try:
    high = pd.read_csv(OUT / "high_risk_customers.csv")
    check(len(high) > 0, "高风险名单非空")
    check((high["predicted_churn"] == 1).all(), "高风险名单均预测为流失")
    check(high["churn_probability"].is_monotonic_decreasing, "高风险名单按概率降序排列")
except Exception as exc:
    print("[失败] high_risk_customers.csv：", exc)
    failures += 1

try:
    importance = pd.read_csv(OUT / "feature_importance.csv")
    check(len(importance) >= 30, "特征重要性文件包含转换后的特征")
    check(importance["importance"].is_monotonic_decreasing, "特征重要性已降序排列")
except Exception as exc:
    print("[失败] feature_importance.csv：", exc)
    failures += 1

try:
    metadata = json.loads((OUT / "model_metadata.json").read_text(encoding="utf-8"))
    check(metadata["selected_model"] in {"logistic_regression", "decision_tree", "random_forest"}, "最终模型名称有效")
    check(metadata["random_state"] == 42 and metadata["test_rows"] == 1126, "模型元数据口径正确")
    joblib.load(OUT / "selected_model.joblib")
    check(True, "模型文件可以重新加载")
except Exception as exc:
    print("[失败] 模型保存结果：", exc)
    failures += 1

selection_note = (OUT / "model_selection_note.txt").read_text(encoding="utf-8") if (OUT / "model_selection_note.txt").exists() else ""
reflection = (OUT / "reflection.txt").read_text(encoding="utf-8") if (OUT / "reflection.txt").exists() else ""
check(80 <= len(selection_note) <= 180, "模型选择说明为80～180字")
check(150 <= len(reflection) <= 250, "学习复盘为150～250字")

notebooks = list((ROOT / "notebooks").glob("*.ipynb"))
try:
    nb = nbformat.read(notebooks[0], as_version=4)
    source = "\n".join("".join(cell.get("source", "")) for cell in nb.cells)
    check("请填写" not in source, "Notebook关键选择已填写")
    check("selection_note = ''" not in source and "reflection = ''" not in source, "Notebook解释任务已完成")
except Exception as exc:
    print("[失败] Notebook检查：", exc)
    failures += 1

print(f"\n结论：{failures}项失败，{warnings}项提醒。")
sys.exit(1 if failures else 0)
