"""Flask server and API functions"""
from urllib.parse import urlparse
import re
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from categories_api import users

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@app.route('/categories.txt')
def serve_file():
    """Return the current categories.txt"""
    return open('./categories.txt', 'r', encoding='utf8').read()

@auth.verify_password
def verify_password(username, password):
    """Compare username and password with the contents of users.py"""
    key_list = list(users.users.keys())
    if username in key_list:
        if check_password_hash(users.users[username], password):
            return username
    return None

def parse_file():
    """Parse the contents of categories.txt into a dictionary"""
    results = {}
    with open('./categories.txt', 'r', encoding='utf8') as cat_file:
        cur_cat = None
        for line in cat_file:
            match = re.search(r'(?<=define\ category\ )\w+', line)
            if match:
                new_cat = match.group(0)
                cur_cat = new_cat
                results[cur_cat] = []
            else:
                match = re.search(r'(?<=end)', line)
                if match:
                    cur_cat = None
                else:
                    match = line.strip()
                    if match and cur_cat:
                        results[cur_cat].append(match)
    return results

def encode_file(content):
    """Turn a dictionary into a valid categories file"""
    with open('./categories.txt', 'w', encoding='utf8') as cat_file:
        for key in content:
            cat_file.write("define category "+key+"\n")
            for domain in content[key]:
                cat_file.write("      "+domain+"\n")
            cat_file.write("end\n\n")

class Edit(Resource):
    """For /edit Path"""
    decorators = [auth.login_required]

    def parse(self):
        """Parse given arguments"""
        parser = reqparse.RequestParser()
        parser.add_argument('category', required=True)
        parser.add_argument('domain', required=True)
        return parser

    def get_domain_name(self, domain):
        """Try to extract Domain name and remove bad arguments"""
        if '/' in domain:
            domain = urlparse(domain).netloc
        if not re.match(r'^[A-Za-z0-9.\-]+$', domain):
            return ""
        if '.' not in domain:
            return ""
        return domain

    def post(self):
        """Add a new domain to a existing Category"""
        parser = self.parse()
        args = parser.parse_args()

        if not self.get_domain_name(args['domain']):
            return {'message': 'Domain can not be parsed', 'data': args}, 400

        cat_dict = parse_file()

        if args['category'] in cat_dict:
            if args['domain'] not in cat_dict[args['category']]:
                cat_dict[args['category']].append(args['domain'])
                encode_file(cat_dict)
                return {'message': 'Domain added', 'data': args}, 201
            return {'message': 'Domain already in Category', 'data': args}, 400
        return {'message': 'Category invalid', 'data': args}, 400

    def delete(self):
        """Remove a domain from a existing Category"""
        parser = self.parse()
        args = parser.parse_args()

        if not self.get_domain_name(args['domain']):
            return {'message': 'Domain can not be parsed', 'data': args}, 400

        cat_dict = parse_file()

        if args['category'] in cat_dict:
            if args['domain'] in cat_dict[args['category']]:
                cat_dict[args['category']].remove(args['domain'])
                encode_file(cat_dict)
                return {'message': 'Domain removed', 'data': args}, 200
            return {'message': 'Domain not in Category', 'data': args}, 400
        return {'message': 'Category invalid', 'data': args}, 400

api.add_resource(Edit, '/edit')
