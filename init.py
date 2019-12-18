"""This module is intended to create the database and tables
neccessary to run the programm on user's computer"""
import mysql.connector
from mysql.connector import errorcode
import extraction as ex

database_name = 'pur_beurre'
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

connection = mysql.connector.connect(
    user='oc_student', password='password', host='localhost')
kursor = connection.cursor()

def create_database(kursor):
    """Function that create dadabase 'pur_beurre'
    on user's system"""
    try:
        kursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database_name))
    except mysql.connector.Error as err:
        print ("Failed to create new database : {}".format(err))
        exit(1)

try:
    kursor.execute("USE {}".format(database_name))
except mysql.connector.Error as err:
    print ("Database {} does not exist".format(database_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(kursor)
        print ("Database {} created successfully.".format(database_name))
        connection.database = database_name
    else:
        print("An error has occured during database creation : {}".format(err))
        exit(1)

for table in TABLES:
    description = TABLES[table]
    print ("Desc ; {}".format(description))
    try:
        print("Creating table {}".format(table))
        kursor.execute(description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print ("Already exists")
        else:
            print("{}".format(err))

kursor.close()
connection.close()


product_items = ex.import_products(ex.categories)
ex.record_into_database(product_items, ex.categories)
