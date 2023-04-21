import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc4

def test():
    # Ouvrir le xlsx et on garde les données dans le meme ordre
    
    df = pd.read_excel("./data/data_example/data_compilees_grappe/compil_Guyane_Nov2017_J1-2_181.xlsx", keep_default_na=False)    
    # , sheet_name="Sheet1"
    
    # print(df.iloc[1])
    
    # On recupere les noms des colonnes
    col_names = df.columns.tolist()

    # fais le tris dans les données : on supprime les parenthèses MAIS on garde les valeurs entre parenthèse
    # Par exemple : 'Time(ms)' on stock dans une variable 'Time' et on garde la valeur 'ms'
    # On créé une liste vide pour stocker les noms des colonnes
    col_names_clean = []
    # On créé une liste vide pour stocker les unités
    col_units = []
    # On créé une liste vide pour les noms des colonnes qui n'ont pas d'unité
    col_names_no_unit = []

    # On parcours la liste des noms des colonnes
    for col_name in col_names:
        # si il n'y a pas de parenthèses dans le nom de la colonne on l'ajoute dans la liste des noms de colonnes mais pas dans la liste des unités
        if "(" in col_name and "Beta" not in col_name:
        # On récupere les valeurs entre parenthèses
            col_unit = col_name[col_name.find("(")+1:col_name.find(")")]
            # On supprime les parenthèses
            col_name = col_name.replace("("+col_unit+")", "")
            # On ajoute le nom de la colonne dans la liste des noms de colonnes
            col_names_clean.append(col_name)
            # On ajoute l'unité dans la liste des unités
            col_units.append(col_unit)
        else:
            # On ajoute le nom de la colonne dans la liste des noms de colonnes sans unité
            col_names_no_unit.append(col_name)     

    # On créé un dictionnaire pour stocker les noms des colonnes et les unités
    col_names_units = dict(zip(col_names_clean, col_units))

    # On met les parametres globaux
    global_attributes = {
        'title': 'Data from Guyane',
        'institution': 'CNRS',
        'source': 'Data from Guyane',
        'history': 'Created by the CNRS',
        'references': 'https://www.cnrs.fr/',
        'comment': 'Data from Guyane',
        'Conventions': 'CF-1.6',
    }
    # on choppe les valeurs de la colonne en rajoutant le nom de la colonne et l'unite
    # time = sorted(list(set(df[col_names_clean[0]+"("+col_names_units[col_names_clean[0]]+")"])))

    # On fais pareil pour toutes les autres colonnes
    # On créé une liste vide pour stocker les valeurs de chaque colonne
    col_values1 = []
    col_names_values = {}
    # On parcours la liste des noms de colonnes
    for col_name in col_names_clean:
        # On ajoute les valeurs de la colonne dans la liste des valeurs
        col_values1.append(list(df[col_name+"("+col_names_units[col_name]+")"]))
        # print(col_values1)
    # On créé un dictionnaire pour stocker les noms des colonnes et les valeurs
    col_names_values = dict(zip(col_names_clean, col_values1))
    
    # print(col_names_values)

    # On créé une liste vide pour stocker les valeurs de chaque colonne (sans unité)
    col_values2 = []
    # On parcours la liste des noms de colonnes
    for col_name in col_names_no_unit:
        # On ajoute les valeurs de la colonne dans la liste des valeurs
        col_values2.append(list(df[col_name]))

    # On créé un dictionnaire pour stocker les noms des colonnes et les valeurs 
    col_names_values2 = dict(zip(col_names_no_unit, col_values2))

    # On créé la dataset
    ds = xr.Dataset(
        coords = {
            # On prend les valeurs de col_names_values en fonction du nom
            i: (i, col_names_values[i]) for i in col_names_clean
        },  
        
        # data_vars= {
        #     # On prend les valeurs de col_names_values2 en fonction de leur nom contenu dans col_names_no_unit
        #     col_name: (col_names_values2[col_name]) for col_name in col_names_no_unit
        #     },
        attrs = global_attributes
    )

    print(ds)

    # on créé le fichier netcdf avec la dataset
    ds.to_netcdf('okeyy.nc')




if __name__ == "__main__":
    test()