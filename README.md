# Programme d'extration des prix

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
**Le nombre de page à visiter peut être réduit en entête de script.**

## Techologies
Python 3.9
Packages ajoutés : requests et BeautifulSoup4

## Auteur
Cédric M
