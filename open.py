import mysql.connector
import requests


payload = {'action':'process','json':1,'page_size':50,'tag_0':'Boissons avec sucre ajouté',
'tag_contains_0':'contains','tagtype_0':'categories','sort_by':'unique_scans_n'}

response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl',
params = payload,headers = {'User-Agent':'Apptest - GNU/Linux - Version 0.1'})

print(response)

res_json = response.json()

products = res_json['products']
n = len(products)

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'etudiant',
    password = 'motdepasse',
    database = 'pur_beurre'
)

kursor = connection.cursor()

add_product = ("INSERT INTO Product (id,name,nova,category,brand,stores) VALUES (%s,%s,%s,%s,%s,%s)")


for i in range(0,n):
    try:
        data_product = (products[i]['id'],products[i]['product_name_fr'],products[i]['nova_groups'],'boissons',products[i]['brands'],products[i]['stores'])
        kursor.execute(add_product,data_product)
    except KeyError:
        data_product = (products[i]['id'],products[i]['product_name_fr'],None,'boissons',products[i]['brands'],products[i]['stores'])
        kursor.execute(add_product,data_product)
        print ("Une keyerror s'est produite ligne{}".format(i+1))
    except:
        pass
connection.commit()

kursor.close()

connection.close()
