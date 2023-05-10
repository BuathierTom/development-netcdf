import pandas as pd
from netCDF4 import Dataset #type: ignore

def convert_xlsx_to_netcdf(xlsx_file, netcdf_file):
    # Lire les données du fichier XLSX en utilisant Pandas
    df = pd.read_excel(xlsx_file)

    # Extraire les dimensions et les variables des données
    dimensions = df.columns.tolist()
    variables = df.values.T.tolist()

    # Créer un fichier NetCDF
    nc_file = Dataset(netcdf_file, 'w')

    # Créer les dimensions dans le fichier NetCDF
    for dimension in dimensions:
        nc_file.createDimension(dimension, len(df[dimension]))

    # Créer les variables dans le fichier NetCDF
    for i, variable in enumerate(variables):
        nc_var = nc_file.createVariable(dimensions[i], variable.dtype, dimensions)
        nc_var[:] = variable

    # Fermer le fichier NetCDF
    nc_file.close()

    print("Conversion terminée avec succès!")

# Exemple d'utilisation
xlsx_file = "./data/doc_file_log.xlsx"
netcdf_file = "donnees.nc"
convert_xlsx_to_netcdf(xlsx_file, netcdf_file)