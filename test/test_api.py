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
        """Сброс голосов перед всеми тестами"""
        db = SessionLocal()
        db.query(models.Vote).delete()
        db.query(models.Candidate).update({"votes": 0})
        db.commit()
        db.close()

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

    def test_vote_for_candidate(self):
        """Проверка голосования за кандидата"""
        response = client.post("/api/vote/1", headers={"X-Forwarded-For": "192.168.1.1"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)

    def test_duplicate_vote(self):
        """Проверка защиты от повторного голосования"""
        # Первый голос
        client.post("/api/vote/2", headers={"X-Forwarded-For": "192.168.1.2"})
        # Повторный голос с того же IP
        response = client.post("/api/vote/2", headers={"X-Forwarded-For": "192.168.1.2"})
        self.assertEqual(response.status_code, 400)

    def test_vote_invalid_candidate(self):
        """Проверка голосования за несуществующего кандидата"""
        response = client.post("/api/vote/999", headers={"X-Forwarded-For": "192.168.1.99"})
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


if __name__ == "__main__":
    unittest.main()