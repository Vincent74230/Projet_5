import mysql.connector
import requests



class request:
    def __init__(self):
        self.res_json=[]

    def import_products(self,categories):
        l = len(categories)

        for i in range (0,l):

            payload = {'action':'process','json':1,'page_size':1000,'tag_0':categories[i],
            'tag_contains_0':'contains','tagtype_0':'categories','sort_by':'unique_scans_n'}
            try:
                response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl',
                params = payload,headers = {'User-Agent':'Apptest - GNU/Linux - Version 0.1'})
                print ("Extraction des {} du serveur d'OFF: {} 'ok'".format(categories[i],response))
            except:
                print ("Le serveur d'OFF ne répond pas ou la page est introuvable,\n"
                " veuillez réessayer plus tard. Réponse : {}".format(response))
            response = response.json()
            response = response['products']

            self.res_json.append(response)

    def record_into_database(self,products,categories):
        
        connection = mysql.connector.connect(
        host = 'localhost',
        user = 'etudiant',
        password = 'motdepasse',
        database = 'pur_beurre'
        )
        kursor = connection.cursor()
        add_product = ("INSERT INTO Product (id,name,nova,category,brand,stores) VALUES (%s,%s,%s,%s,%s,%s)")
        
        l_cat = len(products)
        for i in range (0,l_cat):
            n_products = len(products[i])
            for x in range (0,n_products):
                try:
                    data = (products[i][x]['id'],products[i][x]['product_name_fr'],products[i][x]['nova_groups'],categories[i],products[i][x]['brands'],products[i][x]['stores'])
                    kursor.execute(add_product,data)
                except:
                    pass


        
        connection.commit()
        kursor.close()
        connection.close()


categories = ['boissons avec sucre ajoute','pate a tartiner','cafe','chocolat','chips']
req= request()
req.import_products(categories)
req.record_into_database(req.res_json,categories)
