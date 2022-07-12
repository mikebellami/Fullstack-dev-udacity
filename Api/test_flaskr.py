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
        self.assertTrue(data["total_plants"])
        self.assertTrue(data["plants"])
        self.assertTrue(len(data["page"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/plants?page=10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")
    

    def search_plants(self):
        res = self.client().post("/plants", json={"search":"hjvh"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_plants"])
        self.assertEqual(len(data["plants"]), 1)

    
    def test_get_plant_search_without_results(self):
        res = self.client().post("/plants", json={"search": "kjkj"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_plants"], 0)
        self.assertEqual(len(data["plants"]), 0)

    def test_update_plants(self):

        res = self.client().patch("/plants/10", json={"name":"hvjh","is_poisonous": True, "primary_color":"white", "scientific_name":"askjckjashk"})
        data = json.loads(res.data)
        plant = Plants.query.filter(Plants.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(plant.format()["is_poisonous"], True)
     

    def test_400_for_failed_update(self):
        res = self.client().patch("/plants/4")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    
     # Delete a different book in each attempt
    def test_delete_plant(self):
        res = self.client().delete("/plants/9")
        data = json.loads(res.data)
        plant = Plants.query.filter(Plants.id == 9).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_plant"], 9)
        self.assertTrue(data["total_plants"])
        self.assertTrue(len(data["plants"]))
        self.assertEqual(plant, None)

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete("/plants/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
  
    def test_create_new_plant(self):
        res = self.client().post("/plants", json=self.new_plant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"], "created")
        self.assertTrue(len(data["plants"]))

    def test_405_if_plants_creation_not_allowed(self):
        res = self.client().post("/plants/45", json=self.new_plant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

   
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()