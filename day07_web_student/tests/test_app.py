import unittest
import sys
from pathlib import Path

# 将项目根目录加入Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret_key"
        self.client = app.test_client()

    def test_correct_login(self):
        """测试正确账号密码登录成功，并重定向到看板页"""
        response = self.client.post(
            "/login",
            data={"username": "student", "password": "day07"},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")

        follow_response = self.client.get("/dashboard")
        self.assertEqual(follow_response.status_code, 200)
        self.assertIn("电商用户行为数据看板", follow_response.data.decode("utf-8"))

    def test_dashboard_without_login(self):
        """测试未登录访问看板，自动跳转到登录页"""
        response = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_ask_api_normal(self):
        """测试智能问答接口，登录后可正常返回答案"""
        self.client.post("/login", data={"username": "student", "password": "day07"})
        
        response = self.client.post(
            "/api/ask",
            json={"question": "总用户数是多少"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["ok"])
        self.assertIn("用户", data["answer"])

if __name__ == "__main__":
    unittest.main()