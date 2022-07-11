import unittest
import json
from venv import create 

from flaskr import create_app
from models import setup_db

class PlantTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app
        self.client = self.test_client
        self.database_name = "palnts_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
