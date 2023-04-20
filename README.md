
# Dev_NetCDF

Scripts python pour améliorer et changer l'extention de fichier xlsx en fichier NetCDF. Ce projet a pour but de remplacer une bases de données postgres SQL essentiellement utilisé avec des fichier xlsx en fichier NetCDF.

## Qu'est ce qu'un fichier NetCDF ?

NetCDF (**Network Common Data Format**) est à la fois un modèle de représentation de données et un format de fichier. Dans le milieu scientifique, il permet de gérer et d'exposer des données qui évoluent en fonction de certaines dimensions. 

**Un fichier netCDF contient trois parties :**
-	Un *header* qui contient toute les informations les dimensions, les attributs et les variables, à l'exception des données variables
-	Les *fixed-size data* qui contenant les données pour les   variables qui n'ont pas de dimension illimitée
-	Et les *record data* qui contiennent les enregistrements de données pour les variables ayant une dimension illimitée.

On définit des variables dans le fichier netCDF comme ceci en suivant les informations données dans le .csv. Les données des fichiers netCDF sont faites de cette façon : 

![nc](https://user-images.githubusercontent.com/97435667/233404512-80776b98-84be-43ed-9735-26beb578efe5.png)

Les variables sont définit en haut du fichier netCDF avec leur types, leurs unités etc.. Les données, elles, sont contenues dans le reste du fichier et associé à leur variables définit justement au dessus.
## Bibliothèques & Modules utilisés

- [Xarray](https://docs.xarray.dev/en/stable/)
- [Pandas](https://pandas.pydata.org/docs/)

## Auteurs

- [@BuathierTom](https://www.github.com/BuathierTom)


## License

[MIT](https://choosealicense.com/licenses/mit/)


