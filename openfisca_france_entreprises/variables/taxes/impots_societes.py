"""This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale


class prelevement_exceptionnel_entreprises_hydrocarbures(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = YEAR
    label = (
        "Prelevement exceptionnel sur les bénéfices imposables des entreprises exploitant des gisements d'hydrocarbures"
    )
    reference = (
        "Article 25 de la loi de fiannces pour 1985, puis à partir de 1992, "
        "article 235 ter Z du code général des impôts."
    )
    end = "1998-12-31"

    def formula_1985_01_01(unite_legale, period, parameters):
        """Exceptional corporate income tax.

        Prélèvement "exceptionnel" de 12% sur le bénéfice imposable des
        entreprises exploitant des gisements d'hydrocarbures en France.
                Instauré par l'article 25 de la loi de finances pour 1985, et reconduit chaque année.

                https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000880778/#JORFARTI000001493148

                The formula to compute the income tax for a given etablissement at a given period
        """
        prelevement = parameters(
            period,
        ).impots_societes.prelevement_exceptionnel_hydrocarbures
        assujetti = unite_legale("chiffre_affaires", period.n_1) <= prelevement.seuil_chiffre_affaires
        benefice_imposable = unite_legale("benefice_imposable", period)
        share_benefice_vente_hydrocarbures = unite_legale(
            "part_benefice_ventes_hydrocarbures",
            period,
        )
        rate = prelevement.taux

        return assujetti * benefice_imposable * share_benefice_vente_hydrocarbures * rate
