"""Correspondance entre les cases de la 2040-TIC et le modèle.

Chaque `Cellule` décrit une case (ou un couple quantité/montant) de la
déclaration : le paramètre du barème censé porter son tarif, la variable du
modèle censée le restituer, et les entrées à fournir pour placer un
établissement dans ce régime.

`variable = None` signale une cellule dont on sait qu'elle n'est pas restituable
en l'état : l'audit la remonte comme lacune de couverture plutôt que de
l'ignorer silencieusement.

`ASSIETTE` marque, dans `entrees`, la variable qui doit recevoir la quantité
déclarée de la case.
"""

from __future__ import annotations

from dataclasses import dataclass, field

ASSIETTE = "<<assiette>>"

TOUS_MILLESIMES = (2022, 2023, 2024, 2025)


@dataclass(frozen=True)
class Cellule:
    case_quantite: str
    cases_montant: tuple[str, ...]
    intitule: str
    millesimes: tuple[int, ...] = TOUS_MILLESIMES
    parametre: str | None = None
    variable: str | None = None
    entrees: dict[str, object] = field(default_factory=dict)
    remarque: str = ""
    constat: str = ""
    """Désaccord établi entre la déclaration et le modèle, à arbitrer.

    Une cellule qui porte un `constat` n'est pas émise en test : le tarif du barème
    et la variable du modèle sont bien identifiés, mais le modèle ne restitue pas le
    montant déclaré, et la cause est comprise. En faire un test le figerait comme
    attendu ; le laisser en échec casserait la CI. Il est donc consigné dans
    AGREGATS_TIC.md et remonté par `audit.py`.
    """

    parametre_majoration: str | None = None
    """Paramètre s'ajoutant à `parametre` pour former le tarif effectivement dû.

    Sert la majoration au titre des zones non interconnectées de l'article L312-37-1 du
    CIBS : depuis le 1er août 2025, les tarifs normaux des combustibles et de l'électricité
    sont majorés d'un montant affecté au financement des ZNI, dû par tous les redevables du
    tarif normal. La déclaration sépare les deux en cases de montant distinctes, mais le
    tarif implicite de la cellule est bien leur somme.
    """

    annee_tarif: int | None = None
    """Millésime du tarif porté par la case, quand il diffère du millésime de dépôt.

    Le millésime du fichier est l'année de dépôt de la déclaration, pas l'année de
    consommation : une case ouverte pour un tarif donné continue de le porter les
    années suivantes, pour les régularisations. C'est ce qui explique qu'une case
    affiche le même tarif implicite sur les quatre millésimes alors que le barème,
    lui, évolue. `annee_tarif` fixe l'année à laquelle lire le paramètre.
    """


# ---------------------------------------------------------------------------
# Gaz naturel
# ---------------------------------------------------------------------------

