import netCDF4 as nc
import pandas as pd
import numpy as np

# Chargement du fichier XLSX en utilisant la bibliothèque pandas
df = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)

# Création d'un nouveau fichier netCDF
netcdf_file = "test_9087654.nc"
dataset = nc.Dataset(netcdf_file, "w", format="NETCDF4") # type: ignore

# Création des dimensions
lat = dataset.createDimension("latitude", len(df))
lon = dataset.createDimension("longitude", len(df))

# Création des variables
# latitude = dataset.createVariable("latitude", "f4", ("latitude",))
# longitude = dataset.createVariable("longitude", "f4", ("longitude",))
doc = dataset.createVariable("doc", "f4", ("latitude", "longitude"))


# Conversion de la colonne "doc" en une liste Python
doc_data = df["doc"].to_list()

# Assigner les nouvelles valeurs à la variable "doc"
doc[:, :] = np.array(doc_data).reshape(len(df), 1)

dataset.close()
