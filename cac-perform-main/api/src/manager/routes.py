from flask import jsonify, make_response, request
from src.model import Manager
from src.manager import manager


@manager.post('/connexion/')
def login():

    data = request.get_json()

    mana = Manager()

    cnx = mana.sign_in(data=data)

    if cnx:
        return make_response(jsonify({"response": cnx}), 200)
    else:
        return make_response(jsonify({"response": "Nothing in the database about you"}), 201)
