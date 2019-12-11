import mysql.connector
from database import *

research = Database()

research.kursor.execute("SELECT DISTINCT category FROM Product")
categories = research.kursor.fetchall()
for element in categories:
    research.categories.append(element[0])
print (research.categories)

print ("\n\t*-+/*-+/*-+/*-+Bienvenue dans ce programme de substitution alimentaire/*-+/*-+/*-+/*-+\n")
print ("\t Ce programme propose une alternative plus saine à ce que vous mangez d'habitude\n")

while True:
    print ("Veuillez faire un choix dans la liste ci-dessous:\n\n")

    for i,element in enumerate (research.categories):
        print ("N°{} : {}".format(i,element))
    categoy_choice = research.secure_input(0,len(research.categories)-1)

    if categoy_choice == 0:
        research.fetch_favourites()
    else:
        research.fetch_examples_in_db(categoy_choice)
    
    print ("Voulez-vous enregistrer le resultat de votre recherche dans vos favorits?\nOui tapez 1, non tapez 0")
    
    logging = research.secure_input(0,1)

    if logging == 0:
        pass
    elif logging == 1:
        research.log_in_bd()
        connection.commit()

    print ("Voulez-vous effectuer une nouvelle recherche ?\nOui tapez 1, non tapez 0")
    again = research.secure_input(0,1)
    if again == 0:
        break
    elif again == 1:
        research.substitutes = []
        research.temporary_list = []
        continue
    break

    
research.kursor.close()
research.connection.close()
