import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from app import app

class Day08ApiTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # 测试1：/health 无需登录返回200
    def test_health_interface(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertEqual(json_data["ok"], True)
        self.assertEqual(json_data["service"], "day08-flask-upgrade")

    # 测试2：未登录访问/api/metrics 被拦截跳转登录
    def test_metrics_no_login_redirect(self):
        res = self.client.get("/api/metrics")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.location)

    # 测试3：登录后正常获取指标接口数据
    def test_metrics_login_success(self):
        # 模拟学生登录
        self.client.post("/login", data={"username": "student", "password": "day07"})
        res = self.client.get("/api/metrics")
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertEqual(json_data["ok"], True)
        self.assertIsInstance(json_data["metrics"], list)
        item = json_data["metrics"][0]
        self.assertTrue("label" in item and "value" in item and "note" in item)

    # 测试4：品类筛选接口，指定品类返回过滤数据
    def test_category_filter_fashion(self):
        self.client.post("/login", data={"username": "student", "password": "day07"})
        res = self.client.get("/api/categories?category=Fashion")
        json_data = res.get_json()
        self.assertEqual(json_data["category"], "Fashion")
        self.assertIsInstance(json_data["rows"], list)

if __name__ == "__main__":
    unittest.main()