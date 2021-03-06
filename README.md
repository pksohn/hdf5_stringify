# HDF5 Stringify Utility

[![Build Status](https://travis-ci.org/pksohn/hdf5_stringify.svg?branch=master)](https://travis-ci.org/pksohn/hdf5_stringify)

This utility is meant to easily convert HDF5 files containing DataFrames that have `bytes` types (or the related `numpy.bytes_` types) as any of the following:
 
 * Index name (single index)
 * Index name (any of a multi-index)
 * Column name
 
 When using an HDF5 with bytes types in these places, and working in Python 3 where strings and bytes are treated differently, a model environment like UrbanSim has a hard time referring to certain column or index names. This utility easily converts HDF5 files to get around this limitation. 
 
 ## Dependencies
 
 Recommend Anaconda with:
 
 * Pandas
 * PyTables
 * Numpy
 * Pytest (for unit tests)
 
 ## Usage
 
```
python stringify.py [path to HFD5 file] -s [optional suffix]
```

## Examples

Default suffix is "converted":
 
```
python stringify.py path/to/model_data.h5

# Creates path/to/model_data_converted.h5
```

Set your own suffix with `-s` option:

```
python stringify.py path/to/model_data.h5 -s new

# Creates path/to/model_data_new.h5
```

## Details

The conversion process has a few hardcoded defaults for now. 

1) New HDF5 store is created using `pandas.HDFStore()` with the following compression settings:
`complib='zlib', complevel=1`
2) Tables are modified and copied over in the `table` format, like so:

```
new_store.put(name, new_table, format='table')
```