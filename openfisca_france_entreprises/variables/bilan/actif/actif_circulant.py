from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_entreprises.entities import UniteLegale  # noqa F401


class matieres_premieres_brutes(Variable):
    cerfa_field = "BL"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Matières premières brutes"
    definition_period = YEAR


class matieres_premieres_ar(Variable):
    cerfa_field = "BM"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Matières premières : amortissements, provisions"
    definition_period = YEAR


class matieres_premieres_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Matières premières nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("matieres_premieres_brutes", period)
        ar = UniteLegale("matieres_premieres_ar", period)

        return brut - ar


class encours_production_biens_bruts(Variable):
    cerfa_field = "BN"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de biens bruts"
    definition_period = YEAR


class encours_production_biens_ar(Variable):
    cerfa_field = "BO"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de biens : amortissements, provisions"
    definition_period = YEAR


class encours_production_biens_nets(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de biens nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("encours_production_biens_bruts", period)
        ar = UniteLegale("encours_production_biens_ar", period)

        return brut - ar


class encours_production_services_bruts(Variable):
    cerfa_field = "BP"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de services bruts"
    definition_period = YEAR


class encours_production_services_ar(Variable):
    cerfa_field = ""
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de services : amortissements, provisions"
    definition_period = YEAR


class encours_production_services_nets(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "En cours de production de services nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("encours_production_services_bruts", period)
        ar = UniteLegale("encours_production_services_ar", period)

        return brut - ar


class produits_intermediaires_finis_bruts(Variable):
    cerfa_field = "BR"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits intermédiaires et finis bruts"
    definition_period = YEAR


class produits_intermediaires_finis_ar(Variable):
    cerfa_field = "BS"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits intermédiaires et finis : amortissements, provisions"
    definition_period = YEAR


class produits_intermediaires_finis_nets(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Produits intermédiaires et finis nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("produits_intermediaires_finis_bruts", period)
        ar = UniteLegale("produits_intermediaires_finis_ar", period)

        return brut - ar


class marchandises_brutes(Variable):
    cerfa_field = "BT"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Marchandises brutes"
    definition_period = YEAR


class marchandises_ar(Variable):
    cerfa_field = ""
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Marchandises : amortissements, provisions"
    definition_period = YEAR


class marchandises_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Marchandises nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("marchandises_brutes", period)
        ar = UniteLegale("marchandises_ar", period)

        return brut - ar


class stocks_bruts(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Stocks bruts"
    definition_period = YEAR

    def formula(UniteLegale, period):
        matieres_premieres = UniteLegale("matieres_premieres_brutes", period)
        encours_production_biens = UniteLegale("encours_production_biens_bruts", period)
        encours_production_services = UniteLegale(
            "encours_production_services_bruts", period
        )
        produits_inter = UniteLegale("produits_intermediaires_finis_bruts", period)
        marchandises = UniteLegale("marchandises_brutes", period)

        stocks = (
            matieres_premieres
            + encours_production_biens
            + encours_production_services
            + produits_inter
            + marchandises
        )

        return stocks


class stocks_ar(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Stocks : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        matieres_premieres = UniteLegale("matieres_premieres_ar", period)
        encours_production_biens = UniteLegale("encours_production_biens_ar", period)
        encours_production_services = UniteLegale(
            "encours_production_services_ar", period
        )
        produits_inter = UniteLegale("produits_intermediaires_finis_ar", period)
        marchandises = UniteLegale("marchandises_ar", period)

        stocks = (
            matieres_premieres
            + encours_production_biens
            + encours_production_services
            + produits_inter
            + marchandises
        )

        return stocks


class stocks_nets(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Stocks nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("stocks_bruts", period)
        ar = UniteLegale("stocks_ar", period)

        return brut - ar


class avances_acomptes_commandes_bruts(Variable):
    cerfa_field = "BV"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Avances et acomptes versés sur commandes bruts"
    definition_period = YEAR


class avances_acomptes_commandes_ar(Variable):
    cerfa_field = "BW"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Avances et acomptes versés sur commandes : amortissements, provisions"
    definition_period = YEAR


class avances_acomptes_commandes_nets(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Avances et acomptes versés sur commandes nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("avances_acomptes_commandes_bruts", period)
        ar = UniteLegale("avances_acomptes_commandes_ar", period)

        return brut - ar


class creances_clients_comptes_rattaches_brutes(Variable):
    cerfa_field = "BX"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances clients et comptes rattachés bruts"
    definition_period = YEAR


class creances_clients_comptes_rattaches_ar(Variable):
    cerfa_field = "BY"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances clients et comptes rattachés : amortissements, provisions"
    definition_period = YEAR


class creances_clients_comptes_rattaches_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances clients et comptes rattachés nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("creances_clients_comptes_rattaches_brutes", period)
        ar = UniteLegale("creances_clients_comptes_rattaches_ar", period)

        return brut - ar


class autres_creances_brutes(Variable):
    cerfa_field = "BZ"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Autres créances brutes"
    definition_period = YEAR


class autres_creances_ar(Variable):
    cerfa_field = "CA"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Autres créances  : amortissements, provisions"
    definition_period = YEAR


class autres_creances_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Autres créances nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_creances_brutes", period)
        ar = UniteLegale("autres_creances_ar", period)

        return brut - ar


class capital_souscrit_appele_non_verse_brut(Variable):
    cerfa_field = "CB"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Capital souscrit et appelé, non versé, brut"
    definition_period = YEAR


class capital_souscrit_appele_non_verse_ar(Variable):
    cerfa_field = "CC"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Capital souscrit et appelé, non versé : amortissements, provisions"
    definition_period = YEAR


class capital_souscrit_appele_non_verse_net(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Capital souscrit et appelé, non versé, net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("capital_souscrit_appele_non_verse_brut", period)
        ar = UniteLegale("capital_souscrit_appele_non_verse_ar", period)

        return brut - ar


class creances_brutes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances brutes"
    definition_period = YEAR

    def formula(UniteLegale, period):

        creances_clients = UniteLegale(
            "creances_clients_comptes_rattaches_brutes", period
        )
        autres = UniteLegale("autres_creances_brutes", period)
        capital_souscrit_appele = UniteLegale(
            "capital_souscrit_appele_non_verse_brut", period
        )

        creances = creances_clients + autres + capital_souscrit_appele

        return creances


class creances_ar(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):

        creances_clients = UniteLegale("creances_clients_comptes_rattaches_ar", period)
        autres = UniteLegale("autres_creances_ar", period)
        capital_souscrit_appele = UniteLegale(
            "capital_souscrit_appele_non_verse_ar", period
        )

        creances = creances_clients + autres + capital_souscrit_appele

        return creances


class creances_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Créances nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("creances_brutes", period)
        ar = UniteLegale("creances_ar", period)

        return brut - ar


class valeurs_mobilieres_placement_brutes(Variable):
    cerfa_field = "CD"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Valeurs mobilières de placement (dont actions propres) brutes"
    definition_period = YEAR


class valeurs_mobilieres_placement_ar(Variable):
    cerfa_field = "CE"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Valeurs mobilières de placement (dont actions propres) : amortissements, provisions"
    definition_period = YEAR


class valeurs_mobilieres_placement_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Valeurs mobilières de placement (dont actions propres) nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("valeurs_mobilieres_placement_brutes", period)
        ar = UniteLegale("valeurs_mobilieres_placement_ar", period)

        return brut - ar


class disponibilites_brutes(Variable):
    cerfa_field = "CF"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Disponibilités brutes"
    definition_period = YEAR


class disponibilites_ar(Variable):
    cerfa_field = "CG"
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Disponibilités : amortissements, provisions"
    definition_period = YEAR


class disponibilites_nettes(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Disponibilités nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("disponibilites_brutes", period)
        ar = UniteLegale("disponibilites_ar", period)

        return brut - ar


class actif_circulant_divers_brut(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant divers brut"
    definition_period = YEAR

    def formula(UniteLegale, period):
        valeurs_mobilieres = UniteLegale("valeurs_mobilieres_placement_brutes", period)
        disponibilites = UniteLegale("disponibilites_brutes", period)

        divers = valeurs_mobilieres + disponibilites

        return divers


class actif_circulant_divers_ar(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant divers : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        valeurs_mobilieres = UniteLegale("valeurs_mobilieres_placement_ar", period)
        disponibilites = UniteLegale("disponibilites_ar", period)

        divers = valeurs_mobilieres + disponibilites

        return divers


class actif_circulant_divers_net(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant divers net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("actif_circulant_divers_brut", period)
        ar = UniteLegale("actif_circulant_divers_ar", period)

        return brut - ar


class actif_circulant_brut(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant brut"
    definition_period = YEAR

    def formula(UniteLegale, period):
        stocks = UniteLegale("stocks_bruts", period)
        avances_acomptes_commandes = UniteLegale(
            "avances_acomptes_commandes_bruts", period
        )
        creances = UniteLegale("creances_brutes", period)
        divers = UniteLegale("actif_circulant_divers_brut", period)

        actif_circulant = stocks + avances_acomptes_commandes + creances + divers

        return actif_circulant


class actif_circulant_ar(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        stocks = UniteLegale("stocks_ar", period)
        avances_acomptes_commandes = UniteLegale(
            "avances_acomptes_commandes_ar", period
        )
        creances = UniteLegale("creances_ar", period)
        divers = UniteLegale("actif_circulant_divers_ar", period)

        actif_circulant = stocks + avances_acomptes_commandes + creances + divers

        return actif_circulant


class actif_circulant_net(Variable):
    value_type = int
    unit = "currency"
    entity = UniteLegale
    label = "Actif circulant net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("actif_circulant_brut", period)
        ar = UniteLegale("actif_circulant_ar", period)

        return brut - ar
