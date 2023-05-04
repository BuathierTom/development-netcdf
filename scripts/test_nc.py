from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import *

"""
    Programme a but de test pour avoir un fichier netcdf en utilisant la bibliothèque netCDF4
"""

data = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)


# Créer un fichier netCDF4 et définir ses dimensions
dataset = Dataset('test_doc_nc.nc', 'w', format='NETCDF4') # type: ignore

# on recupere les valeur de la colonne lat
lat = data['lat'].values
lon = data['lon'].values
doc = data['doc'].values

print(lat)



# # Définir les limites de la grille de latitude et de longitud

# On enleve les '' de toutes les listes
lat = [x for x in lat if x != '']
lon = [x for x in lon if x != '']
doc = [x for x in doc if x != '']

# on prend le plus petit de la liste
lat_min = min(lat)

lat_max = max(lat)
lon_min = min(lon)
lon_max = max(lon)

latitude = dataset.createDimension('lat', len(lat))
longitude = dataset.createDimension('lon', len(lon))

# Créer des variables dans le fichier netCDF4
docs = dataset.createVariable('doc', np.float32, (latitude, longitude))
lats = dataset.createVariable('lat', np.float32, (latitude,))
lons = dataset.createVariable('lon', np.float32, (longitude,))


lats[:] = lat
lons[:] = lon
docs[:] = np.reshape(doc, (lat_min, lat_max))





# Fermer le fichier netCDF4
dataset.close()






