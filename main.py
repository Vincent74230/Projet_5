import mysql.connector
from read_n_write import *

connection = mysql.connector.connect(
        host = 'localhost',
        user = 'etudiant',
        password = 'motdepasse',
        database = 'pur_beurre'
        )

research = Database()
research.kursor = connection.cursor()

research.kursor.execute("SELECT DISTINCT category FROM Product")
categories = research.kursor.fetchall()
for element in categories:
    research.categories.append(element[0])

print ("\n\t*-+/*-+/*-+/*-+Bienvenue dans ce programme de substitution alimentaire/*-+/*-+/*-+/*-+\n")
print ("\t Ce programme propose une alternative plus saine à ce que vous mangez d'habitude")

while True:
    print ("Veuillez choisir une catégorie :\n\n")
    research.kursor.execute("SELECT no FROM Favourites")
    research.favourites_id = research.kursor.fetchall()

    if research.favourites_id == []:
        for i,category in enumerate(research.categories):
            print ("Choix   {}:   n°{}".format(category,i+1))
        cat_choice = research.secure_input(1,len(research.categories))
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
        research.kursor.execute("SELECT name,brand,nova,stores,id FROM Product WHERE id = %s",(research.substitutes[i],))
        total = research.kursor.fetchall()
        print ("\nNom du produit : {}, marque:  {}, indice nova : {}, ce produit est en vente dans les enseignes : {}.\n Lien vers une description complete : https://fr.openfoodfacts.org/produit/{}\n".format(total[0][0],total[0][1],total[0][2],total[0][3],total[0][4]))
    
    print ("Voulez-vous enregistrer le resultat de votre recherche dans vos favorits?\nOui tapez 1, non tapez 2")

    logging = research.secure_input(1,2)

    if logging == 2:
        pass
    elif logging == 1:
        research.log_in_bd()
        connection.commit()

    print ("Voulez-vous effectuer une nouvelle recherche ?\nOui tapez 1, non tapez 2")
    again = research.secure_input(1,2)
    if again == 2:
        break
    elif again == 1:
        research.substitutes = []
        research.temporary_list = []
        continue
    break
    

research.kursor.close()
connection.close()
