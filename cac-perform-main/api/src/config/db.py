from pymongo import MongoClient
import json, os
from bson import ObjectId

class MyMongo():
  def __init__(self) -> None:
    self.mongo_host = None
    self.mongo_port = None
    self.db_name = None
    self.database = None
    self.client = None
    self.collections_infos = {
      'Balance': 'docs/balance_test.json',
      'Client': 'docs/client_test.json',
      # 'Grouping': 'docs/grouping.json',
      'Manager': None,
      'Mission1': 'docs/mission_test.json'
    }

  def init_app(self, app):
    self.mongo_host = app.config['MONGO_HOST']
    self.mongo_port = app.config['MONGO_PORT']
    self.db_name = app.config['DB_NAME']
    # self.create_db_if_dont_exist()
    self.connect_to_db()
  
  def connect_to_db(self):
    self.client = MongoClient(host=self.mongo_host, port=int(self.mongo_port))
    db = self.client[self.db_name]
    self.database = db
    self.create_db_if_dont_exist()
  
  @property
  def get_db(self):
    # print(self.database)
    return self.database


  def create_db_if_dont_exist(self):
    collections_existed = len(self.database.list_collection_names())
    if collections_existed == 0:
      print(f"Base de données <{self.db_name}> absente. Création en cours...")

      for name, json_path in self.collections_infos.items():
        print(f"Création de la collection <{name}>...")
        
        collection = self.database[name]
        if json_path:
          real_path = os.path.abspath(os.path.join(os.getcwd(), '..', json_path))
          try:
            with open(real_path, 'r', encoding='utf-8') as f:
              raw_data = json.load(f)

              if isinstance(raw_data, dict):
                raw_data = [raw_data]
              
              if raw_data:
                data = []
                for doc in raw_data:
                  if "_id" in doc and "$oid" in doc['_id']:
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
                  data.append(doc)

                collection.insert_many(data)
                print(f"Collection {name} créée avec {len(data)} document(s) ajouté(s).")
          except json.JSONDecodeError:
            print(f"Erreur de parsing JSON dans : {json_path}")
        else:
          # Forcer la création de la collection
          collection.insert_one({"_init": True})
          collection.delete_one({"_init": True})
          print(f"Collection '{name}' créée.")

      print(f"Base de données <{self.db_name}> créée avec succès...")
    else:
      print(f"Base de données <{self.db_name}> déjà présente.")
      print(f"Collections de la BD : {self.database.list_collection_names()}")
      # print(self.client.list_database_names())