#!/usr/bin/python3
# -*- coding: utf-8 -*-    ## important d'avoir ca en 2eme ligne pour les accents é et apostrphophe
#
#  csv2NetCDF.py
#  
#  Copyright Aout 2021 Maurice Libes <maurice.libes@osupytheas.fr>
#
#  Objet: convertit tout type de fichiers CSV en fichier NetCDF
#
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import os
import sys
import glob
import re
try:
	import netCDF4 as nc
	import pandas as pd
	import numpy as np
	import datetime
	import argparse
	from termcolor import  cprint # type: ignore
except:
	print("=> Erreur : il manque un de ces module python : netCDF4 | pandas | argparse | numpy | termcolor")
	print("$ pip3 install netCDF4 pandas argparse numpy termcolor")
	sys.exit(0)

from datetime import datetime

####
def Convert_Datenum():
    dateHeure = []

    for dateiso in csvdata[libelle_Datetime]:
        #print("dateiso = ",dateiso)   # on cherche ce format 2018-07-07T10:08:59Z
        pattern=re.compile('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z?')
        try:
            match=pattern.search(dateiso)
            chainedate=match.groups()  # type: ignore
            annee,mois,jour,heure,minut,sec=chainedate
        except:
            cprint("Erreur date ISO "+dateiso,'red',attrs=['bold'])
            sys.exit(0)
		
        #print("annee,mois,jour,heure,minut,sec ", int(annee), int(mois), int(jour), int(heure), int(minut), int(sec))
        
        dateobs = datetime(int(annee), int(mois), int(jour), int(heure), int(minut), int(sec))
        datenum = nc.date2num(dateobs, units=NC_TIME_FMT) # type: ignore
        dateHeure.append(datenum)

    #print("tableau dateHeure ",dateHeure)
        
    return dateHeure



# ========== NETCDF4 file ============
def Generate_NetCDF(csvfile):
    # Generating empty NETCDF file
  
    netCDFFileName = csvfile.replace('.csv', '.nc')
    
    cprint("Generating NetCDF File : " +netCDFFileName, color='blue', attrs=['bold'])
    ncFile = nc.Dataset(netCDFFileName, 'w', format='NETCDF4') # type: ignore

    return ncFile

##
def Get_dimension(fic):
    #cherche la colonne dans le fichier CSV qui contient 1 à la ligne dimension, pour savoir quelle est la dimension
    # des variables du fichier NetCDF
    listdim=[]
    finddim=False
    
    dim = Index_selector('dimension') 
    for key,value in dim.items():   #pandas series can be treated like dictionnaries # type: ignore
        if (value =='1'):
            dim = key
            listdim.append(dim)
            finddim=True
    if (not finddim):
        cprint("Dimensions absente dans le fichier CSV "+fic,color='red',attrs=['bold'] )
        sys.exit(0)
                
    cprint("Dimensions pour le fichier NetCDF "+str(key),color='green',attrs=['bold'] ) # type: ignore
    return dim

##
def Index_selector(index):
    #Selectionne une ligne du fichier csv par son nom d'index
    liste_att_obligatoires=['unites','standard_name','long_name','dimension','cf_role']   #ne sert pas
    
    if(index == 'unites'):
        ligne = csvheader.loc[index].fillna("1") #mets 1 à la place du vide
        #print('ligne unité',ligne)
    elif(index == 'standard_name'):
        ligne = csvheader.loc[index]
    elif(index == 'long_name'):
        ligne = csvheader.loc[index]
    elif(index == 'dimension'):
        ligne = csvheader.loc[index]
    elif(index ==  'station'):   # pas utilisé, il faudrait mettre une ligne station dans l'entete au cas ou
        ligne = csvheader.loc[index,'Station']

    #print("ligne index selector : ",ligne)
    return ligne # type: ignore

