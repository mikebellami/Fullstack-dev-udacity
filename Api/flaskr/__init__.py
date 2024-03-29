
import os
from pickle import NONE
from flask import Flask, jsonify, request, abort
from models import setup_db, Plants
from flask_cors import CORS
import math
from functools import wraps

list_plant_per_page = 5
def paginate(request, selection):
    global page_num
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * list_plant_per_page
    end = page * list_plant_per_page
    total_page = math.ceil(len(selection) / list_plant_per_page)
    page_num = '{} of {}'.format(page, total_page )
    plants = selection[start:end]
    current_plants = [plant.format() for plant in plants]

    return current_plants

def get_token_auth_header():
    # check if authorization is not in request
    if 'Authorization' not in request.headers:
        abort(401)
    # get the token   
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    # check if token is valid
    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401) 
    return header_parts[1]

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        print(jwt)
        return f(jwt, *args, **kwargs)
    return wrapper

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
   
    @app.route('/headers')
    @requires_auth
    def headers(jwt):
        print(jwt)
        return "not implemented"

    @app.route('/plants')
    def get_plants():
        selection = Plants.query.order_by(Plants.id).all()
        formatted_plants = paginate(request, selection)
        
        if len(formatted_plants) == 0:
            abort(404)

        return jsonify({
            "success":True,
            "plants":formatted_plants,
            "page":page_num,
            "total_plants": len(Plants.query.all())
        })

    @app.route('/plants/<int:plant_id>')
    def get_one_plant(plant_id):
        plant = Plants.query.filter(Plants.id == plant_id).one_or_none()
        if plant is None:
            abort(404)
            # return jsonify({
            #     'status':False,
            #     'data': '{} not form'.format(plant_id)
            # })
        else:
            return jsonify({
                'success':True,
                'plant': plant.format()
            })
    
 
    @app.route('/plants/<int:plant_id>', methods =['DELETE'])
    def delete_plants(plant_id):
     
        try:
            plant = Plants.query.filter(Plants.id == plant_id).one_or_none()
            if plant is None:
                abort(404)
            
            plant.delete()
            selection = Plants.query.order_by(Plants.id).all()
            formatted_plants = paginate(request, selection)
            return jsonify({
                'success':True,
                'deleted_plant': plant.id,
                "plants":formatted_plants,
                "page":page_num,
                "total_plants": len(Plants.query.all())
            })
        except:
            abort(422)

    @app.route('/plants', methods=['POST'])
    def create_plants():
      
        data = request.get_json()
        name = data["name"]
        poisonous = data["is_poisonous"]
        primary_color = data["primary_color"]
        scientific_name = data["scientific_name"]    
        search = data["search"]
        try:
            if search:
                selection = Plants.query.filter(
                    Plants.name.ilike(f"%{search}%")
                )
                return jsonify({
                    "here":selection
                })
               # selection = Plants.query.order_by(Plants.id).filter(Plants.name.ilike(f"%{}%".format(search))).all()
                formatted_plants = paginate(request, selection)
                return jsonify({
                    "success": True,
                    "plants":formatted_plants,
                    "page":page_num,
                    "total_plants": len(selection.all())
                })
            else:
                plant = Plants(name=name, scientific_name=scientific_name, is_poisonous=poisonous,primary_color=primary_color )
                plant.insert()
                selection = Plants.query.order_by(Plants.id).all()
                formatted_plants = paginate(request, selection)
                return jsonify({
                    "success":True,
                    "message":"Created",
                    "plants":formatted_plants,
                    "page":page_num,
                    "total_plants": len(Plants.query.all())
                })
        except Exception as e:
            print(data)
            print(e)
            abort(422)

    @app.route('/plants/<int:plant_id>', methods =['PATCH'])
    def update_plants(plant_id):
        data = request.get_json()
        try:
            plant = Plants.query.filter(Plants.id == plant_id).one_or_none()
            if plant is None:
                abort(404)
              
            plant.name = data['name']  
            plant.is_poisonous = data['is_poisonous']  
            plant.primary_color = data['primary_color']  
            plant.scientific_name = data['scientific_name']  
            plant.update()
    
            return jsonify({
                'success':True,
                'plant': plant.id
            })
        except Exception as e:
            abort(400)

    
    # @app.errorhandler(404)
    # def not_found(error):
    #     return jsonify({
    #         "success": False, 
    #         "error": 404,
    #         "message": "Not found"
    #         }), 404

    # @app.errorhandler(422)
    # def unprocessable(error):
    #     return jsonify({
    #     "success": False, 
    #     "error": 422,
    #     "message": "unprocessable"
    #     }), 422

    # @app.errorhandler(405)
    # def not_found(error):
    #     return jsonify({
    #     "success": False, 
    #     "error": 405,
    #     "message": "method not allowed"
    #     }), 405

    # @app.errorhandler(400)
    # def bad_request(error):
    #     return jsonify({
    #     "success": False, 
    #     "error": 400,
    #     "message": "bad request"
    #     }), 400

    return app