GAZ_NATUREL = [
    Cellule(
        case_quantite="_911235",
        cases_montant=("_911236",),
        intitule="Gaz naturel carburant — tarif plein",
        parametre="energies.gaz_naturel.accise.carburants.tarif_normal",
        variable="taxe_accise_gaz_naturel_carburant",
        entrees={"consommation_gaz_carburant": ASSIETTE},
    ),
    Cellule(
        case_quantite="_911237",
        annee_tarif=2021,
        cases_montant=("_911238",),
        intitule="Gaz naturel combustible — TICGN, tarif plein au titre de l'année N",
        parametre="energies.gaz_naturel.ticgn.taux_normal",
        variable="taxe_interieure_consommation_gaz_naturel",
        entrees={"consommation_gaz_combustible": ASSIETTE},
        # Constat n° 9 clos : le modèle appliquait le facteur de conversion PCS/PCI de 1,11, et
        # le rapport modèle/déclaration valait exactement 1,11 sans résidu. La conversion est
        # retirée — la quantité déclarée suit l'unité dans laquelle la loi exprime le tarif.
        remarque=(
            "Case du bloc TICGN, pas du bloc accise : son libellé porte « TICGN - Taux plein » "
            "et son tarif de 8,43 EUR/MWh est le taux normal de la TICGN au 1er janvier 2021 "
            "(article 61 de la LF 2021), figé par les régularisations sur les quatre millésimes."
        ),
    ),
    Cellule(
        case_quantite="_911264",
        annee_tarif=2022,
        cases_montant=("_911265",),
        intitule="Gaz naturel combustible — accise, tarif plein au titre de l'année N+1",
        parametre="energies.gaz_naturel.accise.combustibles.tarif_normal",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE},
        remarque=(
            "Quantités rattachées à l'exercice suivant : tarif implicite 8,41 EUR/MWh, soit le "
            "tarif normal de l'accise en 2022 (arrêté du 8 septembre 2021). Le modèle n'a pas de "
            "notion d'acompte au titre de N+1, mais la cellule reste une cellule tarifaire "
            "homogène : c'est son tarif qu'on vérifie, pas le mécanisme de l'acompte."
        ),
    ),
    Cellule(
        case_quantite="_911272",
        annee_tarif=2023,
        cases_montant=("_911273",),
        intitule="Gaz naturel combustible — tarif à 8,37 €/MWh",
        millesimes=(2023, 2024, 2025),
        parametre="energies.gaz_naturel.accise.combustibles.tarif_normal",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE},
        remarque=(
            "8,37 EUR/MWh est le tarif normal de l'accise en 2023, constaté à l'article 2 de "
            "l'arrêté du 13 décembre 2022 : 8,45 minoré de la part de biométhane injectée."
        ),
    ),
    Cellule(
        case_quantite="_912998",
        annee_tarif=2024,
        cases_montant=("_912999",),
        intitule="Gaz naturel combustible — tarif à 16,37 €/MWh",
        millesimes=(2024, 2025),
        parametre="energies.gaz_naturel.accise.combustibles.tarif_normal",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE},
    ),
    Cellule(
        case_quantite="_914201",
        cases_montant=("_914202",),
        intitule="Gaz naturel combustible — tarif à 17,16 €/MWh",
        millesimes=(2025,),
        parametre="energies.gaz_naturel.accise.combustibles.tarif_normal",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE},
    ),
    Cellule(
        case_quantite="_911241",
        cases_montant=("_911242",),
        intitule="Gaz naturel combustible — grande consommatrice soumise au SEQE",
        parametre="energies.gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_SEQE",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={
            "consommation_gaz_combustible": ASSIETTE,
            "installation_seqe": True,
            "installation_grande_consommatrice_energie": True,
        },
    ),
    Cellule(
        case_quantite="_911243",
        cases_montant=("_911244",),
        intitule="Gaz naturel combustible — risque de fuite de carbone",
        parametre="energies.gaz_naturel.accise.combustibles.tarifs_reduits.intensive_energie_indirect_SEQE",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={
            "consommation_gaz_combustible": ASSIETTE,
            "installation_seqe": False,
            "risque_de_fuite_carbone_eta": True,
            "intensite_energetique_valeur_ajoutee": 0.01,
        },
        remarque=(
            "Constat n° 3 clos : le paramètre était clos au 2024-01-01, clôture rapportée à "
            "l'article 94 II K 2° de la LF 2024 qui vise le charbon et non le gaz. L. 312-75 "
            "conserve « Gaz naturels combustible | L. 312-77 | 1,6 » en 2024 comme en 2025."
        ),
    ),
    Cellule(
        case_quantite="_911245",
        cases_montant=("_911246",),
        intitule="Gaz naturel combustible — déshydratation de légumes et plantes aromatiques",
        parametre="energies.gaz_naturel.accise.combustibles.tarifs_reduits.deshydratation",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={
            "consommation_gaz_combustible": ASSIETTE,
            "gaz_dehydration_legumes_et_plantes_aromatiques": True,
            "consommation_par_valeur_ajoutee": 0.001,
        },
    ),
    Cellule(
        case_quantite="_914387",
        cases_montant=("_914388", "_914389"),
        intitule="Gaz naturel combustible — tarif ZNI 15,43 €/MWh (10,54 + majoration 4,89)",
        millesimes=(2025,),
        parametre="energies.gaz_naturel.accise.combustibles.tarif_normal",
        parametre_majoration="energies.majoration_zni",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE},
    ),
]

# ---------------------------------------------------------------------------
# Charbon
# ---------------------------------------------------------------------------

