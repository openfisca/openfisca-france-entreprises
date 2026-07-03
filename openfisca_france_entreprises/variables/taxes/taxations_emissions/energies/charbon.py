"""
Tarification effective du CO2 sur le vecteur charbon. 

Rapporte la taxe énergétique effectivement payée sur le charbon
(taxe_interieure_consommation_charbon) aux émissions de CO2 correspondantes
(emissions_charbon_brute), afin d'obtenir un prix implicite du carbone en €/tCO2
"""

import numpy as np
from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import Etablissement


class tarification_effective_charbon(Variable):
    value_type = float
    unit = "€/t CO2e"
    entity = Etablissement
    label = "Tarification effective du CO2 sur la combustion de charbon (taxe énergétique / émissions) (FAUSSE ATM)"
    definition_period = YEAR

    def formula(etablissement, period):
        taxe = etablissement("taxe_interieure_consommation_charbon", period)
        emissions = etablissement("emissions_charbon_brute", period)

        if emissions == 0:
            return 0.0

        return taxe / emissions