import random
import mysql.connector

class Database:
    def __init__(self):
        self.categories = ['Voir vos favorits']
        self.sub_list = []
        self.product_choice_id = 0
        
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
        self.product_choice_id = ten_examples[product_choice-1]
        self.fetch_substitutes(cat_choice)
        
    def display_product_from_id(self,product_id):
        self.kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(product_id,))
        response = self.kursor.fetchall()
        response = response[0]
        print ("{} de la marque {} (indice nova : {}), disponible dans les magasins {}.\nLien vers une description complete https://fr.openfoodfacts.org/produit/{}\n".format(response[0],response[1],response[2],response[3],response[4]))

    def fetch_substitutes(self,cat_choice):
        category = self.categories[cat_choice]
        for i in range(1,4):
            self.kursor.execute("SELECT id FROM Product WHERE nova = %s AND category = %s",(i,category))
            response = self.kursor.fetchall()
            if response != []:
                self.sub_list.append(response[random.randint(0,len(response)-1)][0])

        print ("Voici les substituts trouvés pour:")
        self.display_product_from_id(self.product_choice_id)
        for element in self.sub_list:
            self.display_product_from_id(element)

        print ("Voulez-vous enregistrer votre recherche dans vos favoris? Oui tapez 1 Non tapez 0")

        logging = self.secure_input(0,1)

        if logging == 0:
            pass
        elif logging == 1:
            self.log_in_DB()
            self.connection.commit()
        
    def log_in_DB(self):
        for element in self.sub_list:
            add_id = ("INSERT INTO Product_substitute (product_id,substitute_id) VALUES(%s,%s)")
            data = (self.product_choice_id,element)
            self.kursor.execute(add_id,data)

    def fetch_favourites(self):
        while True:
            self.kursor.execute("SELECT DISTINCT product_id FROM Product_substitute")
            response = self.kursor.fetchall()
            
            for i,element in enumerate (response):
                print ("Tapez {} pour voir les substituts de:".format(i+1))
                self.display_product_from_id(element[0])
            
            choice_id = response[self.secure_input(1,len(response))-1]
            
            self.kursor.execute("SELECT substitute_id FROM Product_substitute WHERE product_id = %s",(choice_id[0],))
            response = self.kursor.fetchall()

            print("Voici les substituts trouves pour:")
            self.display_product_from_id(choice_id[0])
            for element in response:
                self.display_product_from_id(element[0])

            print("Faire une autre recherche dans vos favoris? Oui = 1 non =0")
            again = self.secure_input(0,1)
            if again == 1:
                continue
            else:
                break
