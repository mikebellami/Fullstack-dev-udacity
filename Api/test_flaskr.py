import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Plants

class PlantTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "plants_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_plant = {"name":"testing", "scientific_name":"jam question", "is_poisonous":True, "primary_color":"black"}

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_paginated_plants(self):
        res = self.client().get("/plants")
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_plant"])
        self.assertTrue(data["plants"])
        self.assertTrue(len(data["page"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/books?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()