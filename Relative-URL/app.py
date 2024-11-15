# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, Blueprint
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

static = Blueprint('static', __name__, static_folder='static')

# Flask constructor takes the name of 
# current module (__name__) as argument.
# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.register_blueprint(static, url_prefix='/geolytics')
# app.config["SERVER_NAME"] = "http://127.0.0.1:5000/"
app.config["APPLICATION_ROOT"] = "/geolytics"

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/dummy')
def dummy():
    return render_template('index.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')


# app.wsgi_app = DispatcherMiddleware(run_simple('localhost', 8080, app, use_reloader=True), {'/temp': app.wsgi_app})
app.wsgi_app = DispatcherMiddleware(run_simple, {'/geolytics': app.wsgi_app})

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
