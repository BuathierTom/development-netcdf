import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime

# Version 1 avec Xarray, mais qui ne fonctionne pas car les dimensions n'ont pas le même nombre de valeurs.

df_t1 = pd.read_excel("./data/jeu_temps1.xlsx", keep_default_na=False)
df_t2 = pd.read_excel("./data/jeu_temps2.xlsx", keep_default_na=False)
df_t3 = pd.read_excel("./data/jeu_temps3.xlsx", keep_default_na=False)

# On récupere les colonnes :
# T1
pression_t1 = df_t1["Pression"]
# Tout les noms des colonnes sauf celui de la pression
lambda_t1 = [col for col in df_t1.columns if col != "Pression"]
# on recupere toutes les données des colonnes sauf celle de la pression pour la mettre dans une liste
data_t1 = df_t1[lambda_t1].values.tolist()

# T2
pression_t2 = df_t2["Pression"]
lambda_t2 = [col for col in df_t2.columns if col != "Pression"]
data_t2 = df_t2[lambda_t2].values.tolist()

# T3
pression_t3 = df_t3["Pression"]
lambda_t3 = [col for col in df_t3.columns if col != "Pression"]
data_t3 = df_t3[lambda_t3].values.tolist()


# on ajoute toute les datas dans une seule liste
data = data_t1 + data_t2 + data_t3

# Récuperation pour le fichier NetCDF

pression = pression_t1.tolist()

pression.remove('') 

lambda_ = lambda_t1

data = data_t1 + data_t2 + data_t3

temps = ["T1", "T2", "T3"]


# on cree le fichier netCDF 
ds = xr.Dataset(
    data_vars={
        "pression": (("time"), pression),
        "eclairement": (("lambda", "time"), data),
    },
    coords={
        "time": temps,
        "lambda": lambda_,
    },
    attrs={
        "auteur": "Moi",
        "description": "Jeu de données",
    },
)

print(ds)

# on enregistre le fichier netCDF
ds.to_netcdf("eclairement.nc")

############################################################################################################

# Version avec Pandas, non fonctionnel car pas de dimensions qui vont bien.

# df_t1["time"] = temps


# df_t1["coord"] = df_t1[['time', 'lambda']].apply(tuple, axis=1)
# df_t1 = df_t1.loc[:,["time", "lambda", "pression", "eclairement"]]
# df_t1.set_index(['time', 'lambda'], inplace=False)

# print(df_t1.to_xarray())