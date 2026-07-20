from pathlib import Path
import pandas as pd

def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")

def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")
    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    # 4项指标卡
    total_users = metric_map["用户数"]
    churn_users = metric_map["流失人数"]
    overall_churn_rate = metric_map["流失率"]
    avg_order = metric_map["平均订单数"]
    metrics = [
        {"label": "总用户数", "value": f"{int(total_users):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(churn_users):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{overall_churn_rate:.1%}", "note": ""},
        {"label": "平均订单数", "value": f"{avg_order:.2f}", "note": "单/人"},
    ]
    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    # 品类筛选逻辑
    if selected_category != "全部":
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]
    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")
    # 生命周期风险数据观察
    max_churn_idx = segment_df["流失率"].idxmax()
    max_churn_row = segment_df.loc[max_churn_idx]
    risk_stage = max_churn_row["TenureGroup"]
    max_churn_rate = max_churn_row["流失率"]
    insight = f"生命周期中风险最高的阶段为「{risk_stage}」，流失率达{max_churn_rate:.1%}，是用户留存运营的核心关注群体。"
    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }

def load_metric_api_data(base_dir: Path):
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    total_users = metric_map["用户数"]
    churn_users = metric_map["流失人数"]
    overall_churn_rate = metric_map["流失率"]
    avg_order = metric_map["平均订单数"]
    metric_list = [
        {"label": "总用户数", "value": int(total_users), "note": "全部用户总量"},
        {"label": "流失用户", "value": int(churn_users), "note": "已流失用户数量"},
        {"label": "总体流失率", "value": round(overall_churn_rate, 4), "note": "整体流失占比"},
        {"label": "平均订单数", "value": round(avg_order, 2), "note": "人均下单数量"},
    ]
    return metric_list

def load_category_api_data(base_dir: Path, category: str):
    data_dir = base_dir / "data"
    category_df = _read_csv(data_dir / "category_analysis.csv")
    if category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == category]
    return category_df.to_dict("records")