"""第9天零基础版环境与输入检查。"""
from importlib.util import find_spec
from pathlib import Path
import sys
import pandas as pd

def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    checks = [(f"Python包：{p}", find_spec(p) is not None) for p in ("pandas", "numpy", "sklearn", "nbformat")]
    for relative in ("README.md", "requirements.txt", "data/ecommerce_customer_cleaned.csv"):
        checks.append((f"文件：{relative}", (root / relative).is_file()))
    notebook_ok = any((root / "notebooks" / name).is_file() for name in (
        "day09_ml_preparation_student.ipynb", "day09_ml_preparation_teacher_reference.ipynb"))
    checks.append(("文件：第9天Notebook", notebook_ok))
    data_path = root / "data/ecommerce_customer_cleaned.csv"
    if data_path.is_file():
        df = pd.read_csv(data_path)
        checks.extend([
            ("数据形状：5630行、22列", df.shape == (5630, 22)),
            ("CustomerID唯一", df["CustomerID"].is_unique),
            ("Churn仅包含0和1", set(df["Churn"].unique()) == {0, 1}),
            ("清洗后数据无缺失", int(df.isna().sum().sum()) == 0),
        ])
    for label, ok in checks:
        print(f"[{'通过' if ok else '失败'}] {label}")
    failed = [label for label, ok in checks if not ok]
    print(f"\n结论：{len(failed)}项失败。")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
