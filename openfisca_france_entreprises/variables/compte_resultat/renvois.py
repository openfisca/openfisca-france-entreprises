from openfisca_core.model_api import *
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_france_entreprises.entities import UniteLegale, Etablissement  # noqa F401


class produits_nets_partiels_operations_lt(Variable):
    cerfa_field = "HO"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits nets partiels sur opérations à long terme"
    definition_period = YEAR


class produits_locations_immobilieres(Variable):
    cerfa_field = "HY"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits de locations immobilières"
    definition_period = YEAR


class produits_exploitation_exercices_anterieurs(Variable):
    cerfa_field = "1G"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits d'exploitation afférents à des exercices antérieurs"
    definition_period = YEAR


class credit_bail_mobilier(Variable):
    cerfa_field = "HP"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Crédit-bail mobilier"
    definition_period = YEAR


class credit_bail_immobilier(Variable):
    cerfa_field = "HQ"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Crédit-bail immobilier"
    definition_period = YEAR


class charges_exploitation_exercices_anterieurs(Variable):
    cerfa_field = "1H"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Charges d'exploitation afférentes à des exercices antérieurs"
    definition_period = YEAR


class produits_entreprises_liees(Variable):
    cerfa_field = "1J"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Produits concernant les entreprises liées"
    definition_period = YEAR


class interets_entreprises_liees(Variable):
    cerfa_field = "1K"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Intérêts concernant les entreprises liées"
    definition_period = YEAR


class dons_organismes_ig(Variable):
    cerfa_field = "HX"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Dons faits aux organismes d'intérêt général (article 238 bis du CGI)"
    definition_period = YEAR


class amortissements_souscriptions_pme_innovantes(Variable):
    cerfa_field = "RC"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Amortissements des souscriptions dans des PME innovantes (art. 217 octies du CGI)"
    definition_period = YEAR


class amortissements_exeptionnels_constructions_nouvelles(Variable):
    cerfa_field = "RD"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Amortissements exceptionnels de 25% des constructions nouvelles (art. 39 quinquies du D du CGI)"
    definition_period = YEAR


class transfert_de_charges(Variable):
    cerfa_field = "A1"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Transfert de charges"
    definition_period = YEAR


class cotisations_personnelles_exploitant(Variable):
    cerfa_field = "A2"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Cotisations personnelles de l'exploitant"
    definition_period = YEAR


class cotisations_sociales_obligatoires_exploitant(Variable):
    cerfa_field = "A5"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Cotisations personnelles de l'exploitant : Montant des cotisations sociales obligatoires hors CSG/CRDS"
    definition_period = YEAR


class redevances_concessions_brevets_produits(Variable):
    cerfa_field = "A3"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Redevances pour concessions de brevets, de licences (produits)"
    definition_period = YEAR


class redevances_concessions_brevets_charges(Variable):
    cerfa_field = "A4"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Redevances pour concessions de brevets, de licences (charges)"
    definition_period = YEAR


class primes_cotisations_comp_perso_facultatives(Variable):
    cerfa_field = "A6"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Primes et cotisations complémentaires personnes facultatives"
    definition_period = YEAR


class cotisations_madelin(Variable):
    cerfa_field = "A7"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Cotisations facultatives Madelin"
    definition_period = YEAR


class cotisations_plan_epargne_retraite(Variable):
    cerfa_field = "A8"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Cotisations facultatives aux nouveaux plans d'épargne retraite"
    definition_period = YEAR


class primes_cotisations_comp_perso_obligatoires(Variable):
    cerfa_field = "A9"
    value_type = int
    unit = 'currency'
    entity = UniteLegale
    label = "Primes et cotisations complémentaires personnes obligatoires"
    definition_period = YEAR
