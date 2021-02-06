from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
from categories_api import users
from werkzeug.security import check_password_hash
import re


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@app.route('/categories.txt')
def serve_file():
    return open('/usr/src/app/categories.txt', 'r').read()


@auth.verify_password
def verify_password(username, password):
    key_list = list(users.users.keys())
    if username in key_list:
        if check_password_hash(users.users[username], password):
            return username

def parse_file():
    results = {}
    with open('/usr/src/app/categories.txt', 'r') as cat_file:
        cur_cat = None
        for line in cat_file:
            m = re.search(r'(?<=define\ category\ )\w+', line)
            if m:
                new_cat = m.group(0)
                cur_cat = new_cat
                results[cur_cat] = []
            else:
                m = re.search(r'(?<=end)', line)
                if m:
                    cur_cat = None
                else:
                    m = line.strip()
                    if m and cur_cat:
                        results[cur_cat].append(m)
    return(results)

def encode_file(content):
    key_list = list(content.keys())
    with open('/usr/src/app/categories.txt', 'w') as cat_file:
        for key in key_list:
            cat_file.write("define category "+key+"\n")
            for domain in content[key]:
                cat_file.write("      "+domain+"\n")
            cat_file.write("end\n\n")

class Add(Resource):

    decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('category', required=True)
        parser.add_argument('domain', required=True)

        args = parser.parse_args()
        a = parse_file()

        key_list = list(a.keys())
        if args['category'] in key_list:
            if args['domain'] not in a[args['category']]:
                a[args['category']].append(args['domain'])
                encode_file(a)
                return {'message': 'Domain added', 'data': args}, 201
            return {'message': 'Domain already in Category', 'data': args}, 400
        return {'message': 'Category invalid', 'data': args}, 400

class Remove(Resource):

    decorators = [auth.login_required]

    def delete(self):

        parser = reqparse.RequestParser()

        parser.add_argument('category', required=True)
        parser.add_argument('domain', required=True)

        args = parser.parse_args()
        a = parse_file()

        key_list = list(a.keys())
        if args['category'] in key_list:
            if args['domain'] in a[args['category']]:
                a[args['category']].remove(args['domain'])
                encode_file(a)
                return {'message': 'Domain removed', 'data': args}, 201
            return {'message': 'Domain not in Category', 'data': args}, 400
        return {'message': 'Category invalid', 'data': args}, 400


api.add_resource(Add, '/add')
api.add_resource(Remove, '/remove')
