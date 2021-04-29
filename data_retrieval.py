import requests
import urllib
import os
import shutil
import re
import csv
import time

from bs4 import BeautifulSoup
from pprint import pprint


NBRE_DE_PAGES = 50
# Valeur mini 2, maximum = 50 (pour 1000 livres).
# En cas de test cette valeur peut être diminuée.


liens_vers_livres = []
contenu_page_vue = []
dico_elements = {}

def pages_a_visiter():
    """
    --- ETAPE 1 ----
    - collecte des tous les liens vers les livres en parcourant les 50 pages du site -
    """

    for numero in range(1, NBRE_DE_PAGES+1):
        url_pages_site = "http://books.toscrape.com/catalogue/page-" + str(numero) + ".html"

        response = requests.get(url_pages_site)

        if response.ok:
            soup_site = BeautifulSoup(response.text, "html.parser")
            lis = soup_site.findAll("h3")
            for li in lis:
                a = li.find('a')
                if a is not None:
                    page = a["href"]
                    liens_vers_livres.append(urllib.parse.urljoin(url_pages_site, page))






# def soup_url_finaux():
#     """
#     ---ETAPE 3---
#     Préparation de la soup issue des 1000 pages des livres
#     """
#
#     for url in liens_vers_livres:
#         response_3 = requests.get(url)
#
#         if response_3.ok:
#             soup = BeautifulSoup(response_3.content, "html.parser")
#     return


def collecte_elements_texte():
    """
    # ---ETAPE 4---
    # - BOUCLE SUR CHAQUE PAGE D'UN LIVRE
    # - collecte des éléments textes qui seront chargés dans les fichier csv
    """
    # j'ouvre un dictionnaire
    # dico_elements = {}
    # j'y ajoute des dictionnaires imbriqués numéroté 1 et suivant

    # for num_dict in range(1, len(liens_vers_livres) + 1):

    num_dict = -1
    for url in liens_vers_livres:
        num_dict += 1
        dico_elements[num_dict] = {}
        response_3 = requests.get(url)

        if response_3.ok:
            soup = BeautifulSoup(response_3.content, "html.parser")

        dico_elements[num_dict]["product_page_url"] = url

        for i in soup.find_all("th"):
            if i.text.strip() == "UPC":
                upc = i.find_next("td").text.strip()
                dico_elements[num_dict]["universal_product_code"] = upc
            if i.text.strip() == "Price (incl. tax)":
                price_incl = i.find_next("td").text.strip()
                dico_elements[num_dict]["price_including_tax"] = price_incl
            if i.text.strip() == "Price (excl. tax)":
                price_excl = i.find_next("td").text.strip()
                dico_elements[num_dict]["price_excluding_tax"] = price_excl
            if i.text.strip() == "Availability":
                availability = i.find_next("td").text.strip()
                cell_availability = availability.split("(")
                number_available = cell_availability[1].strip(" available)")
                dico_elements[num_dict]["number_available"] = number_available

        # titre
        title = soup.find("li", class_="active").text
        dico_elements[num_dict]["title"] = title

        # Recherche de la description (deux livres n'ont pas de description)
        if soup.find("div", id="product_description", class_="sub-header") is None:
            dico_elements[num_dict]["product_description"] = "Pas de description"
        else:
            for e in soup.find_all("div", id="product_description", class_="sub-header"):
                dico_elements[num_dict]["product_description"] = e.find_next_sibling().text

        # Recherche de la catégorie
        soup_category = soup.find("ul", class_="breadcrumb")
        link_category = soup_category.findAll("a")
        category = link_category[2].text
        dico_elements[num_dict]["category"] = category

        # Recherche de la notation
        star = []
        for d in soup.find_all("p", class_=re.compile('^star-rating.*')):
            star.append(d["class"][1])
            review_rating = star[0]
            dico_elements[num_dict]["review_rating"] = review_rating

        # !!!! Attention, voir comment ajouter si dico local, le lien image de l'autre fonction

        # dico_elements[upc] = {}
        # dico_elements[upc]["product_page_url"] = url
        # dico_elements[upc]["title"] = title
        # dico_elements[upc]["price_including_tax"] = price_incl
        # dico_elements[upc]["price_excluding_tax"] = price_excl
        # dico_elements[upc]["number_available"] = number_available
        # dico_elements[upc]["product_description"] = product_description
        # dico_elements[upc]["category"] = category
        # dico_elements[upc]["review_rating"] = review_rating

    print(len(dico_elements))


