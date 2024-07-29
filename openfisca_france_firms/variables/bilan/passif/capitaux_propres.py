from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class capital_social_individuel(Variable):
    cerfa_field = "DA"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Capital social ou individuel"
    definition_period = YEAR

class primes_emission_fusion_apport(Variable):
    cerfa_field = "DB"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Primes d'émission, fusion et apport"
    definition_period = YEAR

class ecarts_reevaluation(Variable):
    cerfa_field = "DC"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Ecarts de réévaluation"
    definition_period = YEAR

class ecarts_reevaluation_equivalence(Variable):
    cerfa_field = "EK"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Ecarts de réévaluation : écarts d'équivalence"
    definition_period = YEAR

class reserve_legale(Variable):
    cerfa_field = "DD"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réservele légale"
    definition_period = YEAR

class reserves_statutaires_contractuelles(Variable):
    cerfa_field = "DE"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserves statutaires ou contractuelles"
    definition_period = YEAR

class reserves_reglementees(Variable):
    cerfa_field = "DF"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserves réglementées"
    definition_period = YEAR

class reserve_speciale_fluctuation_cours(Variable):
    cerfa_field = "B1"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserve spéciale des provisions pour fluctuation des cours"
    definition_period = YEAR

class autres_reserves(Variable):
    cerfa_field = "DG"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Autres réserves"
    definition_period = YEAR

class reserve_achat_oeuvres_originales(Variable):
    cerfa_field = "EJ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Réserve relative à l'achat d'oeuvres originales d'artistes vivants"
    definition_period = YEAR

class report_a_nouveau(Variable):
    cerfa_field = "DH"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Report à nouveau"
    definition_period = YEAR

class resultat_exercice_di(Variable):
    cerfa_field = "DI"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Résultat de l'exercice"
    definition_period = YEAR

class subventions_investissement(Variable):
    cerfa_field = "DJ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Subventions d'investissement"
    definition_period = YEAR

class provisions_reglementees(Variable):
    cerfa_field = "DK"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Provisions réglementées"
    definition_period = YEAR

class capitaux_propres(Variable):
    cerfa_field = "DL"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Capitaux propres (total I)"
    definition_period = YEAR

    def formula(Firm, period):
        capital_social_individuel = Firm("capital_social_individuel", period)
        primes_emission_fusion_apport = Firm("primes_emission_fusion_apport", period)
        ecarts_reevaluation = Firm("ecarts_reevaluation", period)
        reserve_legale = Firm("reserve_legale", period)
        reserves_statutaires_contractuelles = Firm("reserves_statutaires_contractuelles", period)
        reserves_reglementees = Firm("reserves_reglementees", period)
        autres_reserves = Firm("autres_reserves", period)
        report_a_nouveau = Firm("report_a_nouveau", period)
        resultat_exercice_di = Firm("resultat_exercice_di", period)
        subventions_investissement = Firm("subventions_investissement", period)
        provisions_reglementees = Firm("provisions_reglementees", period)
        capitaux_propres = (capital_social_individuel+
                            primes_emission_fusion_apport+
                            ecarts_reevaluation+
                            reserve_legale+
                            reserves_statutaires_contractuelles+
                            reserves_reglementees+
                            autres_reserves+
                            report_a_nouveau+
                            resultat_exercice_di+
                            subventions_investissement+
                            provisions_reglementees)
        
        return capitaux_propres
