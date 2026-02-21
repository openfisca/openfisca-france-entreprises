"""Variables and formulas for this module."""

from openfisca_core.model_api import YEAR, Variable, select

from openfisca_france_entreprises.entities import Etablissement


class taxe_communale_consommation_finale_electricite(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula(etablissement, period, parameters):
        taux_tccfe = etablissement("taux_tccfe", period)
        assiette_taxe_electricite = etablissement("assiette_taxe_electricite", period)
        # *** à vérifier que c'est la même assiette

        return assiette_taxe_electricite * taux_tccfe


class taux_tccfe(Variable):
    value_type = float
    entity = Etablissement
    label = ""
    definition_period = YEAR

    def formula_2011_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2011",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2011",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2012_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2012",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2012",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2013_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2013",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2013",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2014_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2014",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2014",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2015_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2015",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2015",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2016_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2016",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2016",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2017_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2017",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2017",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2018_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2018",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2018",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2019_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2019",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2019",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2020_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2020",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2020",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    # 2016 : 0 ; 2 ; 4 ; 6 ; 8 ; 8,50.
    # 2020 :  0 ; 2 ; 4 ; 6 ; 8 ; 8,50
    # 2021 : 4 ; 6 ; 8 ; 8,5.
    # 2022 : 6 ; 8 ; 8,5.
    def formula_2021_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2021",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2021",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)

    def formula_2022_01_01(etablissement, period, parameters):
        amperage = etablissement("amperage", period)
        ticfe = parameters(period).energies.electricite.ticfe
        cond_36 = (amperage <= ticfe.categorie_fiscale_petite_et_moyenne_entreprise) & (amperage != 0)
        cond_250 = (amperage <= ticfe.categorie_fiscale_haut_puissance) & (amperage != 0)
        val_36 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36kVA_et_moins * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2022",
            period,
        )
        val_250 = parameters(
            period,
        ).energies.electricite.tcfe.taux_professionnel_36_a_250kVA * etablissement(
            "tccfe_coefficient_multiplicateur_normal_2022",
            period,
        )
        return select([cond_36, cond_250], [val_36, val_250], default=0)
