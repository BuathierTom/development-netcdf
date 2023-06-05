import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime

df = pd.read_excel("./data/bresil.xlsx", keep_default_na=False)

# On récupère les colonnes "jour" et "heure" et "doc" du fichier XLSX
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
liste_combinee = [jour[i] + "T" + heure_str[i] for i in range(len(jour))]

# On créé un dataset avec les données
ds = xr.Dataset(
    {
        "mission": ("row", mission),
        "num_station": ("row", num_station),
        "lat": ("row", lat),
        "lon": ("row", lon),
        "time" : ("row", liste_combinee),
        "profondeur": ("row", profondeur),
        "chla": ("row", chla),
        "mes": ("row", mes),
        "doc": ("row", doc),
        "poc": ("row", poc),
    },
    
)

# On ajoute les attributs   
ds["lat"].attrs["units"] = "degrees_north"
ds["lat"].attrs["long_name"] = "Latitude"
ds["lat"].attrs["standard_name"] = "latitude"
ds["lat"].attrs["axis"] = "Y"

ds["lon"].attrs["units"] = "degrees_east"
ds["lon"].attrs["long_name"] = "Longitude"
ds["lon"].attrs["standard_name"] = "longitude"
ds["lon"].attrs["axis"] = "X"

ds["profondeur"].attrs["units"] = "m"
ds["profondeur"].attrs["long_name"] = "Profondeur"

ds["chla"].attrs["units"] = "µg.L-1"
ds["chla"].attrs["long_name"] = "Chlorophylle a"

ds["mes"].attrs["units"] = "µg.L-1"
ds["mes"].attrs["long_name"] = "Matière en suspension"

ds["doc"].attrs["units"] = "µmol.L-1"
ds["doc"].attrs["long_name"] = "Dissolved organic carbon"

ds["poc"].attrs["units"] = "µmol.L-1"
ds["poc"].attrs["long_name"] = "Particulate organic carbon"



# ------------ GLOBAL -----------
ds.attrs["Conventions"] = "CF-1.6"
ds.attrs["title"] = "Dissolved organic carbon"
ds.attrs["institution"] = "CNRS"


print(ds)

# On enregistre le fichier netCDF
ds.to_netcdf("bresil.nc")
