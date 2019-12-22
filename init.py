"""This module is intended to create the database and tables
neccessary to run the programm on user's computer"""
import mysql.connector
from mysql.connector import errorcode
import extraction as ex
import settings

DATABASE_NAME = 'pur_beurre'
TABLES = {}

TABLES['Product'] = (
    "CREATE TABLE Product("
    "id VARCHAR(25) NOT NULL,"
    "name VARCHAR(100),"
    "nova VARCHAR(5),"
    "category VARCHAR(30),"
    "brand TEXT,"
    "stores VARCHAR(120),"
    "PRIMARY KEY (id)"
    ")ENGINE = InnoDB")

TABLES['Product_substitute'] = (
    "CREATE TABLE Product_substitute("
    "product_id VARCHAR(25) NOT NULL,"
    "substitute_id VARCHAR(25) NOT NULL,"
    "CONSTRAINT fk_product_id "
    "FOREIGN KEY (product_id) "
    "REFERENCES Product(id)"
    ")ENGINE = InnoDB")

CON = mysql.connector.connect(
    user= settings.user,
    password=settings.password,
    host='localhost')
KURSOR = CON.cursor()

def create_database(kur):
    """Creating database 'pur_beurre'
    on user's system"""
    try:
        kur.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database_name))
    except mysql.connector.Error as err:
        print ("Failed to create new database : {}".format(err))
        exit(1)

try:
    KURSOR.execute("USE {}".format(DATABASE_NAME))
except mysql.connector.Error as err:
    print ("Database {} does not exist".format(DATABASE_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(KURSOR,DATABASE_NAME)
        print ("Database {} created successfully.".format(DATABASE_NAME))
        CON.database = DATABASE_NAME
    else:
        print("An error has occured during database creation : {}".format(err))
        exit(1)

for table in TABLES:
    description = TABLES[table]
    try:
        print("Creating table {}".format(table))
        KURSOR.execute(description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print ("Already exists")
        else:
            print("{}".format(err))

KURSOR.close()
CON.close()


PRODUCT_ITEMS = ex.import_products(ex.categories)
ex.record_into_database(PRODUCT_ITEMS, ex.categories)
