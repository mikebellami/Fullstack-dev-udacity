import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format( "postgres", "password", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_404_invalid_page_numbers(self):
        res = self.client().get("/questions?page=200")
        data = json.loads(res.data)
        
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_page"])
        self.assertTrue(data["total_questions"])

    """test for 404 error with no questions from category"""

    def test_404_get_category_questions(self):
        res = self.client().get("/categories/1000000/questions")
        data = json.loads(res.data)

        # check status code, false success message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def search_question(self):
        res = self.client().post('questions/search', json={"searchTerm": "best"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data["total_page"])
        self.assertTrue(data["total_questions"])

    def test_invalid_search_input(self):
        res = self.client().post('questions/search', json={"searchTerm": "G.O.T"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

     # Delete a different book in each attempt
    def test_delete_question(self):
    
        res = self.client().delete("/questions/25")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_question"], 25)
    
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        new_question={
           "question":"Who invented the personal computer?",
           "answer":"Steve Wozniak",
           "category": 4,
           "difficulty": 2
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
    
    def test_405_if_questions_creation_not_allowed(self):
        new_question={
           "question":"Who invented the personal computer?",
           "answer":"Steve Wozniak",
           "category": 4,
           "difficulty": 2
        }
        res = self.client().post("/questions/45", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_quiz(self):

        quiz = {"previous_questions": [ 26, 25], "quiz_category": {
            "type": "History", "id": 4}}
        res = self.client().post("/quizzes", json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_get_quiz(self):
   
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
       

    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()