CHARBON = [
    Cellule(
        case_quantite="_911293",
        cases_montant=("_911294",),
        intitule="Charbon combustible — tarif plein",
        parametre="energies.charbon.accise.combustibles.tarif_normal",
        variable="taxe_interieure_consommation_charbon",
        entrees={"assiette_ticc": ASSIETTE},
    ),
    Cellule(
        case_quantite="_911295",
        annee_tarif=2022,
        cases_montant=("_911296",),
        intitule="Charbon combustible — grande consommatrice soumise au SEQE",
        millesimes=(2022, 2023, 2024),
        parametre="energies.charbon.accise.combustibles.tarifs_reduits.intensive_energie_SEQE",
        variable="taxe_interieure_consommation_charbon",
        entrees={
            "assiette_ticc": ASSIETTE,
            "installation_seqe": True,
            "intensite_energetique_valeur_production": 0.05,
        },
    ),
    Cellule(
        case_quantite="_911306",
        cases_montant=("_911307",),
        intitule="Charbon — installations intensives soumises au SEQE UE (2,79 €/MWh)",
        millesimes=(2024,),
        parametre="energies.charbon.accise.combustibles.tarifs_reduits.intensive_energie_SEQE",
        variable="taxe_interieure_consommation_charbon",
        entrees={
            "assiette_ticc": ASSIETTE,
            "installation_seqe": True,
            "intensite_energetique_valeur_production": 0.05,
        },
    ),
    Cellule(
        case_quantite="_914207",
        cases_montant=("_914208",),
        intitule="Charbon — installations intensives soumises au SEQE-IF UE (4,39 €/MWh)",
        millesimes=(2025,),
        parametre="energies.charbon.accise.combustibles.tarifs_reduits.intensive_energie_SEQE",
        variable="taxe_interieure_consommation_charbon",
        entrees={
            "assiette_ticc": ASSIETTE,
            "installation_seqe": True,
            "intensite_energetique_valeur_production": 0.05,
        },
    ),
    Cellule(
        case_quantite="_914396",
        cases_montant=("_914397", "_914398"),
        intitule="Charbon — tarif ZNI 15,43 €/MWh (10,54 + majoration 4,89)",
        millesimes=(2025,),
        parametre="energies.charbon.accise.combustibles.tarif_normal",
        parametre_majoration="energies.majoration_zni",
        variable="taxe_interieure_consommation_charbon",
        entrees={"assiette_ticc": ASSIETTE},
    ),
]

# ---------------------------------------------------------------------------
# Électricité
# ---------------------------------------------------------------------------

