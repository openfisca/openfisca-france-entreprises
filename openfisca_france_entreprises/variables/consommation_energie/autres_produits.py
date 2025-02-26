from openfisca_core.model_api import *
from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

class carburant_gaz(Variable): #renoommer à carburant_gaz
    value_type = float
    unit = 'MWh'
    entity = Etablissement
    label = "Consummation en carburant_gaz. Enlevé de taxation_produit petrolier (nom de concept) à gaz_naturel dès 2020"
    reference : "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006071570/LEGISCTA000006122062/1993-01-01/?anchor=LEGIARTI000006615168#LEGIARTI000006615168" 
    definition_period = YEAR


