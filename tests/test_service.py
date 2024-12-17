import unittest
from app import create_app
from models.database import db
from models.service import Service


class ServiceTestCase(unittest.TestCase):
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

    # Tests de base CRUD (Create, Read, Update, Delete)

    def test_create_service(self):
        response = self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Cleaning", str(response.data))

    def test_get_services(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.get("/apii/services")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cleaning", str(response.data))

    def test_get_service(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.get("/apii/services/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cleaning", str(response.data))

    def test_update_service(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.put("/apii/services/1", json={
            "name": "Deep Cleaning",
            "description": "Full apartment deep cleaning",
            "prix": 200
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Deep Cleaning", str(response.data))
        self.assertIn("200", str(response.data))

    def test_delete_service(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.delete("/apii/services/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Service deleted successfully", str(response.data))

    def test_create_service_without_description(self):
        response = self.client.post("/apii/services", json={
            "name": "Cleaning",
            "prix": 150
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", str(response.data))

    def test_create_service_with_invalid_prix(self):
        response = self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": "invalid_price"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid price format", str(response.data))

    def test_create_service_with_duplicate_name(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Another cleaning service",
            "prix": 120
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn("Service name already exists", str(response.data))

    def test_get_nonexistent_service(self):
        response = self.client.get("/apii/services/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Service not found", str(response.data))

    def test_update_service_with_invalid_data(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        response = self.client.put("/apii/services/1", json={
            "prix": "invalid_price"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid price format", str(response.data))

    def test_delete_nonexistent_service(self):
        response = self.client.delete("/apii/services/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Service not found", str(response.data))

    def test_multiple_services_creation_and_retrieval(self):
        self.client.post("/apii/services", json={
            "name": "Cleaning",
            "description": "Apartment deep cleaning service",
            "prix": 150
        })
        self.client.post("/apii/services", json={
            "name": "Babysitting",
            "description": "Professional babysitting services for children",
            "prix": 200
        })
        response = self.client.get("/apii/services")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cleaning", str(response.data))
        self.assertIn("Babysitting", str(response.data))


if __name__ == "__main__":
    unittest.main()
