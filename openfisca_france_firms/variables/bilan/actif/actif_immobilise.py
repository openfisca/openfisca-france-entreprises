from openfisca_core.model_api import *
from openfisca_france_firms.entities import UniteLegale  # noqa F401

class frais_etablissement_bruts(Variable):
    cerfa_field = "AB"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais d'établissement bruts"
    definition_period = YEAR

class frais_etablissement_ar(Variable):
    cerfa_field = "AC"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais d'établissement : amortissements, provisions"
    definition_period = YEAR

class frais_etablissement_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais d'établissement nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("frais_etablissement_bruts", period)
        ar = UniteLegale("frais_etablissement_ar", period)

        return brut - ar

class frais_developpement_bruts(Variable):
    cerfa_field = "CX"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais de développement bruts"
    definition_period = YEAR

class frais_developpement_ar(Variable):
    cerfa_field = "CQ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais de développement : amortissements, provisions"
    definition_period = YEAR

class frais_developpement_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Frais de développement nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("frais_developpement_bruts", period)
        ar = UniteLegale("frais_developpement_ar", period)

        return brut - ar

class concessions_brevets_droits_bruts(Variable):
    cerfa_field = "AF"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Concessions, brevets, et droits similaires bruts"
    definition_period = YEAR

class concessions_brevets_droits_ar(Variable):
    cerfa_field = "AG"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Concessions, brevets, et droits similaires : amortissements, provisions"
    definition_period = YEAR

class concessions_brevets_droits_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Concessions, brevets, et droits similaires nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("concessions_brevets_droits_bruts", period)
        ar = UniteLegale("concessions_brevets_droits_ar", period)

        return brut - ar

class fonds_commercial_brut(Variable):
    cerfa_field = "AH"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Fonds commercial"
    definition_period = YEAR

class fonds_commercial_ar(Variable):
    cerfa_field = "AI"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Fonds commercial : amortissements, provisions"
    definition_period = YEAR

