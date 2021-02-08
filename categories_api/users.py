"""Example users dictionary"""
from werkzeug.security import generate_password_hash

users = { 'admin': generate_password_hash('admin')}
