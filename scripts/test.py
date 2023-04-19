import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc4

# # Pour lire les fichiers csv
# # df = pd.read_csv('./CSV/HFradar_MonthlyAveraged_May2012_Sept2014_2d93_8824_92e9.csv')
# # # on recupere la premiere ligne du csv qui contient les noms des colonnes et on la met dans une liste de noms
# # col_names = df.columns.tolist()
# # df = df.set_index(col_names)

# # xr = df.to_xarray()
# # nc = xr.to_netcdf('./NC/zwip.nc')

# Pour lire les fichiers xlsx
df = pd.read_excel('data_example/data_compilees_grappe/compil_Guyane_Nov2017_J1-2_181.xlsx')
col_names = df.columns.tolist()
col_vals = df.iloc[:,0].tolist()


for i in range(len(col_names)):
    if col_names[i].startswith('Beta'):
        print(" ")
    
    #  si la premiere case est vide 
    elif col_names[i].startswith('Unnamed'):
    # on regarde les valeurs et si elles contients le format Timestamp
        if col_vals[i].startswith('Timestamp'):
            # on met le nom de la colonne à la date
            col_names[i] = 'Time'
        
    else:    
        col_names[i] = col_names[i].split('(')[0]
        col_names[i] = col_names[i].strip()
        col_names[i] = col_names[i].split(')')[0]

        

    
df.columns = col_names

# On met la premiere colonne comme index
df = df.set_index(col_names)

# On les convertit pour les mettre dans un fichier netcdf
xr = df.to_xarray()
nc = xr.to_netcdf('zwip.nc')
print("Created")

## On utilise xarray pour lire le fichier 
# ds = nc4.Dataset('OS_AMAZOMIX-ALL_CTD.nc') # type: ignore

# # On recupere les variables
# var = ds.variables
# # On recupere les dimensions
# dim = ds.dimensions
# # On récupere les attributs et leurs valeurs
# att = ds.__dict__
# # on les affiche avec leur noms devant
# # print("Variables: ", var)
# print("Dimensions: ", dim)
# print("Attributs: ", att)




# # Pour chaque liste de FLU2 récuperer on créé un fichier associe avec les valeurs
# # On recupere les valeurs de la variable FLU2
# flu2 = var['FLU2'][:]
# # On recupere les valeurs de la variable FLU2_QC
# flu2qc = var['FLU2_QC'][:]

# for i in range(len(flu2)):
#     # On créé un fichier xlsx pour stocker les valeurs pour chaque ligne du tableau flu2 et flu2qc
#     df = pd.DataFrame({'FLU2': flu2[i], 'FLU2_QC': flu2qc[i]})
#     # On sauvegarde le fichier
#     df.to_excel('./zwip/test'+str(i)+'.xlsx')
    

# # On créé un fichier xlsx pour stocker les valeurs pour chaque ligne du tableau flu2 et flu2qc
# df = pd.DataFrame({'FLU2': flu2, 'FLU2_QC': flu2qc})
# # # On sauvegarde le fichier
# df.to_excel('test.xlsx')


oof = ['2021-12342534', '2022-879654', 'nan']

for i in range(len(oof)):
    if oof[i].startswith('2021'):
        print("yes")
    elif oof[i].startswith('2022'):
        print("no")
    else:
        print("nan")

