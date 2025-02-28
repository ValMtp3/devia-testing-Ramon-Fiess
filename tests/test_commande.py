import unittest
from app import create_app
from models.database import db
from models.commande import Commande


class CommandeTestCase(unittest.TestCase):
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

    def test_create_commande(self):
        response = self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Drone", str(response.data))

    def test_get_commandes(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.get("/apiii/commandes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Drone", str(response.data))

    def test_get_commande(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.get("/apiii/commandes/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Drone", str(response.data))

    def test_update_commande(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.put("/apiii/commandes/1", json={
            "name": "Drone 2",
            "description": "Second best drone ever",
            "prix": 200,
            "location": "Montpellier",
            "date": "2021-10-10"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Drone 2", str(response.data))
        self.assertIn("200", str(response.data))

    def test_delete_commande(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.delete("/apiii/commandes/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Commande deleted successfully", str(response.data))

    def test_create_commande_without_description(self):
        response = self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "prix": 150
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", str(response.data))

    def test_create_commande_with_invalid_prix(self):
        response = self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": "invalid_price",
            "location": "Dakar",
            "date": "2021-10-10"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid price format", str(response.data))

    def test_create_commande_with_duplicate_name(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Another Drone commande",
            "prix": 120,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn("Commande name already exists", str(response.data))

    def test_get_nonexistent_commande(self):
        response = self.client.get("/apiii/commandes/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Commande not found", str(response.data))

    def test_update_commande_with_invalid_data(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.put("/apiii/commandes/1", json={
            "prix": "invalid_price"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid price format", str(response.data))

    def test_delete_nonexistent_commande(self):
        response = self.client.delete("/apiii/commandes/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Commande not found", str(response.data))

    def test_multiple_commandes_creation_and_retrieval(self):
        self.client.post("/apiii/commandes", json={
            "name": "Drone",
            "description": "Best drone ever",
            "prix": 150,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        self.client.post("/apiii/commandes", json={
            "name": "Babysitting",
            "description": "Professional babysitting commandes for children",
            "prix": 200,
            "location": "Dakar",
            "date": "2021-10-10"
        })
        response = self.client.get("/apiii/commandes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Drone", str(response.data))
        self.assertIn("Babysitting", str(response.data))


if __name__ == "__main__":
    unittest.main()
