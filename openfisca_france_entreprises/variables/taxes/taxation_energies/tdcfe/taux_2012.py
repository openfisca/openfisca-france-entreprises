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

class tdcfe_coefficient_multiplicateur_prof_moins_36kVA_2012(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" 
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.05	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.05	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3	,	#	ARIEGE
        "10":	3.05	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3	,	#	BOUCHES-DU-RHONE
        "14":	3.05	,	#	CALVADOS
        "15":	3.05	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3	,	#	CHARENTE-MARITIME
        "18":	3	,	#	CHER
        "19":	3	,	#	CORREZE
        "21":	3.05	,	#	COTE-D'OR
        "22":	3.05	,	#	COTES-D'ARMOR
        "23":	3.05	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.05	,	#	DROME
        "27":	3	,	#	EURE
        "28":	3	,	#	EURE-ET-LOIR
        "29":	3.05	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.05	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3	,	#	GIRONDE
        "34":	3.05	,	#	HERAULT
        "35":	3.05	,	#	ILLE-ET-VILAINE
        "36":	3.05	,	#	INDRE
        "37":	3.05	,	#	INDRE-ET-LOIRE
        "38":	3.05	,	#	ISERE
        "39":	3	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3	,	#	LOIR-ET-CHER
        "42":	3.05	,	#	LOIRE
        "43":	3	,	#	HAUTE-LOIRE
        "44":	3	,	#	LOIRE-ATLANTIQUE
        "45":	3.05	,	#	LOIRET
        "46":	3.05	,	#	LOT
        "47":	3.05	,	#	LOT-ET-GARONNE
        "48":	3.05	,	#	LOZERE
        "49":	3.05	,	#	MAINE-ET-LOIRE
        "50":	3.05	,	#	MANCHE
        "51":	3.05	,	#	MARNE
        "52":	3.05	,	#	HAUTE-MARNE
        "53":	3.05	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.05	,	#	MOSELLE
        "58":	3	,	#	NIEVRE
        "59":	3.05	,	#	NORD
        "60":	3	,	#	OISE
        "61":	3.05	,	#	ORNE
        "62":	3	,	#	PAS-DE-CALAIS
        "63":	3.05	,	#	PUY-DE-DOME
        "64":	3	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3	,	#	BAS-RHIN
        "68":	3	,	#	HAUT-RHIN
        "69":	3.05	,	#	RHONE
        "70":	3.05	,	#	HAUTE-SAONE
        "71":	3	,	#	SAONE-ET-LOIRE
        "72":	3.05	,	#	SARTHE
        "73":	3.05	,	#	SAVOIE
        "74":	3.05	,	#	HAUTE-SAVOIE
        "75":	3.05	,	#	PARIS
        "76":	3	,	#	SEINE-MARITIME
        "77":	3.05	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.05	,	#	SOMME
        "81":	3.05	,	#	TARN
        "82":	3.05	,	#	TARN-ET-GARONNE
        "83":	3	,	#	VAR
        "84":	3	,	#	VAUCLUSE
        "85":	3.05	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.05	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.05	,	#	YONNE
        "90":	3	,	#	TERRITOIRE DE BELFORT
        "91":	3	,	#	ESSONNE
        "92":	3	,	#	HAUTS-DE-SEINE
        "93":	3.05	,	#	SEINE-SAINT-DENIS
        "94":	3.05	,	#	VAL-DE-MARNE
        "95":	3.05	,	#	VAL-D'OISE
        "101":	3	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE
            
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat
    
class tdcfe_coefficient_multiplicateur_prof_plus_36_moins_250kVA_2012(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	1.02	,	#	AIN
        "2":	1.02	,	#	AISNE
        "3":	1.02	,	#	ALLIER
        "4":	1	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	1	,	#	HAUTES-ALPES
        "6":	1	,	#	ALPES-MARITIMES
        "7":	1	,	#	ARDECHE
        "8":	1.02	,	#	ARDENNES
        "9":	1	,	#	ARIEGE
        "10":	1.02	,	#	AUBE
        "11":	1	,	#	AUDE
        "12":	1	,	#	AVEYRON
        "13":	1	,	#	BOUCHES-DU-RHONE
        "14":	1.02	,	#	CALVADOS
        "15":	1.02	,	#	CANTAL
        "16":	1	,	#	CHARENTE
        "17":	1	,	#	CHARENTE-MARITIME
        "18":	1	,	#	CHER
        "19":	1	,	#	CORREZE
        "21":	1.02	,	#	COTE-D'OR
        "22":	1.02	,	#	COTES-D'ARMOR
        "23":	1.02	,	#	CREUSE
        "24":	1	,	#	DORDOGNE
        "25":	1.02	,	#	DOUBS
        "26":	1.02	,	#	DROME
        "27":	1	,	#	EURE
        "28":	1	,	#	EURE-ET-LOIR
        "29":	1.02	,	#	FINISTERE
        "02A":	1.02	,	#	CORSE-DU-SUD
        "02B":	1	,	#	HAUTE-CORSE
        "30":	1	,	#	GARD
        "31":	1.02	,	#	HAUTE-GARONNE
        "32":	1	,	#	GERS
        "33":	1	,	#	GIRONDE
        "34":	1.02	,	#	HERAULT
        "35":	1.02	,	#	ILLE-ET-VILAINE
        "36":	1.02	,	#	INDRE
        "37":	1.02	,	#	INDRE-ET-LOIRE
        "38":	1.02	,	#	ISERE
        "39":	1	,	#	JURA
        "40":	1	,	#	LANDES
        "41":	1	,	#	LOIR-ET-CHER
        "42":	1.02	,	#	LOIRE
        "43":	1	,	#	HAUTE-LOIRE
        "44":	1	,	#	LOIRE-ATLANTIQUE
        "45":	1.02	,	#	LOIRET
        "46":	1.02	,	#	LOT
        "47":	1.02	,	#	LOT-ET-GARONNE
        "48":	1.02	,	#	LOZERE
        "49":	1.02	,	#	MAINE-ET-LOIRE
        "50":	1.02	,	#	MANCHE
        "51":	1.02	,	#	MARNE
        "52":	1.02	,	#	HAUTE-MARNE
        "53":	1.02	,	#	MAYENNE
        "54":	0.75	,	#	MEURTHE-ET-MOSELLE
        "55":	0.5	,	#	MEUSE
        "56":	1.02	,	#	MORBIHAN
        "57":	1.02	,	#	MOSELLE
        "58":	1	,	#	NIEVRE
        "59":	1.02	,	#	NORD
        "60":	1	,	#	OISE
        "61":	1.02	,	#	ORNE
        "62":	1	,	#	PAS-DE-CALAIS
        "63":	1.02	,	#	PUY-DE-DOME
        "64":	1	,	#	PYRENEES-ATLANTIQUES
        "65":	1	,	#	HAUTES-PYRENEES
        "66":	1	,	#	PYRENEES-ORIENTALES
        "67":	1	,	#	BAS-RHIN
        "68":	1	,	#	HAUT-RHIN
        "69":	1.02	,	#	RHONE
        "70":	1.02	,	#	HAUTE-SAONE
        "71":	1	,	#	SAONE-ET-LOIRE
        "72":	1.02	,	#	SARTHE
        "73":	1.02	,	#	SAVOIE
        "74":	1.02	,	#	HAUTE-SAVOIE
        "75":	1.02	,	#	PARIS
        "76":	1	,	#	SEINE-MARITIME
        "77":	1.02	,	#	SEINE-ET-MARNE
        "78":	1	,	#	YVELINES
        "79":	1	,	#	DEUX-SEVRES
        "80":	1.02	,	#	SOMME
        "81":	1.02	,	#	TARN
        "82":	1.02	,	#	TARN-ET-GARONNE
        "83":	1	,	#	VAR
        "84":	1	,	#	VAUCLUSE
        "85":	1.02	,	#	VENDEE
        "86":	1	,	#	VIENNE
        "87":	1.02	,	#	HAUTE-VIENNE
        "88":	1.02	,	#	VOSGES
        "89":	1.02	,	#	YONNE
        "90":	1	,	#	TERRITOIRE DE BELFORT
        "91":	1	,	#	ESSONNE
        "92":	1	,	#	HAUTS-DE-SEINE
        "93":	1.02	,	#	SEINE-SAINT-DENIS
        "94":	1.02	,	#	VAL-DE-MARNE
        "95":	1.02	,	#	VAL-D'OISE
        "101":	1	,	#	GUADELOUPE
        "102":	1	,	#	GUYANE
        "103":	1	,	#	MARTINIQUE
        "104":	1.02	,	#	LA REUNION
        "143":	2	,	#	MAYOTTE
    
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

class tdcfe_coefficient_multiplicateur_non_prof_moins_250kVA_2012(Variable):
    value_type = float 
    entity = Etablissement
    label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
    definition_period = YEAR
    def formula(etablissement, period):
        departement = etablissement("departement", period)
        taux = {
        "1":	3.05	,	#	AIN
        "2":	3.05	,	#	AISNE
        "3":	3.05	,	#	ALLIER
        "4":	3	,	#	ALPES-DE-HAUTE-PROVENCE
        "5":	3	,	#	HAUTES-ALPES
        "6":	3	,	#	ALPES-MARITIMES
        "7":	3	,	#	ARDECHE
        "8":	3.05	,	#	ARDENNES
        "9":	3	,	#	ARIEGE
        "10":	3.05	,	#	AUBE
        "11":	3	,	#	AUDE
        "12":	3	,	#	AVEYRON
        "13":	3	,	#	BOUCHES-DU-RHONE
        "14":	3.05	,	#	CALVADOS
        "15":	3.05	,	#	CANTAL
        "16":	3	,	#	CHARENTE
        "17":	3	,	#	CHARENTE-MARITIME
        "18":	3	,	#	CHER
        "19":	3	,	#	CORREZE
        "21":	3.05	,	#	COTE-D'OR
        "22":	3.05	,	#	COTES-D'ARMOR
        "23":	3.05	,	#	CREUSE
        "24":	3	,	#	DORDOGNE
        "25":	3.05	,	#	DOUBS
        "26":	3.05	,	#	DROME
        "27":	3	,	#	EURE
        "28":	3	,	#	EURE-ET-LOIR
        "29":	3.05	,	#	FINISTERE
        "02A":	3.05	,	#	CORSE-DU-SUD
        "02B":	3	,	#	HAUTE-CORSE
        "30":	3	,	#	GARD
        "31":	3.05	,	#	HAUTE-GARONNE
        "32":	3	,	#	GERS
        "33":	3	,	#	GIRONDE
        "34":	3.05	,	#	HERAULT
        "35":	3.05	,	#	ILLE-ET-VILAINE
        "36":	3.05	,	#	INDRE
        "37":	3.05	,	#	INDRE-ET-LOIRE
        "38":	3.05	,	#	ISERE
        "39":	3	,	#	JURA
        "40":	3	,	#	LANDES
        "41":	3	,	#	LOIR-ET-CHER
        "42":	3.05	,	#	LOIRE
        "43":	3	,	#	HAUTE-LOIRE
        "44":	3	,	#	LOIRE-ATLANTIQUE
        "45":	3.05	,	#	LOIRET
        "46":	3.05	,	#	LOT
        "47":	3.05	,	#	LOT-ET-GARONNE
        "48":	3.05	,	#	LOZERE
        "49":	3.05	,	#	MAINE-ET-LOIRE
        "50":	3.05	,	#	MANCHE
        "51":	3.05	,	#	MARNE
        "52":	3.05	,	#	HAUTE-MARNE
        "53":	3.05	,	#	MAYENNE
        "54":	2.25	,	#	MEURTHE-ET-MOSELLE
        "55":	1.5	,	#	MEUSE
        "56":	3.05	,	#	MORBIHAN
        "57":	3.05	,	#	MOSELLE
        "58":	3	,	#	NIEVRE
        "59":	3.05	,	#	NORD
        "60":	3	,	#	OISE
        "61":	3.05	,	#	ORNE
        "62":	3	,	#	PAS-DE-CALAIS
        "63":	3.05	,	#	PUY-DE-DOME
        "64":	3	,	#	PYRENEES-ATLANTIQUES
        "65":	3	,	#	HAUTES-PYRENEES
        "66":	3	,	#	PYRENEES-ORIENTALES
        "67":	3	,	#	BAS-RHIN
        "68":	3	,	#	HAUT-RHIN
        "69":	3.05	,	#	RHONE
        "70":	3.05	,	#	HAUTE-SAONE
        "71":	3	,	#	SAONE-ET-LOIRE
        "72":	3.05	,	#	SARTHE
        "73":	3.05	,	#	SAVOIE
        "74":	3.05	,	#	HAUTE-SAVOIE
        "75":	3.05	,	#	PARIS
        "76":	3	,	#	SEINE-MARITIME
        "77":	3.05	,	#	SEINE-ET-MARNE
        "78":	3	,	#	YVELINES
        "79":	3	,	#	DEUX-SEVRES
        "80":	3.05	,	#	SOMME
        "81":	3.05	,	#	TARN
        "82":	3.05	,	#	TARN-ET-GARONNE
        "83":	3	,	#	VAR
        "84":	3	,	#	VAUCLUSE
        "85":	3.05	,	#	VENDEE
        "86":	3	,	#	VIENNE
        "87":	3.05	,	#	HAUTE-VIENNE
        "88":	3.05	,	#	VOSGES
        "89":	3.05	,	#	YONNE
        "90":	3	,	#	TERRITOIRE DE BELFORT
        "91":	3	,	#	ESSONNE
        "92":	3	,	#	HAUTS-DE-SEINE
        "93":	3.05	,	#	SEINE-SAINT-DENIS
        "94":	3.05	,	#	VAL-DE-MARNE
        "95":	3.05	,	#	VAL-D'OISE
        "101":	3	,	#	GUADELOUPE
        "102":	3	,	#	GUYANE
        "103":	3	,	#	MARTINIQUE
        "104":	3.05	,	#	LA REUNION
        "143":	6	,	#	MAYOTTE
    
        
        "manquant" : 0}

        departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
        resultat = taux.get(departement_str, taux["manquant"])
        return resultat

