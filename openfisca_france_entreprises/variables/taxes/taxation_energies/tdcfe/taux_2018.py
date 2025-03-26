# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement
#NB : le code départementale de Mayotte change de 143 en 2014 à 106 en 2015

class tdcfe_coefficient_multiplicateur_normal_2018(Variable):
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

class tdcfe_coefficient_multiplicateur_prof_moins_36kVA_2018(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.1875	,	#	AIN
        "2":	3.1875	,	#	AISNE
        "3":	3.1875	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.1875	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.1875	,	#	ARDECHE
        "8":	3.1875	,	#	ARDENNES
        "9":	3.1875	,	#	ARIEGE
        "10":	3.1875	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.1875	,	#	BOUCHES-DU-RHONE
        "14":	3.1875	,	#	CALVADOS
        "15":	3.1875	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3.1875	,	#	CHARENTE-MARITIME
        "18":	3.1875	,	#	CHER
        "19":	3.1875	,	#	CORREZE
        "21":	3.1875	,	#	COTE-D'OR
        "22":	3.1875	,	#	COTES-D'ARMOR
        "23":	3.1875	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.1875	,	#	DOUBS
        "26":	3.1875	,	#	DROME
        "27":	3.1875	,	#	EURE
        "28":	3.1875	,	#	EURE-ET-LOIR
        "29":	3.1875	,	#	FINISTERE
        "02A":	3	,	#	CORSE-DU-SUD
        "02B":	3.1875	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.1875	,	#	HAUTE-GARONNE
        "32":	3.1875	,	#	GERS
        "33":	3.1875	,	#	GIRONDE
        "34":	3.1875	,	#	HERAULT
        "35":	3.1875	,	#	ILLE-ET-VILAINE
        "36":	3.1875	,	#	INDRE
        "37":	3.1875	,	#	INDRE-ET-LOIRE
        "38":	3.1875	,	#	ISERE
        "39":	3.1875	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.1875	,	#	LOIR-ET-CHER
        "42":	3.1875	,	#	LOIRE
        "43":	3.1875	,	#	HAUTE-LOIRE
        "44":	3.1875	,	#	LOIRE-ATLANTIQUE
        "45":	3.1875	,	#	LOIRET
        "46":	3.1875	,	#	LOT
        "47":	3.1875	,	#	LOT-ET-GARONNE
        "48":	3.1875	,	#	LOZERE
        "49":	3.1875	,	#	MAINE-ET-LOIRE
        "50":	3.1875	,	#	MANCHE
        "51":	3.1875	,	#	MARNE
        "52":	3.1875	,	#	HAUTE-MARNE
        "53":	3.1875	,	#	MAYENNE
        "54":	3	,	#	MEURTHE-ET-MOSELLE
        "55":	3.1875	,	#	MEUSE
        "56":	3	,	#	MORBIHAN
        "57":	3.1875	,	#	MOSELLE
        "58":	3.1875	,	#	NIEVRE
        "59":	3.1875	,	#	NORD
        "60":	3.1875	,	#	OISE
        "61":	3.1875	,	#	ORNE
        "62":	3.1875	,	#	PAS-DE-CALAIS
        "63":	3.1875	,	#	PUY-DE-DOME
        "64":	3.1875	,	#	PYRENEES-ATLANTIQUES
        "65":	3.1875	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.1875	,	#	BAS-RHIN
        "68":	3.1875	,	#	HAUT-RHIN
        "69":	3.1875	,	#	RHONE
        #"69":	3.1875	,	#	METROPOLE DE LYON
        "70":	3.1875	,	#	HAUTE-SAONE
        "71":	3.1875	,	#	SAONE-ET-LOIRE
        "72":	3.1875	,	#	SARTHE
        "73":	3.1875	,	#	SAVOIE
        "74":	3.1875	,	#	HAUTE-SAVOIE
        "75":	3.1875	,	#	PARIS
        "76":	3.1875	,	#	SEINE-MARITIME
        "77":	3.1875	,	#	SEINE-ET-MARNE
        "78":	3.1875	,	#	YVELINES
        "79":	3.1875	,	#	DEUX-SEVRES
        "80":	3.1875	,	#	SOMME
        "81":	3.1875	,	#	TARN
        "82":	3.1875	,	#	TARN-ET-GARONNE
        "83":	3.1875	,	#	VAR
        "84":	3.1875	,	#	VAUCLUSE
        "85":	3.1875	,	#	VENDEE
        "86":	3.1875	,	#	VIENNE
        "87":	3.1875	,	#	HAUTE-VIENNE
        "88":	3.1875	,	#	VOSGES
        "89":	3.1875	,	#	YONNE
        "90":	3.1875	,	#	TERRITOIRE DE BELFORT
        "91":	3.1875	,	#	ESSONNE
        "92":	3.1875	,	#	HAUTS-DE-SEINE
        "93":	3.1875	,	#	SEINE-SAINT-DENIS
        "94":	3.1875	,	#	VAL-DE-MARNE
        "95":	3.1875	,	#	VAL-D'OISE
        "101":	3.1875	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.1875	,	#	LA REUNION
        "106":	3.1875	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
    
class tdcfe_coefficient_multiplicateur_prof_plus_36_moins_250kVA_2018(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	1.0625	,	#	AIN
        "2":	1.0625	,	#	AISNE
        "3":	1.0625	,	#	ALLIER
        "4":	1	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	1.0625	,	#	HAUTES-ALPES
        "6":	1	,	#	ALPES-MARITIMES
        "7":	1.0625	,	#	ARDECHE
        "8":	1.0625	,	#	ARDENNES
        "9":	1.0625	,	#	ARIEGE
        "10":	1.0625	,	#	AUBE
        "11":	1	,	#	AUDE
        "12":	1	,	#	AVEYRON
        "13":	1.0625	,	#	BOUCHES-DU-RHONE
        "14":	1.0625	,	#	CALVADOS
        "15":	1.0625	,	#	CANTAL
        "16":	1	,	#	CHARENTE
        "17":	1.0625	,	#	CHARENTE-MARITIME
        "18":	1.0625	,	#	CHER
        "19":	1.0625	,	#	CORREZE
        "21":	1.0625	,	#	COTE-D'OR
        "22":	1.0625	,	#	COTES-D'ARMOR
        "23":	1.0625	,	#	CREUSE
        "24":	1	,	#	DORDOGNE
        "25":	1.0625	,	#	DOUBS
        "26":	1.0625	,	#	DROME
        "27":	1.0625	,	#	EURE
        "28":	1.0625	,	#	EURE-ET-LOIR
        "29":	1.0625	,	#	FINISTERE
        "02A":	1	,	#	CORSE-DU-SUD
        "02B":	1.0625	,	#	HAUTE-CORSE
        "30":	1	,	#	GARD
        "31":	1.0625	,	#	HAUTE-GARONNE
        "32":	1.0625	,	#	GERS
        "33":	1.0625	,	#	GIRONDE
        "34":	1.0625	,	#	HERAULT
        "35":	1.0625	,	#	ILLE-ET-VILAINE
        "36":	1.0625	,	#	INDRE
        "37":	1.0625	,	#	INDRE-ET-LOIRE
        "38":	1.0625	,	#	ISERE
        "39":	1.0625	,	#	JURA
        "40":	1	,	#	LANDES
        "41":	1.0625	,	#	LOIR-ET-CHER
        "42":	1.0625	,	#	LOIRE
        "43":	1.0625	,	#	HAUTE-LOIRE
        "44":	1.0625	,	#	LOIRE-ATLANTIQUE
        "45":	1.0625	,	#	LOIRET
        "46":	1.0625	,	#	LOT
        "47":	1.0625	,	#	LOT-ET-GARONNE
        "48":	1.0625	,	#	LOZERE
        "49":	1.0625	,	#	MAINE-ET-LOIRE
        "50":	1.0625	,	#	MANCHE
        "51":	1.0625	,	#	MARNE
        "52":	1.0625	,	#	HAUTE-MARNE
        "53":	1.0625	,	#	MAYENNE
        "54":	1	,	#	MEURTHE-ET-MOSELLE
        "55":	1.0625	,	#	MEUSE
        "56":	1	,	#	MORBIHAN
        "57":	1.0625	,	#	MOSELLE
        "58":	1.0625	,	#	NIEVRE
        "59":	1.0625	,	#	NORD
        "60":	1.0625	,	#	OISE
        "61":	1.0625	,	#	ORNE
        "62":	1.0625	,	#	PAS-DE-CALAIS
        "63":	1.0625	,	#	PUY-DE-DOME
        "64":	1.0625	,	#	PYRENEES-ATLANTIQUES
        "65":	1.0625	,	#	HAUTES-PYRENEES
        "66":	1	,	#	PYRENEES-ORIENTALES
        "67":	1.0625	,	#	BAS-RHIN
        "68":	1.0625	,	#	HAUT-RHIN
        "69":	1.0625	,	#	RHONE
        #"69":	1.0625	,	#	METROPOLE DE LYON
        "70":	1.0625	,	#	HAUTE-SAONE
        "71":	1.0625	,	#	SAONE-ET-LOIRE
        "72":	1.0625	,	#	SARTHE
        "73":	1.0625	,	#	SAVOIE
        "74":	1.0625	,	#	HAUTE-SAVOIE
        "75":	1.0625	,	#	PARIS
        "76":	1.0625	,	#	SEINE-MARITIME
        "77":	1.0625	,	#	SEINE-ET-MARNE
        "78":	1.0625	,	#	YVELINES
        "79":	1.0625	,	#	DEUX-SEVRES
        "80":	1.0625	,	#	SOMME
        "81":	1.0625	,	#	TARN
        "82":	1.0625	,	#	TARN-ET-GARONNE
        "83":	1.0625	,	#	VAR
        "84":	1.0625	,	#	VAUCLUSE
        "85":	1.0625	,	#	VENDEE
        "86":	1.0625	,	#	VIENNE
        "87":	1.0625	,	#	HAUTE-VIENNE
        "88":	1.0625	,	#	VOSGES
        "89":	1.0625	,	#	YONNE
        "90":	1.0625	,	#	TERRITOIRE DE BELFORT
        "91":	1.0625	,	#	ESSONNE
        "92":	1.0625	,	#	HAUTS-DE-SEINE
        "93":	1.0625	,	#	SEINE-SAINT-DENIS
        "94":	1.0625	,	#	VAL-DE-MARNE
        "95":	1.0625	,	#	VAL-D'OISE
        "101":	1.0625	,	#	GUADELOUPE
        "102":	1	,	#	GUYANE
        "103":	1	,	#	MARTINIQUE
        "104":	1.0625	,	#	LA REUNION
        "106":	1.0625	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_non_prof_moins_250kVA_2018(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.1875	,	#	AIN
        "2":	3.1875	,	#	AISNE
        "3":	3.1875	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.1875	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.1875	,	#	ARDECHE
        "8":	3.1875	,	#	ARDENNES
        "9":	3.1875	,	#	ARIEGE
        "10":	3.1875	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.1875	,	#	BOUCHES-DU-RHONE
        "14":	3.1875	,	#	CALVADOS
        "15":	3.1875	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3.1875	,	#	CHARENTE-MARITIME
        "18":	3.1875	,	#	CHER
        "19":	3.1875	,	#	CORREZE
        "21":	3.1875	,	#	COTE-D'OR
        "22":	3.1875	,	#	COTES-D'ARMOR
        "23":	3.1875	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.1875	,	#	DOUBS
        "26":	3.1875	,	#	DROME
        "27":	3.1875	,	#	EURE
        "28":	3.1875	,	#	EURE-ET-LOIR
        "29":	3.1875	,	#	FINISTERE
        "02A":	3	,	#	CORSE-DU-SUD
        "02B":	3.1875	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.1875	,	#	HAUTE-GARONNE
        "32":	3.1875	,	#	GERS
        "33":	3.1875	,	#	GIRONDE
        "34":	3.1875	,	#	HERAULT
        "35":	3.1875	,	#	ILLE-ET-VILAINE
        "36":	3.1875	,	#	INDRE
        "37":	3.1875	,	#	INDRE-ET-LOIRE
        "38":	3.1875	,	#	ISERE
        "39":	3.1875	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.1875	,	#	LOIR-ET-CHER
        "42":	3.1875	,	#	LOIRE
        "43":	3.1875	,	#	HAUTE-LOIRE
        "44":	3.1875	,	#	LOIRE-ATLANTIQUE
        "45":	3.1875	,	#	LOIRET
        "46":	3.1875	,	#	LOT
        "47":	3.1875	,	#	LOT-ET-GARONNE
        "48":	3.1875	,	#	LOZERE
        "49":	3.1875	,	#	MAINE-ET-LOIRE
        "50":	3.1875	,	#	MANCHE
        "51":	3.1875	,	#	MARNE
        "52":	3.1875	,	#	HAUTE-MARNE
        "53":	3.1875	,	#	MAYENNE
        "54":	3	,	#	MEURTHE-ET-MOSELLE
        "55":	3.1875	,	#	MEUSE
        "56":	3	,	#	MORBIHAN
        "57":	3.1875	,	#	MOSELLE
        "58":	3.1875	,	#	NIEVRE
        "59":	3.1875	,	#	NORD
        "60":	3.1875	,	#	OISE
        "61":	3.1875	,	#	ORNE
        "62":	3.1875	,	#	PAS-DE-CALAIS
        "63":	3.1875	,	#	PUY-DE-DOME
        "64":	3.1875	,	#	PYRENEES-ATLANTIQUES
        "65":	3.1875	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.1875	,	#	BAS-RHIN
        "68":	3.1875	,	#	HAUT-RHIN
        "69":	3.1875	,	#	RHONE
        #"69":	3.1875	,	#	METROPOLE DE LYON
        "70":	3.1875	,	#	HAUTE-SAONE
        "71":	3.1875	,	#	SAONE-ET-LOIRE
        "72":	3.1875	,	#	SARTHE
        "73":	3.1875	,	#	SAVOIE
        "74":	3.1875	,	#	HAUTE-SAVOIE
        "75":	3.1875	,	#	PARIS
        "76":	3.1875	,	#	SEINE-MARITIME
        "77":	3.1875	,	#	SEINE-ET-MARNE
        "78":	3.1875	,	#	YVELINES
        "79":	3.1875	,	#	DEUX-SEVRES
        "80":	3.1875	,	#	SOMME
        "81":	3.1875	,	#	TARN
        "82":	3.1875	,	#	TARN-ET-GARONNE
        "83":	3.1875	,	#	VAR
        "84":	3.1875	,	#	VAUCLUSE
        "85":	3.1875	,	#	VENDEE
        "86":	3.1875	,	#	VIENNE
        "87":	3.1875	,	#	HAUTE-VIENNE
        "88":	3.1875	,	#	VOSGES
        "89":	3.1875	,	#	YONNE
        "90":	3.1875	,	#	TERRITOIRE DE BELFORT
        "91":	3.1875	,	#	ESSONNE
        "92":	3.1875	,	#	HAUTS-DE-SEINE
        "93":	3.1875	,	#	SEINE-SAINT-DENIS
        "94":	3.1875	,	#	VAL-DE-MARNE
        "95":	3.1875	,	#	VAL-D'OISE
        "101":	3.1875	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.1875	,	#	LA REUNION
        "106":	3.1875	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

