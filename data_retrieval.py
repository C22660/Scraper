import requests
import urllib
import os
import re
import csv

from bs4 import BeautifulSoup

from suivi_execution import suivi_collecte_csv, suivi_collecte_images


num_dict = -1


def pages_a_visiter(NBRE_DE_PAGES):
    """
    --- ETAPE 1 ----
    - collecte des tous les liens vers les livres en parcourant les 50 pages du site -
    """

    liens_livres = []

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
                    liens_livres.append(urllib.parse.urljoin(url_pages_site, page))

    return liens_livres


def soup_url_finaux(url):
    """
    ---ETAPE 3---
    Préparation de la soupe issue des 1000 pages des livres
    """

    # for url in liens:
    response_3 = requests.get(url)

    if response_3.ok:
        soup = BeautifulSoup(response_3.content, "html.parser")
    return soup


def collecte_elements_texte(liens, soup, dico_elements):
    """
    ---ETAPE 4---
    - BOUCLE SUR CHAQUE PAGE D'UN LIVRE
    - collecte des éléments textes qui seront chargés dans les fichier csv
    """

    # j'ajoute des dictionnaires imbriqués numérotés 0 et suivant
    global num_dict

    # for url in liens_vers_livres:
    num_dict += 1
    dico_elements[num_dict] = {}

    dico_elements[num_dict]["product_page_url"] = liens

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


def collecte_images(link_img, liens, soup, dico_elements):
    """
    ---ETAPE 5---
    - Collecte des images des livres en les classant dans un dossier images.
    - Pour une meilleure indentification, le nom de l'image sera l'upc du livre correspondant
    """
    images_find = []

    # collecte des liens images
    for img in soup.find_all("div", class_="item active"):
        images_find.append(img.find("img")["src"])

    # reconstruction du lien complet
    for elm in images_find:
        link_img.append(urllib.parse.urljoin(liens, elm))

        # création d'un dossier pour collecter les images
        chemin_dossier_parent = os.path.dirname(__file__)
        dossier_images = os.path.join(chemin_dossier_parent, "images")
        if not os.path.exists(dossier_images):
            os.makedirs(dossier_images)
    #
    # # sauvegarde en local de l'image
    for ref, lien_img in enumerate(link_img):
        resource = urllib.request.urlopen(lien_img)
        image_file_name = (dico_elements[ref]["universal_product_code"]) + ".jpg"
        chemin_fichier_image = os.path.join(chemin_dossier_parent, dossier_images, image_file_name)
        output = open(chemin_fichier_image, "wb")
        output.write(resource.read())
        output.close()

    # ajout dans le dico du lien de l'image
        dico_elements[ref]["image_url"] = lien_img

def creation_des_fichiers(dico_elements, NBRE_DE_PAGES):
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

    # recap nombre d'images collectées et affichage du nombre de fichier csv créés
    print(36 * "~")
    suivi_collecte_images(NBRE_DE_PAGES)
    suivi_collecte_csv(dico_elements)
    print(36 * "~")

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
            writer.writerow({
                            "product_page_url": dico_elements[item]["product_page_url"],
                            "universal_product_code": dico_elements[item]["universal_product_code"],
                            "title": dico_elements[item]["title"],
                            "price_including_tax": dico_elements[item]["price_including_tax"],
                            "price_excluding_tax": dico_elements[item]["price_excluding_tax"],
                            "number_available": dico_elements[item]["number_available"],
                            "product_description": dico_elements[item]["product_description"],
                            "category": dico_elements[item]["category"],
                            "review_rating": dico_elements[item]["review_rating"],
                            "image_url": dico_elements[item]["image_url"]
                            })
