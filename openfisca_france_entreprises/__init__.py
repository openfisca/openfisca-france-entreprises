"""
This file defines our country's tax and benefit system.

A tax and benefit system is the higher-level instance in OpenFisca.
Its goal is to model the legislation of a country.
Basically a tax and benefit system contains simulation variables (source code) and legislation parameters (data).

See https://openfisca.org/doc/key-concepts/tax_and_benefit_system.html
"""

import os

# Workaround for enum index overflow: openfisca_core encodes enum indices as uint8
# (0-255), but our NAF enum has 733 members. Indices > 255 overflow (e.g. 555 -> 43).
# Reimplement encoding to use int16 (ENUM_ARRAY_DTYPE) so all indices are preserved.
# We patch both _utils and the enum module, since enum.py does "from _utils import ..."
# at load time and keeps a reference to the original functions.
import numpy as _np
from openfisca_core import indexed_enums
from openfisca_core.taxbenefitsystems import TaxBenefitSystem

_enum_dtype = indexed_enums.ENUM_ARRAY_DTYPE
_utils = indexed_enums._utils  # noqa: SLF001
_enum_module = indexed_enums.enum  # noqa: SLF001


def _str_to_index(enum_class, value):
    values = _np.asarray(value)
    names = enum_class.names
    mask = _np.isin(values, names)
    sorter = _np.argsort(names)
    result = sorter[_np.searchsorted(names, values[mask], sorter=sorter)]
    return result.astype(_enum_dtype)


def _int_to_index(enum_class, value):
    indices = enum_class.indices
    values = _np.asarray(value)
    return values[values < indices.size].astype(_enum_dtype)


def _enum_to_index(value):
    return _np.array([enum.index for enum in value], _enum_dtype)


for _mod in (_utils, _enum_module):
    _mod._str_to_index = _str_to_index
    _mod._int_to_index = _int_to_index
    _mod._enum_to_index = _enum_to_index

from openfisca_france_entreprises import entities
from openfisca_france_entreprises.situation_examples import couple

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


# Our country tax and benefit class inherits from the general TaxBenefitSystem class.
# The name CountryTaxBenefitSystem must not be changed, as all tools of the OpenFisca ecosystem expect a CountryTaxBenefitSystem class to be exposed in the __init__ module of a country package.
class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        # We initialize our tax and benefit system with the general constructor
        super().__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, "variables"))

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = os.path.join(COUNTRY_DIR, "parameters")
        self.load_parameters(param_path)

        # We define which variable, parameter and simulation example will be used in the OpenAPI specification
        self.open_api_config = {
            "variable_example": "apet",
            "parameter_example": "energies.autres_produits_energetiques.major_regionale_ticpe_gazole.ile_france",
            "simulation_example": couple,
        }
