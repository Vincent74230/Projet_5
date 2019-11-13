TODO list du Projet 5 : Utiliser les données publiques d'OpenFoodFacts.



Core 1 : Créer une base de donnée avec 1 table contenant : Le nom des catégories et le nom des aliments correspondants.
(Voir si on peut télécharger cela sur openfoodfacts)




Fonctionnalité n°1 : Rechercher un aliment à substituer.

User story 1 : En tant qu'utilisateur, je veux choisir un aliment pour obtenir une liste de substituts.

Spec fonctionnelles : 
L'utilisateur arrive sur le terminal, le système lui propose 2 options: Rechercher des aliments de substitution ou retrouver des aliments substitués (anciennes recherches enregistrées). L'utilisateur choisit l'option 1.
Le système demande de choisir une catégorie (user choisit) puis un aliment dans cette catégorie (user choisit).
Le système renvoie une liste d'aliments de substitution, description et l'adresse où le trouver.
User peut alors enregistrer le resultat et/ou faire une autre recherche ou quitter.

Spec Techniques:
La recherche se fera via l'API d'OpenFoodFacts qui renvoie une réponse en JSON.

A faire : 

1 - Créer un programme en Python qui contiendra les packages "Main" et "API".
2 - Dans le main écrire les messages d'accueil et explicatifs du programme, les boucles, ainsi que les champs "input"
pour recueillir les choix de l'utilisateur, prévoir un choix pour quitter le programme à tout moment, 
prévoir une boucle de relance si l'utilisateur insere autrechose qu'un chiffre.
3 - Dans API creer une classe qui interroge l'API openffoodfacts (grace aux noms de catégorie et aliments)
4 - A la réception du JSON, afficher les résultats et proposer à l'utilisateur d'enregistrer ou de quitter.



User story 2 : En tant qu'utilisateur, je veux enregistrer une recherche pour la garder en mémoire.

Spec fonctionnelles:
Pendant l'étape précédente, l'utilisateur choisit d'enregistrer sa recherche, le système enregistre les informations
(nom de l'aliment recherché, les noms des aliments de substitution, points de vente où les trouver)

Spec techniques : Ces informations seront enregistrées en base de donnée

A faire pour cette story:

1 - Créer 1 nouvelle table qui devra contenir la recherche de l'utilisateur.
2 - Classer le resultat d'une recherche en fonction de sa catégorie et du nom de l'aliment.




Fonctionnalité 2 : Consulter les recherches enregistrées

User story 3 : En tant qu'utilisateur je veux pouvoir consulter mes anciennes recherches.

Spec fonctionnelles : L'utilisateur se trouve sur le terminal et décide de consulter une ancienne recherche (choix 2)
le système affiche un tableau avec le nom des aliments affectés d'un numéro, utilisateur fait un choix et presse entrée, le système affiche une ligne avec les résultats obtenus.

Spec techniques : Le système récupère les infos préalablement ernregistrées en BDD

A faire :

1 - Proposer un choix multiple parmi les anciennes recherches (prévoir une boucle de relance si user entre une donnée non conforme)
2 - Utiliser clé primaire / clé étrangère pour lier et afficher le résultat dans la console.