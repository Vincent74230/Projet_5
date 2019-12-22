import mysql.connector
import random
import settings

class Connect:
    def __init__(self):
        self.con = mysql.connector.connect(
            host='localhost',
            user=settings.user,
            password = settings.password,
            database = 'pur_beurre')
        self.cur = self.con.cursor()
        self.categories = ['Voir vos favorits']
        self.sub_list = []
        self.product_choice_id = 0

    def secure_input(self, minimum, maximum):
        """Give it a low and high limit, it returns a secure int within it"""
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

    def fetch_examples_in_db(self, cat_choice):
        """Fetches and display 10 examples of nova 4 indice from DB"""
        ten_examples = []
        product_choice_id = 0
        self.cur.execute("SELECT id FROM Product WHERE nova = 4 AND category = %s",
            (self.categories[cat_choice], ))
        examples = self.cur.fetchall()
        for i in range (0, 10):
            ten_examples.append(examples[random.randint(0, len(examples))][0])
        for i, element in enumerate(ten_examples):
            print ("Choix n°{}".format(i+1))
            self.display_product_from_id(element)

        print ("Veuillez choisir le produit que vous voulez substituer:")
        product_choice = self.secure_input(1, len(ten_examples))
        self.product_choice_id = ten_examples[product_choice-1]
        self.fetch_substitutes(cat_choice)
    def display_product_from_id(self, product_id):
        """Give it a single id, it will fetch the whole info refering to it"""
        self.cur.execute("SELECT name, brand, nova, stores, id FROM Product WHERE id = %s", (product_id, ))
        response = self.cur.fetchall()
        response = response[0]
        print ("{} de la marque {} (indice nova : {}), disponible dans les magasins {}.\n"
               "Lien vers une description complete https://fr.openfoodfacts.org/produit/{}\n".
               format(response[0], response[1], response[2], response[3], response[4]))

    def fetch_substitutes(self, cat_choice):
        """Fetches maximum 3 substitutes, of 1,2 and 3 nova indices in DB,and displays it""" 
        category = self.categories[cat_choice]
        for i in range(1, 4):
            self.cur.execute("SELECT id FROM Product WHERE nova = %s AND category = %s", (i, category))
            response = self.cur.fetchall()
            if response != []:
                self.sub_list.append(response[random.randint(0, len(response)-1)][0])

        print ("Voici les substituts trouvés pour:")
        self.display_product_from_id(self.product_choice_id)
        for element in self.sub_list:
            self.display_product_from_id(element)

        print ("Voulez-vous enregistrer votre recherche dans vos favoris? Oui tapez 1 Non tapez 0")

        logging = self.secure_input(0, 1)

        if logging == 0:
            pass
        elif logging == 1:
            self.log_in_DB()
            self.con.commit()
        
    def log_in_DB(self):
        """Logs favourite resulsts in DB, (the design of Product_substitute in DB is "many-to-many")"""
        for element in self.sub_list:
            add_id = ("INSERT INTO Product_substitute (product_id, substitute_id) VALUES(%s, %s)")
            data = (self.product_choice_id, element)
            self.cur.execute(add_id, data)

    def fetch_favourites(self):
        """Fetches favourites in DB, from an favourite id"""
        while True:
            self.cur.execute("SELECT DISTINCT product_id FROM Product_substitute")
            response = self.cur.fetchall()

            for i, element in enumerate (response):
                print ("Tapez {} pour voir les substituts de:".format(i+1))
                self.display_product_from_id(element[0])
            
            choice_id = response[self.secure_input(1, len(response))-1]
            
            self.cur.execute("SELECT substitute_id FROM Product_substitute WHERE product_id = %s", (choice_id[0], ))
            response = self.cur.fetchall()

            print("Voici les substituts trouves pour:")
            self.display_product_from_id(choice_id[0])
            for element in response:
                self.display_product_from_id(element[0])

            print("Faire une autre recherche dans vos favoris? Oui = 1 non =0")
            again = self.secure_input(0, 1)
            if again == 1:
                continue
            else:
                break