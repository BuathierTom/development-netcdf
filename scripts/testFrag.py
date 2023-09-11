import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime

df = pd.read_excel("./data/test.xlsx", keep_default_na=False)

# on récupère les données
jour = df["jour"].tolist()
heure = df["heure"].tolist()
# 
mission = df["mission"].tolist()
num_station = df["num_station"].tolist()
lat = df["lat"].tolist()
lon = df["lon"].tolist()
profondeur = df["profondeur"].tolist()
chla = df["chla"].tolist()
mes = df["mes"].tolist()
doc = df["doc"].tolist()
poc = df["poc"].tolist()


# On compte le nombre de lignes du fichier XLSX
row = len(df) # 3334

# On récupère seulement la date
jour = [str(jour[i])[:10] for i in range(len(jour))]
heure_str = [str(h) for h in heure]
# si il y a pas d'hreures, on met 00:00:00
for i in range(len(heure_str)):
    if heure_str[i] == "":
        heure_str[i] = "00:00:00"
    else:
        heure_str[i] = heure_str[i]

# On convertit la date avec jour et heure_str en ce modèle : 1995-10-11T15:25:00Z
liste_combinee = []
for i in range(len(jour)):
    date_str = jour[i] + "T" + heure_str[i] + "Z"
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    liste_combinee.append(date)
    
df["time"] = liste_combinee

df2 = df.copy()

df2["coord"] = df2[['lat', 'lon']].apply(tuple, axis=1)
df2 = df2.loc[:,["mission", "num_station", "lat", "lon", "time", "profondeur","chla", "doc", "poc", "mes",   ]]
df2.set_index(['lat', 'lon'], inplace=False)


print(df2.to_xarray())

# # ------------ GLOBAL -----------
df2.attrs["Conventions"] = "CF-1.6"
df2.attrs["title"] = "TEST"
df2.attrs["institution"] = "LOG"

df2.to_xarray().to_netcdf("test.nc")