class fonds_commercial_net(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Fonds commercial net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("fonds_commercial_brut", period)
        ar = UniteLegale("fonds_commercial_ar", period)

        return brut - ar

class autres_immobilisations_incorporelles_brutes(Variable):
    cerfa_field = "AJ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations incorporelles brutes"
    definition_period = YEAR

class autres_immobilisations_incorporelles_ar(Variable):
    cerfa_field = "AK"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations incorporelles brutes : amortissements, provisions"
    definition_period = YEAR

class autres_immobilisations_incorporelles_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations incorporelles nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_immobilisations_incorporelles_brutes", period)
        ar = UniteLegale("autres_immobilisations_incorporelles_ar", period)

        return brut - ar

class immobilisations_incorporelles_avances_acomptes_bruts(Variable):
    cerfa_field = "AL"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes sur immobilisations incorporelles bruts"
    definition_period = YEAR

class immobilisations_incorporelles_avances_acomptes_ar(Variable):
    cerfa_field = "AM"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes sur immobilisations incorporelles : amortissements, provisions"
    definition_period = YEAR

class immobilisations_incorporelles_avances_acomptes_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes sur immobilisations incorporelles nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("immobilisations_incorporelles_avances_acomptes_bruts", period)
        ar = UniteLegale("immobilisations_incorporelles_avances_acomptes_ar", period)

        return brut - ar

class immobilisations_incorporelles_brutes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations incorporelles brutes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        frais_etab = UniteLegale("frais_etablissement_bruts", period)
        frais_dev = UniteLegale("frais_developpement_bruts", period)
        concessions_brevets = UniteLegale("concessions_brevets_droits_bruts", period)
        fonds_comm = UniteLegale("fonds_commercial_brut", period)
        autres = UniteLegale("autres_immobilisations_incorporelles_brutes", period)
        avances_acomptes = UniteLegale("immobilisations_incorporelles_avances_acomptes_bruts", period)

        immo_incorp = (
            frais_etab
            + frais_dev
            + concessions_brevets
            + fonds_comm
            + autres
            + avances_acomptes
            )

        return immo_incorp

class immobilisations_incorporelles_ar(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations incorporelles : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        frais_etab = UniteLegale("frais_etablissement_ar", period)
        frais_dev = UniteLegale("frais_developpement_ar", period)
        concessions_brevets = UniteLegale("concessions_brevets_droits_ar", period)
        fonds_comm = UniteLegale("fonds_commercial_ar", period)
        autres = UniteLegale("autres_immobilisations_incorporelles_ar", period)
        avances_acomptes = UniteLegale("immobilisations_incorporelles_avances_acomptes_ar", period)

        immo_incorp = (
            frais_etab
            + frais_dev
            + concessions_brevets
            + fonds_comm
            + autres
            + avances_acomptes
            )

        return immo_incorp

class immobilisations_incorporelles_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations incorporelles nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("immobilisations_incorporelles_brutes", period)
        ar = UniteLegale("immobilisations_incorporelles_ar", period)

        return brut - ar

class terrains_bruts(Variable):
    cerfa_field = "AN"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Terrains bruts"
    definition_period = YEAR

class terrains_ar(Variable):
    cerfa_field = "AO"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Terrains : amortissements, provisions"
    definition_period = YEAR

class terrains_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Terrains"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("terrains_bruts", period)
        ar = UniteLegale("terrains_ar", period)

        return brut - ar

class constructions_brutes(Variable):
    cerfa_field = "AP"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Constructions brutes"
    definition_period = YEAR

class constructions_ar(Variable):
    cerfa_field = "AQ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Constructions : amortissements, provisions"
    definition_period = YEAR

class constructions_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Constructions nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("constructions_brutes", period)
        ar = UniteLegale("constructions_ar", period)

        return brut - ar

class installations_techniques_brutes(Variable):
    cerfa_field = "AR"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Installations techniques, matériel et outillage industriels bruts"
    definition_period = YEAR

class installations_techniques_ar(Variable):
    cerfa_field = "AS"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Installations techniques, matériel et outillage industriels : amortissements, provisions"
    definition_period = YEAR

class installations_techniques_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Installations techniques, matériel et outillage industriels nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("installations_techniques_brutes", period)
        ar = UniteLegale("installations_techniques_ar", period)

        return brut - ar

class autres_immobilisations_corporelles_brutes(Variable):
    cerfa_field = "AT"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations corporelles brutes"
    definition_period = YEAR

class autres_immobilisations_corporelles_ar(Variable):
    cerfa_field = "AU"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations corporelles : amortissements, provisions"
    definition_period = YEAR

class autres_immobilisations_corporelles_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations corporelles nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_immobilisations_corporelles_brutes", period)
        ar = UniteLegale("autres_immobilisations_corporelles_ar", period)

        return brut - ar
class immobilisations_en_cours_brutes(Variable):
    cerfa_field = "AV"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations en cours brutes"
    definition_period = YEAR

class immobilisations_en_cours_ar(Variable):
    cerfa_field = "AW"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations en cours : amortissements, provisions"
    definition_period = YEAR

class immobilisations_en_cours_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations en cours nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("immobilisations_en_cours_brutes", period)
        ar = UniteLegale("immobilisations_en_cours_ar", period)

        return brut - ar

class avances_acomptes_bruts(Variable):
    cerfa_field = "AX"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes bruts"
    definition_period = YEAR

class avances_acomptes_ar(Variable):
    cerfa_field = "AY"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes : amortissements, provisions"
    definition_period = YEAR

class avances_acomptes_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Avances et acomptes nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("avances_acomptes_bruts", period)
        ar = UniteLegale("avances_acomptes_ar", period)

        return brut - ar

class immobilisations_corporelles_brutes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations corporelles brutes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        terrains = UniteLegale("terrains_bruts", period)
        constructions = UniteLegale("constructions_brutes", period)
        installations_techniques = UniteLegale("installations_techniques_brutes", period)
        autres = UniteLegale("autres_immobilisations_corporelles_brutes", period)
        immo_en_cours = UniteLegale("immobilisations_en_cours_brutes", period)
        avances_acomptes = UniteLegale("avances_acomptes_bruts", period)

        immo_corp = (
            terrains
            + constructions
            + installations_techniques
            + autres
            + immo_en_cours
            + avances_acomptes
            )

        return immo_corp

class immobilisations_corporelles_ar(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations corporelles : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        terrains = UniteLegale("terrains_ar", period)
        constructions = UniteLegale("constructions_ar", period)
        installations_techniques = UniteLegale("installations_techniques_ar", period)
        autres = UniteLegale("autres_immobilisations_corporelles_ar", period)
        immo_en_cours = UniteLegale("immobilisations_en_cours_ar", period)
        avances_acomptes = UniteLegale("avances_acomptes_ar", period)

        immo_corp = (
            terrains
            + constructions
            + installations_techniques
            + autres
            + immo_en_cours
            + avances_acomptes
            )

        return immo_corp

class immobilisations_corporelles_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations corporelles nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("immobilisations_corporelles_brutes", period)
        ar = UniteLegale("immobilisations_corporelles_ar", period)

        return brut - ar

class participations_mise_equivalence_brutes(Variable):
    cerfa_field = "CS"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Paricipations évaluées selon la méthode de mise en équivalence brutes"
    definition_period = YEAR

class participations_mise_equivalence_ar(Variable):
    cerfa_field = "CT"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Paricipations évaluées selon la méthode de mise en équivalence : amortissements, provisions"
    definition_period = YEAR

class participations_mise_equivalence_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Paricipations évaluées selon la méthode de mise en équivalence nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("participations_mise_equivalence_brutes", period)
        ar = UniteLegale("participations_mise_equivalence_ar", period)

        return brut - ar

class autres_participations_brutes(Variable):
    cerfa_field = "CU"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres participations brutes"
    definition_period = YEAR

class autres_participations_ar(Variable):
    cerfa_field = "CV"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres participations  : amortissements, provisions"
    definition_period = YEAR

class autres_participations_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres participations nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_participations_brutes", period)
        ar = UniteLegale("autres_participations_ar", period)

        return brut - ar

class creances_participations_brutes(Variable):
    cerfa_field = "BB"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Créances rattachées à des participations brutes"
    definition_period = YEAR

class creances_participations_ar(Variable):
    cerfa_field = "BC"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Créances rattachées à des participations : amortissements, provisions"
    definition_period = YEAR

class creances_participations_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Créances rattachées à des participations nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("creances_participations_brutes", period)
        ar = UniteLegale("creances_participations_ar", period)

        return brut - ar

class autres_titres_immobilises_bruts(Variable):
    cerfa_field = "BD"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres titres immobilisés bruts"
    definition_period = YEAR

class autres_titres_immobilises_ar(Variable):
    cerfa_field = "BE"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres titres immobilisés : amortissements, provisions"
    definition_period = YEAR

class autres_titres_immobilises_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres titres immobilisés nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_titres_immobilises_bruts", period)
        ar = UniteLegale("autres_titres_immobilises_ar", period)

        return brut - ar

class prets_bruts(Variable):
    cerfa_field = "BF"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Prêts bruts"
    definition_period = YEAR

class prets_ar(Variable):
    cerfa_field = "BG"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Prêts : amortissements, provisions"
    definition_period = YEAR

class prets_nets(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Prêts nets"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("prets_bruts", period)
        ar = UniteLegale("prets_ar", period)

        return brut - ar

class autres_immobilisations_financieres_brutes(Variable):
    cerfa_field = "BH"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations financières brutes"
    definition_period = YEAR

class autres_immobilisations_financieres_ar(Variable):
    cerfa_field = "BI"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations financières : amortissements, provisions"
    definition_period = YEAR

class autres_immobilisations_financieres_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Autres immobilisations financières nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("autres_immobilisations_financieres_brutes", period)
        ar = UniteLegale("autres_immobilisations_financieres_ar", period)

        return brut - ar

class immobilisations_financieres_brutes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations financières brutes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        participations = UniteLegale("participations_mise_equivalence_brutes", period)
        autres_participations = UniteLegale("autres_participations_brutes", period)
        creances = UniteLegale("creances_participations_brutes", period)
        autres_titres = UniteLegale("autres_titres_immobilises_bruts", period)
        prets = UniteLegale("prets_bruts", period)
        autres = UniteLegale("autres_immobilisations_financieres_brutes", period)

        immo_fin = (
            participations
            + autres_participations
            + creances
            + autres_titres
            + prets
            + autres
            )

        return immo_fin

class immobilisations_financieres_ar(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations financières : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        participations = UniteLegale("participations_mise_equivalence_ar", period)
        autres_participations = UniteLegale("autres_participations_ar", period)
        creances = UniteLegale("creances_participations_ar", period)
        autres_titres = UniteLegale("autres_titres_immobilises_ar", period)
        prets = UniteLegale("prets_ar", period)
        autres = UniteLegale("autres_immobilisations_financieres_ar", period)

        immo_fin = (
            participations
            + autres_participations
            + creances
            + autres_titres
            + prets
            + autres
            )

        return immo_fin

class immobilisations_financieres_nettes(Variable):
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Immobilisations financières nettes"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("immobilisations_financieres_brutes", period)
        ar  = UniteLegale("immobilisations_financieres_ar", period)

        return brut - ar

class actif_immobilise_brut(Variable):
    cerfa_field = "BJ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Actif immobilise brut"
    definition_period = YEAR

    def formula(UniteLegale, period):
        immo_incorporelles = UniteLegale("immobilisations_incorporelles_brutes", period)
        immo_corporelles = UniteLegale("immobilisations_corporelles_brutes", period)
        immo_financieres = UniteLegale("immobilisations_financieres_brutes", period)

        return immo_incorporelles + immo_corporelles + immo_financieres

class actif_immobilise_ar(Variable):
    cerfa_field = "BK"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Actif immobilise : amortissements, provisions"
    definition_period = YEAR

    def formula(UniteLegale, period):
        immo_incorporelles = UniteLegale("immobilisations_incorporelles_ar", period)
        immo_corporelles = UniteLegale("immobilisations_corporelles_ar", period)
        immo_financieres = UniteLegale("immobilisations_financieres_ar", period)

        return immo_incorporelles + immo_corporelles + immo_financieres

class actif_immobilise_net(Variable):
    cerfa_field = "BK"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Actif immobilise net"
    definition_period = YEAR

    def formula(UniteLegale, period):
        brut = UniteLegale("actif_immobilise_brut", period)
        ar = UniteLegale("actif_immobilise_ar", period)

        return brut - ar
