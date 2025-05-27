"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_

from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement

from openfisca_core.periods import Instant

class taxe_electricite_bouclier_tarifaire(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = ""  #
    def formula_2022_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(Instant((2022, 2, 1))).energies.bouclier_tarifaire.entreprises #0.5 en 2022
        taxe = assiette_taxe_electricite * taux
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)

        
        if taxe > taxe_accise_electricite: 
            return taxe_accise_electricite
        else:
            return taxe
    def formula_2023_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taux = parameters(Instant((2023, 2, 1))).energies.bouclier_tarifaire.entreprises #0.5 en 2023
        taxe = assiette_taxe_electricite * taux
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)

        
        if taxe > taxe_accise_electricite: 
            return taxe_accise_electricite
        else:
            return taxe
    def formula_2024_01_01(etablissement, period, parameters):
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite",period)
        taxe_accise_electricite = etablissement('taxe_accise_electricite', period)
        taux = parameters(Instant((2024, 2, 1))).energies.bouclier_tarifaire.entreprises #20.5 en 2024
        taxe = assiette_taxe_electricite * taux

        if taxe > taxe_accise_electricite: 
            return taxe_accise_electricite
        else:
            return taxe
        

#On a fini par assumer que toutes les entreprises lui sont eligibles
# class eligibilite_bouclier_tarifaire(Variable):
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#     label = "https://www.economie.gouv.fr/entreprises/tpe-pme-aides-hausse-prix-energie#:~:text=Bouclier%20tarifaire%20%3A%20de%20quoi%20s,de%20l%27%C3%A9lectricit%C3%A9%20en%202022"
#     reference = ""  #
#     def formula_2022_01_01(etablissement, period, parameters):
        
#         eligibilite = False

#         if etablissement("effectif_3112_ul", period) < 10 and etablissement("chiffre_affaires_ul", period) < 4000000 and etablissement("amperage", period) < 36 :
#             eligibilite = True 

#         return eligibilite 

# Moins de 10 salariés.
# Un chiffre d’affaires inférieur à deux millions d’euros.
# Un compteur électrique d’une puissance inférieure à 36 kVA.


#Le bouclier tarifaire est un dispositif qui permet de contenir à 4 % la hausse des prix de l’électricité en 2022.
# class bouclier_tarifaire(Variable):
#     value_type = float
#     entity = Etablissement
#     definition_period = YEAR
#     label = "https://www.economie.gouv.fr/entreprises/tpe-pme-aides-hausse-prix-energie#:~:text=Bouclier%20tarifaire%20%3A%20de%20quoi%20s,de%20l%27%C3%A9lectricit%C3%A9%20en%202022"
#     reference = ""  #
#     def formula_2022_01_01(etablissement, period, parameters):
        
#         fracteur_energie_avec_bouclier_tarifaire = etablissement("facture_energie_ul", 2023)
        
#         if etablissement("eligibilite_bouclier_tarifaire", 2023) == True:
#             if etablissement("facture_energie_ul", 2022) * 1.04 < etablissement("facture_energie_ul", 2023) :
#                 fracteur_energie_avec_bouclier_tarifaire =  etablissement("facture_energie_ul", 2022) * 1.04 
        
#         return fracteur_energie_avec_bouclier_tarifaire
#on a fini par décidé que toutes les entreprises theoratiquement beneificienent dubouclier tarifiare  
