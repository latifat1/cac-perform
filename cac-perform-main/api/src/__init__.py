from flask import Flask
from flask_cors import CORS
from src.config.db import MyMongo

mongo = MyMongo()

def create_app():
    # instancier l'app
    app = Flask(__name__)

    CORS(app, resources={
        r"/*": {
            # Autorisez uniquement les requêtes depuis ce domaine
            "origins": ["http://localhost:5173"],
            "methods": "GET, POST, PUT, DELETE",  # Autorisez ces méthodes HTTP
            # Autorisez ces en-têtes
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })

    # Set mode
    mode = 'dev'

    # Load config
    if mode == 'prod':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    mongo.init_app(app)
    
   # importation et enregistrement des blueprint
    from src.collaborateur import collab
    from src.mission import mission
    from src.manager import manager
    from src.customer import client

    app.register_blueprint(collab)
    app.register_blueprint(mission)
    app.register_blueprint(client)
    app.register_blueprint(manager)

    # config telechargement facture
    # BALANCES_FOLDER = 'Balance'
    # app.config['BALANCES_FOLDER'] = BALANCES_FOLDER

    # if not os.path.exists(BALANCES_FOLDER):
    #     os.makedirs(BALANCES_FOLDER)

    return app, mode