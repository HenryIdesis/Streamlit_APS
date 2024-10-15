from flask import Flask, request, make_response, json
import pandas as pd
from flask import Flask, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/usuarios', methods=['GET'])
def get_all_users():

    filtro = {}
    projecao = {"_id" : 0}
    dados_usuarios = mongo.db.usuarios.find(filtro, projecao)

    resp = {
        "usuarios": list( dados_usuarios )
    }

    return resp, 200

@app.route('/usuarios/<string:_id>', methods=['GET'])
def get_user(_id):
    
    user = mongo.db.usuarios.find_one({"_id": ObjectId(_id)})

    
    if user is None:
        return {"erro": "Usuario não encontrado"}, 404
        
    
    user['_id'] = str(user['_id'])
        
    return user, 200


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/usuarios', methods=['POST'])
def post_user():
    
    data = request.json
    

    if "cpf" not in data:
        return {"erro": "cpf é obrigatório"}, 400
    if "nome" not in data:
        return {"erro": "nome é obrigatório"}, 400
    if "data_de_nascimento" not in data:
        return {"erro": "data de nascimento é obrigatório"}, 400
    
    result = mongo.db.usuarios.insert_one(data)

    return {"id": str(result.inserted_id)}, 201


@app.route('/usuarios/<string:_id>', methods=['PUT'])
def put_user(_id):

    data = request.json

    result = mongo.db.usuarios.update_one({"_id": ObjectId(_id)}, {"$set": data})
    
    if result.modified_count == 0:
        return {"erro": "usuario não encontrado ou nenhuma alteração realizada"}, 404

    return {"message": "usuario atualizado com sucesso"}, 200


@app.route('/usuarios/<string:_id>', methods=['DELETE'])
def delete_user(_id):
    
        # Tenta deletar o documento no MongoDB
    result = mongo.db.usuarios.delete_one({"_id": ObjectId(_id)})

        # Verifica se um documento foi deletado
    if result.deleted_count == 0:
        return {"erro": "usuarios não encontrado"}, 404

    return {"message": "usuarios deletado com sucesso"}, 200

@app.route('/bikes', methods=['GET'])
def get_all_bikes():

    filtro = {}
    projecao = {"_id" : 1, "marca": 1, "modelo": 1, "cidade": 1}
    dados_bikes = mongo.db.bikes.find(filtro, projecao)

    resp = {
        "bikes": list( dados_bikes )
    }

    return resp, 200

@app.route('/bikes/<string:_id>', methods=['GET'])
def get_bike(_id):
    
    bike = mongo.db.bikes.find_one({"_id": ObjectId(_id)})

    if bike is None:
        return {"erro": "bike não encontrado"}, 404
        
    
    bike['_id'] = str(bike['_id'])
        
    return bike, 200


@app.route('/bikes', methods=['POST'])
def post_bike():
    
    data = request.json

    if "marca" not in data or "modelo" not in data or "cidade" not in data:
        return {"erro": "Todas informacoes sao obrigatórias"}, 400
    
    result = mongo.db.bikes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/bikes/<string:_id>', methods=['PUT'])
def put_bike(_id):

    data = request.json

    result = mongo.db.bikes.update_one({"_id": ObjectId(_id)}, {"$set": data})
    
    if result.modified_count == 0:
        return {"erro": "bike não encontrado ou nenhuma alteração realizada"}, 404

    return {"message": "bike atualizado com sucesso"}, 200

@app.route('/bikes/<string:_id>', methods=['DELETE'])
def delete_bike(_id):
    result = mongo.db.bikes.delete_one({"_id": ObjectId(_id)})

        # Verifica se um documento foi deletado
    if result.deleted_count == 0:
        return {"erro": "bikes não encontrado"}, 404

    return {"message": "bikes deletado com sucesso"}, 200


if __name__ == '__main__':
    app.run(debug=True)
