import mysql.connector
from off_open import categories

connection = mysql.connector.connect()


print ("\n\t*-+/*-+/*-+/*-+Bienvenue dans ce programme de substitution alimentaire/*-+/*-+/*-+/*-+\n")
print ("\t Ce programme propose une alternative plus saine à ce que vous mangez d'habitude")


cat_len = len(categories)

while True:
    
    print ("Veuillez choisir une catégorie :\n\nAttention : veuillez n'entrer qu'un chiffre correspondant à la categorie et pressez 'entree'\n")

    for i in range (0,cat_len):
        print ("Choix {}:{}".format(categories[i],i+1))





    wrong_input = True
    while wrong_input:
        while True:
            try:
                cat_choice = int(input())
                break
            except ValueError:
                print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
        if cat_choice <=0 or cat_choice > cat_len:
            print("choisissez un chiffre qui vous est proposé dans la liste plus haut")
        else:
            wrong_input = False
            


    



    print (cat_choice)

    break