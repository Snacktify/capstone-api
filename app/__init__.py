from flask import Flask, request 
from flask_jwt_extended import JWTManager
import os
import psycopg2
from dotenv import load_dotenv

CREATE_IKEA_TABLE = ("""CREATE TABLE IF NOT EXISTS ikea (
    id INT,
    item_id INT,
    name VARCHAR(21),
    category VARCHAR(13),
    price NUMERIC(5, 1),
    old_price VARCHAR(12),
    sellable_online VARCHAR(5),
    link VARCHAR(127),
    other_colors VARCHAR(3),
    short_description VARCHAR(66),
    designer VARCHAR(518),
    depth INT,
    height INT,
    width INT
    );"""
)

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (username VARCHAR, password VARCHAR);"
)

INSERT_IKEA = ("""INSERT INTO ikea VALUES
    (3,80155205,'STIG','Bar furniture',69.0,'No old price','True','https://www.ikea.com/sa/en/p/stig-bar-stool-with-backrest-black-silver-colour-80155205/','Yes','        Bar stool with backrest,          74 cm','Henrik Preutz',50,100,60),
    (4,30180504,'NORBERG','Bar furniture',225.0,'No old price','True','https://www.ikea.com/sa/en/p/norberg-wall-mounted-drop-leaf-table-white-30180504/','No','        Wall-mounted drop-leaf table,          74x60 cm','Marcus Arvonen',60,43,74),
    (5,10122647,'INGOLF','Bar furniture',345.0,'No old price','True','https://www.ikea.com/sa/en/p/ingolf-bar-stool-with-backrest-white-10122647/','No','        Bar stool with backrest,          63 cm','Carina Bengs',45,91,40);"""
)
load_dotenv()



host = "tiny.db.elephantsql.com"
databae = "evraaplf"
user = "evraaplf"
password = "NFS3gR7li2xSae2TgMWqKXdWqGYm7S69"

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(host=host, database=databae, user=user, password=password)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     database="tubestst",
# )
# mydb_cursor = mydb.cursor()
connection_cursor = connection.cursor()
from app import routes #Memanggil file routes (akan segera dibuat)