##
def Get_Formats():
    #retourne le format (type) de chaque valeur des colonnes du fichier CSV
    # retourne une liste de formats ['f4', 'f4', 'i4' ...]
    
    liste_formats = []  #on recoit un tableau numpy a ce niveau, les types numpy sont np.float, np.int
    
    ligne=csvdata.iloc[1]# on prend une ligne de données sous forme de série pandas
    l=ligne.tolist()			 # on la converti en tableau numpy avec la fonction tolist()
    i=0
    for value in ligne:
        if isinstance(value,str):
            lmax=max(csvdata.iloc[:,i].apply(len))  ## on calcule la longueur de chaine maximale dans la colonne "i"
            #print("indice de colonne String ",i," longueur de chaine max = ",lmax)
            frmt = 'S'+str(lmax)  # format S de la longueur xx max de la colonne 'Sxx'
            #print("value = ",value,type(value))
        elif isinstance(value,np.floating):   # np.floating renvoie True si on est en float64 ou float32
            frmt = 'f4'
            #print("value = ",value,type(value))
        elif isinstance(value,np.int64): # type: ignore
            frmt = 'i4'
        i+=1     
        liste_formats.append(frmt) # type: ignore
        #print("value = ",value,type(value))
    
    #print('sortie liste_formats ', liste_formats)
    return liste_formats


##
def Create_Dimensions(dimension):
    # Creation des dimensions du ficher NetCDF :
    ncFile.createDimension(dimension, None)
    ncFile.createDimension('lenstation', len(stationname))
    
    cprint('Dimension du fichier NetCDF : colonne '+dimension, color='green', attrs=['bold'])
    return 0


##
def Create_Write_Variables(dim, csvfile):
    #Creation des variables NetCDF et remplissage de leurs tableaux automatiquement sauf pour le cas particulier 'Date'
   
    units = Index_selector('unites')
    standard_name = Index_selector('standard_name')
    long_name = Index_selector('long_name')
    
    # déterminer le type des variables (int, float, str...)
    frmt=Get_Formats()
    print("Formats des colonnes : ", frmt)

    # convertit les dates ISO 2011-01-16T09:38:00 en format numérique pour NetCDF
    dateHeure=Convert_Datenum()
    #print("sortie dateHeure ", dateHeure)
                
    i = 0 # index de colonnes
    for col in cols:
        cprint("\t Traitement col -"+col+'-', 'yellow', attrs=['bold'])

        if (col == libelle_Datetime):
            frmt[i]='i4'   #on force la date en Int car on l'a convertie en Int avec la fonction Convert_Datenum()
            units[i] = NC_TIME_FMT # type: ignore

        ## creation des variables NetCDf avec le nom des colonnes du fichier CSV
        colnc=col.strip()
        #print("creation variable ",colnc, frmt[i], dim)
        tabcol = ncFile.createVariable(colnc, frmt[i], dim)   #on cree la variable NetCDF et on l'associe a un tableau tabcol        
        
        ## rajout de certains attributs Netcdf en fonction des variables
        ## Attention : si on rajoute des atributs "toto" dans le header du fichier CSV, il  FAUDRA modifier le code ici
        ## tabcol.toto = toto[i]
        
        # attributs standards , présents dans le header du fichier  CSV, pour toutes les variables
        tabcol.units = units[i] # type: ignore
        tabcol.long_name = long_name[i] # type: ignore
        tabcol.standard_name = standard_name[i] # type: ignore
        
        #cas particuliers si on veut ajouter des attributs specifiques a certaines variables
        if (col=="Latitude"):
            tabcol.axis="Y"
        if (col=="Longitude"):
            tabcol.axis="X"
        if (col=="Depth" or col=="Profondeur"):
            tabcol.axis="Z"

	## cas des valeurs en chaines de caracteres : elles sont traitées différement pour Netcdf
        if ( frmt[i][0] =='S'):
            #value=csvdata[col]
            #print("valeur ",value.values[0])
            #print("** longueur  tableau: ",len(value),"long chaine ",l)
            tabcol._Encoding = 'ascii'
            #print("** S1 col = ",col)
            string_values = np.array(csvdata[col].values,dtype=frmt[i])         

 ## ecriture des colonnes de valeurs CSV dans les tableaux tabcol[] des variables de Netcdf
        if (col==libelle_Datetime):
            tabcol[:] = dateHeure# cas particulier ecriture des valeurs de temps dans la variable NetCDF
            tabcol.origin = NC_TIME_ORIGIN
            tabcol.calendar = "julian"  #obligatoire en CF convention 1.6
        else:
            #print("*** ",csvdata[col].values)
            if ( frmt[i][0] =='S'):
                #print("** S2 col = ",col)
                tabcol[:] = string_values # type: ignore
            else:
                #print("** cas gen col = ",col)
                csvdata[col]=csvdata[col].replace(to_replace = missing_value, value = "NaN")
                tabcol[:] = csvdata[col].tolist()   # on ecrit les valeurs des colonnes du fichier CSV dans le tableau de la  variable NetCDF
            
        i += 1

    cprint('Ecriture variables NetCDF OK', color='green', attrs=['bold'])
 
    return 1
