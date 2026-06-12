import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from backend.database import SessionLocal
from backend import models
from fastapi.testclient import TestClient

client = TestClient(app)


class TestVotingAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Сброс голосов и регистрация тестовых пользователей перед тестами"""
        db = SessionLocal()
        db.query(models.Vote).delete()
        db.query(models.Candidate).update({"votes": 0})
        db.commit()
        db.close()
        
        # Регистрируем двух тестовых пользователей
        client.post("/api/register", data={"username": "testuser1", "password": "test123"})
        client.post("/api/register", data={"username": "testuser2", "password": "test123"})

    def login(self, username, password):
        """Вспомогательная функция для входа"""
        return client.post("/api/login", data={"username": username, "password": password})

    def test_home_page(self):
        """Проверка загрузки главной страницы"""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_candidates(self):
        """Проверка получения списка кандидатов"""
        response = client.get("/api/candidates")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_vote_without_login(self):
        """Проверка отказа в голосовании без авторизации"""
        response = client.post("/api/vote/1")
        self.assertIn(response.status_code, [400, 401])

    def test_vote_for_candidate(self):
        """Проверка голосования за кандидата"""
        self.login("testuser1", "test123")
        response = client.post("/api/vote/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)

    def test_duplicate_vote(self):
        """Проверка защиты от повторного голосования"""
        self.login("testuser2", "test123")
        # Первый голос
        client.post("/api/vote/2")
        # Повторный голос от того же пользователя
        response = client.post("/api/vote/3")
        self.assertEqual(response.status_code, 400)

    def test_vote_invalid_candidate(self):
        """Проверка голосования за несуществующего кандидата"""
        self.login("testuser1", "test123")
        response = client.post("/api/vote/999")
        self.assertEqual(response.status_code, 404)

    def test_results_page(self):
        """Проверка загрузки страницы результатов"""
        response = client.get("/results")
        self.assertEqual(response.status_code, 200)

    def test_swagger_docs(self):
        """Проверка доступности Swagger"""
        response = client.get("/docs")
        self.assertEqual(response.status_code, 200)

    def test_openapi_json(self):
        """Проверка доступности OpenAPI схемы"""
        response = client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)

    def test_has_voted(self):
        """Проверка эндпоинта проверки голосования"""
        self.login("testuser1", "test123")
        response = client.get("/api/has-voted")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["voted"])


if __name__ == "__main__":
    unittest.main()