import random

class Database:
    def __init__(self):
        self.categories = []
        self.cat_len = 0
        self.substitutes = []
        self.temporary_list = []
        self.user_first_choice_id = 0
        self.favourites_id = []
        self.kursor = 0

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
        self.kursor.execute("SELECT id,name,brand,nova,category FROM Product WHERE nova = '4' AND category = %s",(self.categories[cat_choice-1],))
        examples = self.kursor.fetchall()
        for i in range (0,10):
            rand = random.randint(0,len(examples))
            self.temporary_list.append(examples[rand]) #todo later : check to pick unique numbers in that list

    def fetch_substitutes(self,product_choice):
        self.user_first_choice_id = self.temporary_list[product_choice-1][0]
        user_first_choice_category = self.temporary_list[product_choice-1][4]

        for i in range (1,4):
            try:
                self.kursor.execute ("SELECT id FROM Product WHERE nova = %s AND category = %s",(i,user_first_choice_category))
                substitute = self.kursor.fetchall()
                rand = random.randint (0,len(substitute))
                self.substitutes.append(substitute[rand][0])
            except:
                pass

    def log_in_bd(self):
        string_substitutes = ",".join(self.substitutes)
        add_ids = ("INSERT INTO Favourites (no,sub) VALUES (%s,%s)")
        data_ids = (self.user_first_choice_id,string_substitutes)
        self.kursor.execute(add_ids,data_ids)

    def fetch_favourites(self):
        while True:
            for i,ele in enumerate (self.favourites_id):
                self.kursor.execute("SELECT name,brand,nova FROM Product WHERE id = %s",(ele[0],))
                response = self.kursor.fetchall()
                print (response[0][0])
                print ("Tapez {} pour revoir les substituts de : {} de la marque {} (indice nova {})".format(i+1,response[0][0],response[0][1],response[0][2]))

            choice = self.secure_input(1,len(self.favourites_id))
            self.kursor.execute("SELECT sub FROM Favourites WHERE no = %s",(self.favourites_id[choice-1][0],))
            response = self.kursor.fetchall()
            substitute_list = response[0][0].split(",")
            for element in substitute_list:
                self.kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(element,))
                response = self.kursor.fetchall()
                response = response[0]
                print ("Voici les substitus proposés pour votre recherche :\nNom:{}, marque:{}, indice nova:{}, magasins où l'acheter : {}, lien vers une description complete: https://fr.openfoodfacts.org/produit/{}".format(response[0],response[1],response[2],response[3],response[4]))

            print ("Voulez-vous effectuer une autre recherche dans vos favorits ? Oui = 1, non =0")
            again = self.secure_input(0,1)
            if again == 1:
                continue
            else:
                break
            break