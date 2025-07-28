#les valeurs qui varient avec l'ativité 
#valeur_ajouté 

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

class valeur_ajoutee_ul(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = YEAR
    label = "La valeur ajoutée d'une année donnée au niveau d'unité legale"

class valeur_ajoutee_eta(Variable):
    #la valeur ajoutée au niveau établissement
    value_type = float 
    entity = Etablissement
    definition_period = YEAR
    label = "La valeur ajoutée d'une année donnée au niveau d'établissement, en fonction du effectif."
    def formula_1986_01_01(etablissement, period, parameters):
        valeur_ajoutee_ul = etablissement.unite_legale("valeur_ajoutee_ul", period)
        effectif_3112_ul = etablissement.unite_legale("effectif_3112_ul", period)
        effectif_3112_eta = etablissement("effectif_3112_eta", period)
        valeur_ajoutee_eta = 0
        if effectif_3112_ul:
            valeur_ajoutee_eta = valeur_ajoutee_ul * (effectif_3112_eta/effectif_3112_ul)
        return valeur_ajoutee_eta
    
class consommation_par_valeur_ajoutee(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    unit = 'MWh par Euro' 
    label = "Méasure de l'intensité de consommation d'énergie pour la valeur ajoutée."

    def formula_1960_01_01(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)
        assiette_ticgn = etablissement("assiette_ticgn", period)
        
        consommation__divisee_par_valeur_ajoutee = 0
        if valeur_ajoutee_eta:
            consommation__divisee_par_valeur_ajoutee = assiette_ticgn/valeur_ajoutee_eta
        return consommation__divisee_par_valeur_ajoutee
    
class chiffre_affaires_ul(Variable):
    value_type = float
    entity = UniteLegale
    label = "La chiffre d'affaires pour une année donnée pour une unité legale"
    definition_period = YEAR

class chiffre_affaires_eta(Variable):
    value_type = float
    entity = Etablissement
    label = "La chiffre d'affaires pour une année donnée pour une établissement, en fonction du effectif."
    definition_period = YEAR
    def formula_1986_01_01(etablissement, period, parameters):
        chiffre_affaires_ul = etablissement.unite_legale("chiffre_affaires_ul", period)
        effectif_3112_ul = etablissement.unite_legale("effectif_3112_ul", period)
        effectif_3112_eta = etablissement("effectif_3112_eta", period)
        if effectif_3112_ul:
            chiffre_affaires_eta = chiffre_affaires_ul * (effectif_3112_eta/effectif_3112_ul)
        else :
            chiffre_affaires_eta = 0

        return chiffre_affaires_eta


class facture_energie_ul(Variable):
    value_type = float
    entity = UniteLegale
    label = "La facture energie pour une année donnée pour une unité legale"
    definition_period = YEAR

class facture_energie_eta(Variable):
    value_type = float
    entity = Etablissement
    label = "La facture energie pour une année donnée pour une établissement"
    definition_period = YEAR


class facture_energie_par_valeur_ajoutee_eta(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    unit = '' 
    label = "Méasure de l'intensité énergetique sur la valeur ajoutée."

    def formula_1960_01_01(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)
        facture_energie_eta = etablissement("facture_energie_eta", period)
        facture_energie_par_valeur_ajoutee_eta = 0
        if valeur_ajoutee_eta:
            facture_energie_par_valeur_ajoutee_eta = facture_energie_eta/valeur_ajoutee_eta
        return facture_energie_par_valeur_ajoutee_eta


class electro_intensite(Variable):
    value_type = float
    unit = ''
    entity = Etablissement
    label = "niveau d'electro-intensité, défini par L312-44"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=2%C2%B0%20Le%20niveau,la%20valeur%20ajout%C3%A9e."
    def formula(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period) 

        consommation_electricite = etablissement('consommation_electricite', period)
        
        partie_electricite = consommation_electricite*parameters(period).energies.electricite.ticfe.taux_normal

        numerateur = partie_electricite
        if valeur_ajoutee_eta != 0:
            resultat = numerateur/valeur_ajoutee_eta
        else  : 
            resultat = 0

        return resultat


class intensite_energetique_valeur_ajoutee(Variable):
    value_type = float
    unit = ''
    entity = Etablissement
    label = "niveau d'intensité énergetique, défini par L312-44"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=2%C2%B0%20Le%20niveau,la%20valeur%20ajout%C3%A9e."
    #normalement ça commence à être utilisé dès 2022, après la mis en effet de l'accise
    def formula(etablissement, period, parameters):
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period) 

        consommation_electricite = etablissement('consommation_electricite', period)
        
        partie_electricite = consommation_electricite*parameters(period).energies.electricite.ticfe.taux_normal

        consommation_charbon = etablissement('consommation_charbon', period)
        partie_charbon = consommation_charbon*parameters(period).energies.charbon.ticc

        consommation_gaz_naturel = etablissement('consommation_gaz_naturel', period)
        partie_gaz_naturel = consommation_gaz_naturel * parameters(period).energies.gaz_naturel.ticgn.taux_normal * parameters(period).energies.gaz_naturel.ticgn.conversion_pcs_pci
 
        #*** TO DO : ajout les autres formes d'énergie, i.g. gazoles 

        numerateur = partie_electricite + partie_charbon + partie_gaz_naturel
        if valeur_ajoutee_eta != 0:
            resultat = numerateur/valeur_ajoutee_eta
        else  : 
            resultat = 0

        return resultat
# Le niveau d'intensité énergétique en valeur ajoutée s'entend du quotient entre :
# a) Au numérateur, le montant total de l'accise sur les produits utilisés, en appliquant le 
# tarif normal. Pour l'électricité, le tarif normal pour les consommations haute puissance 
# (Supérieure à 250 kVA) est retenu ;
# b) Au dénominateur, le chiffre d'affaires total soumis à la taxe sur la valeur ajoutée 
# diminué de la totalité des achats soumis à la taxe sur la valeur ajoutée.
# (L312-45) Toutefois, ils peuvent être appréciés sur un sous-ensemble restreint de ces produits. 
# Lorsque le niveau mentionné au 2° de l'article L. 312-44 est apprécié uniquement sur 
# l'électricité, il est dénommé niveau d'électro-intensité.

#Montant théorique des accises au tarif normal (même si réduit en réalité) / Chiffre d'affaires – achats (les deux soumis à la TVA) = valeur ajoutée fiscale


class intensite_energetique_valeur_production(Variable):
    value_type = float
    unit = ''
    entity = Etablissement
    label = "niveau d'intensité énergetique, défini par L312-44"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=2%C2%B0%20Le%20niveau,la%20valeur%20ajout%C3%A9e."
    #normalement ça commence à être utilisé dès 2022, après la mis en effet de l'accise
    def formula(etablissement, period, parameters):
    #ça doit être difficile à utiliser parce que on manque de donnés sur le côut d'acquisition
    
        facture_energie_eta = etablissement('facture_energie_eta', period)
        chiffre_affaires_eta = etablissement('chiffre_affaires_eta', period)

        if chiffre_affaires_eta != 0:
            quotient = facture_energie_eta/chiffre_affaires_eta
        else :        
            quotient = 0

        return quotient
# 1° Le niveau d'intensité énergétique en valeur de production s'entend du quotient entre :
# a) Au numérateur, le coût total d'acquisition, toute taxe comprise à l'exception de la taxe
#  sur la valeur ajoutée déductible, des produits taxables et de la chaleur ;
# b) Au dénominateur, le chiffre d'affaires, y compris les subventions directement liées au 
# prix du produit, corrigé de la variation des stocks de produits finis, les travaux en cours 
# et les biens ou les services achetés à des fins de revente, diminué des acquisitions de 
# biens et services destinés à la revente ;

#côut d'énergie / chiffres d'affaires
#Coût réel TTC de l’énergie utilisée (toutes taxes sauf TVA récupérable) / Chiffre d'affaires + subventions + variation de stock – achats pour revente