ELECTRICITE = [
    Cellule(
        case_quantite="_911319",
        cases_montant=("_911320",),
        intitule="Électricité — puissance de raccordement > 250 kVA",
        parametre="energies.electricite.accise.tarifs_normaux.haute_puissance",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 400},
    ),
    Cellule(
        case_quantite="_911321",
        annee_tarif=2022,
        cases_montant=("_911322",),
        intitule="Électricité — puissance de raccordement < 250 kVA",
        parametre="energies.electricite.accise.tarifs_normaux.menages_et_assimiles",
        variable=None,
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 20},
        remarque="Tarif implicite 25,8291 €/MWh, contre 25,6875 au barème (voir le rapport).",
    ),
    Cellule(
        case_quantite="_911323",
        annee_tarif=2022,
        cases_montant=("_911324",),
        intitule="Électricité — activités économiques, puissance > 36 kVA",
        parametre="energies.electricite.accise.tarifs_normaux.pme_activites_economiques",
        variable=None,
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 100},
        remarque="Tarif implicite 23,6097 €/MWh, contre 23,5625 au barème (voir le rapport).",
    ),
    Cellule(
        case_quantite="_911327",
        cases_montant=("_911328",),
        intitule="Électricité — IEI, consommation > 3 kWh/€ de VA",
        parametre="energies.electricite.accise.tarifs_reduits.electro_intensives.industrie_6_75",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electro_intensive_activite_industrielle": True,
            # 10 %, soit au-delà du niveau minimal de 6,75 % qui ouvre le tarif de 2 €/MWh
            # (L312-65). L'électro-intensité est un rapport sans dimension, pas des kWh par
            # euro : le libellé de la case reprend le vocabulaire de la TICFE d'avant 2022.
            "electro_intensite": 0.10,
        },
    ),
    Cellule(
        case_quantite="_911329",
        cases_montant=("_911330",),
        intitule="Électricité — IEI, consommation comprise entre 1,5 et 3 kWh/€ de VA",
        parametre="energies.electricite.accise.tarifs_reduits.electro_intensives.industrie_3_375",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electro_intensive_activite_industrielle": True,
            # 5 %, dans la bande [3,375 % ; 6,75 %) qui ouvre le tarif de 5 €/MWh (L312-65).
            "electro_intensite": 0.05,
        },
        remarque=(
            "Le modèle borne cette tranche à [0,5 ; 3,375[ alors que la déclaration la borne "
            "à [1,5 ; 3[. Un test discriminant est produit à part."
        ),
    ),
    Cellule(
        case_quantite="_911331",
        cases_montant=("_911332",),
        intitule="Électricité — IEI, consommation < 1,5 kWh/€ de VA",
        parametre="energies.electricite.accise.tarifs_reduits.electro_intensives.industrie_0_5",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electro_intensive_activite_industrielle": True,
            # 1 %, dans la bande [0,5 % ; 3,375 %) qui ouvre le tarif de 7,5 €/MWh (L312-65).
            "electro_intensite": 0.01,
        },
        remarque="Même réserve de bornes que la tranche 1,5–3.",
    ),
    Cellule(
        case_quantite="_911339",
        cases_montant=("_911340",),
        intitule="Électricité — installation hyper-électro-intensive",
        parametre="energies.electricite.accise.tarifs_reduits.electro_intensives.industrie_concurrence_13_5",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electro_intensive_concurrence_internationale": True,
            "electro_intensite": 15.0,
            "intensite_echanges_avec_pays_tiers": 30,
            "risque_de_fuite_carbone_eta": True,
        },
    ),
    Cellule(
        case_quantite="_911341",
        cases_montant=("_911342",),
        intitule="Électricité — transport guidé de personnes et de marchandises",
        parametre="energies.electricite.accise.tarifs_reduits.transport_personnes_marchandises",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "electricite_transport_guide": True},
    ),
    Cellule(
        case_quantite="_911343",
        annee_tarif=2022,
        cases_montant=("_911344",),
        intitule="Électricité — centres de stockage de données numériques",
        millesimes=(2022,),
        parametre="energies.electricite.accise.tarifs_reduits.data_center",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_centres_de_stockage_donnees": True,
        },
    ),
    Cellule(
        case_quantite="_911345",
        annee_tarif=2022,
        cases_montant=("_911346",),
        intitule="Électricité — exploitants d'aérodromes électro-intensifs",
        millesimes=(2022,),
        parametre="energies.electricite.accise.tarifs_reduits.aerodromes",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_exploitation_aerodrome": True,
            "electro_intensite": 1.0,
        },
    ),
    Cellule(
        case_quantite="_911445",
        cases_montant=("_911446",),
        intitule="Électricité — alimentation à quai des navires",
        parametre="energies.electricite.accise.tarifs_reduits.alimentation_engins_flottants",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "electricite_alimentation_a_quai": True},
    ),
    Cellule(
        case_quantite="_912993",
        cases_montant=("_912994",),
        intitule="Électricité — transport collectif routier de personnes",
        millesimes=(2024, 2025),
        parametre="energies.electricite.accise.tarifs_reduits.transport_collectif_routier_personnes",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_transport_collectif_personnes": True,
        },
    ),
    Cellule(
        case_quantite="_912995",
        cases_montant=("_912996",),
        intitule="Électricité — manutention portuaire (électro-intensité ≥ 0,5 %)",
        millesimes=(2024, 2025),
        parametre="energies.electricite.accise.tarifs_reduits.manutention_portuaire",
        variable=None,
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_manutention_portuaire": True,
        },
        remarque="La variable d'entrée existe mais n'est pas branchée dans le select de l'accise 2022+.",
    ),
    Cellule(
        case_quantite="_913035",
        # Constat n° 5 clos : boulier_tarifaire.py n'appliquait que bouclier_tarifaire.entreprises,
        # sans regarder la catégorie fiscale. Il lit désormais bouclier_tarifaire.menages sous
        # 36 kVA, seuil de la catégorie « ménages et assimilés » de l'accise.
        annee_tarif=2024,
        cases_montant=("_913036",),
        intitule="Électricité — tarif à 21,00 €/MWh (bouclier, ménages et assimilés)",
        millesimes=(2024, 2025),
        parametre="energies.electricite.accise.bouclier_tarifaire.menages",
        variable="taxe_electricite_bouclier_tarifaire",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 20},
    ),
    Cellule(
        case_quantite="_913037",
        annee_tarif=2024,
        cases_montant=("_913038",),
        intitule="Électricité — tarif à 20,50 €/MWh (bouclier, entreprises)",
        millesimes=(2024, 2025),
        parametre="energies.electricite.accise.bouclier_tarifaire.entreprises",
        variable="taxe_electricite_bouclier_tarifaire",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 100},
    ),
    Cellule(
        case_quantite="_914195",
        # Constat n° 6 clos : le tarif change au 1er février, et le modèle lisait la valeur du
        # 1er janvier faute de variables mensuelles. Les consommations étant désormais en
        # definition_period = MONTH, la quantité se pose sur un mois où s'applique le tarif
        # déclaré, et le modèle le restitue.
        cases_montant=("_914196",),
        intitule="Électricité — tarif à 33,70 €/MWh (ménages et assimilés)",
        millesimes=(2025,),
        parametre="energies.electricite.accise.tarifs_normaux.menages_et_assimiles",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 20},
    ),
    Cellule(
        case_quantite="_914197",
        # Constat n° 6 clos : voir _914195.
        cases_montant=("_914198",),
        intitule="Électricité — tarif à 26,23 €/MWh (PME et activités économiques)",
        millesimes=(2025,),
        parametre="energies.electricite.accise.tarifs_normaux.pme_activites_economiques",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 100},
    ),
    Cellule(
        case_quantite="_911369",
        annee_tarif=2022,
        cases_montant=("_911370",),
        intitule="Électricité — bouclier tarifaire, entreprises (tarif de référence 22,50)",
        parametre="energies.electricite.accise.bouclier_tarifaire.entreprises",
        variable="taxe_electricite_bouclier_tarifaire",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 400},
        remarque="Le libellé nomme le tarif d'avant bouclier ; le montant déclaré applique le plancher.",
    ),
    Cellule(
        case_quantite="_911371",
        # Constat n° 5 clos : boulier_tarifaire.py n'appliquait que bouclier_tarifaire.entreprises,
        # sans regarder la catégorie fiscale. Il lit désormais bouclier_tarifaire.menages sous
        # 36 kVA, seuil de la catégorie « ménages et assimilés » de l'accise.
        annee_tarif=2022,
        cases_montant=("_911372",),
        intitule="Électricité — bouclier tarifaire, ménages (tarif de référence 25,8291)",
        parametre="energies.electricite.accise.bouclier_tarifaire.menages",
        variable="taxe_electricite_bouclier_tarifaire",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 20},
        remarque="Le libellé nomme le tarif d'avant bouclier ; le montant déclaré applique le plancher.",
    ),
    Cellule(
        case_quantite="_914374",
        cases_montant=("_914375", "_914376"),
        intitule="Électricité — tarif ZNI 29,98 €/MWh (25,09 + majoration 4,89)",
        millesimes=(2025,),
        parametre="energies.electricite.accise.tarifs_normaux.menages_et_assimiles",
        parametre_majoration="energies.majoration_zni",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 20},
    ),
    Cellule(
        case_quantite="_914377",
        cases_montant=("_914378", "_914379"),
        intitule="Électricité — tarif ZNI 25,79 €/MWh (20,90 + majoration 4,89)",
        millesimes=(2025,),
        parametre="energies.electricite.accise.tarifs_normaux.haute_puissance",
        parametre_majoration="energies.majoration_zni",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "amperage": 400},
    ),
]