##
def Create_Variable_Station():
    #Creation de la variable station name (cas particulier|fausse dimension)
    station_name = ncFile.createVariable('station_name', 'S1', 'lenstation')
    station_name.long_name = "station_name"
    station_name.cf_role = featuretype+"_id"   #important une variable doit jouer le role de cf_role
    station_name[:] = nc.stringtoarr(stationname,len(stationname)) # type: ignore
    
    return 0

  
##
def Create_Global_Attributes(ncFile):
    # Creation des global attributs/metadata du fichier NC lues dans un fichier CSV externe
    indexlist = glob_att.index
    for index in indexlist:
        value = glob_att.loc[index].values[0]
        if index == 'Conventions':
            ncFile.setncattr(index, value)
        else:
            ncFile.setncattr(index.casefold(), value)
    cprint('Global Attributs OK', color='green', attrs=['bold'])
    return 0

##
def Control_Global_Attributes():
    #Test s'il existe bien dans notre ficher csv metadata les 4 colonnes importante featuretype|conventions...
    indexlist = glob_att.index
    #print("feature type ",featuretype)
    if ( ('featuretype' in indexlist) and ('cdm_data_type' in indexlist)  and ('Conventions' in indexlist) ):
        cprint("Control Global Attributes OK", color='green', attrs=['bold'])
        if (featuretype=="timeserie"):
            if ('cdm_timeserie_variables' not in indexlist):
                cprint("il manque cdm_timeserie_variables", color='red', attrs=['bold'])
                sys.exit(0)
        elif (featuretype=="profile"):
            if ('cdm_profile_variables' not in indexlist):
                cprint("il manque cdm_profile_variables", color='red', attrs=['bold'])
                sys.exit(0)
    else:
        cprint("Control failed! \nIl manque : featuretype | cdm_data_type | cdm_timeserie_variables | Conventions dans le fichier:"+fileMetaData, color='red', attrs=['bold'])
        cprint(" Conventions avec un C majuscule dans le fichier:"+fileMetaData, color='red', attrs=['bold'])
        sys.exit(0)
    return 0

##
def Control_Illegal_char(cols):
	# verifie les caracteres interdits qui posent probleme dans le nom des colonnes
    Illegal_char=['#','|',',',"'","''","/"," "]
    for elements in Illegal_char:
        for columns in cols:
            if(elements in columns):
                cprint('** Caractère interdit trouvé dans la colonne du nom:'+columns, color='red', attrs=['bold'])
                sys.exit(0)
    
    cprint("Control Illegal char OK", color='green', attrs=['bold'])
    return 0

##
def Control_Header_Columns(cols):
    #Controle si les columns date|latitude|longitude existe bien dans le fichier csv
    #print("COLS ",cols)
    for i in range(0, len(cols)):  #on enleve les espace en debut et fin de chaine
        cols[i]=cols[i].lstrip()	
        cols[i]=cols[i].rstrip()
        #cols[i]=cols[i].capitalize()
        #print("cols",i,"."+cols[i]+".")
	
    for col in colonnes_obligatoires:
        if (col not in cols):
            cprint(cols,color="yellow",attrs=['bold'])
            cprint("Control failed!\nIl manque une des colonnes "+str(colonnes_obligatoires)+" dans le fichier :"+fic, color='red', attrs=['bold'])
            sys.exit(0)
    
    cprint("Control Columns OK", color='green', attrs=['bold'])
    return 1

##
def Control_Attributes_Var(indexdrop):
    #print("index du fichier ",indexdrop)
    
    for att in attributs_obligatoires:
        if att not in indexdrop:
            cprint("Control failed!\nIl manque l\'attribut \'"+att+"\' dans le ficher : "+fic, color='red', attrs=['bold'])
            sys.exit(0)
            
    cprint('Control Attributs variable OK', color='green', attrs=['bold'])
    return 1


