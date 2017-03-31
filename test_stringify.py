import pandas as pd
import pytest
from . import stringify


@pytest.fixture
def df_byte_col():
    data = {
        b'a': [1, 2, 3],
        'b': [1, 2, 3],
        b'c': [1, 2, 3]
    }
    index = [0, 1, 2]
    return pd.DataFrame(data, index)


@pytest.fixture
def df_byte_index_name():
    data = {
        'a': [1, 2, 3],
        'b': [1, 2, 3],
        'c': [1, 2, 3]
    }
    index = [0, 1, 2]
    df = pd.DataFrame(data, index)
    df.index.name = b'index'
    return df


@pytest.fixture
def df_normal():
    data = {
        'a': [1, 2, 3],
        'b': [1, 2, 3],
        'c': [1, 2, 3]
    }
    index = [0, 1, 2]
    df = pd.DataFrame(data, index)
    df.index.name = 'index'
    return df


@pytest.fixture
def byte_store(df_byte_col, df_byte_index_name, df_normal, tmpdir):
    p = tmpdir.mkdir('data').join('byte_store.h5')
    store = pd.HDFStore(str(p), 'w')

    dfs_to_add = {
        'df_byte_col': df_byte_col,
        'df_byte_index_name': df_byte_index_name,
        'df_normal': df_normal
    }

    for name, df in dfs_to_add.items():
        store.put(name, df)

    store.close()
    return str(p)


def test_check_for_bytes(byte_store):
    with pd.HDFStore(byte_store) as store:

        assert stringify.check_df_for_bytes(
            store['df_byte_col']) is True
        assert stringify.check_df_for_bytes(
            store['df_byte_index_name']) is True
        assert stringify.check_df_for_bytes(
            store['df_normal']) is False


def test_decode_bytes(byte_store, tmpdir):

    stringify.convert_store(byte_store, 'converted')
    converted_fp = str(tmpdir.join('byte_store_converted.h5'))

    with pd.HDFStore(converted_fp) as new:
        for name in new.keys():
            assert stringify.check_df_for_bytes(new[name]) is False
