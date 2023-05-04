import numpy as np
from scipy.interpolate import griddata
from netCDF4 import *
import pandas as pd

# Charger les données à partir du fichier Excel
data = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)

# Créer un fichier netCDF4 et définir ses dimensions
dataset = Dataset('test_doc.nc', 'w', format='NETCDF4') #type: ignore

# Extraire les valeurs de lat, lon et doc
lat = data['lat'].values
lon = data['lon'].values
doc = data['doc'].values


# Pour chaque valeur de la liste lat, lon et doc, vérifier si elle est vide et si elle est vide alors on la remplace par 0
lat = [x if x != '' else 0 for x in lat]
lon = [x if x != '' else 0 for x in lon]
doc = [x if x != '' else 0 for x in doc]

# Créer une grille de latitude et de longitude avec une résolution de 0,1 degré
lat_grid = np.arange(np.floor(np.min(lat)), np.ceil(np.max(lat))+0.1, 0.1)
lon_grid = np.arange(np.floor(np.min(lon)), np.ceil(np.max(lon))+0.1, 0.1)

# Créer une grille de points de latitude et de longitude
lat_points, lon_points = np.meshgrid(lat_grid, lon_grid)

# Interpoler les données sur la grille
doc_grid = griddata((lat, lon), doc, (lat_points, lon_points), method='linear')

latitude = dataset.createDimension('lat', None)
longitude = dataset.createDimension('lon', None)

# Créer des variables dans le fichier netCDF4
lats = dataset.createVariable('lat', np.float32, (latitude,))
lons = dataset.createVariable('lon', np.float32, (longitude,))
docs = dataset.createVariable('doc', np.float32, (latitude, longitude))


# Ajouter les valeurs aux variables
docs[:] = doc_grid.astype(np.float32)
lats[:] = lat_grid
lons[:] = lon_grid

# Ajouter des attributs aux variables
docs.units = 'kg/m2'
lats.units = 'degrees_north'
lons.units = 'degrees_east'
docs.long_name = 'Example tests'

# Fermer le fichier netCDF4
dataset.close()
