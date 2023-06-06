from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import *

# A installer pour pouvoir utiliser les bibliothèques
# pip install netCDF4 
# pip install xarray
# pip install pandas
# pip install numpy

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

# Définir les limites de la grille de latitude et de longitude

# lat = data['lat'].replace(to_replace = '', value = 0)

# lon = data['lon'].replace(to_replace = '', value = 0)

# doc = data['doc'].replace(to_replace = '', value = 0)

# On ne considère pas les valeurs égales à -999
lat = lat[lat != -999]
lon = lon[lon != -999]
doc = doc[doc != -999]

print(doc)

latitude = dataset.createDimension('lat', 1716)
longitude = dataset.createDimension('lon', 1716)

# Créer les variables lat, lon et doc
lats = dataset.createVariable('lat', np.float64, ('lat',))
lons = dataset.createVariable('lon', np.float64, ('lon',))

docs = dataset.createVariable('doc', np.float64, ('lat', 'lon'))


# on créé des listes arranger avec numpy de lat et lon entre -90 et 90 et que la liste soit de taille 1544
lat = np.linspace(min(lat),max(lat), 1716)
lon = np.linspace(min(lon),max(lon), 1716)

# On rajoute des valeurs à la liste doc pour qu'elle soit de taille 1716
doc = np.append(doc, np.zeros(1716 - len(doc)))

lats[:] = lat
lons[:] = lon
docs[:] = doc

docs.units = 'µmol.L-1'
lats.units = 'degrees_north'
lons.units = 'degrees_east'
docs.long_name = 'Dissolved Organic Carbon'

# Fermer le fichier netCDF4
dataset.close()






