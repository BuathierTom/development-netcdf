import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc4

def nc_to_xlsx__FLUO(path):
    
    ds = nc4.Dataset('OS_AMAZOMIX-ALL_CTD.nc') # type: ignore

    # On recupere les variables
    var = ds.variables

    # Pour chaque liste de FLU2 récuperer on créé un fichier associe avec les valeurs
    # On recupere les valeurs de la variable FLU2
    flu2 = var['FLU2'][:]
    # On recupere les valeurs de la variable FLU2_QC
    flu2qc = var['FLU2_QC'][:]
    # On recupere les valeurs de la variable DEPTH
    depth = var['DEPTH'][:]

    for i in range(len(flu2)):
        # On créé un fichier xlsx pour stocker les valeurs pour chaque ligne du tableau flu2 et flu2qc
        df = pd.DataFrame({'DEPTH': depth[i],'FLU2': flu2[i], 'FLU2_QC': flu2qc[i]})
        # On sauvegarde le fichier
        df.to_excel('./'+path+'/fluorimetrie'+str(i)+'.xlsx')
    print("Fichiers sauvegardés avec succès")
        
def nc_to_xlsx__TRANS(path):
    
    ds = nc4.Dataset('OS_AMAZOMIX-ALL_CTD.nc') # type: ignore

    # On recupere les variables
    var = ds.variables

    # Pour chaque liste de FLU2 récuperer on créé un fichier associe avec les valeurs
    # On recupere les valeurs de la variable FLU2
    tur3 = var['TUR3'][:]
    # On recupere les valeurs de la variable FLU2_QC
    tur3qc = var['TUR3_QC'][:]
    # On recupere les valeurs de la variable DEPTH
    depth = var['DEPTH'][:]

    for i in range(len(tur3)):
        # On créé un fichier xlsx pour stocker les valeurs pour chaque ligne du tableau flu2 et flu2qc
        df = pd.DataFrame({'DEPTH': depth[i],'TUR3': tur3[i], 'TUR3_QC': tur3qc[i]})
        # On sauvegarde le fichier
        df.to_excel('./'+path+'/transmission'+str(i)+'.xlsx')
    print("Fichiers sauvegardés avec succès")



if __name__ == "__main__":
    path_fluo = 'TEST_FLUO_TRANS/FLUORIMETRIE/'
    path_trans = 'TEST_FLUO_TRANS/TRANSMISSION/'
    # path_radeau = 'TESTS/XLSX_RADEAU/'
    
    # nc_to_xlsx__FLUO(path_fluo)
    # nc_to_xlsx__TRANS(path_trans)
    