import pandas as pd
import xarray as xr
import numpy as np

df = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)

# On récupère les colonnes "lat" et "lon" et "doc" du fichier XLSX
lat = df["lat"].tolist()
lon = df["lon"].tolist()
doc = df["doc"].tolist()

# On transforme les listes en np.array
lat = np.array(lat, dtype=object)
lon = np.array(lon, dtype=object)

doc = np.append(doc, np.zeros(1626 - len(doc)))

# Création du DataArray
doc_grid = np.zeros((1626, 1626))
for i in range(len(lat)):
    for j in range(len(lon)):
        doc_grid[i, j] = doc[i]

# Création du DataArray
da = xr.DataArray(doc_grid, dims=["lat", "lon"], coords={"lat": lat, "lon": lon})

# Création du Dataset
ds = xr.Dataset({"doc": da})


# ----------- DOC -----------
ds["doc"].attrs["units"] = "µmol.L-1"
ds["doc"].attrs["long_name"] = "Dissolved organic carbon"
ds["doc"].attrs["_FillValue"] = -999  # Le _FillValue est utilisé pour dire au fichier netCDF que la valeur -999 est une valeur manquante
# ----------- LAT -----------
ds["lat"].attrs["units"] = "degrees_north"
ds["lat"].attrs["long_name"] = "Latitude"
ds["lat"].attrs["_FillValue"] = -999
# ----------- LON -----------
ds["lon"].attrs["units"] = "degrees_east"
ds["lon"].attrs["long_name"] = "Longitude"
ds["lon"].attrs["_FillValue"] = -999
# ------------ GLOBAL -----------
ds.attrs["Conventions"] = "CF-1.6"
ds.attrs["title"] = "Dissolved organic carbon"
ds.attrs["institution"] = "CNRS"

print(ds)

# On enregistre le fichier netCDF
ds.to_netcdf("test.nc")
