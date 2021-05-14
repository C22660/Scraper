import time


from data_retrieval import pages_a_visiter, soup_url_finaux, collecte_elements_texte, sauvegarde_images, \
    collecte_images, creation_des_fichiers

from suivi_execution import annonce_lancement, suivi_collecte_images

# Nombre de pages maximum = 50 (pour 1000 livres).
# Pour cas de test cette valeur est ramenée à 1 page.
NBRE_DE_PAGES = 1

contenu_page_vue = []

dico_elements = {}
link_img = []


def main():
    start_time = time.time()
    annonce_lancement()
    liste_liens = pages_a_visiter(NBRE_DE_PAGES)
    for liens in liste_liens:
        suivi_collecte_images(NBRE_DE_PAGES)
        soup = soup_url_finaux(liens)
        collecte_elements_texte(liens, soup, dico_elements)
        collecte_images(link_img, liens, soup, dico_elements)
    sauvegarde_images(link_img, dico_elements)
    creation_des_fichiers(dico_elements, NBRE_DE_PAGES)
    print("--- %s minutes ---" % ((time.time() - start_time)/60))


if __name__ == "__main__":
    main()
