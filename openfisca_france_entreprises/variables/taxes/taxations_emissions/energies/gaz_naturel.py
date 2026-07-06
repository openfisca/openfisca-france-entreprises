"""
Tarification effective du CO2 sur le vecteur gaz naturel. 

Rapporte la taxe énergétique effectivement payée sur le gaz naturel
(taxe_interieure_consommation_gaz_naturel) aux émissions de CO2 correspondantes
(emissions_gaz_naturel_brute), afin d'obtenir un prix implicite du carbone en €/tCO2
"""

import numpy as np
from openfisca_core.model_api import YEAR, Variable

from openfisca_france_entreprises.entities import Etablissement


class tarification_effective_gaz_naturel(Variable):
    value_type = float
    unit = "€/t CO2e"
    entity = Etablissement
    label = "Tarification effective du CO2 sur la combustion de gaz naturel (taxe énergétique / émissions) (FAUSSE ATM)"
    definition_period = YEAR

    def formula(etablissement, period):
        taxe = etablissement("taxe_interieure_consommation_gaz_naturel", period)
        emissions = etablissement("emissions_gaz_naturel_brute", period)

        if emissions == 0:
            return 0.0

        return taxe / emissions