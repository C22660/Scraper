import time

from data_retrieval import pages_a_visiter, soup_url_finaux, collecte_elements_texte, \
    collecte_images, creation_des_fichiers

from suivi_execution import annonce_lancement

# Nombre de pages maximum = 50 (pour 1000 livres).
# Pour cas de test cette valeur est ramenée à 1 page.
NBRE_DE_PAGES = 1

dico_elements = {}


def main():
    start_time = time.time()
    annonce_lancement()
    liste_liens = pages_a_visiter(NBRE_DE_PAGES)
    for ref, lien in enumerate(liste_liens):
        soup = soup_url_finaux(lien)
        collecte_elements_texte(lien, soup, dico_elements)
        collecte_images(lien, soup, dico_elements, ref)
    creation_des_fichiers(dico_elements, NBRE_DE_PAGES)
    print("--- %s minutes ---" % ((time.time() - start_time)/60))


if __name__ == "__main__":
    main()
