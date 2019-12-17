"""Main module, from here controls database module,
to read and write into local database"""
# -*- coding: utf-8 -*-
from database import *

def main():
    """Main : contains the main loop of the programm"""

    research = Database()

    research.kursor.execute("SELECT DISTINCT category FROM Product")
    categories = research.kursor.fetchall()
    for element in categories:
        research.categories.append(element[0])


    print ("\n\t*-+/*-+/*-+/Bienvenue dans ce programme de substitution alimentaire/*-+/*-+/*-+/\n")
    print ("\t Ce programme propose une alternative plus saine à ce que vous mangez d'habitude\n")

    while True:
        print ("Veuillez faire un choix dans la liste ci-dessous:\n\n")

        for i, element in enumerate(research.categories):
            print ("N°{} : {}".format(i, element))
        categoy_choice = research.secure_input(0, len(research.categories)-1)

        if categoy_choice == 0:
            research.fetch_favourites()
        else:
            research.fetch_examples_in_db(categoy_choice)

        print ("Voulez-vous effectuer une nouvelle recherche ?\nOui tapez 1, non tapez 0")
        again = research.secure_input(0, 1)
        if again == 0:
            break
        elif again == 1:
            research.sub_list = []
            research.product_choice_id = 0
            continue
        break

    research.kursor.close()
    research.connection.close()

if __name__ == "__main__":
    main()
