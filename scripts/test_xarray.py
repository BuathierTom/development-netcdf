from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc4

def test_grappe():
    # Ouvrir le xlsx et on garde les données dans le meme ordre
    
    df = pd.read_excel("./data/data_example/data_compilees_grappe/compil_Guyane_Nov2017_J1-2_181.xlsx", keep_default_na=False)    
    # , sheet_name="Sheet1"
    
    # print(df.iloc[1])
    
    # On recupere les noms des colonnes
    col_names = df.columns.tolist()

    # fais le tris dans les données : on supprime les parenthèses MAIS on garde les valeurs entre parenthèses
    # Par exemple : 'Time(ms)' on stock dans une variable 'Time' et on garde la valeur 'ms'
    # On créé une liste vide pour stocker les noms des colonnes
    col_names_clean = []
    # On créé une liste vide pour stocker les unités
    col_units = []
    # On créé une liste vide pour les noms des colonnes qui n'ont pas d'unité
    col_names_no_unit = []

    # On parcours la liste des noms des colonnes
    for col_name in col_names:
        # si il n'y a pas de parenthèses dans le nom de la colonne on l'ajoute dans la liste des noms de colonnes mais pas dans la liste des unités
        if "(" in col_name and "Beta" not in col_name:
        # On récupere les valeurs entre parenthèses
            col_unit = col_name[col_name.find("(")+1:col_name.find(")")]
            # On supprime les parenthèses
            col_name = col_name.replace("("+col_unit+")", "")
            # On ajoute le nom de la colonne dans la liste des noms de colonnes
            col_names_clean.append(col_name)
            # On ajoute l'unité dans la liste des unités
            col_units.append(col_unit)
        else:
            # On ajoute le nom de la colonne dans la liste des noms de colonnes sans unité
            col_names_no_unit.append(col_name)     

    # On créé un dictionnaire pour stocker les noms des colonnes et les unités
    col_names_units = dict(zip(col_names_clean, col_units))
    
    # On met les parametres globaux
    global_attributes = {
        'title': 'Data from Guyane',
        'institution': 'CNRS',
        'source': 'Data from Guyane',
        'history': 'Created by the CNRS',
        'references': 'https://www.cnrs.fr/',
        'comment': 'Data from Guyane',
        'Conventions': 'CF-1.6',
    }
    # on choppe les valeurs de la colonne en rajoutant le nom de la colonne et l'unite
    # time = list(set(df[col_names_clean[0]+"("+col_names_units[col_names_clean[0]]+")"]))

    # On fais pareil pour toutes les autres colonnes
    # On créé une liste vide pour stocker les valeurs de chaque colonne
    col_values1 = []
    col_names_values = {}
    # On parcours la liste des noms de colonnes
    for col_name in col_names_clean:
        # On ajoute les valeurs de la colonne dans la liste des valeurs
        col_values1.append(list(df[col_name+"("+col_names_units[col_name]+")"]))
        # print(col_values1)
    # On créé un dictionnaire pour stocker les noms des colonnes et les valeurs
    col_names_values = dict(zip(col_names_clean, col_values1))
    
    # print(col_names_values)

    # On créé une liste vide pour stocker les valeurs de chaque colonne (sans unité)
    col_values2 = []
    # On parcours la liste des noms de colonnes
    for col_name in col_names_no_unit:
        # On ajoute les valeurs de la colonne dans la liste des valeurs
        col_values2.append(list(df[col_name]))

    # On créé un dictionnaire pour stocker les noms des colonnes et les valeurs 
    col_names_values2 = dict(zip(col_names_no_unit, col_values2))    
    
    coords = {}
    # On fais une boucle for pour parcourir tout les noms de la liste col_names_clean et on affiche la valeur de la colonne
    for i in col_names_clean:
        # On ajoute les valeurs de la colonne dans le dictionnaire coords
        coords[i] = (i, col_names_values[i])
        
        

        
    
    zwip = ['Time', 'Pressure', 'Temperature', 'Electrical conductivity', 'Salinity', 'Chlorophyll concentration']
    
    data = []
    
    for i in col_names_no_unit:
        if i.startswith('a') or i.startswith('c'):
            data.append((col_values2[col_names_no_unit.index(i)]))
        else:
            data.append((col_values2[col_names_no_unit.index(i)]))
    
    # Avec dictionnaire
    # for i in col_names_no_unit:
    #     if i.startswith('a') or i.startswith('c'):
    #         data[i] = (("Time", "Pres"), col_values2[col_names_no_unit.index(i)])
    #     else:
    #         data[i] = ("Données brute", col_values2[col_names_no_unit.index(i)])
            
    
    # On crée une dataArray
    data_array = xr.DataArray(
        data = data,
        coords = coords,
        dims = ['Time', 'Pres', 'Temp', 'Cond', 'Sal', 'CHL'],
    )    
    
    
    # On créé une dataset avec toutes les valeurs et on y met dans la section Data Variables
    ds = xr.Dataset(
        dict(bar = data_array),
        attrs = global_attributes
    )
    
    
    
    
    name_standard = ['time', 'sea_water_pressure', 'sea_water_temperature', 'sea_water_electrical_conductivity', 'sea_water_salinity', 'chlorophyll_concentration_in_sea_water']
    long_name = ['Time', 'Pressure', 'Temperature', 'Electrical conductivity', 'Salinity', 'Chlorophyll concentration']

    # Ajout des attributs pour chaque variable
    for i in col_names_clean:
        ds[i].attrs['units'] = col_names_units[i]
        ds[i].attrs['long_name'] = long_name[col_names_clean.index(i)]                    # Nom descriptif de la variable
        ds[i].attrs['standard_name'] = name_standard[col_names_clean.index(i)]            # Nom standard de la variable (cf. Convention CF-1.6)
        ds[i].attrs['source'] = 'Data from Guyane'
        ds[i].attrs['institution'] = 'CNRS'
        ds[i].attrs['Conventions'] = 'CF-1.6'
    
    
    print(ds)
    
    
    
    # on créé le fichier netcdf avec la dataset
    ds.to_netcdf('test_grappe.nc')

