import unittest
from app import create_app
from models.database import db
from models.user import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("John Doe", str(response.data))

    def test_get_users(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    def test_get_user(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.get("/api/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    def test_update_user(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.put("/api/users/1", json={"name": "Jane Doe"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", str(response.data))

    def test_delete_user(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.delete("/api/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", str(response.data))

    # Nouveaux tests

    def test_create_user_without_name(self):
        response = self.client.post("/api/users", json={"email": "john@example.com"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", str(response.data))

    def test_create_user_with_invalid_email(self):
        response = self.client.post("/api/users", json={"name": "John Doe", "email": "invalid-email"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", str(response.data))

    def test_create_user_with_duplicate_email(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 409)
        self.assertIn("Email already exists", str(response.data))

    def test_get_nonexistent_user(self):
        response = self.client.get("/api/users/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", str(response.data))

    def test_update_user_with_invalid_data(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        response = self.client.put("/api/users/1", json={"email": "invalid-email"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", str(response.data))

    def test_delete_nonexistent_user(self):
        response = self.client.delete("/api/users/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", str(response.data))

    def test_multiple_users_creation_and_retrieval(self):
        self.client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        self.client.post("/api/users", json={"name": "Jane Doe", "email": "jane@example.com"})
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))
        self.assertIn("Jane Doe", str(response.data))


if __name__ == "__main__":
    unittest.main()
