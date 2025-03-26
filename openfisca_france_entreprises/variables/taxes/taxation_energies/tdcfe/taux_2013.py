# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_france_entreprises.entities import UniteLegale, Etablissement


class tdcfe_coefficient_multiplicateur_normal_2013(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	4.14	,	#	AIN
        "2":	4.06	,	#	AISNE
        "3":	4.14	,	#	ALLIER
        "4":	4	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	4.14	,	#	HAUTES-ALPES
        "6":	4	,	#	ALPES-MARITIMES
        "7":	4.14	,	#	ARDECHE
        "8":	4.06	,	#	ARDENNES
        "9":	4.14	,	#	ARIEGE
        "10":	4.14	,	#	AUBE
        "11":	4	,	#	AUDE
        "12":	4	,	#	AVEYRON
        "13":	4.06	,	#	BOUCHES-DU-RHONE
        "14":	4.14	,	#	CALVADOS
        "15":	4.14	,	#	CANTAL
        "16":	4	,	#	CHARENTE
        "17":	4	,	#	CHARENTE-MARITIME
        "18":	4	,	#	CHER
        "19":	4	,	#	CORREZE
        "21":	4.14	,	#	COTE-D'OR
        "22":	4.14	,	#	COTES-D'ARMOR
        "23":	4.06	,	#	CREUSE
        "24":	4	,	#	DORDOGNE
        "25":	4.06	,	#	DOUBS
        "26":	4.06	,	#	DROME
        "27":	4.14	,	#	EURE
        "28":	4	,	#	EURE-ET-LOIR
        "29":	4.14	,	#	FINISTERE
        "02A":	4.06	,	#	CORSE-DU-SUD
        "02B":	4.14	,	#	HAUTE-CORSE
        "30":	4	,	#	GARD
        "31":	4.14	,	#	HAUTE-GARONNE
        "32":	4	,	#	GERS
        "33":	4	,	#	GIRONDE
        "34":	4.14	,	#	HERAULT
        "35":	4.06	,	#	ILLE-ET-VILAINE
        "36":	4.14	,	#	INDRE
        "37":	4.14	,	#	INDRE-ET-LOIRE
        "38":	4.14	,	#	ISERE
        "39":	4.14	,	#	JURA
        "40":	4	,	#	LANDES
        "41":	4.06	,	#	LOIR-ET-CHER
        "42":	4.14	,	#	LOIRE
        "43":	4.14	,	#	HAUTE-LOIRE
        "44":	4.14	,	#	LOIRE-ATLANTIQUE
        "45":	4.14	,	#	LOIRET
        "46":	4.14	,	#	LOT
        "47":	4.06	,	#	LOT-ET-GARONNE
        "48":	4.14	,	#	LOZERE
        "49":	4.06	,	#	MAINE-ET-LOIRE
        "50":	4.14	,	#	MANCHE
        "51":	4.14	,	#	MARNE
        "52":	4.14	,	#	HAUTE-MARNE
        "53":	4.14	,	#	MAYENNE
        "54":	3	,	#	MEURTHE-ET-MOSELLE
        "55":	2	,	#	MEUSE
        "56":	4.06	,	#	MORBIHAN
        "57":	4.14	,	#	MOSELLE
        "58":	4.14	,	#	NIEVRE
        "59":	4.14	,	#	NORD
        "60":	4.06	,	#	OISE
        "61":	4.14	,	#	ORNE
        "62":	4.14	,	#	PAS-DE-CALAIS
        "63":	4.14	,	#	PUY-DE-DOME
        "64":	4.14	,	#	PYRENEES-ATLANTIQUES
        "65":	4	,	#	HAUTES-PYRENEES
        "66":	4	,	#	PYRENEES-ORIENTALES
        "67":	4.14	,	#	BAS-RHIN
        "68":	4.14	,	#	HAUT-RHIN
        "69":	4.14	,	#	RHONE
        "70":	4.14	,	#	HAUTE-SAONE
        "71":	4.14	,	#	SAONE-ET-LOIRE
        "72":	4.14	,	#	SARTHE
        "73":	4.06	,	#	SAVOIE
        "74":	4.14	,	#	HAUTE-SAVOIE
        "75":	4.14	,	#	PARIS
        "76":	4	,	#	SEINE-MARITIME
        "77":	4.14	,	#	SEINE-ET-MARNE
        "78":	4	,	#	YVELINES
        "79":	4	,	#	DEUX-SEVRES
        "80":	4.06	,	#	SOMME
        "81":	4.14	,	#	TARN
        "82":	4.1	,	#	TARN-ET-GARONNE
        "83":	4.14	,	#	VAR
        "84":	4.14	,	#	VAUCLUSE
        "85":	4.14	,	#	VENDEE
        "86":	4	,	#	VIENNE
        "87":	4.14	,	#	HAUTE-VIENNE
        "88":	4.06	,	#	VOSGES
        "89":	4.06	,	#	YONNE
        "90":	4.14	,	#	TERRITOIRE DE BELFORT
        "91":	4.14	,	#	ESSONNE
        "92":	4.14	,	#	HAUTS-DE-SEINE
        "93":	4.14	,	#	SEINE-SAINT-DENIS
        "94":	4.06	,	#	VAL-DE-MARNE
        "95":	4.14	,	#	VAL-D'OISE
        "101":	4	,	#	GUADELOUPE
        "102":	4	,	#	GUYANE
        "103":	4	,	#	MARTINIQUE
        "104":	4.06	,	#	LA REUNION
        "143":	8	,	#	MAYOTTE

        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_prof_moins_36kVA_2013(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.11	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.11	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.11	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.11	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3.11	,	#	ARIEGE
        "10":	3.11	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.05	,	#	BOUCHES-DU-RHONE
        "14":	3.11	,	#	CALVADOS
        "15":	3.11	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3	,	#	CHARENTE-MARITIME
        "18":	3	,	#	CHER
        "19":	3	,	#	CORREZE
        "21":	3.11	,	#	COTE-D'OR
        "22":	3.11	,	#	COTES-D'ARMOR
        "23":	3.05	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.05	,	#	DROME
        "27":	3.11	,	#	EURE
        "28":	3	,	#	EURE-ET-LOIR
        "29":	3.11	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3.11	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.11	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3	,	#	GIRONDE
        "34":	3.11	,	#	HERAULT
        "35":	3.05	,	#	ILLE-ET-VILAINE
        "36":	3.11	,	#	INDRE
        "37":	3.11	,	#	INDRE-ET-LOIRE
        "38":	3.11	,	#	ISERE
        "39":	3.11	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.05	,	#	LOIR-ET-CHER
        "42":	3.11	,	#	LOIRE
        "43":	3.11	,	#	HAUTE-LOIRE
        "44":	3.11	,	#	LOIRE-ATLANTIQUE
        "45":	3.11	,	#	LOIRET
        "46":	3.11	,	#	LOT
        "47":	3.05	,	#	LOT-ET-GARONNE
        "48":	3.11	,	#	LOZERE
        "49":	3.05	,	#	MAINE-ET-LOIRE
        "50":	3.11	,	#	MANCHE
        "51":	3.11	,	#	MARNE
        "52":	3.11	,	#	HAUTE-MARNE
        "53":	3.11	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.11	,	#	MOSELLE
        "58":	3.11	,	#	NIEVRE
        "59":	3.11	,	#	NORD
        "60":	3.05	,	#	OISE
        "61":	3.11	,	#	ORNE
        "62":	3.11	,	#	PAS-DE-CALAIS
        "63":	3.11	,	#	PUY-DE-DOME
        "64":	3.11	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.11	,	#	BAS-RHIN
        "68":	3.11	,	#	HAUT-RHIN
        "69":	3.11	,	#	RHONE
        "70":	3.11	,	#	HAUTE-SAONE
        "71":	3.11	,	#	SAONE-ET-LOIRE
        "72":	3.11	,	#	SARTHE
        "73":	3.05	,	#	SAVOIE
        "74":	3.11	,	#	HAUTE-SAVOIE
        "75":	3.11	,	#	PARIS
        "76":	3	,	#	SEINE-MARITIME
        "77":	3.11	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.05	,	#	SOMME
        "81":	3.11	,	#	TARN
        "82":	3.08	,	#	TARN-ET-GARONNE
        "83":	3.11	,	#	VAR
        "84":	3.11	,	#	VAUCLUSE
        "85":	3.11	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.11	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.05	,	#	YONNE
        "90":	3.11	,	#	TERRITOIRE DE BELFORT
        "91":	3.11	,	#	ESSONNE
        "92":	3.11	,	#	HAUTS-DE-SEINE
        "93":	3.11	,	#	SEINE-SAINT-DENIS
        "94":	3.05	,	#	VAL-DE-MARNE
        "95":	3.11	,	#	VAL-D'OISE
        "101":	3	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE
    
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
    
class tdcfe_coefficient_multiplicateur_prof_plus_36_moins_250kVA_2013(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	1.04	,	#	AIN
        "2":	1.02	,	#	AISNE
        "3":	1.04	,	#	ALLIER
        "4":	1	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	1.04	,	#	HAUTES-ALPES
        "6":	1	,	#	ALPES-MARITIMES
        "7":	1.04	,	#	ARDECHE
        "8":	1.02	,	#	ARDENNES
        "9":	1.04	,	#	ARIEGE
        "10":	1.04	,	#	AUBE
        "11":	1	,	#	AUDE
        "12":	1	,	#	AVEYRON
        "13":	1.02	,	#	BOUCHES-DU-RHONE
        "14":	1.04	,	#	CALVADOS
        "15":	1.04	,	#	CANTAL
        "16":	1	,	#	CHARENTE
        "17":	1	,	#	CHARENTE-MARITIME
        "18":	1	,	#	CHER
        "19":	1	,	#	CORREZE
        "21":	1.04	,	#	COTE-D'OR
        "22":	1.04	,	#	COTES-D'ARMOR
        "23":	1.02	,	#	CREUSE
        "24":	1	,	#	DORDOGNE
        "25":	1.02	,	#	DOUBS
        "26":	1.02	,	#	DROME
        "27":	1.04	,	#	EURE
        "28":	1	,	#	EURE-ET-LOIR
        "29":	1.04	,	#	FINISTERE
        "02A":	1.02	,	#	CORSE-DU-SUD
        "02B":	1.04	,	#	HAUTE-CORSE
        "30":	1	,	#	GARD
        "31":	1.04	,	#	HAUTE-GARONNE
        "32":	1	,	#	GERS
        "33":	1	,	#	GIRONDE
        "34":	1.04	,	#	HERAULT
        "35":	1.02	,	#	ILLE-ET-VILAINE
        "36":	1.04	,	#	INDRE
        "37":	1.04	,	#	INDRE-ET-LOIRE
        "38":	1.04	,	#	ISERE
        "39":	1.04	,	#	JURA
        "40":	1	,	#	LANDES
        "41":	1.02	,	#	LOIR-ET-CHER
        "42":	1.04	,	#	LOIRE
        "43":	1.04	,	#	HAUTE-LOIRE
        "44":	1.04	,	#	LOIRE-ATLANTIQUE
        "45":	1.04	,	#	LOIRET
        "46":	1.04	,	#	LOT
        "47":	1.02	,	#	LOT-ET-GARONNE
        "48":	1.04	,	#	LOZERE
        "49":	1.02	,	#	MAINE-ET-LOIRE
        "50":	1.04	,	#	MANCHE
        "51":	1.04	,	#	MARNE
        "52":	1.04	,	#	HAUTE-MARNE
        "53":	1.04	,	#	MAYENNE
        "54":	0.75	,	#	MEURTHE-ET-MOSELLE
        "55":	0.5	,	#	MEUSE
        "56":	1.02	,	#	MORBIHAN
        "57":	1.04	,	#	MOSELLE
        "58":	1.04	,	#	NIEVRE
        "59":	1.04	,	#	NORD
        "60":	1.02	,	#	OISE
        "61":	1.04	,	#	ORNE
        "62":	1.04	,	#	PAS-DE-CALAIS
        "63":	1.04	,	#	PUY-DE-DOME
        "64":	1.04	,	#	PYRENEES-ATLANTIQUES
        "65":	1	,	#	HAUTES-PYRENEES
        "66":	1	,	#	PYRENEES-ORIENTALES
        "67":	1.04	,	#	BAS-RHIN
        "68":	1.04	,	#	HAUT-RHIN
        "69":	1.04	,	#	RHONE
        "70":	1.04	,	#	HAUTE-SAONE
        "71":	1.04	,	#	SAONE-ET-LOIRE
        "72":	1.04	,	#	SARTHE
        "73":	1.02	,	#	SAVOIE
        "74":	1.04	,	#	HAUTE-SAVOIE
        "75":	1.04	,	#	PARIS
        "76":	1	,	#	SEINE-MARITIME
        "77":	1.04	,	#	SEINE-ET-MARNE
        "78":	1	,	#	YVELINES
        "79":	1	,	#	DEUX-SEVRES
        "80":	1.02	,	#	SOMME
        "81":	1.04	,	#	TARN
        "82":	1.03	,	#	TARN-ET-GARONNE
        "83":	1.04	,	#	VAR
        "84":	1.04	,	#	VAUCLUSE
        "85":	1.04	,	#	VENDEE
        "86":	1	,	#	VIENNE
        "87":	1.04	,	#	HAUTE-VIENNE
        "88":	1.02	,	#	VOSGES
        "89":	1.02	,	#	YONNE
        "90":	1.04	,	#	TERRITOIRE DE BELFORT
        "91":	1.04	,	#	ESSONNE
        "92":	1.04	,	#	HAUTS-DE-SEINE
        "93":	1.04	,	#	SEINE-SAINT-DENIS
        "94":	1.02	,	#	VAL-DE-MARNE
        "95":	1.04	,	#	VAL-D'OISE
        "101":	1	,	#	GUADELOUPE
        "102":	1	,	#	GUYANE
        "103":	1	,	#	MARTINIQUE
        "104":	1.02	,	#	LA REUNION
        "143":	2	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_non_prof_moins_250kVA_2013(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.11	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.11	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3.11	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3.11	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3.11	,	#	ARIEGE
        "10":	3.11	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3.05	,	#	BOUCHES-DU-RHONE
        "14":	3.11	,	#	CALVADOS
        "15":	3.11	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3	,	#	CHARENTE-MARITIME
        "18":	3	,	#	CHER
        "19":	3	,	#	CORREZE
        "21":	3.11	,	#	COTE-D'OR
        "22":	3.11	,	#	COTES-D'ARMOR
        "23":	3.05	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.05	,	#	DROME
        "27":	3.11	,	#	EURE
        "28":	3	,	#	EURE-ET-LOIR
        "29":	3.11	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3.11	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.11	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3	,	#	GIRONDE
        "34":	3.11	,	#	HERAULT
        "35":	3.05	,	#	ILLE-ET-VILAINE
        "36":	3.11	,	#	INDRE
        "37":	3.11	,	#	INDRE-ET-LOIRE
        "38":	3.11	,	#	ISERE
        "39":	3.11	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3.05	,	#	LOIR-ET-CHER
        "42":	3.11	,	#	LOIRE
        "43":	3.11	,	#	HAUTE-LOIRE
        "44":	3.11	,	#	LOIRE-ATLANTIQUE
        "45":	3.11	,	#	LOIRET
        "46":	3.11	,	#	LOT
        "47":	3.05	,	#	LOT-ET-GARONNE
        "48":	3.11	,	#	LOZERE
        "49":	3.05	,	#	MAINE-ET-LOIRE
        "50":	3.11	,	#	MANCHE
        "51":	3.11	,	#	MARNE
        "52":	3.11	,	#	HAUTE-MARNE
        "53":	3.11	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.11	,	#	MOSELLE
        "58":	3.11	,	#	NIEVRE
        "59":	3.11	,	#	NORD
        "60":	3.05	,	#	OISE
        "61":	3.11	,	#	ORNE
        "62":	3.11	,	#	PAS-DE-CALAIS
        "63":	3.11	,	#	PUY-DE-DOME
        "64":	3.11	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3.11	,	#	BAS-RHIN
        "68":	3.11	,	#	HAUT-RHIN
        "69":	3.11	,	#	RHONE
        "70":	3.11	,	#	HAUTE-SAONE
        "71":	3.11	,	#	SAONE-ET-LOIRE
        "72":	3.11	,	#	SARTHE
        "73":	3.05	,	#	SAVOIE
        "74":	3.11	,	#	HAUTE-SAVOIE
        "75":	3.11	,	#	PARIS
        "76":	3	,	#	SEINE-MARITIME
        "77":	3.11	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.05	,	#	SOMME
        "81":	3.11	,	#	TARN
        "82":	3.08	,	#	TARN-ET-GARONNE
        "83":	3.11	,	#	VAR
        "84":	3.11	,	#	VAUCLUSE
        "85":	3.11	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.11	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.05	,	#	YONNE
        "90":	3.11	,	#	TERRITOIRE DE BELFORT
        "91":	3.11	,	#	ESSONNE
        "92":	3.11	,	#	HAUTS-DE-SEINE
        "93":	3.11	,	#	SEINE-SAINT-DENIS
        "94":	3.05	,	#	VAL-DE-MARNE
        "95":	3.11	,	#	VAL-D'OISE
        "101":	3	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE

        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

