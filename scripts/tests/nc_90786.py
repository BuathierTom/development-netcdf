from netCDF4 import Dataset # type: ignore
import os 
import warnings
warnings.filterwarnings("ignore")

file_name = "./DATA/2D_Temperature.nc"
if os.path.isfile(file_name):
    os.remove(file_name)
    
ds = Dataset(file_name, mode="w")

ds.createDimension("x", 20)
ds.createDimension("y", 20)
ds.createDimension("time", None)

var1 = ds.createVariable("field1", "f4", ("time", "x", "y"))
var2 = ds.createVariable("field2", "f4", ("time", "x", "y"))

#add netcdf attributes
var1.units = "Celcius"
var1.long_name = "Surface air temperature"

var2.units = "Kelvin"
var2.long_name = "Surface air temperature"

import numpy as np
data = np.random.randn(10, 20, 20)
var1[:] = data
var2[:] =  data + 273.15
ds.close();