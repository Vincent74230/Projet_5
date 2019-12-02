import mysql.connector
import random


class Database:
    def __init__(self):
        self.categories = []
        self.cat_len = 0
        self.user_research = []
        self.temporary_list = []

        kursor.execute("SELECT DISTINCT category FROM Product")
        cat_row = kursor.fetchall()
        self.cat_len = len(cat_row)
        for i in range(0,self.cat_len):
            self.categories.append(cat_row[i][0])

    def secure_input(self,limit):

        wrong_input = True
        while wrong_input:
            while True:
                try:
                    choice = int(input())
                    break
                except ValueError:
                    print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
            if choice <=0 or choice > limit:
                print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
            else:
                wrong_input = False
        return choice

    def fetch_in_db(self,choice):#fetches 10 products in bd
        kursor.execute("SELECT id,name,brand,nova,category FROM Product WHERE nova = '4' AND category = %s",(self.categories[choice-1],))
        ids = kursor.fetchall()
        len_ids = len(ids)
        
        try:
            for i in range (0,10):
                rand = random.randint(0,len_ids)
                self.temporary_list.append(ids[rand])
        except:
            pass

    def fetch_substitute(self,category,users_choice_id):
        self.user_research.append(users_choice_id)

        for i in range (1,4):
            try:
                kursor.execute ("SELECT id FROM Product WHERE nova = %s AND category = %s",(i,category))
                result = kursor.fetchall()
                rand = random.randint (0,len(result))
                self.user_research.append(result[rand][0])
            except:
                pass
"""
    def log_in_bd(self):
        col = ['no','sub1','sub2','sub3']
        for i in range (0,4):
            try:
                kursor.execute("INSERT INTO Favourites (%s) VALUES (%s)",(col[i],self.user_research[i]))
            except:
                pass
        

        kursor.execute("INSERT INTO Favourites (%s) VALUES (%s)",(col[0],self.user_research[0]))
        connection.commit()
"""

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
    for i in range (0,research.cat_len):
            print ("Choix   {}:   n°{}".format(research.categories[i],i+1))
    cat_choice = research.secure_input(research.cat_len)
    research.fetch_in_db(cat_choice)

    print ("Veuillez choisir le produit que vous souhaitez substituer:")
    for i in range (0,len(research.temporary_list)):
        print ("Choix n° {} : Nom : {}, marque : {}, indice nova : {}".format(i+1,research.temporary_list[i][1],research.temporary_list[i][2],research.temporary_list[i][3]))
    
    product_choice = research.secure_input(len(research.temporary_list))

    research.fetch_substitute(research.temporary_list[product_choice-1][4],research.temporary_list[product_choice-1][0])

    print ("\nVoici le resultat de votre recherche pour : ")
    kursor.execute("SELECT name,brand,nova FROM Product WHERE id = %s\n",(research.user_research[0],))
    initial_product = kursor.fetchall()
    print ("{}, marque:  {}, indice nova : {}\n".format(initial_product[0][0],initial_product[0][1],initial_product[0][2]))
    print ("Substituts:")
    for i in range (1,len(research.user_research)):
        kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(research.user_research[i],))
        total = kursor.fetchall()
        print ("\nNom du produit : {}, marque:  {}, indice nova : {}, ce produit est en vente dans les enseignes : {}.\n Lien vers une description complete :"
        " https://fr.openfoodfacts.org/produit/{}\n".format(total[0][0],total[0][1],total[0][2],total[0][3],total[0][4]))

    print ("Voulez-vous enregistrer le resultat de votre recherche dans vos favorits?")

    #research.log_in_bd()

    print ("Voulez-vous effectuer une nouvelle recherche ?\nOui tapez 1 , non tapez 2")
    again = research.secure_input(2)
    if again == 2:
        break
    elif again == 1:
        research.user_research = []
        research.temporary_list = []
        continue
    break


kursor.close()
connection.close()