CELLULES = GAZ_NATUREL + CHARBON + ELECTRICITE


# ---------------------------------------------------------------------------
# Exonérations et exemptions : quantités déclarées sans montant, taxe nulle
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Exoneration:
    case: str
    intitule: str
    variable: str | None = None
    entrees: dict[str, object] = field(default_factory=dict)
    remarque: str = ""


EXONERATIONS = [
    Exoneration(
        case="_911252",
        intitule="Gaz naturel — double usage",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE, "gaz_double_usage": True},
    ),
    Exoneration(
        case="_911253",
        intitule="Gaz naturel — fabrication de minéraux non métalliques",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={
            "consommation_gaz_combustible": ASSIETTE,
            "gaz_production_mineraux_non_metalliques": True,
        },
    ),
    Exoneration(
        case="_911256",
        intitule="Gaz naturel — production ou extraction de gaz naturel",
        variable="taxe_accise_gaz_naturel_combustible",
        entrees={"consommation_gaz_combustible": ASSIETTE, "gaz_extraction_production": True},
    ),
    Exoneration(
        case="_911459",
        intitule="Charbon — double usage",
        variable="taxe_interieure_consommation_charbon",
        entrees={"assiette_ticc": ASSIETTE, "charbon_double_usage": True},
    ),
    Exoneration(
        case="_911460",
        intitule="Charbon — fabrication de produits minéraux non métalliques",
        variable="taxe_interieure_consommation_charbon",
        entrees={
            "assiette_ticc": ASSIETTE,
            "charbon_fabrication_produits_mineraux_non_metalliques": True,
        },
    ),
    Exoneration(
        case="_911464",
        intitule="Charbon — valorisation de la biomasse",
        variable="taxe_interieure_consommation_charbon",
        entrees={
            "assiette_ticc": ASSIETTE,
            "charbon_biomasse": True,
            "installation_seqe": True,
            "intensite_energetique_valeur_production": 0.05,
        },
    ),
    Exoneration(
        case="_911352",
        intitule="Électricité — fabrication de produits minéraux non métalliques",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_fabrication_produits_mineraux_non_metalliques": True,
        },
    ),
    Exoneration(
        case="_911355",
        intitule="Électricité — production d'électricité",
        variable="taxe_accise_electricite",
        entrees={
            "assiette_taxe_electricite": ASSIETTE,
            "electricite_production_electricite": True,
        },
    ),
    Exoneration(
        case="_911357",
        intitule="Électricité — production à bord des bateaux",
        variable="taxe_accise_electricite",
        entrees={"assiette_taxe_electricite": ASSIETTE, "electricite_production_a_bord": True},
    ),
]


