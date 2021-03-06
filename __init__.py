import os
import json
import logging

from flask import Flask, render_template, request


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

    # Get API KEY from file
    DEVAPIKEY_FILENAME = 'devapikey.json'
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DEVAPIKEY = THIS_FOLDER + '/' + DEVAPIKEY_FILENAME
    
    with open(DEVAPIKEY) as j:
        STEAM_API_KEY = json.load(j)


    # a simple page that says hello
    @app.route('/')
    def index():

        return render_template('/index/index.html')

    @app.route('/user/<username>', methods = ['GET', 'POST'])
    def user_info(username = ''):
        import steamapi
        steamapi.core.APIConnection(api_key=STEAM_API_KEY['devapikey'], validate_key=True)  # <-- Insert API key here

        if request.method == 'GET':
            steamuser = username
        if request.method == 'POST':    
            steamuser = request.values['username']

        data = {
                'games': steamapi.user.SteamUser(userurl=steamuser).owned_games,
                'country_code': steamapi.user.SteamUser(userurl=steamuser).country_code,
                'avatar': steamapi.user.SteamUser(userurl=steamuser).avatar
            }

        return render_template('/index/user.html', data = data)
        
    return app