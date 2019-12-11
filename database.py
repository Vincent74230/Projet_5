import random
import mysql.connector

class Database:
    def __init__(self):
        self.categories = ['Voir vos favorits']
        self.sub_list = []
        
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'etudiant',
            password = 'motdepasse',
            database = 'pur_beurre')
        self.kursor = self.connection.cursor()

    def secure_input(self,minimum,maximum):
        wrong_input = True
        while wrong_input:
            while True:
                try:
                    choice = int(input())
                    break
                except ValueError:
                    print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
            if choice < minimum or choice > maximum:
                print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
            else:
                wrong_input = False
        return choice

    def fetch_examples_in_db(self,cat_choice):#fetches 10 products in bd
        ten_examples = []
        product_choice_id = 0
        self.kursor.execute("SELECT id FROM Product WHERE nova = 4 AND category = %s",(self.categories[cat_choice],))
        examples = self.kursor.fetchall()
        for i in range (0,10):
            ten_examples.append(examples[random.randint(0,len(examples))][0])
        for i,element in enumerate (ten_examples):
            print ("Choix n°{}".format(i+1))
            self.display_product_from_id(element)

        print ("Veuillez choisir le produit que vous voulez substituer:")
        product_choice = self.secure_input(1,len(ten_examples))
        product_choice_id = ten_examples[product_choice_id-1]
        self.fetch_substitutes(product_choice_id,cat_choice)
        
    def display_product_from_id(self,product_id):
        self.kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(product_id,))
        response = self.kursor.fetchall()
        response = response[0]
        print ("{} de la marque {} (indice nova : {}), disponible dans les magasins {}.\nLien vers une description complete https://fr.openfoodfacts.org/produit/{}\n".format(response[0],response[1],response[2],response[3],response[4]))

    def fetch_substitutes(self,product_choice_id,cat_choice):
        category = self.categories[cat_choice-1]
        for i in range (1,4):
            self.kursor.execute("SELECT id FROM Product WHERE nova = %s AND category = %s",(i,category))
            response = self.kursor.fetchall()
            if response != []:
                self.sub_list.append(response[random.randint(0,len(response))][0])

        print ("Voici les substituts trouvés pour:")
        self.display_product_from_id(product_choice_id)
        for element in self.sub_list:
            self.display_product_from_id(element)
        