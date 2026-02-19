from openfisca_core.model_api import *
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_entreprises.entities import Etablissement  # noqa F401
from openfisca_france_entreprises.variables.naf import naf


class consommation_electricite(Variable):
    value_type = float
    unit = "MWh"
    entity = Etablissement
    label = "Coal consumption of the etablissement"
    definition_period = YEAR
    reference = ""


class amperage(Variable):
    value_type = float
    unit = "kVA"
    entity = Etablissement
    label = "Amperage de la consommation de l'establissement. Ça determine la catégorie fiscale au sein du Article L312-24."
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603823"


class electricite_double_usage(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "qualification au L312-66"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603707"

    def formula_2011_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return (apet == naf._20_13B) | (apet == naf._20_59Z) | (apet == naf._25_50A)


# 1° La réduction chimique ;
# 2° L'électrolyse ;
# 3° Les procédés métallurgiques ;
# 4° Pour les produits taxables en tant que combustible et consommés pour les besoins d'un processus déterminé, la génération d'une substance indispensable à la réalisation de ce processus et ne pouvant être générée qu'à partir de ces produits.
# pour la quatrème catagorie, j'ai aucune idée comment le faire.


class electricite_production_a_bord(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "la catagorie du transport guidé d'élétricité sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2011_01_01(etablissement, period):
        apet = etablissement("apet", period)
        codes_eligibles = [naf._03_11Z, naf._03_12Z, naf._03_21Z, naf._03_22Z]
        result = apet == codes_eligibles[0]
        for code in codes_eligibles[1:]:
            result = result | (apet == code)
        return result


class electricite_transport_guide(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "la catagorie du transport guidé d'élétricité sous L312-48"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2011_01_01(etablissement, period):
        apet = etablissement("apet", period)
        codes_eligibles = [
            naf._33_17Z,
            naf._49_10Z,
            naf._49_20Z,
            naf._49_31Z,
            naf._49_39C,
            naf._52_21Z,
            naf._52_29A,
            naf._52_29B,
            naf._53_10Z,
            naf._53_20Z,
        ]
        result = apet == codes_eligibles[0]
        for code in codes_eligibles[1:]:
            result = result | (apet == code)
        return result


# _33_17Z, _49_10Z, _49_20Z, _49_31Z, _49_39C, _52_21Z, _52_29A, _52_29B, _53_10Z, _53_20Z


class electricite_transport_collectif_personnes(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = (
        "la catagorie du transport collectif d'éléctricité de personnes sous L312-48"
    )
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return apet == naf._49_39A


# _49_39A


class electricite_alimentation_a_quai(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "la catagorie d'alimentation à quai"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return apet == naf._52_22Z


class electricite_manutention_portuaire(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "la catagorie de la manutention portuaire d'électricité"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2023_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return apet == naf._52_24A


class electricite_exploitation_aerodrome(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "la catagorie des exploitation des aérodromes ouverts à la circulation aérienne publique	"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044875774"

    def formula_2019_01_01(etablissement, period):
        apet = etablissement("apet", period)
        consommation_par_valeur_ajoutee = etablissement(
            "consommation_par_valeur_ajoutee", period
        )
        # 222 wattheures par valeur ajoutée
        return (apet == naf._52_23Z) & (consommation_par_valeur_ajoutee > 0.000222)

    def formula_2022_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return apet == naf._52_23Z


class electricite_fabrication_produits_mineraux_non_metalliques(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "coonditions du L314-64"
    definition_period = YEAR
    reference = ""

    def formula_2011_01_01(etablissement, period):
        apet = etablissement("apet", period)
        codes_eligibles = [
            naf._23_11Z,
            naf._23_12Z,
            naf._23_13Z,
            naf._23_14Z,
            naf._23_19Z,
            naf._23_31Z,
            naf._23_41Z,
            naf._23_42Z,
            naf._23_43Z,
            naf._23_44Z,
            naf._23_49Z,
            naf._23_32Z,
            naf._23_20Z,
            naf._23_51Z,
            naf._23_65Z,
            naf._23_69Z,
            naf._23_61Z,
            naf._23_62Z,
            naf._23_63Z,
            naf._23_64Z,
            naf._23_52Z,
            naf._23_70Z,
            naf._08_11Z,
            naf._23_91Z,
            naf._23_99Z,
        ]
        result = apet == codes_eligibles[0]
        for code in codes_eligibles[1:]:
            result = result | (apet == code)
        return result


# _23_11Z, _23_12Z, _23_13Z, _23_14Z, _23_19Z,
# _23_31Z, _23_41Z, _23_42Z, _23_43Z, _23_44Z, _23_49Z, _23_32Z, _23_20Z
# _23_51Z, _23_65Z, _23_69Z, _23_61Z, _23_62Z, _23_63Z, _23_64Z, _23_69Z, _23_52Z
# _23_70Z, _08_11Z
# _23_91Z, _23_99Z,


class electricite_production_biens_electro_intensive(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "conditions du L312-64/68"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603703/2025-03-05"


# si l’électricité représente plus de la moitié du coût total de production d’un bien, l’entreprise peut bénéficier d’un allègement fiscal
# to do : normalement il y aurait une formule quelque part, mais on a pas les donnés à ce niveau.


class electricite_centres_de_stockage_donnees(Variable):
    value_type = bool
    unit = ""
    entity = Etablissement
    label = "qualification du L314-70"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200586"

    def formula_2019_01_01(etablissement, period):
        apet = etablissement("apet", period)
        return apet == naf._63_11Z


class electro_intensive_activite_industrielle(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = "sous L312-64/65/71"
    reference = (
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603709"
    )

    def formula_2022_01_01(etablissement, period, parameters):
        apet = etablissement("apet", period)
        return (
            (apet == naf._08_12Z)
            | (apet == naf._08_99Z)
            | (apet == naf._09_90Z)
            | (apet == naf._28_92Z)
        )


class electro_intensive_concurrence_internationale(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = "concurrence internationale sous L312-65/72"
    reference = (
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044603709"
    )

    def formula_2022_01_01(etablissement, period, parameters):
        apet = etablissement("apet", period)
        codes_eligibles = [
            naf._07_10Z,
            naf._08_91Z,
            naf._09_90Z,
            naf._24_42Z,
            naf._24_43Z,
            naf._24_44Z,
            naf._24_45Z,
            naf._22_21Z,
            naf._24_20Z,
            naf._24_31Z,
            naf._20_13B,
            naf._20_14Z,
            naf._07_21Z,
            naf._11_01Z,
            naf._20_15Z,
            naf._38_21Z,
            naf._20_60Z,
            naf._14_11Z,
            naf._17_11Z,
            naf._17_12Z,
        ]
        result = apet == codes_eligibles[0]
        for code in codes_eligibles[1:]:
            result = result | (apet == code)
        return result


class consommation_electricite_energie_ou_gaz_renouvelable(Variable):
    value_type = float
    unit = "MWh"
    entity = Etablissement
    label = "partie une du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"


class consommation_electricite_puissance_moins_1_MW(Variable):
    value_type = float
    unit = "MWh"
    entity = Etablissement
    label = "partie deux du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"


# La puissance installée sur le site de production est inférieure à un mégawatt


class consommation_electricite_auto_consommation(Variable):
    value_type = float
    unit = "MWh"
    entity = Etablissement
    label = "partie trois du L312-87"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051216635"


class electricite_production_electricite(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=la%20production%20de%20l%27%C3%A9lectricit%C3%A9, https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Sont%20exon%C3%A9r%C3%A9s%20de%20l%27accise%20les%20produits%20taxables%20consomm%C3%A9s%20pour%20les%20besoins%20de%20la%20production%20d%27%C3%A9lectricit%C3%A9"

    def formula_2011_01_01(etablissement, period, parameters):
        apet = etablissement("apet", period)
        return apet == naf._35_11Z


# Centrals de production d'électricité


class consommation_electricite_petite_producteur_electricite(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    unit = "MWh"
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000023216102/2011-01-01/#:~:text=4%C2%B0%20Produite%20par,site%20de%20production%20%3B"


# Produite par de petits producteurs d'électricité qui la consomment pour les besoins de leur activité.
# Sont considérées comme petits producteurs d'électricité les personnes qui exploitent des installations de production d'électricité
# dont la production annuelle n'excède pas 240 millions de kilowattheures par site de production ;


class electricite_installations_industrielles_electro_intensives(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000031814811/2016-01-01/#:~:text=C.%2Da.%20Pour,est%20fix%C3%A9%20%C3%A0%20%3A"

    def formula_2016_01_01(etablissement, period):
        taxe_accise_electricite_taux_normal = etablissement(
            "taxe_accise_electricite_taux_normal", period
        )
        valeur_ajoutee_eta = etablissement("valeur_ajoutee_eta", period)
        return (valeur_ajoutee_eta != 0) & (
            taxe_accise_electricite_taux_normal >= valeur_ajoutee_eta * 0.005
        )


# C.-a. Pour les personnes qui exploitent des installations industrielles électro-intensives
# au sens où, au niveau de l'entreprise ou de ses sites, le montant de la taxe qui aurait été
# due en application du B, sans application des exonérations et exemptions, est au moins égal
# à 0,5 % de la valeur ajoutée, le tarif de la taxe intérieure de consommation applicable aux
# consommations finales d'électricité effectuées pour leurs besoins est fixé à :


class electricite_installations_industrielles_hyper_electro_intensives(Variable):
    value_type = bool
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000031814811/2016-01-01/#:~:text=Est%20consid%C3%A9r%C3%A9e%20comme%20hyper%C3%A9lectro%2Dintensive%20une%20installation%20qui%20v%C3%A9rifie%20les%20deux%20conditions%20suivantes%20%3A"

    def formula_2016_01_01(etablissement, period):
        consommation_par_valeur_ajoutee = etablissement(
            "consommation_par_valeur_ajoutee", period
        )
        intensite_echanges_avec_pays_tiers = etablissement(
            "intensite_echanges_avec_pays_tiers", period
        )
        return (consommation_par_valeur_ajoutee >= 0.006) & (
            intensite_echanges_avec_pays_tiers >= 25
        )


# Est considérée comme hyperélectro-intensive une installation qui vérifie les deux conditions suivantes :
# -sa consommation d'électricité représente plus de 6 kilowattheures par euro de valeur ajoutée ;
# -son activité appartient à un secteur dont l'intensité des échanges avec des pays tiers,
# telle que déterminée par la Commission européenne aux fins de l'article 10 bis de la
# directive 2003/87/ CE du Parlement européen et du Conseil du 13 octobre 2003 établissant
# un système d'échange de quotas d'émission de gaz à effet de serre dans la Communauté et
# modifiant la directive 96/61/ CE du Conseil, est supérieure à 25 %.


class consommation_electricite_fournie_aux_navires(Variable):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000043811132/2021-01-01/#:~:text=h.%20Le%20tarif%20de%20la%20taxe%20applicable%20%C3%A0%20l%27%C3%A9lectricit%C3%A9%20directement%20fournie%2C%20lors%20de%20leur%20stationnement%20%C3%A0%20quai%20dans%20les%20ports%2C%20aux%20navires%20mentionn%C3%A9s%20au%20c%20du%201%20de%20l%27article%20265%20bis%20et%20aux%20engins%20b%C3%A9n%C3%A9ficiant%20de%20l%27exon%C3%A9ration%20mentionn%C3%A9e%20au%20e%20du%20m%C3%AAme%201%20est%20fix%C3%A9%20%C3%A0%200%2C5%20%E2%82%AC%20par%20m%C3%A9gawattheure."


# Alimentation des aéronefs lors de leur stationnement sur les aérodromes ouverts à la circulation aérienne publique
# Electricité consommée pour les besoins des activités économiques
class electricite_alimentation_aeronefs_stationnement_aerodromes_activites_economiques(
    Variable
):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Alimentation%20des%20a%C3%A9ronefs%20lors%20de%20leur%20stationnement%20sur%20les%20a%C3%A9rodromes%20ouverts%20%C3%A0%20la%20circulation%20a%C3%A9rienne%20publique"


# Alimentation des aéronefs lors de leur stationnement sur les aérodromes ouverts à la circulation aérienne publique
# Electricité consommée pour les besoins des activités non économiques
class electricite_alimentation_aeronefs_stationnement_aerodromes_activites_non_economiques(
    Variable
):
    value_type = float
    entity = Etablissement
    definition_period = YEAR
    label = ""
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000044595989/LEGISCTA000044598327/#LEGISCTA000044603893:~:text=Alimentation%20des%20a%C3%A9ronefs%20lors%20de%20leur%20stationnement%20sur%20les%20a%C3%A9rodromes%20ouverts%20%C3%A0%20la%20circulation%20a%C3%A9rienne%20publique"
