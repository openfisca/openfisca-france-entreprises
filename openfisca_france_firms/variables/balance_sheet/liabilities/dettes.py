from openfisca_core.model_api import *
from openfisca_france_firms.entities import Firm  # noqa F401

class emprunts_obligatoires_convertibles(Variable):
    cerfa_field = "DS"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Emprunts obligatoires convertibles"
    definition_period = YEAR

class autres_emprunts_obligatoires(Variable):
    cerfa_field = "DT"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Autres emprunts obligatoires"
    definition_period = YEAR

class emprunts_dettes_etablissement_credit(Variable):
    cerfa_field = "DU"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Emprunts et dettes auprès des établissements de crédit"
    definition_period = YEAR

class emprunts_dettes_divers(Variable):
    cerfa_field = "DV"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Emprunts et dettes financières divers"
    definition_period = YEAR

class emprunts_participatifs(Variable):
    cerfa_field = "EI"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Emprunts participatifs"
    definition_period = YEAR

class avances_acomptes_recus_commandes(Variable):
    cerfa_field = "DW"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Avances et acomptes reçus sur commandes en cours"
    definition_period = YEAR

class dettes_fournisseurs(Variable):
    cerfa_field = "DX"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dettes fournisseurs et comptes rattachés"
    definition_period = YEAR

class dettes_fiscales_sociales(Variable):
    cerfa_field = "DY"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dettes fiscales et sociales"
    definition_period = YEAR

class dettes_immobilisations(Variable):
    cerfa_field = "DZ"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dettes sur immobilisations et comptes rattachés"
    definition_period = YEAR

class autres_dettes(Variable):
    cerfa_field = "EA"
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Autres dettes"
    definition_period = YEAR

class dettes(Variable):
    value_type = int
    unit = 'currency'
    entity = Firm
    label = "Dettes"
    definition_period = YEAR

    def formula(Firm, period):
        emprunts_obligatoires_convertibles = Firm("emprunts_obligatoires_convertibles", period) 
        autres_emprunts_obligatoires = Firm("autres_emprunts_obligatoires", period)
        emprunts_dettes_etablissement_credit = Firm("emprunts_dettes_etablissement_credit", period)
        emprunts_dettes_divers = Firm("emprunts_dettes_divers", period)
        avances_acomptes_recus_commandes = Firm("avances_acomptes_recus_commandes", period)
        dettes_fournisseurs = Firm("dettes_fournisseurs", period)
        dettes_fiscales_sociales = Firm("dettes_fiscales_sociales", period)
        dettes_immobilisations = Firm("dettes_immobilisations", period)
        autres_dettes = Firm("autres_dettes", period)

        dettes = (emprunts_obligatoires_convertibles+
                  autres_emprunts_obligatoires+
                  emprunts_dettes_etablissement_credit+
                  emprunts_dettes_divers+
                  avances_acomptes_recus_commandes+
                  dettes_fournisseurs+
                  dettes_fiscales_sociales+
                  dettes_immobilisations+
                  autres_dettes)

        return dettes
