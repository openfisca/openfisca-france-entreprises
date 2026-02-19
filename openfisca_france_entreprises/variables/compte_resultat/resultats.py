from openfisca_core.model_api import *
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import (  # noqa F401
    Etablissement,
    UniteLegale,
)


class resultat_exploitation(Variable):
    cerfa_field = "GG"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Résultat d'exploitation (I - II)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_exploitation = UniteLegale("produits_exploitation", period)
        charges_exploitation = UniteLegale("charges_exploitation", period)

        resultat = produits_exploitation - charges_exploitation

        return resultat


class resultat_financier(Variable):
    cerfa_field = "GV"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Résultat financier (V - VI)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_financiers = UniteLegale("produits_financiers", period)
        charges_financieres = UniteLegale("charges_financieres", period)

        resultat = produits_financiers - charges_financieres

        return resultat


class resultat_courant_avant_impot(Variable):
    cerfa_field = "GW"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Résultat courant avant impôt (I - II + III - IV + V - VI)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_exploitation = UniteLegale("produits_exploitation", period)
        charges_exploitation = UniteLegale("charges_exploitation", period)
        benefice_attribue = UniteLegale("benefice_attribue", period)
        perte_supportee = UniteLegale("perte_supportee", period)
        produits_financiers = UniteLegale("produits_financiers", period)
        charges_financieres = UniteLegale("charges_financieres", period)

        resultat = (
            produits_exploitation
            + charges_exploitation
            + benefice_attribue
            + perte_supportee
            + produits_financiers
            + charges_financieres
        )

        return resultat


class resultat_exceptionnel(Variable):
    cerfa_field = "HI"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Résultat exceptionnel (VII - VIII)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_exceptionnels = UniteLegale("produits_exceptionnels", period)
        charges_exceptionnelles = UniteLegale("charges_exceptionnelles", period)

        resultat = produits_exceptionnels - charges_exceptionnelles

        return resultat


class participation_salaries(Variable):
    cerfa_field = "HJ"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Participation des salariés aux résultats de l'entreprise"
    definition_period = YEAR


class impot_benefices(Variable):
    cerfa_field = "HK"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Impôts sur les bénéfices"
    definition_period = YEAR


class produits(Variable):
    cerfa_field = "HL"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Total des produits (I + III + V + VII"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits_exploitation = UniteLegale("produits_exploitation", period)
        produits_financiers = UniteLegale("produits_financiers", period)
        benefice_attribue = UniteLegale("benefice_attribue", period)
        produits_exceptionnels = UniteLegale("produits_exceptionnels", period)

        produits = (
            produits_exploitation
            + produits_financiers
            + benefice_attribue
            + produits_exceptionnels
        )

        return produits


class charges(Variable):
    cerfa_field = "HM"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Total des produits (I + III + V + VII"
    definition_period = YEAR

    def formula(UniteLegale, period):
        charges_exploitation = UniteLegale("charges_exploitation", period)
        charges_financieres = UniteLegale("charges_financieres", period)
        perte_supportee = UniteLegale("perte_supportee", period)
        charges_exceptionnelles = UniteLegale("charges_exceptionnelles", period)

        charges = (
            charges_exploitation
            + charges_financieres
            + perte_supportee
            + charges_exceptionnelles
        )

        return charges


class resultat_exercice(Variable):
    cerfa_field = "HN"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Résultat de l'exercice (bénéfice ou perte)"
    definition_period = YEAR

    def formula(UniteLegale, period):
        produits = UniteLegale("produits", period)
        charges = UniteLegale("charges", period)

        resultat = produits - charges

        return resultat
