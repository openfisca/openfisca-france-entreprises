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

class tdcfe_coefficient_multiplicateur_prof_moins_36kVA_2014(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.17	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.17	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.17	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.17	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3.17	,	#	ARIEGE
        "10":	3.17	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.17	,	#	BOUCHES-DU-RHONE
        "14":	3.17	,	#	CALVADOS
        "15":	3.17	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3.17	,	#	CHARENTE-MARITIME
        "18":	3.17	,	#	CHER
        "19":	3.17	,	#	CORREZE
        "21":	3.17	,	#	COTE-D'OR
        "22":	3.11	,	#	COTES-D'ARMOR
        "23":	3.17	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.17	,	#	DROME
        "27":	3.17	,	#	EURE
        "28":	3.11	,	#	EURE-ET-LOIR
        "29":	3.17	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3.11	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.17	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3.17	,	#	GIRONDE
        "34":	3.17	,	#	HERAULT
        "35":	3.17	,	#	ILLE-ET-VILAINE
        "36":	3.17	,	#	INDRE
        "37":	3.17	,	#	INDRE-ET-LOIRE
        "38":	3.17	,	#	ISERE
        "39":	3.17	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.11	,	#	LOIR-ET-CHER
        "42":	3.17	,	#	LOIRE
        "43":	3.17	,	#	HAUTE-LOIRE
        "44":	3.17	,	#	LOIRE-ATLANTIQUE
        "45":	3.17	,	#	LOIRET
        "46":	3.17	,	#	LOT
        "47":	3.11	,	#	LOT-ET-GARONNE
        "48":	3.17	,	#	LOZERE
        "49":	3.17	,	#	MAINE-ET-LOIRE
        "50":	3.17	,	#	MANCHE
        "51":	3.17	,	#	MARNE
        "52":	3.17	,	#	HAUTE-MARNE
        "53":	3.15	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.17	,	#	MOSELLE
        "58":	3.11	,	#	NIEVRE
        "59":	3.17	,	#	NORD
        "60":	3.17	,	#	OISE
        "61":	3.17	,	#	ORNE
        "62":	3.11	,	#	PAS-DE-CALAIS
        "63":	3.17	,	#	PUY-DE-DOME
        "64":	3.17	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.17	,	#	BAS-RHIN
        "68":	3.17	,	#	HAUT-RHIN
        "69":	3.11	,	#	RHONE
        "70":	3.17	,	#	HAUTE-SAONE
        "71":	3.17	,	#	SAONE-ET-LOIRE
        "72":	3.17	,	#	SARTHE
        "73":	3.17	,	#	SAVOIE
        "74":	3.17	,	#	HAUTE-SAVOIE
        "75":	3.11	,	#	PARIS
        "76":	3.17	,	#	SEINE-MARITIME
        "77":	3.17	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.17	,	#	SOMME
        "81":	3.17	,	#	TARN
        "82":	3.08	,	#	TARN-ET-GARONNE
        "83":	3.17	,	#	VAR
        "84":	3.17	,	#	VAUCLUSE
        "85":	3.17	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.17	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.17	,	#	YONNE
        "90":	3.17	,	#	TERRITOIRE DE BELFORT
        "91":	3.17	,	#	ESSONNE
        "92":	3.17	,	#	HAUTS-DE-SEINE
        "93":	3.11	,	#	SEINE-SAINT-DENIS
        "94":	3.11	,	#	VAL-DE-MARNE
        "95":	3.17	,	#	VAL-D'OISE
        "101":	3.17	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE
    
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
    
class tdcfe_coefficient_multiplicateur_prof_plus_36_moins_250kVA_2014(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	1.06	,	#	AIN
        "2":	1.02	,	#	AISNE
        "3":	1.06	,	#	ALLIER
        "4":	1	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	1.06	,	#	HAUTES-ALPES
        "6":	1	,	#	ALPES-MARITIMES
        "7":	1.06	,	#	ARDECHE
        "8":	1.02	,	#	ARDENNES
        "9":	1.06	,	#	ARIEGE
        "10":	1.06	,	#	AUBE
        "11":	1	,	#	AUDE
        "12":	1	,	#	AVEYRON
        "13":	1.06	,	#	BOUCHES-DU-RHONE
        "14":	1.06	,	#	CALVADOS
        "15":	1.06	,	#	CANTAL
        "16":	1	,	#	CHARENTE
        "17":	1.06	,	#	CHARENTE-MARITIME
        "18":	1.06	,	#	CHER
        "19":	1.06	,	#	CORREZE
        "21":	1.06	,	#	COTE-D'OR
        "22":	1.04	,	#	COTES-D'ARMOR
        "23":	1.06	,	#	CREUSE
        "24":	1	,	#	DORDOGNE
        "25":	1.02	,	#	DOUBS
        "26":	1.06	,	#	DROME
        "27":	1.06	,	#	EURE
        "28":	1.04	,	#	EURE-ET-LOIR
        "29":	1.06	,	#	FINISTERE
        "02A":	1.02	,	#	CORSE-DU-SUD
        "02B":	1.04	,	#	HAUTE-CORSE
        "30":	1	,	#	GARD
        "31":	1.06	,	#	HAUTE-GARONNE
        "32":	1	,	#	GERS
        "33":	1.06	,	#	GIRONDE
        "34":	1.06	,	#	HERAULT
        "35":	1.06	,	#	ILLE-ET-VILAINE
        "36":	1.06	,	#	INDRE
        "37":	1.06	,	#	INDRE-ET-LOIRE
        "38":	1.06	,	#	ISERE
        "39":	1.06	,	#	JURA
        "40":	1	,	#	LANDES
        "41":	1.04	,	#	LOIR-ET-CHER
        "42":	1.06	,	#	LOIRE
        "43":	1.06	,	#	HAUTE-LOIRE
        "44":	1.06	,	#	LOIRE-ATLANTIQUE
        "45":	1.06	,	#	LOIRET
        "46":	1.06	,	#	LOT
        "47":	1.04	,	#	LOT-ET-GARONNE
        "48":	1.06	,	#	LOZERE
        "49":	1.06	,	#	MAINE-ET-LOIRE
        "50":	1.06	,	#	MANCHE
        "51":	1.06	,	#	MARNE
        "52":	1.06	,	#	HAUTE-MARNE
        "53":	1.05	,	#	MAYENNE
        "54":	0.75	,	#	MEURTHE-ET-MOSELLE
        "55":	0.5	,	#	MEUSE
        "56":	1.02	,	#	MORBIHAN
        "57":	1.06	,	#	MOSELLE
        "58":	1.04	,	#	NIEVRE
        "59":	1.06	,	#	NORD
        "60":	1.06	,	#	OISE
        "61":	1.06	,	#	ORNE
        "62":	1.04	,	#	PAS-DE-CALAIS
        "63":	1.06	,	#	PUY-DE-DOME
        "64":	1.06	,	#	PYRENEES-ATLANTIQUES
        "65":	1	,	#	HAUTES-PYRENEES
        "66":	1	,	#	PYRENEES-ORIENTALES
        "67":	1.06	,	#	BAS-RHIN
        "68":	1.06	,	#	HAUT-RHIN
        "69":	1.04	,	#	RHONE
        "70":	1.06	,	#	HAUTE-SAONE
        "71":	1.06	,	#	SAONE-ET-LOIRE
        "72":	1.06	,	#	SARTHE
        "73":	1.06	,	#	SAVOIE
        "74":	1.06	,	#	HAUTE-SAVOIE
        "75":	1.04	,	#	PARIS
        "76":	1.06	,	#	SEINE-MARITIME
        "77":	1.06	,	#	SEINE-ET-MARNE
        "78":	1	,	#	YVELINES
        "79":	1	,	#	DEUX-SEVRES
        "80":	1.06	,	#	SOMME
        "81":	1.06	,	#	TARN
        "82":	1.03	,	#	TARN-ET-GARONNE
        "83":	1.06	,	#	VAR
        "84":	1.06	,	#	VAUCLUSE
        "85":	1.06	,	#	VENDEE
        "86":	1	,	#	VIENNE
        "87":	1.06	,	#	HAUTE-VIENNE
        "88":	1.02	,	#	VOSGES
        "89":	1.06	,	#	YONNE
        "90":	1.06	,	#	TERRITOIRE DE BELFORT
        "91":	1.06	,	#	ESSONNE
        "92":	1.06	,	#	HAUTS-DE-SEINE
        "93":	1.04	,	#	SEINE-SAINT-DENIS
        "94":	1.04	,	#	VAL-DE-MARNE
        "95":	1.06	,	#	VAL-D'OISE
        "101":	1.06	,	#	GUADELOUPE
        "102":	1	,	#	GUYANE
        "103":	1	,	#	MARTINIQUE
        "104":	1.02	,	#	LA REUNION
        "143":	2	,	#	MAYOTTE
    
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_non_prof_moins_250kVA_2014(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.17	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.17	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.17	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.17	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3.17	,	#	ARIEGE
        "10":	3.17	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.17	,	#	BOUCHES-DU-RHONE
        "14":	3.17	,	#	CALVADOS
        "15":	3.17	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3.17	,	#	CHARENTE-MARITIME
        "18":	3.17	,	#	CHER
        "19":	3.17	,	#	CORREZE
        "21":	3.17	,	#	COTE-D'OR
        "22":	3.11	,	#	COTES-D'ARMOR
        "23":	3.17	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.17	,	#	DROME
        "27":	3.17	,	#	EURE
        "28":	3.11	,	#	EURE-ET-LOIR
        "29":	3.17	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3.11	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.17	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3.17	,	#	GIRONDE
        "34":	3.17	,	#	HERAULT
        "35":	3.17	,	#	ILLE-ET-VILAINE
        "36":	3.17	,	#	INDRE
        "37":	3.17	,	#	INDRE-ET-LOIRE
        "38":	3.17	,	#	ISERE
        "39":	3.17	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.11	,	#	LOIR-ET-CHER
        "42":	3.17	,	#	LOIRE
        "43":	3.17	,	#	HAUTE-LOIRE
        "44":	3.17	,	#	LOIRE-ATLANTIQUE
        "45":	3.17	,	#	LOIRET
        "46":	3.17	,	#	LOT
        "47":	3.11	,	#	LOT-ET-GARONNE
        "48":	3.17	,	#	LOZERE
        "49":	3.17	,	#	MAINE-ET-LOIRE
        "50":	3.17	,	#	MANCHE
        "51":	3.17	,	#	MARNE
        "52":	3.17	,	#	HAUTE-MARNE
        "53":	3.15	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.17	,	#	MOSELLE
        "58":	3.11	,	#	NIEVRE
        "59":	3.17	,	#	NORD
        "60":	3.17	,	#	OISE
        "61":	3.17	,	#	ORNE
        "62":	3.11	,	#	PAS-DE-CALAIS
        "63":	3.17	,	#	PUY-DE-DOME
        "64":	3.17	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.17	,	#	BAS-RHIN
        "68":	3.17	,	#	HAUT-RHIN
        "69":	3.11	,	#	RHONE
        "70":	3.17	,	#	HAUTE-SAONE
        "71":	3.17	,	#	SAONE-ET-LOIRE
        "72":	3.17	,	#	SARTHE
        "73":	3.17	,	#	SAVOIE
        "74":	3.17	,	#	HAUTE-SAVOIE
        "75":	3.11	,	#	PARIS
        "76":	3.17	,	#	SEINE-MARITIME
        "77":	3.17	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.17	,	#	SOMME
        "81":	3.17	,	#	TARN
        "82":	3.08	,	#	TARN-ET-GARONNE
        "83":	3.17	,	#	VAR
        "84":	3.17	,	#	VAUCLUSE
        "85":	3.17	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.17	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.17	,	#	YONNE
        "90":	3.17	,	#	TERRITOIRE DE BELFORT
        "91":	3.17	,	#	ESSONNE
        "92":	3.17	,	#	HAUTS-DE-SEINE
        "93":	3.11	,	#	SEINE-SAINT-DENIS
        "94":	3.11	,	#	VAL-DE-MARNE
        "95":	3.17	,	#	VAL-D'OISE
        "101":	3.17	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

