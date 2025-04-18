import pandas as pd

# Chargement des préférences des étudiants et des universités
df_etudiants = pd.read_excel("D:/MyDataSet/Preferences_Etudiants.xlsx")
df_universites = pd.read_excel("D:/MyDataSet/Preferences_Universites.xlsx")


# Transformation en dictionnaires
# Création du dictionnaire avec chaque étudiant et sa liste de préférences
preferences_etudiants = {}
for i, row in df_etudiants.iterrows():
    nom_etudiant = row["Etudiant"]
    # Exclure la première colonne (nom) et garder uniquement les préférences
    preferences = [uni for uni in row[1:].tolist() if pd.notna(uni)]
    preferences_etudiants[nom_etudiant] = preferences

# Création du dictionnaire avec chaque université et sa liste de préférences
preferences_universites = {}
for i, row in df_universites.iterrows():
    nom_universite = row["Université"]
    # Exclure la première colonne (nom) et garder uniquement les préférences
    preferences = [etu for etu in row[1:].tolist() if pd.notna(etu)]
    preferences_universites[nom_universite] = preferences
    

def gale_shapley(preferences_etudiants, preferences_universites):
    # Initialisation de tous les étudiants comme libres
    etudiants_libres = list(preferences_etudiants.keys())
    
    # Dictionnaire pour garder l’université assignée à chaque étudiant
    appariements = {}
    
    # Dictionnaire pour garder l’étudiant assigné à chaque université
    universite_partenaire = {}

    # Pour suivre à qui chaque étudiant a déjà proposé
    propositions_faites = {etudiant: [] for etudiant in preferences_etudiants}

    while etudiants_libres:
        etudiant = etudiants_libres[0]  # Prend un étudiant libre

        # Obtenir la prochaine université à qui il n'a pas encore proposé
        for universite in preferences_etudiants[etudiant]:
            if universite not in propositions_faites[etudiant]:
                propositions_faites[etudiant].append(universite)

                if universite not in universite_partenaire:
                    # Si l'université n'a pas encore de partenaire, accepte la proposition
                    appariements[etudiant] = universite
                    universite_partenaire[universite] = etudiant
                    etudiants_libres.pop(0)
                else:
                    partenaire_actuel = universite_partenaire[universite]
                    # Vérifie si l'université préfère le nouvel étudiant
                    if preferences_universites[universite].index(etudiant) < preferences_universites[universite].index(partenaire_actuel):
                        # Nouveau plus préféré, switch
                        universite_partenaire[universite] = etudiant
                        appariements[etudiant] = universite
                        etudiants_libres.pop(0)
                        etudiants_libres.append(partenaire_actuel)  # L'ancien partenaire devient libre
                        del appariements[partenaire_actuel]
                    # Sinon, l’université rejette l’étudiant, on continue avec le suivant
                break  # Sortir du for une fois qu'on a proposé

    return appariements



appariements_final = gale_shapley(preferences_etudiants, preferences_universites)

# Affichage des résultats 
print("\n APPARIEMENTS FINAUX \n")
for etudiant, universite in appariements_final.items():
    print(f"{etudiant} est assigné à {universite}")
