import os
import json

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    DEVAPIKEY_FILENAME = 'devapikey.json'
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DEVAPIKEY = THIS_FOLDER + '/' + DEVAPIKEY_FILENAME
    
    with open(DEVAPIKEY) as j:
        FOO = json.load(j)


    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('/index/index.html', foo = FOO)

    return app