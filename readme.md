##### TODO list du Projet 5 : Utiliser les données publiques d'OpenFoodFacts.



### Core 1 : 
__A faire__
Créer une base de donnée avec 2 tables :

Produits:
La première contiendra environ 500 produits (500 lignes) avec les attributs (colonnes) suivantes :
- Id
- Categorie du produit
- Nom du produit
- Marque
- Denomination generique
- indice nova
- indice nutriscore
- Magasin ou trouver le produit
- code barre (qui servira à generer un lien vers le site OFF)

N.B : Les produits présents seront répartis selon 5 categories

Mes favoris:
La seconde (vide tant que l'utilisateur n'a pas enregistre une recherche)
- id
- id du produit choisi par user en premier lieu
- id du ou des produits proposée en substitution.


### Fonctionnalité n°1 : Rechercher un aliment à substituer.

## User story 1 : En tant qu'utilisateur, je veux choisir un aliment pour obtenir une liste de substituts.

Spec fonctionnelles : 
L'utilisateur arrive sur le terminal, le système lui propose 2 options: 
- Rechercher des aliments de substitution
- Mes produits favoris 
L'utilisateur choisit l'option 1.
Le système demande de choisir une catégorie (user choisit) puis un aliment dans cette catégorie (user choisit).
Le système renvoie une liste d'aliments de substitution, description et l'adresse où le trouver.
User peut alors enregistrer le resultat et/ou faire une autre recherche ou quitter.

Spec Techniques:
La BDD OFF étant enorme (+ de 17000 categories), et crash souvent, faire une choix quant aux produits a extraire et ne le faire
que si la BDD interne est inexistante. Proposer a l'utilisateur une MAJ manuelle.
Le programme reçoit le produit que l'utilisateur souhaite substituer, affiche les carateristiques de ce produit et propose
des substituts presents dans la BDD (avec un indice nova et nutriscore plus favorable, a determiner)

__A faire :__ 

1 - Créer un programme en Python qui contiendra les packages "Main", "API" et "Compare"
2 - Dans le main écrire les messages d'accueil et explicatifs du programme, les boucles, ainsi que les champs "input"
pour recueillir les choix de l'utilisateur, prévoir un choix pour quitter le programme à tout moment, 
une exception si autre-chose qu'un nombre.
3 - Créer une classe dans API qui récupère les donnees OFF et les enregistre en BDD, a ne faire qu'au premier lancement du programme, ou si user le demande
4 - Creer une classe dans "compare" qui récupère en BDD un produit choisi par user et recherche un substitut en f(x) de son indice nova et nutriscore


## User story 2 : En tant qu'utilisateur, je veux enregistrer une recherche pour la garder en mémoire.

Spec fonctionnelles:
Pendant l'étape précédente, l'utilisateur choisit d'enregistrer sa recherche

Spec techniques : le système enregistre l'id du produit recherché et du ou des substituts si ils existent

__A faire :__

1 - Si user demande a enregistrer sa recherche, enregistrer id produit et id substituts dans la table "mes produits favoris"




### Fonctionnalité n°2 : Consulter les recherches enregistrées

## User story 3 : En tant qu'utilisateur je veux pouvoir consulter mes anciennes recherches.__

Spec fonctionnelles : L'utilisateur se trouve sur le terminal et décide de consulter une ancienne recherche (choix 2)
le système affiche un tableau avec le nom des aliments affectés d'un numéro, utilisateur fait un choix et presse entrée, le système affiche une ligne avec les résultats obtenus.

Spec techniques : Le système récupère les infos préalablement ernregistrées en BDD (dans la table 1 et 2 à l'aide d'une clé étrangere)

__A faire :__

1 - Utiliser clé primaire / clé étrangère pour lier et afficher le résultat dans la console.