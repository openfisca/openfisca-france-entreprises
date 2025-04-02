# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement
#NB : le code départementale de Mayotte change de 143 en 2014 à 106 en 2015

class tdcfe_coefficient_multiplicateur_normal_2015(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	4.250000	,	#	AIN
        "2":	4.060000	,	#	AISNE
        "3":	4.250000	,	#	ALLIER
        "4":	4.000000	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	4.220000	,	#	HAUTES-ALPES
        "6":	4.000000	,	#	ALPES-MARITIMES
        "7":	4.250000	,	#	ARDECHE
        "8":	4.250000	,	#	ARDENNES
        "9":	4.250000	,	#	ARIEGE
        "10":	4.250000	,	#	AUBE
        "11":	4.000000	,	#	AUDE
        "12":	4.000000	,	#	AVEYRON
        "13":	4.220000	,	#	BOUCHES-DU-RHONE
        "14":	4.250000	,	#	CALVADOS
        "15":	4.220000	,	#	CANTAL
        "16":	4.000000	,	#	CHARENTE
        "17":	4.250000	,	#	CHARENTE-MARITIME
        "18":	4.220000	,	#	CHER
        "19":	4.250000	,	#	CORREZE
        "21":	4.250000	,	#	COTE-D'OR
        "22":	4.250000	,	#	COTES-D'ARMOR
        "23":	4.250000	,	#	CREUSE
        "24":	4.000000	,	#	DORDOGNE
        "25":	4.060000	,	#	DOUBS
        "26":	4.220000	,	#	DROME
        "27":	4.220000	,	#	EURE
        "28":	4.220000	,	#	EURE-ET-LOIR
        "29":	4.250000	,	#	FINISTERE
        "02A":	4.060000	,	#	CORSE-DU-SUD
        "02B":	4.250000	,	#	HAUTE-CORSE
        "30":	4.000000	,	#	GARD
        "31":	4.250000	,	#	HAUTE-GARONNE
        "32":	4.000000	,	#	GERS
        "33":	4.250000	,	#	GIRONDE
        "34":	4.250000	,	#	HERAULT
        "35":	4.250000	,	#	ILLE-ET-VILAINE
        "36":	4.250000	,	#	INDRE
        "37":	4.250000	,	#	INDRE-ET-LOIRE
        "38":	4.250000	,	#	ISERE
        "39":	4.250000	,	#	JURA
        "40":	4.000000	,	#	LANDES
        "41":	4.220000	,	#	LOIR-ET-CHER
        "42":	4.250000	,	#	LOIRE
        "43":	4.220000	,	#	HAUTE-LOIRE
        "44":	4.250000	,	#	LOIRE-ATLANTIQUE
        "45":	4.250000	,	#	LOIRET
        "46":	4.250000	,	#	LOT
        "47":	4.140000	,	#	LOT-ET-GARONNE
        "48":	4.250000	,	#	LOZERE
        "49":	4.250000	,	#	MAINE-ET-LOIRE
        "50":	4.250000	,	#	MANCHE
        "51":	4.250000	,	#	MARNE
        "52":	4.250000	,	#	HAUTE-MARNE
        "53":	4.200000	,	#	MAYENNE
        "54":	3.000000	,	#	MEURTHE-ET-MOSELLE
        "55":	2.000000	,	#	MEUSE
        "56":	4.060000	,	#	MORBIHAN
        "57":	4.250000	,	#	MOSELLE
        "58":	4.250000	,	#	NIEVRE
        "59":	4.250000	,	#	NORD
        "60":	4.220000	,	#	OISE
        "61":	4.250000	,	#	ORNE
        "62":	4.140000	,	#	PAS-DE-CALAIS
        "63":	4.250000	,	#	PUY-DE-DOME
        "64":	4.250000	,	#	PYRENEES-ATLANTIQUES
        "65":	4.250000	,	#	HAUTES-PYRENEES
        "66":	4.000000	,	#	PYRENEES-ORIENTALES
        "67":	4.250000	,	#	BAS-RHIN
        "68":	4.250000	,	#	HAUT-RHIN
        "69":	4.140000	,	#	RHONE
        #"69":	4.140000	,	#	METROPOLE DE LYON
        "70":	4.250000	,	#	HAUTE-SAONE
        "71":	4.250000	,	#	SAONE-ET-LOIRE
        "72":	4.250000	,	#	SARTHE
        "73":	4.250000	,	#	SAVOIE
        "74":	4.250000	,	#	HAUTE-SAVOIE
        "75":	4.140000	,	#	PARIS
        "76":	4.250000	,	#	SEINE-MARITIME
        "77":	4.250000	,	#	SEINE-ET-MARNE
        "78":	4.000000	,	#	YVELINES
        "79":	4.000000	,	#	DEUX-SEVRES
        "80":	4.220000	,	#	SOMME
        "81":	4.250000	,	#	TARN
        "82":	4.100000	,	#	TARN-ET-GARONNE
        "83":	4.250000	,	#	VAR
        "84":	4.250000	,	#	VAUCLUSE
        "85":	4.250000	,	#	VENDEE
        "86":	4.250000	,	#	VIENNE
        "87":	4.250000	,	#	HAUTE-VIENNE
        "88":	4.060000	,	#	VOSGES
        "89":	4.220000	,	#	YONNE
        "90":	4.220000	,	#	TERRITOIRE DE BELFORT
        "91":	4.250000	,	#	ESSONNE
        "92":	4.250000	,	#	HAUTS-DE-SEINE
        "93":	4.250000	,	#	SEINE-SAINT-DENIS
        "94":	4.250000	,	#	VAL-DE-MARNE
        "95":	4.250000	,	#	VAL-D'OISE
        "101":	4.220000	,	#	GUADELOUPE
        "102":	4.000000	,	#	GUYANE
        "103":	4.000000	,	#	MARTINIQUE
        "104":	4.060000	,	#	LA REUNION
        "106":	4.250000	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
