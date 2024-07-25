"""
This file defines the entities needed by our legislation.

Taxes and benefits can be calculated for different entities: establishments, firm, companies, etc.

See https://openfisca.org/doc/key-concepts/establishment,_entities,_role.html
"""

from openfisca_core.entities import build_entity

Firm = build_entity(
    key = "firm",
    plural = "firms",
    label = "All the establishments in a legal unit defined by a SIREN.",
    doc = """
    A firm entity contains one or more establishments.
    Each establishment in a firm has a role (e.g. headquarters or secondary establishment). There can only be one headquarter establishment.

    Usage:
    Check the number of establishments of a specific role (e.g. check if there is a unique 'headquarter' establishment within a firm).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    roles = [
        {
            "key": "headquarter",
            "plural": "headquarters",
            "label": "Headquarter",
            "max": 1,
            "doc": "The one establishment that is headquarters to the firm.",
            },
        {
            "key": "secondary",
            "plural": "secondaries",
            "label": "Secondary establishments",
            "doc": "Other establishments in the firm.",
            },
        ],
    )

Establishment = build_entity(
    key = "establishment",
    plural = "establishments",
    label = "An establishment. The minimal legal entity on which a legislation might be applied.",
    doc = """

    Variables like 'wagebill' and 'energyconsumption' are usually defined for the entity 'Establishment'.

    Usage:
    Calculate a variable applied to a 'Establishment' (e.g. access the 'example_salary' of a specific month with establishment("example_salary", "2017-05")).
    Check the role of a 'Establishment' in a group entity (e.g. check if a the 'Establishment' is a 'headquarter' in a 'firm' entity with establishment.has_role(firm.HEADQUARTER)).

    For more information, see: https://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    is_person = True,
    )

entities = [Firm, Establishment]
