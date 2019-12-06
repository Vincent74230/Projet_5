import mysql.connector
import random


class Database:
    def __init__(self):
        self.categories = []
        self.cat_len = 0
        self.substitutes = []
        self.temporary_list = []
        self.user_first_choice_id = 0
        self.favourites_id = []

        kursor.execute("SELECT DISTINCT category FROM Product")
        cat_row = kursor.fetchall()
        self.cat_len = len(cat_row)
        for i in range(0,self.cat_len):
            self.categories.append(cat_row[i][0])

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
        kursor.execute("SELECT id,name,brand,nova,category FROM Product WHERE nova = '4' AND category = %s",(self.categories[cat_choice-1],))
        examples = kursor.fetchall()
        for i in range (0,10):
            rand = random.randint(0,len(examples))
            self.temporary_list.append(examples[rand]) # todo later : check to pick unique numbers in that list

    def fetch_substitutes(self,product_choice):
        self.user_first_choice_id = self.temporary_list[product_choice-1][0]
        user_first_choice_category = self.temporary_list[product_choice-1][4]

        for i in range (1,4):
            try:
                kursor.execute ("SELECT id FROM Product WHERE nova = %s AND category = %s",(i,user_first_choice_category))
                substitute = kursor.fetchall()
                rand = random.randint (0,len(substitute))
                self.substitutes.append(substitute[rand][0])
            except:
                pass

    def log_in_bd(self):
        string_substitutes = ",".join(self.substitutes)
        add_ids = ("INSERT INTO Favourites (no,sub) VALUES (%s,%s)")
        data_ids = (self.user_first_choice_id,string_substitutes)
        kursor.execute(add_ids,data_ids)
        connection.commit()

    def fetch_favourites(self):
        while True:
            for i,ele in enumerate (self.favourites_id):
                kursor.execute("SELECT name,brand,nova FROM Product WHERE id = %s",(ele[0],))
                response = kursor.fetchall()
                print (response[0][0])
                print ("Tapez {} pour revoir les substituts de : {} de la marque {} (indice nova {})".format(i+1,response[0][0],response[0][1],response[0][2]))

            choice = self.secure_input(1,len(self.favourites_id))
            kursor.execute("SELECT sub FROM Favourites WHERE no = %s",(self.favourites_id[choice-1][0],))
            response = kursor.fetchall()
            substitute_list = response[0][0].split(",")
            for element in substitute_list:
                kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(element,))
                response = kursor.fetchall()
                response = response[0]
                print ("Voici les substitus proposés pour votre recherche :\nNom:{}, marque:{}, indice nova:{}, magasins où l'acheter : {}, lien vers une description complete: https://fr.openfoodfacts.org/produit/{}".format(response[0],response[1],response[2],response[3],response[4]))

            print ("Voulez-vous effectuer une autre recherche dans vos favorits ? Oui = 1, non =0")
            again = self.secure_input(0,1)
            if again == 1:
                continue
            else:
                break
            break
        


connection = mysql.connector.connect(
host = 'localhost',
user = 'etudiant',
password = 'motdepasse',
database = 'pur_beurre'
)
kursor = connection.cursor()


print ("\n\t*-+/*-+/*-+/*-+Bienvenue dans ce programme de substitution alimentaire/*-+/*-+/*-+/*-+\n")
print ("\t Ce programme propose une alternative plus saine à ce que vous mangez d'habitude")
research = Database()

while True:
    print ("Veuillez choisir une catégorie :\n\n")
    kursor.execute("SELECT no FROM Favourites")
    research.favourites_id = kursor.fetchall()

    if research.favourites_id == []:
        for i in range (0,research.cat_len):
            print ("Choix   {}:   n°{}".format(research.categories[i],i+1))
        cat_choice = research.secure_input(1,research.cat_len)
    else:
        print ("Voir vos resultats favoris : pressez 0\n")
        for i in range (0,research.cat_len):
            print ("Choix   {}:   n°{}".format(research.categories[i],i+1))
        cat_choice = research.secure_input(0,research.cat_len)
    
    if cat_choice == 0:
        research.fetch_favourites()

    research.fetch_examples_in_db(cat_choice)

    print ("Veuillez choisir le produit que vous souhaitez substituer:")
    for i in range (0,len(research.temporary_list)):
        print ("Choix n° {} : Nom : {}, marque : {}, indice nova : {}".format(i+1,research.temporary_list[i][1],research.temporary_list[i][2],research.temporary_list[i][3]))
    
    product_choice = research.secure_input(1,len(research.temporary_list))

    research.fetch_substitutes(product_choice)
    
    print ("\nVoici le resultat de votre recherche pour : ")
    print ("{}, marque:  {}, indice nova : {}\n".format(research.temporary_list[product_choice-1][1],research.temporary_list[product_choice-1][2],research.temporary_list[product_choice-1][3]))
    print ("Substituts trouvés:")
    for i in range (0,len(research.substitutes)):
        kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(research.substitutes[i],))
        total = kursor.fetchall()
        print ("\nNom du produit : {}, marque:  {}, indice nova : {}, ce produit est en vente dans les enseignes : {}.\n Lien vers une description complete : https://fr.openfoodfacts.org/produit/{}\n".format(total[0][0],total[0][1],total[0][2],total[0][3],total[0][4]))
    
    print ("Voulez-vous enregistrer le resultat de votre recherche dans vos favorits?\nOui tapez 1, non tapez 2")

    logging = research.secure_input(1,2)

    if logging == 2:
        pass
    elif logging == 1:
        research.log_in_bd()


    print ("Voulez-vous effectuer une nouvelle recherche ?\nOui tapez 1 , non tapez 2")
    again = research.secure_input(1,2)
    if again == 2:
        break
    elif again == 1:
        research.substitutes = []
        research.temporary_list = []
        continue
    break
    

kursor.close()
connection.close()
