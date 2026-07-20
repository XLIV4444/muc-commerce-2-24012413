from functools import wraps
from pathlib import Path
from io import StringIO, BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import quote
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, Response
from services.data_service import (
    load_dashboard_data,
    load_metric_api_data,
    load_category_api_data
)
from services.qa_service import answer_question
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["SECRET_KEY"] = "day07-classroom-demo-key"
# ========== 权限装饰器 ==========
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view
def teacher_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("role") != "teacher":
            flash("该功能仅教师账号可访问。", "danger")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)
    return wrapped_view
# ========== 基础路由 ==========
@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # 普通学生账号
        if username == "student" and password == "day07":
            session["username"] = username
            session["role"] = "student"
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        
        # 教师账号
        if username == "teacher" and password == "day07":
            session["username"] = username
            session["role"] = "teacher"
            flash("教师账号登录成功，已开放全部功能。", "success")
            return redirect(url_for("dashboard"))
        
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))
@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部")
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )
@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])
@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"ok": False, "answer": "请输入一个与项目数据有关的问题。"}), 400
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})
# ========== 第8天新增API接口 ==========
# 健康探测接口，无需登录
@app.route("/health")
def health():
    """用于确认服务是否存活，不需要登录。"""
    return jsonify({"ok": True, "service": "day08-flask-upgrade"})

@app.route("/api/metrics")
@login_required
def metrics_api():
    return jsonify({"ok": True, "metrics": load_metric_api_data(BASE_DIR)})

@app.route("/api/categories")
@login_required
def categories_api():
    category = request.args.get("category", "全部")
    return jsonify({"ok": True, "category": category, "rows": load_category_api_data(BASE_DIR, category)})

# ========== 原有拓展功能（导出、生命周期页面、图表） ==========
@app.route("/download")
@login_required
@teacher_required
def download_category_csv():
    category = request.args.get("category", "全部")
    category_df = pd.read_csv(BASE_DIR / "data" / "category_analysis.csv", encoding="utf-8-sig")
    
    if category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == category]
    
    output = StringIO()
    category_df.to_csv(output, index=False, encoding="utf-8-sig")
    output.seek(0)
    
    filename = f"品类分析数据_{category}.csv"
    encoded_filename = quote(filename)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"}
    )
@app.route("/segments")
@login_required
@teacher_required
def segments():
    segment_df = pd.read_csv(BASE_DIR / "data" / "segment_analysis.csv", encoding="utf-8-sig")
    
    max_churn_idx = segment_df["流失率"].idxmax()
    max_churn_row = segment_df.loc[max_churn_idx]
    segment_insight = f"用户生命周期中，「{max_churn_row['TenureGroup']}」阶段流失风险最高，流失率达到{max_churn_row['流失率']:.1%}，是用户召回与留存运营的重点群体。"
    
    segment_df["流失率"] = segment_df["流失率"].map(lambda x: f"{x:.1%}")
    segment_df["平均订单数"] = segment_df["平均订单数"].map(lambda x: f"{x:.2f}")
    
    return render_template(
        "segments.html",
        username=session["username"],
        segment_rows=segment_df.to_dict("records"),
        insight=segment_insight
    )
@app.route("/chart/category.png")
@login_required
def category_chart():
    category = request.args.get("category", "全部")
    category_df = pd.read_csv(BASE_DIR / "data" / "category_analysis.csv", encoding="utf-8-sig")
    if category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == category]
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(category_df["PreferedOrderCat"], category_df["用户数"], color="#4e79f1")
    ax.set_title("偏好品类用户数分布", fontsize=14, pad=15)
    ax.set_xlabel("品类")
    ax.set_ylabel("用户数（人）")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f"{int(height)}", ha="center", va="bottom")
    plt.tight_layout()
    img_io = BytesIO()
    fig.savefig(img_io, format="png", dpi=100)
    img_io.seek(0)
    plt.close(fig)
    return Response(img_io, mimetype="image/png")
@app.route("/chart/order_line.png")
@login_required
def order_line_chart():
    category = request.args.get("category", "全部")
    category_df = pd.read_csv(BASE_DIR / "data" / "category_analysis.csv", encoding="utf-8-sig")
    if category != "全部":
        category_df = category_df[category_df["PreferedOrderCat"] == category]
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        category_df["PreferedOrderCat"],
        category_df["平均订单数"],
        marker="o",
        color="#27ae60",
        linewidth=2
    )
    ax.set_title("各品类平均订单数趋势", fontsize=14, pad=15)
    ax.set_xlabel("品类")
    ax.set_ylabel("平均订单数（单/人）")
    ax.grid(True, alpha=0.3)
    for x, y in zip(category_df["PreferedOrderCat"], category_df["平均订单数"]):
        ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom")
    plt.tight_layout()
    img_io = BytesIO()
    fig.savefig(img_io, format="png", dpi=100)
    img_io.seek(0)
    plt.close(fig)
    return Response(img_io, mimetype="image/png")

@app.errorhandler(400)
def bad_request(_error):
    return jsonify({"ok": False, "error": "请求格式不正确。"}), 400

# 404页面
@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404
if __name__ == "__main__":
    app.run(debug=False, port=5000)