def collecte_images():
    """
    ---ETAPE 5---
    - Collecte des images des livres en les classant dans un dossier images.
    - Pour une meilleure indentification, le nom de l'image sera l'upc du livre correspondant
    """
    images_find = []
    link_img = []

    for url in liens_vers_livres:
        response_3 = requests.get(url)

        if response_3.ok:
            soup = BeautifulSoup(response_3.text, "html.parser")

        # création d'un dossier pour collecter les images
        chemin_dossier_parent = os.path.dirname(__file__)
        dossier_images = os.path.join(chemin_dossier_parent, "images")
        if not os.path.exists(dossier_images):
            os.makedirs(dossier_images)

        # collecte des liens images
        for img in soup.find_all("div", class_="item active"):
            images_find.append(img.find("img")["src"])

    # reconstruction du lien complet
    for elm in images_find:
        link_img.append(urllib.parse.urljoin(url, elm))


    # sauvegarde en local de l'image
    for ref, lien_img in enumerate(link_img):
        resource = urllib.request.urlopen(lien_img)
        image_file_name = (dico_elements[ref]["universal_product_code"]) + ".jpg"
        output = open(image_file_name, "wb")
        output.write(resource.read())
        output.close()

        # déplacement de l'image dans le dossier image
        chemin_fichier_image = os.path.join(chemin_dossier_parent, image_file_name)
        shutil.move(chemin_fichier_image, dossier_images)

        # !!!!!!! ajout dans le dico, comment récupérer upc
        dico_elements[ref]["image_url"] = lien_img

def creation_des_fichiers():
    """
    ---- ETAPE 6 - FICHIER CSV module CSV
    _ création d'un dossier de collecte des fichiers
    - un fichier par catégorie de livre
    Attention, configuration pour excel en français avec modification du delimiteur en point virgule et
    ajout de dialect=csv.excel, sinon ouverture dans la première colonne uniquement.
    """

    # création d'un dossier pour collecter les fichiers csv

    chemin_dossier_parent = os.path.dirname(__file__)
    dossier_csv = os.path.join(chemin_dossier_parent, "fichiers_csv")
    if not os.path.exists(dossier_csv):
        os.makedirs(dossier_csv)

    # Création du fichier avec, pour nom, la catégorie (avec vérif si déjà présent)
    for item in dico_elements:
        nom_fichier_csv = dico_elements[item]["category"] + ".csv"
        chemin_fichier_csv = os.path.join(dossier_csv, nom_fichier_csv)

        if not os.path.exists(chemin_fichier_csv):
            csv.excel.delimiter = ";"
            with open(chemin_fichier_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                              "price_excluding_tax",
                              "number_available", "product_description", "category", "review_rating", "image_url"]
                writer = csv.DictWriter(csvfile, dialect=csv.excel, fieldnames=fieldnames)

                writer.writeheader()

    # Ecriture dans les fichiers correspondants
    for item in dico_elements:
        fichier_a_ouvrir = dico_elements[item]["category"] + ".csv"
        chemin_fichier_csv = os.path.join(dossier_csv, fichier_a_ouvrir)
        csv.excel.delimiter = ";"
        with open(chemin_fichier_csv, 'a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                          "price_excluding_tax",
                          "number_available", "product_description", "category", "review_rating", "image_url"]
            writer = csv.DictWriter(csvfile, dialect=csv.excel, fieldnames=fieldnames)
            writer.writerow({"product_page_url": dico_elements[item]["product_page_url"],
        "universal_product_code": dico_elements[item]["universal_product_code"],"title": dico_elements[item]["title"],
        "price_including_tax": dico_elements[item]["price_including_tax"],
        "price_excluding_tax": dico_elements[item]["price_excluding_tax"],
        "number_available": dico_elements[item]["number_available"],
        "product_description": dico_elements[item]["product_description"], "category": dico_elements[item]["category"],
        "review_rating": dico_elements[item]["review_rating"], "image_url": dico_elements[item]["image_url"]})


if __name__ == "__main__":
    start_time = time.time()
    pages_a_visiter()
    # soup_url_finaux()
    collecte_elements_texte()
    collecte_images()
    creation_des_fichiers()
    # pprint(liens_vers_livres)
    # print(len(liens_vers_livres))
    # print(dico_elements)
    # print(len(dico_elements))
    # print("upc "+str(len(upc)))
    # print("title "+str(len(title)))
    # print("price in "+str(len(price_incl)))
    # print("price ex "+str(len(price_excl)))
    # print("available "+str(len(number_available)))
    # print("prd descr "+str(len(product_description)))
    # print("categ "+str(len(category)))
    # print("files catge "+str(len(files_category)))
    # print("ratin "+str(len(review_rating)))
    # print("link img "+len(link_img))
    print("--- %s seconds ---" % (time.time() - start_time))
