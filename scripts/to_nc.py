import os
import pandas as pd
import xarray as xr

def xlsx_to_nc(path):
    # On recupere le nom de tout les fichiers dans le dossier CSV
    # path = './CSV/'
    files = os.listdir(path)

    # On cree une liste vide pour y mettre les noms des colonnes
    col_names = []

    # On lit tout les fichiers du dossier XLSX
    for file in files:
        df = pd.read_excel(path + file) # pd.read_csv(path + file) -> pour les csv
        col_names = df.columns.tolist()
        # récupere le contenu de la premiere colonne du fichier
        col_vals = df.iloc[:,0].tolist()
        # Pour chaque element de la liste, on les met entre ''
        col_vals = [str(i) for i in col_vals]
        col_names = [str(i) for i in col_names]
        
        
        for i in range(len(col_names)):
            if col_names[i].startswith('Unnamed'):
                # on regarde les valeurs et si elles contients le format Timestamp
                if col_vals[i].startswith('2021'):
                    # On remplace le nom de la colonne Unnamed par Time
                    col_names[i] = 'Time'
            elif col_names[i].startswith('Beta'):
                print(" ")
                
            else:    
                col_names[i] = col_names[i].split('(')[0]
                col_names[i] = col_names[i].strip()
                col_names[i] = col_names[i].split(')')[0]
                
        df.columns = col_names
        
        df = df.set_index(col_names)
        # On les convertit pour les mettre dans un fichier netcdf
        xr = df.to_xarray()
        nc = xr.to_netcdf('./TESTS/XLSX_RADEAU/' + file[:-5] +'.nc')
    
    
if __name__ == "__main__":
    path = './data_example/data_radeau/'
    xlsx_to_nc(path)
 