def test_radeau():
    # read excel file
    df = pd.read_excel("./data/data_example/data_radeau/df_Rrs_corr_CV_1-1.xlsx", keep_default_na=False)
    # On recupere les noms des colonnes
    col_names = df.columns.tolist()
    
    # récupere le contenu de la premiere colonne du fichier
    col_vals = df.iloc[:,0].tolist()
    # Pour chaque element de la liste, on les met entre ''
    col_vals = [str(i) for i in col_vals]
    col_names = [str(i) for i in col_names]
    
    for i in range(len(col_names)):
        if col_names[i].startswith('Unnamed'):
            # on regarde les valeurs et si elles contients le format Timestamp
            if col_vals[i].startswith('2021'):
                # On remplace le nom de la colonne Unnamed par Time
                col_names[i] = 'Time'
                
    col_names_int = []
    col_names_dims = [] 
    
    val_tag = []
    
    # on verifie si l'element dans col_names est un int, si c'est un int alors il va dans la liste col_names_int sinon col_names_dims
    for i in col_names:
        if i.isdigit():
            col_names_int.append(i)
        # si i est 'Tag' alors on le met dans la liste val_tag
        elif i == 'Tag':
            val_tag.append(i)
        else:
            col_names_dims.append(i)
            
            
    # On récupere les valeurs des colonnes 
    col_vals_int = []
    col_vals_dims = []
    col_vals_tag = []
    
    # print(df['310'])
    # on affiche les valeurs de la colonne 310
    # print(df[int(315)][1])
    
    # On parcours la liste des noms de colonnes
    for i in col_names:
        # On ajoute les valeurs de la colonne dans la liste des valeurs
        if i in col_names_int:
            # si la 2ème cases d'une colonne est vide alors on passe a la suivante
            if df[int(i)][1] != '':
                col_vals_int.append(list(df[int(i)]))
                    
        elif i.startswith('Time'):    
            col_vals_dims.append(list(df['Unnamed: 0']))
        
        elif i in col_names_dims:
            # si le nom de la colonne est Unnamed alors on ajoute les valeurs dans la liste col_vals_dims
            col_vals_dims.append(list(df[i]))
        
        elif i in val_tag:
            # on ajoute que 1 seule valeur dans la liste col_vals_tag
            col_vals_tag.append(list(df[i][1]))
    
    time = []
    
    # # Pour l'element Time dans la liste col_names_dims, on va elever les TimeStamp et les parenthèses et garder juste les valeurs
    # for i in col_vals_dims[0]:
    #     # time[i] = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
    #     print(i)
        
    # Pour chaques nom et valeurs on les met dans un dictionnaire
    col_dict_int = dict(zip(col_names_int, col_vals_int))
    col_dict_dims = dict(zip(col_names_dims, col_vals_dims))
    col_dict_tag = dict(zip(val_tag, col_vals_tag))
    
    
    global_attributes = {
        'title': 'Data de radeau',
        'institution': 'CNRS',
        'source': 'Mission CNRS',
        'history': 'Created by the CNRS',
        'references': 'https://www.cnrs.fr/',
        'Conventions': 'CF-1.6',
    }
    
    
    coords = {}
    
    for i in col_names_dims:
        # On ajoute les valeurs de la colonne dans le dictionnaire coords
        coords[i] = (i, col_dict_dims[i])
        
    # print(coords)
         
    data = {}
    # on fais un tuple avec les valeurs de la liste col_names_dims
    
    for i in col_dict_int:          
        # On ajoute les valeurs de la colonne dans le dictionnaire data
        data[i] = 'Time' , col_dict_int[i]
        # La ligne du dessus ne marche pas car on a pas le meme nombre de valeurs dans les colonnes
        
        # df = xr.DataArray(col_dict_int[i], dims=('Time', 'Distance'), coords=coords)
                                
    df = xr.Dataset(
        coords=coords,
        data_vars=data,
        attrs=global_attributes
    )
    
    units = ['days since 2021-9-1 0:0:0', ''] # Distance ? // InclX ? // InclY ??? 
    long_name = []
    name_standard = []
    
    # # On met a jour les attributs de toutes les variables de la liste col_names_dims
    # for i in col_names_dims:
    #     df[i].attrs['units'] = units[i]
    #     df[i].attrs['long_name'] = long_name[col_names_dims.index(i)]                    # Nom descriptif de la variable
    #     df[i].attrs['standard_name'] = name_standard[col_names_dims.index(i)]            # Nom standard de la variable (cf. Convention CF-1.6)
    #     df[i].attrs['source'] = 'Data from Guyane'
    #     df[i].attrs['institution'] = 'CNRS'
    #     df[i].attrs['Conventions'] = 'CF-1.6'
    
    
    print(df)


    df.to_netcdf('test_rad.nc')
    
