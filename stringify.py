import argparse
import os
import pandas as pd
import numpy as np


def check_df_for_bytes(df):
    """
    Checks DataFrame for bytes types in index names (single or multi-index)
    and column names
    
    Parameters
    ----------
    df : DataFrame
        Input DataFrame to check
        
    Returns
    -------
    bool
        True if there is a bytes type in the DataFrame index name(s) or column
        names
    """

    byte_types = (np.bytes_, bytes)

    if isinstance(df.index, pd.core.index.MultiIndex):
        for name in df.index.names:
            if type(name) in byte_types:
                return True

    if df.index.name and type(df.index.name) in byte_types:
        return True

    for col in df.columns:
        if type(col) in byte_types:
            return True

    return False


def decode_byte_df(df):
    """
    Converts bytes types to strings in index names and column names
    of a DataFrame

    Parameters
    ----------
    df : DataFrame
        Input DataFrame to convert

    Returns
    -------
    df : DataFrame
        Output DataFrame, with converted index names and column names

    """
    byte_types = (np.bytes_, bytes)

    if isinstance(df.index, pd.core.index.MultiIndex):
        new_names = [name.decode() if type(name) in byte_types else name
                     for name in df.index.names]
        df.index.set_names(new_names, inplace=True)

    elif df.index.name and type(df.index.name) in byte_types:
        df.index.name = df.index.name.decode()

    df.columns = [col.decode() if type(col) in byte_types else col
                  for col in df.columns]

    return df


def convert_store(store_path, suffix):
    """
    Modifies HDF5 file to stringify all bytes type column names and index
    names. Saves with specified suffix.
    
    Parameters
    ----------
    store_path : str
        Path to original HDF5 file
    suffix : str
        String to append to new file name (e.g. "converted" to get
        "oldfilename_converted.h5")

    Returns
    -------
    None
    """

    if suffix is None:
        suffix = 'converted'

    dirname, filename = os.path.split(store_path)
    filename_no_ext = filename.split('.')[0]
    new_filename = '{}_{}.h5'.format(filename_no_ext, suffix)
    new_filepath = os.path.join(dirname, new_filename)
    new_store = pd.HDFStore(new_filepath, mode='w')

    with pd.HDFStore(store_path, mode='r') as store:
        for name in store.keys():
            table = store[name]
            if check_df_for_bytes(table):
                new_table = decode_byte_df(table)
                new_store.put(name, new_table)
            else:
                new_store.put(name, table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-s', '--suffix')
    args = parser.parse_args()

    fp = args.filepath
    suffix = args.suffix or None

    convert_store(fp, suffix)
