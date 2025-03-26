#faut remplacer celles suivantes avec ""
#"	<
#	"<

# class tdcfe_coefficient_multiplicateur_(Variable):
#     value_type = float 
#     entity = Etablissement
#     label = "le coefficient multiplicateur du département pour le tdcfe en 2012" #nomencultures des activités françaises
#     definition_period = YEAR
#     def formula(etablissement, period):
#         departement = etablissement("departement", period)
#         taux = {
            
        
#         "manquant" : 4}

#         departement_str = str(departement[0])  # car c’est un tableau numpy apparemment
#         resultat = taux.get(departement_str, taux["manquant"])
#         return resultat