from crypt import methods
import os
from pickle import NONE
from unicodedata import category
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, math

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
    # global page_num, total_questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE
    total_page = math.ceil(len(selection) / QUESTIONS_PER_PAGE)
    total_questions = len(selection)
    page_num = '{} of {}'.format(page, total_page )
    questions = selection[start:end]
    current_questions = [question.format() for question in questions]

    # return current_questions
    return {
        "questions" : current_questions,
        "total_page" : page_num,
        "total_questions" : total_questions
    }

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={"/": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        categories_list = {}
        
        for category in categories:
            categories_list[category.id] = category.type
        
        if (len(categories_list) == 0):
            abort(404)
        
        return jsonify({
            "success": True,
            "categories": categories_list
        })
       
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_question():
        questions = Question.query.order_by(Question.id).all()

        results = paginate(request, questions)

        numberofquestion = len(results['questions'])
 
        if numberofquestion == 0:
            abort(404)

        # get categories
        categories = Category.query.order_by(Category.id).all()
        categories_list = {}
        
        for category in categories:
            categories_list[category.id] = category.type

        return jsonify({
            "success": True,
            "categories" : categories_list,
            "questions": results["questions"],
            "total_page": results["total_page"],
            "total_questions": results["total_questions"],
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            
            return jsonify({
                "success": True,
                "deleted_question": question.id
            })
        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_questions():
        data = request.get_json()

        if not ("qustion" in data, "answer" in data, "category" in data, "difficulty" in data):
            abort(422)
        
        new_question = data.get('question')
        new_answer = data.get('answer')
        new_category = data.get('category')
        new_difficulty = data.get('difficulty')
       
        try: 
            question = Question(question=new_question, answer=new_answer,category=new_category,difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            results = paginate(request, selection)

            return jsonify({
                "success": True,
                "created": question.id,
                "questions": results["questions"],
                "total_page": results["total_page"],
                "total_questions": results["total_questions"],
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        data = request.get_json()
        search = data.get('searchTerm')
        print(search)

        try:
            if search:
                selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
                results = paginate(request, selection)

            return jsonify({
                "success": True,
                "questions": results["questions"],
                "total_page": results["total_page"],
                "total_questions": results["total_questions"],
            })

        except Exception as e:
            print(e)
            abort(404)
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        
        if category is None:
            abort(404)

        try:
            questions = Question.query.filter_by(category=category.id).all()
            results = paginate(request, questions)

            return jsonify({
                "success": True,
                "questions": results["questions"],
                "total_page": results["total_page"],
                "total_questions": results["total_questions"],
            })
            
        except Exception as e:
            print(e)
            abort(400)
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
 
        data = request.get_json()

        try:
            previous_questions = data.get('previous_questions')
            category = data.get('quiz_category')
            
            if int(category["id"]) != 0:
                all_question = Question.query.filter_by(category=int(category["id"])).all()
            else:
                all_question = Question.query.all()

            new_question = []
            for question in all_question:
                if question.id not in previous_questions:
                    new_question.append(question)
            
            if len(new_question) == 0:
                return jsonify({
                    "success": True,
                    "question": []
                })
            else:
                random_question = random.choice(new_question)
                return jsonify({
                    "success": True,
                    "question": random_question.format()
                })
    
        except Exception as e:
            print(e)
            abort(422)
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
     
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False, 
                "error": 404,
                "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400

    return app

