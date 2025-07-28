# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class tdcfe_coefficient_multiplicateur_normal_2014(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	4.22	,	#	AIN
        "2":	4.06	,	#	AISNE
        "3":	4.22	,	#	ALLIER
        "4":	4	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	4.22	,	#	HAUTES-ALPES
        "6":	4	,	#	ALPES-MARITIMES
        "7":	4.22	,	#	ARDECHE
        "8":	4.06	,	#	ARDENNES
        "9":	4.22	,	#	ARIEGE
        "10":	4.22	,	#	AUBE
        "11":	4	,	#	AUDE
        "12":	4	,	#	AVEYRON
        "13":	4.22	,	#	BOUCHES-DU-RHONE
        "14":	4.22	,	#	CALVADOS
        "15":	4.22	,	#	CANTAL
        "16":	4	,	#	CHARENTE
        "17":	4.22	,	#	CHARENTE-MARITIME
        "18":	4.22	,	#	CHER
        "19":	4.22	,	#	CORREZE
        "21":	4.22	,	#	COTE-D'OR
        "22":	4.14	,	#	COTES-D'ARMOR
        "23":	4.22	,	#	CREUSE
        "24":	4	,	#	DORDOGNE
        "25":	4.06	,	#	DOUBS
        "26":	4.22	,	#	DROME
        "27":	4.22	,	#	EURE
        "28":	4.14	,	#	EURE-ET-LOIR
        "29":	4.22	,	#	FINISTERE
        "02A":	4.06	,	#	CORSE-DU-SUD
        "02B":	4.14	,	#	HAUTE-CORSE
        "30":	4	,	#	GARD
        "31":	4.22	,	#	HAUTE-GARONNE
        "32":	4	,	#	GERS
        "33":	4.22	,	#	GIRONDE
        "34":	4.22	,	#	HERAULT
        "35":	4.22	,	#	ILLE-ET-VILAINE
        "36":	4.22	,	#	INDRE
        "37":	4.22	,	#	INDRE-ET-LOIRE
        "38":	4.22	,	#	ISERE
        "39":	4.22	,	#	JURA
        "40":	4	,	#	LANDES
        "41":	4.14	,	#	LOIR-ET-CHER
        "42":	4.22	,	#	LOIRE
        "43":	4.22	,	#	HAUTE-LOIRE
        "44":	4.22	,	#	LOIRE-ATLANTIQUE
        "45":	4.22	,	#	LOIRET
        "46":	4.22	,	#	LOT
        "47":	4.14	,	#	LOT-ET-GARONNE
        "48":	4.22	,	#	LOZERE
        "49":	4.22	,	#	MAINE-ET-LOIRE
        "50":	4.22	,	#	MANCHE
        "51":	4.22	,	#	MARNE
        "52":	4.22	,	#	HAUTE-MARNE
        "53":	4.2	,	#	MAYENNE
        "54":	3	,	#	MEURTHE-ET-MOSELLE
        "55":	2	,	#	MEUSE
        "56":	4.06	,	#	MORBIHAN
        "57":	4.22	,	#	MOSELLE
        "58":	4.14	,	#	NIEVRE
        "59":	4.22	,	#	NORD
        "60":	4.22	,	#	OISE
        "61":	4.22	,	#	ORNE
        "62":	4.14	,	#	PAS-DE-CALAIS
        "63":	4.22	,	#	PUY-DE-DOME
        "64":	4.22	,	#	PYRENEES-ATLANTIQUES
        "65":	4	,	#	HAUTES-PYRENEES
        "66":	4	,	#	PYRENEES-ORIENTALES
        "67":	4.22	,	#	BAS-RHIN
        "68":	4.22	,	#	HAUT-RHIN
        "69":	4.14	,	#	RHONE
        "70":	4.22	,	#	HAUTE-SAONE
        "71":	4.22	,	#	SAONE-ET-LOIRE
        "72":	4.22	,	#	SARTHE
        "73":	4.22	,	#	SAVOIE
        "74":	4.22	,	#	HAUTE-SAVOIE
        "75":	4.14	,	#	PARIS
        "76":	4.22	,	#	SEINE-MARITIME
        "77":	4.22	,	#	SEINE-ET-MARNE
        "78":	4	,	#	YVELINES
        "79":	4	,	#	DEUX-SEVRES
        "80":	4.22	,	#	SOMME
        "81":	4.22	,	#	TARN
        "82":	4.1	,	#	TARN-ET-GARONNE
        "83":	4.22	,	#	VAR
        "84":	4.22	,	#	VAUCLUSE
        "85":	4.22	,	#	VENDEE
        "86":	4	,	#	VIENNE
        "87":	4.22	,	#	HAUTE-VIENNE
        "88":	4.06	,	#	VOSGES
        "89":	4.22	,	#	YONNE
        "90":	4.22	,	#	TERRITOIRE DE BELFORT
        "91":	4.22	,	#	ESSONNE
        "92":	4.22	,	#	HAUTS-DE-SEINE
        "93":	4.14	,	#	SEINE-SAINT-DENIS
        "94":	4.14	,	#	VAL-DE-MARNE
        "95":	4.22	,	#	VAL-D'OISE
        "101":	4.22	,	#	GUADELOUPE
        "102":	4	,	#	GUYANE
        "103":	4	,	#	MARTINIQUE
        "104":	4.06	,	#	LA REUNION
        "143":	8	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
