# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement
#NB : le code départementale de Mayotte change de 143 en 2014 à 106 en 2015

class tdcfe_coefficient_multiplicateur_normal_2017(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	4.25	,	#	AIN
        "2":	4.25	,	#	AISNE
        "3":	4.25	,	#	ALLIER
        "4":	4	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	4.25	,	#	HAUTES-ALPES
        "6":	4	,	#	ALPES-MARITIMES
        "7":	4.25	,	#	ARDECHE
        "8":	4.25	,	#	ARDENNES
        "9":	4.25	,	#	ARIEGE
        "10":	4.25	,	#	AUBE
        "11":	4	,	#	AUDE
        "12":	4	,	#	AVEYRON
        "13":	4.25	,	#	BOUCHES-DU-RHONE
        "14":	4.25	,	#	CALVADOS
        "15":	4.25	,	#	CANTAL
        "16":	4	,	#	CHARENTE
        "17":	4.25	,	#	CHARENTE-MARITIME
        "18":	4.25	,	#	CHER
        "19":	4.25	,	#	CORREZE
        "21":	4.25	,	#	COTE-D'OR
        "22":	4.25	,	#	COTES-D'ARMOR
        "23":	4.25	,	#	CREUSE
        "24":	4	,	#	DORDOGNE
        "25":	4.25	,	#	DOUBS
        "26":	4.25	,	#	DROME
        "27":	4.25	,	#	EURE
        "28":	4.25	,	#	EURE-ET-LOIR
        "29":	4.25	,	#	FINISTERE
        "02A":	4	,	#	CORSE-DU-SUD
        "02B":	4.25	,	#	HAUTE-CORSE
        "30":	4	,	#	GARD
        "31":	4.25	,	#	HAUTE-GARONNE
        "32":	4.25	,	#	GERS
        "33":	4.25	,	#	GIRONDE
        "34":	4.25	,	#	HERAULT
        "35":	4.25	,	#	ILLE-ET-VILAINE
        "36":	4.25	,	#	INDRE
        "37":	4.25	,	#	INDRE-ET-LOIRE
        "38":	4.25	,	#	ISERE
        "39":	4.25	,	#	JURA
        "40":	4	,	#	LANDES
        "41":	4.25	,	#	LOIR-ET-CHER
        "42":	4.25	,	#	LOIRE
        "43":	4.25	,	#	HAUTE-LOIRE
        "44":	4.25	,	#	LOIRE-ATLANTIQUE
        "45":	4.25	,	#	LOIRET
        "46":	4.25	,	#	LOT
        "47":	4.25	,	#	LOT-ET-GARONNE
        "48":	4.25	,	#	LOZERE
        "49":	4.25	,	#	MAINE-ET-LOIRE
        "50":	4.25	,	#	MANCHE
        "51":	4.25	,	#	MARNE
        "52":	4.25	,	#	HAUTE-MARNE
        "53":	4.25	,	#	MAYENNE
        "54":	4	,	#	MEURTHE-ET-MOSELLE
        "55":	4.25	,	#	MEUSE
        "56":	4	,	#	MORBIHAN
        "57":	4.25	,	#	MOSELLE
        "58":	4.25	,	#	NIEVRE
        "59":	4.25	,	#	NORD
        "60":	4.25	,	#	OISE
        "61":	4.25	,	#	ORNE
        "62":	4.25	,	#	PAS-DE-CALAIS
        "63":	4.25	,	#	PUY-DE-DOME
        "64":	4.25	,	#	PYRENEES-ATLANTIQUES
        "65":	4.25	,	#	HAUTES-PYRENEES
        "66":	4	,	#	PYRENEES-ORIENTALES
        "67":	4.25	,	#	BAS-RHIN
        "68":	4.25	,	#	HAUT-RHIN
        "69":	4.25	,	#	RHONE
        #"69":	4.25	,	#	METROPOLE DE LYON
        "70":	4.25	,	#	HAUTE-SAONE
        "71":	4.25	,	#	SAONE-ET-LOIRE
        "72":	4.25	,	#	SARTHE
        "73":	4.25	,	#	SAVOIE
        "74":	4.25	,	#	HAUTE-SAVOIE
        "75":	4.25	,	#	PARIS
        "76":	4.25	,	#	SEINE-MARITIME
        "77":	4.25	,	#	SEINE-ET-MARNE
        "78":	4.25	,	#	YVELINES
        "79":	4.25	,	#	DEUX-SEVRES
        "80":	4.25	,	#	SOMME
        "81":	4.25	,	#	TARN
        "82":	4.25	,	#	TARN-ET-GARONNE
        "83":	4.25	,	#	VAR
        "84":	4.25	,	#	VAUCLUSE
        "85":	4.25	,	#	VENDEE
        "86":	4.25	,	#	VIENNE
        "87":	4.25	,	#	HAUTE-VIENNE
        "88":	4.25	,	#	VOSGES
        "89":	4.25	,	#	YONNE
        "90":	4.25	,	#	TERRITOIRE DE BELFORT
        "91":	4.25	,	#	ESSONNE
        "92":	4.25	,	#	HAUTS-DE-SEINE
        "93":	4.25	,	#	SEINE-SAINT-DENIS
        "94":	4.25	,	#	VAL-DE-MARNE
        "95":	4.25	,	#	VAL-D'OISE
        "101":	4.25	,	#	GUADELOUPE
        "102":	4	,	#	GUYANE
        "103":	4	,	#	MARTINIQUE
        "104":	4.25	,	#	LA REUNION
        "106":	4.25	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
