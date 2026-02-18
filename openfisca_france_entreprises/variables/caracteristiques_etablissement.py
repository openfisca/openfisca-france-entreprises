"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
from openfisca_france_entreprises.variables.naf import naf

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class apet(Variable):
    value_type = Enum  # voir dans openfisca_france comment le faire
    entity = Etablissement
    label = "Secteur NAF de l'établissement"  # nomencultures des activités françaises
    # mettre tous les valeurs NAF, les deux colomnes
    definition_period = YEAR
    possible_values = naf
    default_value = naf.manquant


class postal_code(Variable):
    value_type = str
    max_length = 5
    entity = Etablissement
    definition_period = MONTH
    label = "Postal code of the etablissement"


class effectif_3112_eta(Variable):
    # le nombre de personnes qui travaillent
    value_type = float
    entity = Etablissement
    label = "Effectifs en fin d'année, ETP"
    definition_period = YEAR


class installation_cogeneration(Variable):
    value_type = bool
    entity = Etablissement
    label = "Installation de cogénération pour la production combinée de chaleur et d'électricité"
    definition_period = YEAR


class date_installation_cogeneration(Variable):
    value_type = int
    entity = Etablissement
    label = "Date d'installation de cogéneration"
    definition_period = YEAR


class date_creation_eta(Variable):
    value_type = int
    entity = Etablissement
    label = "Date de création de l'établissement"
    definition_period = YEAR


class date_creation_ul(Variable):
    value_type = int
    entity = Etablissement
    label = "Date de création de l'unité légale"
    definition_period = YEAR


class installation_seqe(Variable):
    value_type = bool
    entity = Etablissement
    label = "Installation soumise au système européen de quotas carbone"
    definition_period = YEAR


# class installation_electro_intensive(Variable):
#     value_type = bool
#     entity = Etablissement
#     label = "Installation électrointensive"
#     definition_period = YEAR


#     def formula_2014_01_01(etablissement, period):

#         return True

#     def formula_2021_01_01(etablissement, period):

#         return True


class installation_grande_consommatrice_energie(Variable):
    value_type = bool
    entity = Etablissement
    label = "Installation grande consommatrice d'énergie"
    definition_period = YEAR

    def formula(etablissement, period):
        seqe = etablissement("installation_seqe", period)
        facture_energie_eta = etablissement("facture_energie_eta", period)
        chiffre_affaires_eta = etablissement("chiffre_affaires_eta", period)
        taxe_accise_electricite_taux_normal = etablissement(
            "taxe_accise_electricite_taux_normal", period
        )
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)

        cond1 = (
            seqe
            & (chiffre_affaires_eta != 0)
            & (facture_energie_eta >= 0.03 * chiffre_affaires_eta)
        )
        cond2 = (valeur_ajoutee_eta != 0) & (
            taxe_accise_electricite_taux_normal >= valeur_ajoutee_eta * 0.005
        )
        return cond1 | cond2


# Sont considérées comme grandes consommatrices en énergie les entreprises :

# ― dont les achats d'électricité de puissance souscrite supérieure à 250 kilovoltampères et
# de produits énergétiques soumis aux taxes intérieures de consommation visées aux articles 265,
#  266 quinquies et 266 quinquies B du présent code atteignent au moins 3 % du chiffre d'affaires ;

# ― ou pour lesquelles le montant total de la taxe applicable à l'électricité de puissance
# souscrite supérieure à 250 kilovoltampères et des taxes intérieures de consommation visées
# au précédent alinéa est au moins égal à 0,5 % de la valeur ajoutée telle que définie à
# l' article 1586 sexies du code général des impôts .


class risque_de_fuite_carbone_eta(Variable):
    value_type = bool
    entity = Etablissement
    label = "Entreprise exposée au risque de fuite carbone"
    definition_period = YEAR
    reference = "DÉCISION DÉLÉGUÉE (UE) 2019/708 DE LA COMMISSION du 15 février 2019"

    def formula_2019_01_01(etablissement, period):
        apet = etablissement("apet", period)
        codes_eligibles = [
            naf._05_10Z,
            naf._05_20Z,
            naf._07_10Z,
            naf._07_29Z,
            naf._08_91Z,
            naf._08_99Z,
            naf._10_41A,
            naf._10_41B,
            naf._10_62Z,
            naf._10_81Z,
            naf._11_06Z,
            naf._13_10Z,
            naf._13_95Z,
            naf._14_11Z,
            naf._16_21Z,
            naf._17_11Z,
            naf._17_12Z,
            naf._19_10Z,
            naf._19_20Z,
            naf._20_11Z,
            naf._20_12Z,
            naf._20_13B,
            naf._20_14Z,
            naf._20_15Z,
            naf._20_16Z,
            naf._20_17Z,
            naf._20_60Z,
            naf._23_11Z,
            naf._23_13Z,
            naf._23_14Z,
            naf._23_19Z,
            naf._23_20Z,
            naf._23_31Z,
            naf._23_51Z,
            naf._23_52Z,
            naf._23_99Z,
            naf._24_10Z,
            naf._24_20Z,
            naf._24_31Z,
            naf._24_42Z,
            naf._24_43Z,
            naf._24_44Z,
            naf._24_45Z,
            naf._24_46Z,
            naf._24_51Z,
            naf._08_93Z,
            naf._13_30Z,
            naf._21_10Z,
            naf._23_41Z,
            naf._23_42Z,
            naf._23_32Z,
            naf._08_12Z,
            naf._10_31Z,
            naf._10_39A,
            naf._10_51D,
            naf._10_89Z,
            naf._20_30Z,
            naf._25_50A,
        ]
        result = apet == codes_eligibles[0]
        for code in codes_eligibles[1:]:
            result = result | (apet == code)
        return result


# faut changer à l'établissement
# faut faire des autres listes selon la période d'utilisation


class intensite_echanges_avec_pays_tiers(Variable):
    value_type = float
    unit = "pourcentage"
    entity = Etablissement
    label = (
        "L'intensité des échanges avec les pays tiers, appliqué au sein de L312-65, -73"
    )
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046196784"


class departement(Variable):
    # NB : les codes pour la corse est 02A et 02B, tandis que pour les autres codes départementales avec qu'une chiffre, le code commence PAS par un 0.
    value_type = str
    unit = ""
    entity = Etablissement
    label = "code departementale INSEE"
    definition_period = YEAR
    reference = ""


class commune(Variable):
    value_type = str
    unit = ""
    entity = Etablissement
    label = "code SIREN commune"
    definition_period = YEAR
    reference = ""