##
def Compare_Files(cols,firstcols):
## compare les fichiers .csv qui sont dans le repértoire CsvFiles : ils doivent etre de meme nature

    if (len(cols) != len(firstcols)):
        print("\n==> nombre de colonnes différents ",len(cols),len(firstcols) )
        cprint("Les fichiers CSV dans le repertoire CsvFiles sont differents !!", color='red',attrs=['bold'])
        cprint("Le programme ne traite que un ensemble de fichiers identiques !!", color='red',attrs=['bold'])
        sys.exit(0)
    
    if (not np.array_equal(cols,firstcols) ):
        for i in range(0,len(firstcols) ): 
            if (cols[i] != firstcols[i]):
                print("\n==> ",cols[i],firstcols[i])
                cprint("Les libelles des colonnes dans le repertoire CsvFiles sont differents !!", color='red',attrs=['bold'])
                cprint("Le programme ne traite que un ensemble de fichiers identiques !!", color='red',attrs=['bold'])
        sys.exit(0)

    return 1

### Programme Principal 
###

if __name__ == "__main__":
    global NC_TIME_FMT, NC_TIME_ORIGIN
    global csvheader, csvdata
    global stationname, lenstation, OutputPath
    global glob_att,featuretype
    global ncFile,fic
    global cols,indexlist,indexdrop
    global libelle_Datetime, colonnes_obligatoires, attributs_obligatoires
    
    
    NC_TIME_FMT = 'minutes since 1990-01-01 00:00:00 UTC'
    NC_TIME_ORIGIN = "01-JAN-1990 00:00:00"

    # ========== Read CSV file =============

    InputPath="./CsvFiles/"
    OutputPath="./NcFiles/"
    fileMetaData = "global_attributes.csv"
    libelle_Datetime="datetime"
    colonnes_obligatoires=['datetime','latitude','longitude']
    attributs_obligatoires=['unites','dimension','standard_name','long_name']
    missing_value=-999.9
	
    parser = argparse.ArgumentParser(description='-s delimiter of the csv file ')
    parser.add_argument('-s', '--separator', help='Please enter a separator for you csvFile', required=True)           
    parser.add_argument('-n', '--name', help='Please enter the name of the station', required=False)
    args = parser.parse_args()

    motif=InputPath+'*.csv'  ## pour tous les fichier seabird finissant par .csv
    ficcsv=glob.glob(motif)  ## pour lister fichiers d'un certain motif
    ficcsv=sorted(ficcsv)
    if (len(ficcsv) ==0): 
        cprint("Aucun fichier CSV *.csv a traiter dans "+InputPath,color='red',attrs=['bold'])
        cprint("=> Placer les fichiers CSV *.csv a traiter dans le répertoire "+InputPath,color='yellow',attrs=['bold'])
        sys.exit()
     
    firstcols=[]; nbfic=0
    for fic in ficcsv:
        fic=os.path.basename(fic)
        if fic.endswith(".csv"):
            cprint("\n Traitement fichier "+fic, color='blue', attrs=['bold'])
           
            n=args.name
            if (n == None ):
                cprint("Donnez le nom de la station pour le fichier "+fic, color='yellow', attrs=['bold'])
                stationname=input()
            else:
                stationname = args.name
                lenstation = len(stationname)

            csvheader = pd.read_csv(InputPath+fic,  low_memory=False, sep=args.separator,index_col=0)

            nbfic+=1
            #print('test',csvheader)
            indexdrop=csvheader.index.dropna() #selectionne la 1eree colonne du fichier CSV en supprimant toute les valeurs vides (NAN)
            #print("Attributs des variables : ",indexdrop)
            #on lit les data en sautant les lignes de header
            csvdata=pd.read_csv(InputPath+fic, sep=args.separator,skiprows=range(1,len(indexdrop)+1),index_col=0)

            ## on extrait le nom des colonnes du fichier CSV
            cols = csvdata.columns.values
            #print('cols',cols); print(type(cols))
           
            Control_Attributes_Var(indexdrop)
            Control_Header_Columns(cols)
            Control_Illegal_char(cols)
            
            if (nbfic > 1): ## verifie que les entetes des fichiers CSV dans le repertoire CsvFiles soient les memes
                Compare_Files(cols,firstcols)  
            else:
                firstcols = cols
                 
            glob_att = pd.read_csv(fileMetaData, delimiter='=', header=None, index_col=0)
            indexlist = glob_att.index
            # retourne le type de donnees netcdf : timeserie ou profile ou trajectory
            featuretype = glob_att.loc['featuretype'].values[0]  # voir si on calcule le featuretype automatiquement?
            Control_Global_Attributes()
#         
            dimension = Get_dimension(fic)
#
            ncFile = Generate_NetCDF(OutputPath+fic)
            Create_Dimensions(dimension)
            Create_Global_Attributes(ncFile)
#
            Create_Variable_Station()
#
            Create_Write_Variables(dimension, fic)



