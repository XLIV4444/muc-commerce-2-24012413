from pathlib import Path
import pandas as pd
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def _build_data_summary(base_dir: Path) -> str:
    """组装指标摘要，仅发送统计结论，不发送原始数据"""
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")

    summary = f"""
    电商用户分析数据摘要：
    - 总用户数：{int(metrics['用户数'])}人，流失用户{int(metrics['流失人数'])}人，总体流失率{metrics['流失率']:.1%}
    - 用户平均订单数{metrics['平均订单数']:.2f}单，订单中位数{int(metrics['订单数中位数'])}单
    - 偏好品类：{','.join(category_df['PreferedOrderCat'].tolist())}，其中用户最多的品类是{category_df.loc[category_df['用户数'].idxmax(), 'PreferedOrderCat']}
    - 生命周期阶段中流失率最高的是{segment_df.loc[segment_df['流失率'].idxmax(), 'TenureGroup']}，流失率{segment_df['流失率'].max():.1%}
    请仅基于以上数据回答用户问题，不要编造数据，回答简洁。
    """
    return summary.strip()

def _call_llm(question: str, data_summary: str) -> str | None:
    """调用大模型，失败返回None触发降级"""
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    if not api_key or not base_url or not model:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": data_summary},
                {"role": "user", "content": question}
            ],
            temperature=0.2,
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None

def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")

    normalized = question.replace(" ", "").lower()

    # ========== 规则问答（优先命中，稳定可靠） ==========
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    if any(word in normalized for word in ["流失率", "流失情况", "多少人流失", "流失用户"]):
        churn_rate = metrics["流失率"]
        return f"数据集总体流失率为{churn_rate:.1%}，流失用户共{int(metrics['流失人数']):,}人。"

    if any(word in normalized for word in ["偏好品类", "哪个品类用户最多", "品类", "最多用户"]):
        max_cat_row = category_df.loc[category_df["用户数"].idxmax()]
        return f"用户最多的偏好品类是「{max_cat_row['PreferedOrderCat']}」，共有{int(max_cat_row['用户数']):,}名用户。"

    if any(word in normalized for word in ["生命周期", "风险最高", "哪个阶段", "流失最高阶段"]):
        max_churn_row = segment_df.loc[segment_df["流失率"].idxmax()]
        return f"生命周期中风险最高的阶段是「{max_churn_row['TenureGroup']}」，流失率为{max_churn_row['流失率']:.1%}。"

    if any(word in normalized for word in ["平均订单数", "订单数", "订单", "人均订单"]):
        avg_val = metrics["平均订单数"]
        median_val = metrics["订单数中位数"]
        return f"用户平均订单数为{avg_val:.2f}单，订单数中位数为{int(median_val)}单。"

    # ========== 规则未命中，调用大模型 ==========
    data_summary = _build_data_summary(base_dir)
    llm_answer = _call_llm(question, data_summary)
    if llm_answer:
        return llm_answer

    # 最终降级
    return "抱歉，我暂时无法回答这个问题。你可以询问总用户数、流失率、偏好品类、生命周期风险或平均订单数相关问题。"