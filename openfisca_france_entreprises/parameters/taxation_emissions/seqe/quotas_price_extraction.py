import pandas as pd
import os
import re
import requests
import zipfile
import io
import yaml
import shutil
from datetime import date

URL_ZIP = "https://www.eex.com/fileadmin/EEX/Downloads/EUA_Emission_Spot_Primary_Market_Auction_Report/Archive_Reports/emission-spot-primary-market-auction-report-2012-2025-data.zip"
DOSSIER_EXTRACTION = "donnees_extraites"
COLONNE = 'Auction Price €/tCO2'
PONDERATION = 'Auction Volume tCO2'


def moyennes_par_annee(colonne=COLONNE, url_zip=URL_ZIP, dossier_extraction=DOSSIER_EXTRACTION):
    """
    Télécharge le zip EEX (toutes les années en un seul fichier), extrait
    les rapports xls, et calcule la moyenne d'une colonne pour chaque année.

    Paramètres :
    - colonne : nom de la colonne dont on veut la moyenne
    - url_zip : lien vers le zip (par défaut celui d'EEX, 2012 à aujourd'hui)
    - dossier_extraction : dossier local où extraire les fichiers

    Retourne :
    - un DataFrame trié par année, colonnes 'annee' et 'moyenne'
    """

    # 1. Télécharger le zip en mémoire
    reponse = requests.get(url_zip)
    reponse.raise_for_status()  # Assure que la requête a réussi, sinon lève une exception

    # 2. Extraire tous les fichiers dans le dossier local
    with zipfile.ZipFile(io.BytesIO(reponse.content)) as archive:  # Ouvre le zip en mémoire, cad sans l'écrire sur le disque 
        os.makedirs(dossier_extraction, exist_ok=True)  # Crée le dossier s'il n'existe pas
        archive.extractall(dossier_extraction)

    # 3. Récupérer tous les fichiers xls extraits dans le dossier
    dossier = os.listdir(dossier_extraction)
    fichiers = os.listdir(os.path.join(dossier_extraction, dossier[0]))

    values = {}
    for fichier in fichiers:
        nom = os.path.basename(fichier)  # Récupère uniquement le nom du fichier pour identifier l'année

        match = re.search(r"(\d{4})", nom)  # cherche une séquence de 4 chiffres donc une année dans le nom du fichier
        if not match:
            continue
        annee = int(match.group(1))  # convertit l'année en entier

        chemin = os.path.join(dossier_extraction,dossier[0], fichier)

        # Les en-têtes des fichiers ne sont pas au même endroit selon l'année, donc on ajuste le paramètre header de pd.read_excel 
        if annee >= 2017:
            header = 5
        else:
            header = 2

        # Cette boucle traite le changement d'extension des fichiers xls en xlsx à partir de 2020
        if nom.lower().endswith(".xlsx"):
            df = pd.read_excel(chemin, engine="openpyxl", header=header)
        else:
            df = pd.read_excel(chemin, header=header)

        # Pour l'année 2016 les variables ont des noms légèrement différents ¯\_(ツ)_/¯
        if annee == 2016:
            df.columns = [col.replace("EUR/tCO2", "€/tCO2") for col in df.columns]
            df.rename(columns={'Auction Volume': 'Auction Volume tCO2'}, inplace=True)

        moyenne_pondérée = (df[colonne] * df[PONDERATION]).sum() / df[PONDERATION].sum()
        values[date(annee, 1, 1)] = {'value': round(float(moyenne_pondérée), 2)}

    # pour supprimer le dossier créé au moment de l'extraction des fichiers xls, on peut utiliser la fonction shutil.rmtree() qui supprime un dossier et tout son contenu.
    if os.path.exists(DOSSIER_EXTRACTION):
            shutil.rmtree(DOSSIER_EXTRACTION, ignore_errors=True)    
    return values

prices_quotas = {'description': "Prix moyen des quotas du SEQE (EUR/tCO2) pondéré par le volume de quotas vendus",
                 'metadata': {'unit': "EUR/tCO2",
                               'reference': "https://www.eex.com/en/market-data/environmental-markets/emission-spot-auction-report", 
                               'source': "EEX, European Energy Exchange"},
                 'values': moyennes_par_annee()}

with open(os.path.join(os.path.dirname(__file__), "price_quotas.yaml"), "w", encoding="utf-8") as file:
    yaml.dump(prices_quotas, file, allow_unicode=True)