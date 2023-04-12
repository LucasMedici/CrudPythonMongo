import redis
import os
import json
import bson
from bson import ObjectId

from crud_cliente import *;



conR = redis.Redis(
  host='redis-13523.c14.us-east-1-3.ec2.cloud.redislabs.com',
  port=13523,
  password='C2JYyEBusx1c6TUlzgzP8zVfKa5ksi7j')


def AddFavsPeloRedis():

    class MongoEncoder(json.JSONEncoder):
        def default (self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return json.JSONEncoder.default(self, obj)



    print("### CADASTRANDO UM NOVO FAVORITO NO REDIS ###")
    cpf_usuario = input("Digite o CPF do usuario que deseja cadastrar um novo favorito: ")
    obj_cliente = Cliente_findQuery(cpf_usuario)



    favoritos_em_string = json.dumps((obj_cliente),cls=MongoEncoder)

    def sincronizandoRedis():
        conR.delete('cliente:favoritos')
        conR.set('cliente:favoritos', favoritos_em_string)
        
            
            
    def novoFavorito():
        os.system('cls')
        print('### CADASTRANDO UM NOVO FAVORITO ###')
        id_novofavorito = input("Digite o ID do novo favorito: ")
        nome_novofavorito = input("Digite o nome do novo favorito: ")
        novo_favorito = {"id_produto":id_novofavorito,"nome_produto":nome_novofavorito}
        
        string_redis = str(conR.get('cliente:favoritos'))
        string_redis = string_redis[2:-1]
        string_to_obj = json.loads(string_redis)
        string_to_obj['favoritos'].append(novo_favorito)
        
        transf_em_obj = json.dumps(string_to_obj)
        conR.set('cliente:favoritos', transf_em_obj)
        print(conR.get('cliente:favoritos'))
        

    def sincronizandoMongo():
        pont_usuario_para_substituir = str(conR.get('cliente:favoritos')) 
        pont_usuario_para_substituir = pont_usuario_para_substituir[2:-1]
        obj = json.loads(pont_usuario_para_substituir)
        obj['_id']= bson.ObjectId(obj['_id'])
        SubstituindoClienteCompleto(cpf_usuario, obj)
    
        
        
    sincronizandoRedis()
    novoFavorito()
    sincronizandoMongo()