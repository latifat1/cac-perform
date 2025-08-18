import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
  DEBUG=False
  TESTING=False


class ProductionConfig(Config):
  ENV='production'
  SECRET_KEY=os.getenv('SECRET_KEY')
  MONGO_HOST=os.getenv('MONGO_HOST')
  MONGO_PORT=os.getenv('MONGO_PORT')
  DB_NAME=os.getenv('DB_NAME')


class DevelopmentConfig(Config):
  DEBUG=True
  ENV='development'

  SECRET_KEY="i_love_you"
  MONGO_HOST="localhost:27017"
  MONGO_PORT=27017
  DB_NAME="cac_perform"