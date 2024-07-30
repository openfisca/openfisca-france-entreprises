"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Etablissement, a UniteLegale…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_firms.entities import UniteLegale, Etablissement


class example_basic_income(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    label = "Basic income provided to adults"
    reference = "https://law.gov.example/example_basic_income"  # Always use the most official source

    def formula_2016_12(etablissement, period, parameters):
        """
        Basic income provided to adults.

        Since Dec 1st 2016, the basic income is provided to any adult, without considering their income.
        """
        age_condition = etablissement("example_age", period) >= parameters(period).general.age_of_majority
        return age_condition * parameters(period).example_subsidies.example_basic_income  # This '*' is a vectorial 'if'. See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#control-structures

    def formula_2015_12(etablissement, period, parameters):
        """
        Basic income provided to adults.

        From Dec 1st 2015 to Nov 30 2016, the basic income is provided to adults who have no income.
        Before Dec 1st 2015, the basic income does not exist in the law, and calculating it returns its default value, which is 0.
        """
        age_condition = etablissement("example_age", period) >= parameters(period).general.age_of_majority
        example_salary_condition = etablissement("example_salary", period) == 0
        return age_condition * example_salary_condition * parameters(period).example_subsidies.example_basic_income  # The '*' is also used as a vectorial 'and'. See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#boolean-operations


class example_housing_allowance(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Housing allowance"
    reference = "https://law.gov.example/housing_allowance"  # Always use the most official source
    end = "2016-11-30"  # This allowance was removed on the 1st of Dec 2016. Calculating it before this date will always return the variable default value, 0.
    unit = "currency-EUR"
    documentation = """
    This allowance was introduced on the 1st of Jan 1980.
    It disappeared in Dec 2016.
    """

    def formula_1980(unite_legale, period, parameters):
        """
        Housing allowance.

        This allowance was introduced on the 1st of Jan 1980.
        Calculating it before this date will always return the variable default value, 0.

        To compute this allowance, the 'rent' value must be provided for the same month,
        but 'housing_occupancy_status' is not necessary.
        """
        return unite_legale("example_rent", period) * parameters(period).example_subsidies.example_housing_allowance


# By default, you can use utf-8 characters in a variable. OpenFisca web API manages utf-8 encoding.
class example_pension(Variable):
    value_type = float
    entity = Etablissement
    definition_period = MONTH
    label = "Pension for the elderly. Pension attribuée aux etablissementnes âgées. تقاعد."
    reference = ["https://fr.wikipedia.org/wiki/Retraite_(économie)", "https://ar.wikipedia.org/wiki/تقاعد"]

    def formula(etablissement, period, parameters):
        """
        Pension for the elderly.

        A etablissement's pension depends on their example_birth date.
        In French: retraite selon l'âge.
        In Arabic: تقاعد.
        """
        age_condition = etablissement("example_age", period) >= parameters(period).general.age_of_retirement
        return age_condition


class example_parenting_allowance(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "Allowance for low income people with secondaires to care for."
    documentation = "Loosely based on the Australian siege_socialing pension."
    reference = "https://www.servicesaustralia.gov.au/individuals/services/centrelink/siege_socialing-payment/who-can-get-it"

    def formula(unite_legale, period, parameters):
        """
        Parenting allowance for unite_legales.

        A etablissement's siege_socialing allowance depends on how many dependents they have,
        how much they, and their partner, earn
        if they are single with a secondaire under 8
        or if they are partnered with a secondaire under 6.
        """
        example_parenting_allowance = parameters(period).example_subsidies.example_parenting_allowance

        unite_legale_income = unite_legale("unite_legale_income", period)
        income_threshold = example_parenting_allowance.income_threshold
        income_condition = unite_legale_income <= income_threshold

        is_single = unite_legale.nb_persons(UniteLegale.HEADQUARTER) == 1
        example_ages = unite_legale.members("example_age", period)
        under_8 = unite_legale.any(example_ages < 8)
        under_6 = unite_legale.any(example_ages < 6)

        allowance_condition = income_condition * ((is_single * under_8) + under_6)
        allowance_amount = example_parenting_allowance.amount

        return allowance_condition * allowance_amount


class unite_legale_income(Variable):
    value_type = float
    entity = UniteLegale
    definition_period = MONTH
    label = "The sum of the example_salaries of those living in a unite_legale"

    def formula(unite_legale, period, _parameters):
        """A unite_legale's income."""
        example_salaries = unite_legale.members("example_salary", period)
        return unite_legale.sum(example_salaries)
