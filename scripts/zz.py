import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from netCDF4 import *

# Charger les données à partir d'un fichier Excel
data = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)

# Filtrer les données manquantes et convertir les colonnes de latitude et de longitude en flottants
data = data.dropna()
lat = data['lat']
lon = data['lon']
doc = data['doc']

lat = [x for x in lat if x != '']
lon = [x for x in lon if x != '']
doc = [x for x in doc if x != '']

# Définir les limites de la grille de latitude et de longitude
lat_min = min(lat)
lat_max = max(lat)
lon_min = min(lon)
lon_max = max(lon)

# Définir la résolution de la grille
resolution = 0.01

# Créer une grille de latitude et de longitude
lat_grid, lon_grid = np.mgrid[lat_min:lat_max:resolution, lon_min:lon_max:resolution]

# Interpoler les données sur la grille
doc_grid = griddata((lat, lon), doc, (lat_grid, lon_grid), method='nearest')

# Créer un fichier netCDF4 et définir ses dimensions
dataset = Dataset('doc_file_log_interp.nc', 'w', format='NETCDF4') #type: ignore

# Créer des dimensions dans le fichier netCDF4
latitude = dataset.createDimension('lat', lat_grid.shape[0])
longitude = dataset.createDimension('lon', lon_grid.shape[1])

# Créer des variables dans le fichier netCDF4
docs = dataset.createVariable('doc', np.float32, ('lat', 'lon'))
lats = dataset.createVariable('lat', np.float32, ('lat',))
lons = dataset.createVariable('lon', np.float32, ('lon',))

# Ajouter les valeurs aux variables
docs[:] = doc_grid.astype(np.float32)
lats[:] = lat_grid[:, 0]
lons[:] = lon_grid[0, :]

# Ajouter des attributs aux variables
docs.units = 'kg/m2'
lats.units = 'degrees_north'
lons.units = 'degrees_east'
docs.long_name = 'Document Quantity'

# Fermer le fichier netCDF4
dataset.close()

