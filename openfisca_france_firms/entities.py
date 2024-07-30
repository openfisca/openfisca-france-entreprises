"""
This file defines the entities needed by our legislation.

Taxes and benefits can be calculated for different entities: etablissements, unite_legale, companies, etc.

See https://openfisca.org/doc/key-concepts/etablissement,_entities,_role.html
"""

from openfisca_core.entities import build_entity

UniteLegale = build_entity(
    key = "unite_legale",
    plural = "unite_legales",
    label = "All the etablissements in a legal unit defined by a SIREN.",
    doc = """
    A unite_legale entity contains one or more etablissements.
    Each etablissement in a unite_legale has a role (e.g. siege_socials or secondaire etablissement). There can only be one siege_social etablissement.

    Usage:
    Check the number of etablissements of a specific role (e.g. check if there is a unique 'siege_social' etablissement within a unite_legale).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    roles = [
        {
            "key": "siege_social",
            "plural": "siege_socials",
            "label": "SiegeSocial",
            "max": 1,
            "doc": "The one etablissement that is siege_socials to the unite_legale.",
            },
        {
            "key": "secondaire",
            "plural": "secondaires",
            "label": "Secondary etablissements",
            "doc": "Other etablissements in the unite_legale.",
            },
        ],
    )

Etablissement = build_entity(
    key = "etablissement",
    plural = "etablissements",
    label = "An etablissement. The minimal legal entity on which a legislation might be applied.",
    doc = """

    Variables like 'masse_salariale' and 'consommation_energie' are usually defined for the entity 'Etablissement'.

    Usage:
    Calculate a variable applied to a 'Etablissement' (e.g. access the 'example_salary' of a specific month with etablissement("example_salary", "2017-05")).
    Check the role of a 'Etablissement' in a group entity (e.g. check if a the 'Etablissement' is a 'siege_social' in a 'unite_legale' entity with etablissement.has_role(unite_legale.HEADQUARTER)).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    is_person = True,
    )

entities = [UniteLegale, Etablissement]
