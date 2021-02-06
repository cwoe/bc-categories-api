from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

@app.route('/categories.txt')
def hello_world():
    return open('/var/www/categories.txt', 'r').read()



class Add(Resource):

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('category', required=True)
        parser.add_argument('domain', required=True)

        args = parser.parse_args()

        return {'message': 'Device registered', 'data': args}, 201


class Remove(Resource):

    def delete(self, identifier):
        
        parser = reqparse.RequestParser()

        parser.add_argument('category', required=True)
        parser.add_argument('domain', required=True)

        args = parser.parse_args()
        return {'message': 'Device not found', 'data': args}, 201


api.add_resource(Add, '/add')
api.add_resource(Remove, '/remove')
