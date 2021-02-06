from categories_api import app
from waitress import serve

#app.run(host='0.0.0.0', port=80, debug=False)
serve(app, host='0.0.0.0', port=80)
