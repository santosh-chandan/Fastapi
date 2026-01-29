from dotenv import load_dotenv
import os

load_dotenv()   # load .env into os.envornment

# Postgresql
PG_DB_URL= os.getenv('PG_DB_URL')
PG_SYNCH_DB_URL= os.getenv('PG_DB_URL')

# MongoDB
MONGO_DB_URL= os.getenv('MONGO_DB_URL')
MONGO_DB= os.getenv('MONGO_DB')

# Openapi Key
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
