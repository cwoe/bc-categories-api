"""Starts the webapp"""
from waitress import serve
from categories_api import app

#app.run(host='0.0.0.0', port=80, debug=False)
serve(app, host='0.0.0.0', port=80)
