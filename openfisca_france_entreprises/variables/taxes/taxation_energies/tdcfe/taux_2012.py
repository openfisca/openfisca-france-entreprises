# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class tdcfe_coefficient_multiplicateur_normal_2012(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	4.06	,	#	AIN
        "2":	4.06	,	#	AISNE
        "3":	4.06	,	#	ALLIER
        "4":	4	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	4	,	#	HAUTES-ALPES
        "6":	4	,	#	ALPES-MARITIMES
        "7":	4	,	#	ARDECHE
        "8":	4.06	,	#	ARDENNES
        "9":	4	,	#	ARIEGE
        "10":	4.06	,	#	AUBE
        "11":	4	,	#	AUDE
        "12":	4	,	#	AVEYRON
        "13":	4	,	#	BOUCHES-DU-RHONE
        "14":	4.06	,	#	CALVADOS
        "15":	4.06	,	#	CANTAL
        "16":	4	,	#	CHARENTE
        "17":	4	,	#	CHARENTE-MARITIME
        "18":	4	,	#	CHER
        "19":	4	,	#	CORREZE
        "21":	4.06	,	#	COTE-D'OR
        "22":	4.06	,	#	COTES-D'ARMOR
        "23":	4.06	,	#	CREUSE
        "24":	4	,	#	DORDOGNE
        "25":	4.06	,	#	DOUBS
        "26":	4.06	,	#	DROME
        "27":	4	,	#	EURE
        "28":	4	,	#	EURE-ET-LOIR
        "29":	4.06	,	#	FINISTERE
        "02A":	4.06	,	#	CORSE-DU-SUD
        "02B":	4	,	#	HAUTE-CORSE
        "30":	4	,	#	GARD
        "31":	4.06	,	#	HAUTE-GARONNE
        "32":	4	,	#	GERS
        "33":	4	,	#	GIRONDE
        "34":	4.06	,	#	HERAULT
        "35":	4.06	,	#	ILLE-ET-VILAINE
        "36":	4.06	,	#	INDRE
        "37":	4.06	,	#	INDRE-ET-LOIRE
        "38":	4.06	,	#	ISERE
        "39":	4	,	#	JURA
        "40":	4	,	#	LANDES
        "41":	4	,	#	LOIR-ET-CHER
        "42":	4.06	,	#	LOIRE
        "43":	4	,	#	HAUTE-LOIRE
        "44":	4	,	#	LOIRE-ATLANTIQUE
        "45":	4.06	,	#	LOIRET
        "46":	4.06	,	#	LOT
        "47":	4.06	,	#	LOT-ET-GARONNE
        "48":	4.06	,	#	LOZERE
        "49":	4.06	,	#	MAINE-ET-LOIRE
        "50":	4.06	,	#	MANCHE
        "51":	4.06	,	#	MARNE
        "52":	4.06	,	#	HAUTE-MARNE
        "53":	4.06	,	#	MAYENNE
        "54":	3	,	#	MEURTHE-ET-MOSELLE
        "55":	2	,	#	MEUSE
        "56":	4.06	,	#	MORBIHAN
        "57":	4.06	,	#	MOSELLE
        "58":	4	,	#	NIEVRE
        "59":	4.06	,	#	NORD
        "60":	4	,	#	OISE
        "61":	4.06	,	#	ORNE
        "62":	4	,	#	PAS-DE-CALAIS
        "63":	4.06	,	#	PUY-DE-DOME
        "64":	4	,	#	PYRENEES-ATLANTIQUES
        "65":	4	,	#	HAUTES-PYRENEES
        "66":	4	,	#	PYRENEES-ORIENTALES
        "67":	4	,	#	BAS-RHIN
        "68":	4	,	#	HAUT-RHIN
        "69":	4.06	,	#	RHONE
        "70":	4.06	,	#	HAUTE-SAONE
        "71":	4	,	#	SAONE-ET-LOIRE
        "72":	4.06	,	#	SARTHE
        "73":	4.06	,	#	SAVOIE
        "74":	4.06	,	#	HAUTE-SAVOIE
        "75":	4.06	,	#	PARIS
        "76":	4	,	#	SEINE-MARITIME
        "77":	4.06	,	#	SEINE-ET-MARNE
        "78":	4	,	#	YVELINES
        "79":	4	,	#	DEUX-SEVRES
        "80":	4.06	,	#	SOMME
        "81":	4.06	,	#	TARN
        "82":	4.06	,	#	TARN-ET-GARONNE
        "83":	4	,	#	VAR
        "84":	4	,	#	VAUCLUSE
        "85":	4.06	,	#	VENDEE
        "86":	4	,	#	VIENNE
        "87":	4.06	,	#	HAUTE-VIENNE
        "88":	4.06	,	#	VOSGES
        "89":	4.06	,	#	YONNE
        "90":	4	,	#	TERRITOIRE DE BELFORT
        "91":	4	,	#	ESSONNE
        "92":	4	,	#	HAUTS-DE-SEINE
        "93":	4.06	,	#	SEINE-SAINT-DENIS
        "94":	4.06	,	#	VAL-DE-MARNE
        "95":	4.06	,	#	VAL-D'OISE
        "101":	4	,	#	GUADELOUPE
        "102":	4	,	#	GUYANE
        "103":	4	,	#	MARTINIQUE
        "104":	4.06	,	#	LA REUNION
        "143":	8	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
