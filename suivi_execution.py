import os
from glob import glob
import time

# NBRE_DE_PAGES = 1
# dico_elements = {}

# !!!!! fonction execution_programme_origine ci-dessous non exécutée, laissée pour échange


def execution_programme_origine():
    """ Suivi du déroulé en comptant le nombre de fichiers images et CSV constitué """
    dossier_parent = os.path.dirname(__file__)

    print()
    print("--- Collecte d'éléments en cours ---")
    print(36*"~")
    print()

    # suivi des fichiers images
    dossier_images = os.path.join(dossier_parent, "images")
    while "images" not in os.listdir(dossier_parent):
        print("Attente du dossier Images")
        time.sleep(4)

    if os.path.exists(dossier_images):
        contenu_dossier_images = os.listdir(dossier_images)
        while len(contenu_dossier_images) <= (NBRE_DE_PAGES * 20):
            contenu_dossier_images = os.listdir(dossier_images)
            print("Nombre d'images collectées = " + str(len(contenu_dossier_images)) + " / " + str(NBRE_DE_PAGES * 20))
            time.sleep(10)
    #
    # # Suivi des fichiers csv
    # dossier_csv = os.path.join(dossier_parent, "fichiers_csv")
    # while dossier_csv not in os.listdir(dossier_parent):
    #     print("Attente du dossier fichiers_csv")
    #     time.sleep(4)
    # if os.path.exists(dossier_csv):
    #     contenu_dossier_csv = os.listdir(dossier_csv)
    #     nbre_de_categories = {}
    #     for clef, valeur in dico_elements.items():
    #         if clef == "category":
    #             nbre_de_categories["category"] = nbre_de_categories("category", 0) + 1
    #
    #     print("Nombre de fichiers csv créés = " + str(len(contenu_dossier_csv)) + " / " + str(nbre_de_categories["category"]))


def annonce_lancement():
    print()
    print("--- Collecte d'éléments en cours ---")
    print(36 * "~")
    print()


def suivi_collecte_images(NBRE_DE_PAGES):
    """ Suivi du déroulé en comptant le nombre de fichiers images et CSV constitué """
    dossier_parent = os.path.dirname(__file__)
    # suivi des fichiers images
    dossier_images = os.path.join(dossier_parent, "images")

    if os.path.exists(dossier_images):
        contenu_dossier_images = os.listdir(dossier_images)
        print("Nombre d'images collectées = " + str(len(contenu_dossier_images)) + " / " + str(NBRE_DE_PAGES * 20))


def suivi_collecte_csv(dico_elements):
    dossier_parent = os.path.dirname(__file__)
    # Suivi des fichiers csv
    dossier_csv = os.path.join(dossier_parent, "fichiers_csv")

    if os.path.exists(dossier_csv):
        contenu_dossier_csv = os.listdir(dossier_csv)
        nbre_de_categories = []
        for clef in dico_elements.keys():
            nbre_de_categories.append(dico_elements[clef]["category"])
        print("Nombre de fichiers csv créés = " + str(len(contenu_dossier_csv)) + " / "
              + str(len(set(nbre_de_categories))))


if __name__ == "__main__":
    execution_programme_origine(NBRE_DE_PAGES, dico_elements)
