import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime

df = pd.read_excel("./data/Autres/bre1.xlsx", keep_default_na=False)

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
    
# Pour chla, mes, doc, poc on les definit comme float et si il y a pas de valeur, on met NaN
for i in range(len(chla)):
    if chla[i] == "":
        chla[i] = np.nan
    else:
        chla[i] = float(chla[i])

for i in range(len(mes)):
    if mes[i] == "":
        mes[i] = np.nan
    else:
        mes[i] = float(mes[i])

for i in range(len(doc)):
    if doc[i] == "":
        doc[i] = np.nan
    else:
        doc[i] = float(doc[i])

for i in range(len(poc)):
    if poc[i] == "":
        poc[i] = np.nan
    else:
        poc[i] = float(poc[i])

# 



# On créé un dataset avec les données
ds = xr.Dataset(
    {
        "mission": ("row", mission),
        "num_station": ("row", num_station),
        
        "lat": ("row", lat, 
                    {'units': 'degrees_north',
                     'long_name': 'Latitude',
                     'standard_name': 'latitude',
                     'axis': 'Y'}),
        
        "lon": ("row", lon,
                    {'units': 'degrees_east',
                     'long_name': 'Longitude',
                     'standard_name': 'longitude',
                     'axis': 'X'}),
        
        "time" : ("row", liste_combinee, 
                    {'long_name': 'Start Time',
                     'standard_name': 'time',
                     'axis': 'T'}),
        
        "profondeur": ("row", profondeur,
                        {'units': 'm',
                         'long_name': 'Profondeur'}),
        
        "chla": ("row", chla,
                    {'units': 'µg.L-1',
                     'long_name': 'Chlorophylle a'}),
        
        "mes": ("row", mes,
                    {'units': 'µg.L-1',
                     'long_name': 'Matière en suspension'}),
        
        "doc": ("row", doc,
                    {'units': 'µmol.L-1',
                     'long_name': 'Dissolved organic carbon'}),
        
        "poc": ("row", poc,
                    {'units': 'µmol.L-1',
                     'long_name': 'Particulate organic carbon'}),
        
    },
    
        coords={
        # row doit commencer à 1737
        "row": np.arange(row),
    },
)

# ------------ GLOBAL -----------
ds.attrs["Conventions"] = "CF-1.6"
ds.attrs["title"] = "Données de la campagne BRESIL"
ds.attrs["institution"] = "CNRS"

# ds["time"].attrs["units"] = "seconds since 1995-10-11 15:25:00"

print(ds)

# On enregistre le fichier netCDF
ds.to_netcdf("bre1.nc")

