import data_retrieval as data


def main():
    data.pages_a_visiter()
    data.soup_url_finaux()
    data.collecte_elements_texte()
    data.collecte_images()
    data.creation_des_fichiers()


if __name__ == "__main":
    main()
