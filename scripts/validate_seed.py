from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main():
    product_path = ROOT / "data" / "淘宝全品类全国数据.csv"
    customer_path = ROOT / "data" / "E Commerce Dataset.xlsx"

    assert product_path.exists(), f"缺少数据：{product_path.relative_to(ROOT)}"
    assert customer_path.exists(), f"缺少数据：{customer_path.relative_to(ROOT)}"

    product_df = pd.read_csv(product_path)
    customer_df = pd.read_excel(customer_path, sheet_name="E Comm")

    assert product_df.shape == (25000, 15), "淘宝商品数据形状不正确"
    assert customer_df.shape == (5630, 20), "电商用户原始数据形状不正确"

    notebook_paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    assert len(notebook_paths) == 4, "种子项目应只包含4个学生Notebook"
    assert not any("teacher" in path.name.lower() for path in notebook_paths), \
        "种子项目不应包含教师Notebook"

    for path in notebook_paths:
        nb = json.loads(path.read_text(encoding="utf-8"))
        assert nb.get("nbformat") == 4, f"Notebook格式错误：{path.name}"
        assert nb.get("cells"), f"Notebook没有单元格：{path.name}"
        assert "/Users/" not in path.read_text(encoding="utf-8"), \
            f"Notebook包含本机绝对路径：{path.name}"

        error_cells = []
        for index, cell in enumerate(nb["cells"]):
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    error_cells.append(index)

        assert not error_cells, f"{path.name}存在错误输出单元格：{error_cells}"
        print(f"通过：{path.relative_to(ROOT)}，cells={len(nb['cells'])}")

    completed_outputs = list((ROOT / "output").rglob("*.csv"))
    completed_images = list((ROOT / "output").rglob("*.png"))
    assert not completed_outputs, "种子项目不应预置已完成的学生CSV成果"
    assert not completed_images, "种子项目不应预置已完成的学生PNG成果"

    print(f"通过：{product_path.relative_to(ROOT)}，shape={product_df.shape}")
    print(f"通过：{customer_path.relative_to(ROOT)}，shape={customer_df.shape}")
    print("种子项目检查通过，可以开始Day03任务。")


if __name__ == "__main__":
    main()