def test_doc():
    
    # On ouvre le .xlsx  
    df = pd.read_excel("./data/doc_file_log.xlsx", keep_default_na=False)
    
    # On récupere les données de la colonne avec le nom 'mission'
    col_mission = df['mission'].tolist()
    # 'jour'
    col_jour = df['jour'].tolist()
    # 'heure'
    col_heure = df['heure'].tolist()
    # 'latitude'
    col_lat = df['lat'].tolist()
    # 'lon'
    col_lon = df['lon'].tolist()
    # 'doc'
    col_doc = df['doc'].tolist()
    # 'acdom412
    col_acdom412 = df['acdom412'].tolist()
    # 'acdom443'
    col_acdom443 = df['acdom443'].tolist()
    
    # On enleve les '' de toutes les listes
    col_mission = [x for x in col_mission if x != '']
    col_jour = [x for x in col_jour if x != '']
    col_heure = [x for x in col_heure if x != '']
    col_lat = [x for x in col_lat if x != '']
    col_lon = [x for x in col_lon if x != '']
    col_doc = [x for x in col_doc if x != '']
    col_acdom412 = [x for x in col_acdom412 if x != '']
    col_acdom443 = [x for x in col_acdom443 if x != '']    
    
    # mission, jour, heure, doc, acdom
    data = {}
    data['mission'] = (col_mission)
    data['jour'] = (col_jour)
    data['heure'] = (col_heure)
    data['doc'] = (('latitude', 'longitude'), [col_doc])
    # data['acdom412'] = (('latitude', 'longitude'), [col_acdom412])
    # data['acdom443'] = (('latitude', 'longitude'), [col_acdom443])
                
    # dt_array = xr.DataArray(data, dims=('lat', 'lon'), coords={'lat': ('lat', [col_lat]), 'lon': ('lon',[col_lon])})
    
    # mtn un dataset avec le dataarray
    
    df = xr.Dataset(
        coords={'lat': ("x", col_lat), 'lon': ("y", col_lon)},
        data_vars= {'doc': (('lat', 'lon'), [col_doc])}
        
    )    
    
    print(df)
    
    df.to_netcdf('test_doc.nc')
    
        
    

if __name__ == "__main__":
    # test_grappe()
    # test_radeau()
    test_doc()