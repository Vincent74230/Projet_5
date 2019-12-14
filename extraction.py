# -*- coding: utf-8 -*-
"""Module that contains 2 fonctions:
- one for extracting datas from OpenFoodFacts API(retrieve a list as a Json file)
- the second to record datas in SQL database via mysql client """
import mysql.connector
import requests


def import_products(cats):
    """fonction that fetches json datas on Open FoodFacts API, returns a list of dict"""
    product_items = []
    for element in cats:

        payload = {'action':'process', 'json':1, 'page_size':1000, 'tag_0':element,
                   'tag_contains_0':'contains', 'tagtype_0':'categories',
                   'sort_by':'unique_scans_n'}
        try:
            response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl',
                                    params=payload, headers={'User-Agent':'Apptest - GNU/Linux - Version 0.1'})
            print("Extraction des {} du serveur d'OFF: {} 'ok'".format(element, response))
        except:
            print("Le serveur d'OFF ne répond pas ou la page est introuvable, \n"
                  " veuillez réessayer plus tard. Réponse : {}".format(response))
        response = response.json()
        response = response['products']
        product_items.append(response)
    return product_items

def record_into_database(product_items, cats):
    """fonction that logs datas in local SQL DB"""
    connection = mysql.connector.connect(
        host='localhost',
        user='etudiant',
        password='motdepasse',
        database='pur_beurre'
        )
    kursor = connection.cursor()
    add_product = ("INSERT INTO Prod (id, name, nova, category, brand, stores)"
                   " VALUES (%s, %s, %s, %s, %s, %s)")

    for category_nb, elements in enumerate(product_items):#going to see each category of list
        for element in elements:#log each product in DB..
            try:
                data = (element['id'], element['product_name_fr'], element['nova_groups'],
                        cats[category_nb], element['brands'], element['stores'])
                kursor.execute(add_product, data)
            except KeyError:
                print("Fixed an issue with aff datas (key_error)")
            except mysql.connector.Error:
                print("Issue with mysql : Fixed")
        connection.commit()
    kursor.close()
    connection.close()

categories = ['boissons avec sucre ajoute', 'pate a tartiner', 'cafe', 'chocolat', 'chips']
#Those names will be useful BOTH to find products in OpenFF DB..
#..AND to rename category of each product in local DB (2 elements minimum)
product_items = import_products(categories)
record_into_database(product_items, categories)
