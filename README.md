# Programme d'extraction des prix

Ce programme à pour objet de **parcourir les pages d'un site de vente en ligne**
de livres pour relever :
- identification des livres,
- informations de prix (HT, TTC),
- titres
- quantité disponible
- catégorie
- notation

Ces informations seront collectées dans des fichiers CSV selon les catégories.

Enfin, les images seront classées dans un dossier images selon 
le code UPC du livre pour en faciliter l'identification.

## Information
Ce programme est adapté pour visiter le site Books to Scrape (50 pages, 1000 livres).
**Le nombre de pages à visiter a été ramené en entête de script main pour permettre un test.**

## Techologies
Python 3.9
Packages ajoutés : requests et BeautifulSoup4

## Auteur
Cédric M
