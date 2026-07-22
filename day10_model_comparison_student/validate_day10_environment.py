from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent
failures = 0

def check(ok, label):
    global failures
    print(("[通过] " if ok else "[失败] ") + label)
    if not ok:
        failures += 1

for package in ["pandas", "numpy", "sklearn", "nbformat", "joblib", "IPython"]:
    check(importlib.util.find_spec(package) is not None, f"Python包：{package}")

required = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / "data" / "ecommerce_customer_cleaned.csv",
]
notebooks = list((ROOT / "notebooks").glob("*.ipynb"))
for path in required:
    check(path.exists(), f"文件：{path.relative_to(ROOT)}")
check(len(notebooks) == 1, "Notebook数量为1")

try:
    import pandas as pd
    df = pd.read_csv(ROOT / "data" / "ecommerce_customer_cleaned.csv")
    check(df.shape == (5630, 22), "数据形状：5630行、22列")
    check(df["CustomerID"].is_unique, "CustomerID唯一")
    check(set(df["Churn"].unique()) == {0, 1}, "Churn仅包含0和1")
    check(df.isna().sum().sum() == 0, "数据无缺失")
except Exception as exc:
    print("[失败] 数据读取：", exc)
    failures += 1

print(f"\n结论：{failures}项失败。")
sys.exit(1 if failures else 0)
