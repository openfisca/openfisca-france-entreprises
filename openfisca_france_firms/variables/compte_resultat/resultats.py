from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm, Establishment  # noqa F401

class resultat_exploitation(Variable):
    cerfa_field = "GG"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat d'exploitation (I - II)"
    definition_period = YEAR

    def formula(Firm, period):
        produits_exploitation = Firm("produits_exploitation", period)
        charges_exploitation = Firm("charges_exploitation", period)

        resultat = produits_exploitation - charges_exploitation

        return resultat

class resultat_financier(Variable):
    cerfa_field = "GV"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat financier (V - VI)"
    definition_period = YEAR

    def formula(Firm, period):
        produits_financiers = Firm("produits_financiers", period)
        charges_financieres = Firm("charges_financieres", period)

        resultat = produits_financiers - charges_financieres

        return resultat

class resultat_courant_avant_impot(Variable):
    cerfa_field = "GW"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat courant avant impôt (I - II + III - IV + V - VI)"
    definition_period = YEAR

    def formula(Firm, period):
        produits_exploitation = Firm("produits_exploitation", period)
        charges_exploitation = Firm("charges_exploitation", period)
        benefice_attribue = Firm("benefice_attribue", period)
        perte_supportee = Firm("perte_supportee", period)
        produits_financiers = Firm("produits_financiers", period)
        charges_financieres = Firm("charges_financieres", period)

        resultat = (
            produits_exploitation +
            charges_exploitation +
            benefice_attribue +
            perte_supportee +
            produits_financiers +
            charges_financieres
        )

        return resultat

class resultat_exceptionnel(Variable):
    cerfa_field = "HI"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat exceptionnel (VII - VIII)"
    definition_period = YEAR

    def formula(Firm, period):
        produits_exceptionnels = Firm("produits_exceptionnels", period)
        charges_exceptionnelles = Firm("charges_exceptionnelles", period)

        resultat = produits_exceptionnels - charges_exceptionnelles

        return resultat

class participation_salaries(Variable):
    cerfa_field = "HJ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Participation des salariés aux résultats de l'entreprise"
    definition_period = YEAR

class impot_benefices(Variable):
    cerfa_field = "HK"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Impôts sur les bénéfices"
    definition_period = YEAR

class produits(Variable):
    cerfa_field = "HL"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total des produits (I + III + V + VII"
    definition_period = YEAR

    def formula(Firm, period):
        produits_exploitation = Firm("produits_exploitation", period)
        produits_financiers = Firm("produits_financiers", period)
        benefice_attribue = Firm("benefice_attribue", period)
        produits_exceptionnels = Firm("produits_exceptionnels", period)

        produits = (
            produits_exploitation +
            produits_financiers +
            benefice_attribue +
            produits_exceptionnels
        )

        return produits

class charges(Variable):
    cerfa_field = "HM"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Total des produits (I + III + V + VII"
    definition_period = YEAR

    def formula(Firm, period):
        charges_exploitation = Firm("charges_exploitation", period)
        charges_financieres = Firm("charges_financieres", period)
        perte_supportee = Firm("perte_supportee", period)
        charges_exceptionnelles = Firm("charges_exceptionnelles", period)

        charges = (
            charges_exploitation +
            charges_financieres +
            perte_supportee +
            charges_exceptionnelles
        )

        return charges

class resultat_exercice(Variable):
    cerfa_field = "HN"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat de l'exercice (bénéfice ou perte)"
    definition_period = YEAR

    def formula(Firm, period):
        produits = Firm("produits", period)
        charges = Firm("charges", period)

        resultat = produits - charges

        return resultat