# ---------------------------------------------------------------------------
# Agrégations déclarées : une case TOTAL et ses composantes, par millésime
# ---------------------------------------------------------------------------

TOTAUX = {
    "_911325": {
        "intitule": "TICFE — total des tarifs pleins (quantités)",
        "composantes": dict.fromkeys(
            TOUS_MILLESIMES,
            [
                "_911319", "_911321", "_911323", "_911369", "_911371", "_911373",
                "_913035", "_913037", "_914195", "_914197", "_914374", "_914377",
                "_911310", "_911312", "_911394", "_911396", "_911398", "_911400",
                "_911467", "_911469",
            ],
        ),
    },
    "_911347": {
        "intitule": "TICFE — total des tarifs réduits (quantités)",
        "composantes": dict.fromkeys(
            TOUS_MILLESIMES,
            [
                "_911327", "_911329", "_911331", "_911333", "_911335", "_911337",
                "_911339", "_911341", "_911343", "_911345", "_911375", "_911377",
                "_911379", "_911381", "_911383", "_911385", "_911387", "_911389",
                "_911391", "_911445", "_912993", "_912995", "_914199",
            ],
        ),
    },
    "_911358": {
        "intitule": "TICFE — total des quantités exonérées",
        "composantes": dict.fromkeys(
            TOUS_MILLESIMES,
            ["_911351", "_911352", "_911353", "_911354", "_911355", "_911356", "_911357"],
        ),
    },
    "_911455": {
        "intitule": "TICC — total des tarifs pleins (quantités)",
        "composantes": {2022: ["_911293"], 2023: ["_911293"], 2024: ["_911293"]},
    },
    "_911299": {
        "intitule": "TICC — total des tarifs réduits (quantités)",
        "composantes": {
            2022: ["_911295"],
            2023: ["_911295"],
            2024: ["_911295", "_911306"],
        },
    },
    "_911247": {
        "intitule": "TICGN — total des tarifs réduits (quantités)",
        "composantes": {
            2022: ["_911241", "_911243", "_911245"],
            2023: ["_911241", "_911243", "_911245"],
            2024: ["_911241", "_911243", "_911245"],
            2025: ["_911241", "_911243", "_911245"],
        },
    },
    "_911259": {
        "intitule": "TICGN — total des quantités exemptées",
        "composantes": dict.fromkeys(
            TOUS_MILLESIMES,
            [
                "_911251",
                "_911252",
                "_911253",
                "_911254",
                "_911255",
                "_911256",
                "_911257",
                "_911258",
            ],
        ),
    },
    "_911465": {
        "intitule": "TICC — total des quantités exemptées",
        "composantes": dict.fromkeys(
            TOUS_MILLESIMES,
            ["_911458", "_911459", "_911460", "_911461", "_911462", "_911463", "_911464"],
        ),
    },
    "_911239": {
        "intitule": "TICGN — total des tarifs pleins (quantités)",
        "composantes": {
            2022: ["_911235", "_911237", "_911264"],
            2023: ["_911235", "_911237", "_911264", "_911270", "_911272"],
            2024: ["_911235", "_911237", "_911264", "_911270", "_911272", "_912998"],
            2025: ["_911235", "_911237", "_911264", "_911272", "_912998", "_914201", "_914387"],
        },
    },
}
