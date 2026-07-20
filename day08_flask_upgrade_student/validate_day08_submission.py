"""第8天成果检查：只检查Flask强化项目。"""

from pathlib import Path
import re
import sys


REQUIRED = [
    "app.py", "README.md", "requirements.txt", "services/data_service.py",
    "templates/dashboard.html", "templates/assistant.html",
]


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors, warnings = [], []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"缺少文件：{relative}")
    app = (root / "app.py").read_text(encoding="utf-8") if (root / "app.py").is_file() else ""
    for pattern, message in [
        (r"/health", "未发现/health路由"),
        (r"/api/metrics", "未发现/api/metrics接口"),
        (r"/api/categories", "未发现/api/categories接口"),
        (r"jsonify", "未发现JSON响应"),
    ]:
        if not re.search(pattern, app, re.I | re.S):
            errors.append(message)
    todo_files = [root / "app.py", root / "services/data_service.py"]
    todos = []
    for path in todo_files:
        if path.is_file():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"TODO\s*8-[1-4]", line):
                    todos.append(f"{path.relative_to(root)}:{number}")
    if todos:
        warnings.append("仍有TODO：" + "、".join(todos))
    tests = root / "tests"
    test_files = list(tests.rglob("test_*.py")) if tests.is_dir() else []
    if len(test_files) < 1:
        warnings.append("未发现tests/test_*.py，建议至少编写3条Flask测试")
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for label in ("姓名", "学号", "已完成路由或接口", "测试文件"):
        if re.search(rf"{label}：\s*TODO", readme):
            warnings.append(f"README中的“{label}”尚未填写")
    print(f"检查目录：{root}\n")
    for message in errors:
        print(f"[失败] {message}")
    for message in warnings:
        print(f"[提醒] {message}")
    if not errors:
        print("[通过] 第8天必需结构与接口检查通过")
    print(f"\n结论：{len(errors)}项失败，{len(warnings)}项提醒。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
