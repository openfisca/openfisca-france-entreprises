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

class tdcfe_coefficient_multiplicateur_prof_moins_36kVA_2015(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.19000	,	#	AIN
        "2":	3.05000	,	#	AISNE
        "3":	3.19000	,	#	ALLIER
        "4":	3.00000	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.17000	,	#	HAUTES-ALPES
        "6":	3.00000	,	#	ALPES-MARITIMES
        "7":	3.19000	,	#	ARDECHE
        "8":	3.19000	,	#	ARDENNES
        "9":	3.19000	,	#	ARIEGE
        "10":	3.19000	,	#	AUBE
        "11":	3.00000	,	#	AUDE
        "12":	3.00000	,	#	AVEYRON
        "13":	3.17000	,	#	BOUCHES-DU-RHONE
        "14":	3.19000	,	#	CALVADOS
        "15":	3.17000	,	#	CANTAL
        "16":	3.00000	,	#	CHARENTE
        "17":	3.19000	,	#	CHARENTE-MARITIME
        "18":	3.17000	,	#	CHER
        "19":	3.19000	,	#	CORREZE
        "21":	3.19000	,	#	COTE-D'OR
        "22":	3.19000	,	#	COTES-D'ARMOR
        "23":	3.19000	,	#	CREUSE
        "24":	3.00000	,	#	DORDOGNE
        "25":	3.05000	,	#	DOUBS
        "26":	3.17000	,	#	DROME
        "27":	3.17000	,	#	EURE
        "28":	3.17000	,	#	EURE-ET-LOIR
        "29":	3.19000	,	#	FINISTERE
        "02A":	3.05000	,	#	CORSE-DU-SUD
        "02B":	3.19000	,	#	HAUTE-CORSE
        "30":	3.00000	,	#	GARD
        "31":	3.19000	,	#	HAUTE-GARONNE
        "32":	3.00000	,	#	GERS
        "33":	3.19000	,	#	GIRONDE
        "34":	3.19000	,	#	HERAULT
        "35":	3.19000	,	#	ILLE-ET-VILAINE
        "36":	3.19000	,	#	INDRE
        "37":	3.19000	,	#	INDRE-ET-LOIRE
        "38":	3.19000	,	#	ISERE
        "39":	3.19000	,	#	JURA
        "40":	3.00000	,	#	LANDES
        "41":	3.17000	,	#	LOIR-ET-CHER
        "42":	3.19000	,	#	LOIRE
        "43":	3.17000	,	#	HAUTE-LOIRE
        "44":	3.19000	,	#	LOIRE-ATLANTIQUE
        "45":	3.19000	,	#	LOIRET
        "46":	3.19000	,	#	LOT
        "47":	3.11000	,	#	LOT-ET-GARONNE
        "48":	3.19000	,	#	LOZERE
        "49":	3.19000	,	#	MAINE-ET-LOIRE
        "50":	3.19000	,	#	MANCHE
        "51":	3.19000	,	#	MARNE
        "52":	3.19000	,	#	HAUTE-MARNE
        "53":	3.15000	,	#	MAYENNE
        "54":	2.25000	,	#	MEURTHE-ET-MOSELLE
        "55":	1.50000	,	#	MEUSE
        "56":	3.05000	,	#	MORBIHAN
        "57":	3.19000	,	#	MOSELLE
        "58":	3.19000	,	#	NIEVRE
        "59":	3.19000	,	#	NORD
        "60":	3.17000	,	#	OISE
        "61":	3.19000	,	#	ORNE
        "62":	3.11000	,	#	PAS-DE-CALAIS
        "63":	3.19000	,	#	PUY-DE-DOME
        "64":	3.19000	,	#	PYRENEES-ATLANTIQUES
        "65":	3.19000	,	#	HAUTES-PYRENEES
        "66":	3.00000	,	#	PYRENEES-ORIENTALES
        "67":	3.19000	,	#	BAS-RHIN
        "68":	3.19000	,	#	HAUT-RHIN
        "69":	3.11000	,	#	RHONE
        #"69":	3.11000	,	#	METROPOLE DE LYON
        "70":	3.19000	,	#	HAUTE-SAONE
        "71":	3.19000	,	#	SAONE-ET-LOIRE
        "72":	3.19000	,	#	SARTHE
        "73":	3.19000	,	#	SAVOIE
        "74":	3.19000	,	#	HAUTE-SAVOIE
        "75":	3.11000	,	#	PARIS
        "76":	3.19000	,	#	SEINE-MARITIME
        "77":	3.19000	,	#	SEINE-ET-MARNE
        "78":	3.00000	,	#	YVELINES
        "79":	3.00000	,	#	DEUX-SEVRES
        "80":	3.17000	,	#	SOMME
        "81":	3.19000	,	#	TARN
        "82":	3.08000	,	#	TARN-ET-GARONNE
        "83":	3.19000	,	#	VAR
        "84":	3.19000	,	#	VAUCLUSE
        "85":	3.19000	,	#	VENDEE
        "86":	3.19000	,	#	VIENNE
        "87":	3.19000	,	#	HAUTE-VIENNE
        "88":	3.05000	,	#	VOSGES
        "89":	3.17000	,	#	YONNE
        "90":	3.17000	,	#	TERRITOIRE DE BELFORT
        "91":	3.19000	,	#	ESSONNE
        "92":	3.19000	,	#	HAUTS-DE-SEINE
        "93":	3.19000	,	#	SEINE-SAINT-DENIS
        "94":	3.19000	,	#	VAL-DE-MARNE
        "95":	3.19000	,	#	VAL-D'OISE
        "101":	3.17000	,	#	GUADELOUPE
        "102":	3.00000	,	#	GUYANE
        "103":	3.00000	,	#	MARTINIQUE
        "104":	3.05000	,	#	LA REUNION
        "106":	3.19000	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
    
class tdcfe_coefficient_multiplicateur_prof_plus_36_moins_250kVA_2015(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	1.06000	,	#	AIN
        "2":	1.02000	,	#	AISNE
        "3":	1.06000	,	#	ALLIER
        "4":	1.00000	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	1.06000	,	#	HAUTES-ALPES
        "6":	1.00000	,	#	ALPES-MARITIMES
        "7":	1.06000	,	#	ARDECHE
        "8":	1.06000	,	#	ARDENNES
        "9":	1.06000	,	#	ARIEGE
        "10":	1.06000	,	#	AUBE
        "11":	1.00000	,	#	AUDE
        "12":	1.00000	,	#	AVEYRON
        "13":	1.06000	,	#	BOUCHES-DU-RHONE
        "14":	1.06000	,	#	CALVADOS
        "15":	1.06000	,	#	CANTAL
        "16":	1.00000	,	#	CHARENTE
        "17":	1.06000	,	#	CHARENTE-MARITIME
        "18":	1.06000	,	#	CHER
        "19":	1.06000	,	#	CORREZE
        "21":	1.06000	,	#	COTE-D'OR
        "22":	1.06000	,	#	COTES-D'ARMOR
        "23":	1.06000	,	#	CREUSE
        "24":	1.00000	,	#	DORDOGNE
        "25":	1.02000	,	#	DOUBS
        "26":	1.06000	,	#	DROME
        "27":	1.06000	,	#	EURE
        "28":	1.06000	,	#	EURE-ET-LOIR
        "29":	1.06000	,	#	FINISTERE
        "02A":	1.02000	,	#	CORSE-DU-SUD
        "02B":	1.06000	,	#	HAUTE-CORSE
        "30":	1.00000	,	#	GARD
        "31":	1.06000	,	#	HAUTE-GARONNE
        "32":	1.00000	,	#	GERS
        "33":	1.06000	,	#	GIRONDE
        "34":	1.06000	,	#	HERAULT
        "35":	1.06000	,	#	ILLE-ET-VILAINE
        "36":	1.06000	,	#	INDRE
        "37":	1.06000	,	#	INDRE-ET-LOIRE
        "38":	1.06000	,	#	ISERE
        "39":	1.06000	,	#	JURA
        "40":	1.00000	,	#	LANDES
        "41":	1.06000	,	#	LOIR-ET-CHER
        "42":	1.06000	,	#	LOIRE
        "43":	1.06000	,	#	HAUTE-LOIRE
        "44":	1.06000	,	#	LOIRE-ATLANTIQUE
        "45":	1.06000	,	#	LOIRET
        "46":	1.06000	,	#	LOT
        "47":	1.04000	,	#	LOT-ET-GARONNE
        "48":	1.06000	,	#	LOZERE
        "49":	1.06000	,	#	MAINE-ET-LOIRE
        "50":	1.06000	,	#	MANCHE
        "51":	1.06000	,	#	MARNE
        "52":	1.06000	,	#	HAUTE-MARNE
        "53":	1.05000	,	#	MAYENNE
        "54":	0.75000	,	#	MEURTHE-ET-MOSELLE
        "55":	0.50000	,	#	MEUSE
        "56":	1.02000	,	#	MORBIHAN
        "57":	1.06000	,	#	MOSELLE
        "58":	1.06000	,	#	NIEVRE
        "59":	1.06000	,	#	NORD
        "60":	1.06000	,	#	OISE
        "61":	1.06000	,	#	ORNE
        "62":	1.04000	,	#	PAS-DE-CALAIS
        "63":	1.06000	,	#	PUY-DE-DOME
        "64":	1.06000	,	#	PYRENEES-ATLANTIQUES
        "65":	1.06000	,	#	HAUTES-PYRENEES
        "66":	1.00000	,	#	PYRENEES-ORIENTALES
        "67":	1.06000	,	#	BAS-RHIN
        "68":	1.06000	,	#	HAUT-RHIN
        "69":	1.04000	,	#	RHONE
        "69":	1.04000	,	#	METROPOLE DE LYON
        "70":	1.06000	,	#	HAUTE-SAONE
        "71":	1.06000	,	#	SAONE-ET-LOIRE
        "72":	1.06000	,	#	SARTHE
        "73":	1.06000	,	#	SAVOIE
        "74":	1.06000	,	#	HAUTE-SAVOIE
        "75":	1.04000	,	#	PARIS
        "76":	1.06000	,	#	SEINE-MARITIME
        "77":	1.06000	,	#	SEINE-ET-MARNE
        "78":	1.00000	,	#	YVELINES
        "79":	1.00000	,	#	DEUX-SEVRES
        "80":	1.06000	,	#	SOMME
        "81":	1.06000	,	#	TARN
        "82":	1.03000	,	#	TARN-ET-GARONNE
        "83":	1.06000	,	#	VAR
        "84":	1.06000	,	#	VAUCLUSE
        "85":	1.06000	,	#	VENDEE
        "86":	1.06000	,	#	VIENNE
        "87":	1.06000	,	#	HAUTE-VIENNE
        "88":	1.02000	,	#	VOSGES
        "89":	1.06000	,	#	YONNE
        "90":	1.06000	,	#	TERRITOIRE DE BELFORT
        "91":	1.06000	,	#	ESSONNE
        "92":	1.06000	,	#	HAUTS-DE-SEINE
        "93":	1.06000	,	#	SEINE-SAINT-DENIS
        "94":	1.06000	,	#	VAL-DE-MARNE
        "95":	1.06000	,	#	VAL-D'OISE
        "101":	1.06000	,	#	GUADELOUPE
        "102":	1.00000	,	#	GUYANE
        "103":	1.00000	,	#	MARTINIQUE
        "104":	1.02000	,	#	LA REUNION
        "106":	1.06000	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_non_prof_moins_250kVA_2015(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.19000	,	#	AIN
        "2":	3.05000	,	#	AISNE
        "3":	3.19000	,	#	ALLIER
        "4":	3.00000	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.17000	,	#	HAUTES-ALPES
        "6":	3.00000	,	#	ALPES-MARITIMES
        "7":	3.19000	,	#	ARDECHE
        "8":	3.19000	,	#	ARDENNES
        "9":	3.19000	,	#	ARIEGE
        "10":	3.19000	,	#	AUBE
        "11":	3.00000	,	#	AUDE
        "12":	3.00000	,	#	AVEYRON
        "13":	3.17000	,	#	BOUCHES-DU-RHONE
        "14":	3.19000	,	#	CALVADOS
        "15":	3.17000	,	#	CANTAL
        "16":	3.00000	,	#	CHARENTE
        "17":	3.19000	,	#	CHARENTE-MARITIME
        "18":	3.17000	,	#	CHER
        "19":	3.19000	,	#	CORREZE
        "21":	3.19000	,	#	COTE-D'OR
        "22":	3.19000	,	#	COTES-D'ARMOR
        "23":	3.19000	,	#	CREUSE
        "24":	3.00000	,	#	DORDOGNE
        "25":	3.05000	,	#	DOUBS
        "26":	3.17000	,	#	DROME
        "27":	3.17000	,	#	EURE
        "28":	3.17000	,	#	EURE-ET-LOIR
        "29":	3.19000	,	#	FINISTERE
        "02A":	3.05000	,	#	CORSE-DU-SUD
        "02B":	3.19000	,	#	HAUTE-CORSE
        "30":	3.00000	,	#	GARD
        "31":	3.19000	,	#	HAUTE-GARONNE
        "32":	3.00000	,	#	GERS
        "33":	3.19000	,	#	GIRONDE
        "34":	3.19000	,	#	HERAULT
        "35":	3.19000	,	#	ILLE-ET-VILAINE
        "36":	3.19000	,	#	INDRE
        "37":	3.19000	,	#	INDRE-ET-LOIRE
        "38":	3.19000	,	#	ISERE
        "39":	3.19000	,	#	JURA
        "40":	3.00000	,	#	LANDES
        "41":	3.17000	,	#	LOIR-ET-CHER
        "42":	3.19000	,	#	LOIRE
        "43":	3.17000	,	#	HAUTE-LOIRE
        "44":	3.19000	,	#	LOIRE-ATLANTIQUE
        "45":	3.19000	,	#	LOIRET
        "46":	3.19000	,	#	LOT
        "47":	3.11000	,	#	LOT-ET-GARONNE
        "48":	3.19000	,	#	LOZERE
        "49":	3.19000	,	#	MAINE-ET-LOIRE
        "50":	3.19000	,	#	MANCHE
        "51":	3.19000	,	#	MARNE
        "52":	3.19000	,	#	HAUTE-MARNE
        "53":	3.15000	,	#	MAYENNE
        "54":	2.25000	,	#	MEURTHE-ET-MOSELLE
        "55":	1.50000	,	#	MEUSE
        "56":	3.05000	,	#	MORBIHAN
        "57":	3.19000	,	#	MOSELLE
        "58":	3.19000	,	#	NIEVRE
        "59":	3.19000	,	#	NORD
        "60":	3.17000	,	#	OISE
        "61":	3.19000	,	#	ORNE
        "62":	3.11000	,	#	PAS-DE-CALAIS
        "63":	3.19000	,	#	PUY-DE-DOME
        "64":	3.19000	,	#	PYRENEES-ATLANTIQUES
        "65":	3.19000	,	#	HAUTES-PYRENEES
        "66":	3.00000	,	#	PYRENEES-ORIENTALES
        "67":	3.19000	,	#	BAS-RHIN
        "68":	3.19000	,	#	HAUT-RHIN
        "69":	3.11000	,	#	RHONE
        #"69":	3.11000	,	#	METROPOLE DE LYON
        "70":	3.19000	,	#	HAUTE-SAONE
        "71":	3.19000	,	#	SAONE-ET-LOIRE
        "72":	3.19000	,	#	SARTHE
        "73":	3.19000	,	#	SAVOIE
        "74":	3.19000	,	#	HAUTE-SAVOIE
        "75":	3.11000	,	#	PARIS
        "76":	3.19000	,	#	SEINE-MARITIME
        "77":	3.19000	,	#	SEINE-ET-MARNE
        "78":	3.00000	,	#	YVELINES
        "79":	3.00000	,	#	DEUX-SEVRES
        "80":	3.17000	,	#	SOMME
        "81":	3.19000	,	#	TARN
        "82":	3.08000	,	#	TARN-ET-GARONNE
        "83":	3.19000	,	#	VAR
        "84":	3.19000	,	#	VAUCLUSE
        "85":	3.19000	,	#	VENDEE
        "86":	3.19000	,	#	VIENNE
        "87":	3.19000	,	#	HAUTE-VIENNE
        "88":	3.05000	,	#	VOSGES
        "89":	3.17000	,	#	YONNE
        "90":	3.17000	,	#	TERRITOIRE DE BELFORT
        "91":	3.19000	,	#	ESSONNE
        "92":	3.19000	,	#	HAUTS-DE-SEINE
        "93":	3.19000	,	#	SEINE-SAINT-DENIS
        "94":	3.19000	,	#	VAL-DE-MARNE
        "95":	3.19000	,	#	VAL-D'OISE
        "101":	3.17000	,	#	GUADELOUPE
        "102":	3.00000	,	#	GUYANE
        "103":	3.00000	,	#	MARTINIQUE
        "104":	3.05000	,	#	LA REUNION
        "106":	3.19000	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

