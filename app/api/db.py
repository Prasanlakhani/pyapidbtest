from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from google.cloud import secretmanager



def SECRET_N():
    client = secretmanager.SecretManagerServiceClient()
    SECRET_NAME = {"name": f"projects/736835190022/secrets/sql_pwd/versions/latest"}
    response = client.access_secret_version(SECRET_NAME)
    SECRET_RES = response.payload.data.decode("UTF-8")
    DATABASE_URL = "postgresql+pg8000://postgres:SECRET_RES@34.145.42.112/postgres"
    return SECRET_RES
  
def getconn():
    SECRET_RESPONSE = SECRET_N()
    with Connector() as connector:
        conn = connector.connect(
            "prasan-nirav:us-west1:py-test", # Cloud SQL Instance Connection Name
            "pg8000",
            user="postgres",
            password=SECRET_RESPONSE,
            db="postgres",
            ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )
    return conn

engine = create_engine(DATABASE_URL, creator=getconn)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts', ARRAY(String))
)

database = Database(DATABASE_URL)
