# HDF5 Stringify Utility

This utility is meant to easily convert HDF5 files containing DataFrames that have `bytes` types (or the related `numpy.bytes_` types) as any of the following:
 
 * Index name (single index)
 * Index name (any of a multi-index)
 * Column name
 
 When using an HDF5 with bytes types in these places, and working in Python 3 where strings and bytes are treated differently, a model environment like UrbanSim has a hard time referring to certain column or index names. This utility easily converts HDF5 files to get around this limitation. 
 
 ## Dependencies
 
 * Pandas
 * Numpy
 * Pytest (for unit tests)
 
 ## Usage
 
```
python stringify.py [path to HFD5 file] -s [optional suffix]
```

## Examples

This will take the model_data.h5 file, convert it, and save as model_data_new.h5:

```
python stringify.py path/to/model_data.h5 -s new
```

Default suffix is "converted":
 
```
python stringify.py path/to/model_data.h5

# Creates path/to/model_data_converted.h5
```
