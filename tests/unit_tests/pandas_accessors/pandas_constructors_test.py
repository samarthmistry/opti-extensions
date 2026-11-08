# Copyright 2025 Samarth Mistry
# This file is part of the `opti-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Tests for first-class pandas constructors on IndexSet and ParamDict classes."""

import pandas as pd
import pytest

from opti_extensions import IndexSet1D, IndexSetND, ParamDict1D, ParamDictND
from opti_extensions._pandas_accessors import IndexAccessor, SeriesAccessor

from ..helper_indexset import assert_sets_same

# =============================================================================
# IndexSet1D.from_series
# =============================================================================


def test_indexset1d_from_series_basic():
    s = pd.Series([1, 2, 3])
    res = IndexSet1D.from_series(s)
    assert_sets_same(res, IndexSet1D([1, 2, 3]))
    assert res.name is None


def test_indexset1d_from_series_with_series_name():
    s = pd.Series(['A', 'B', 'C'], name='LETTERS')
    res = IndexSet1D.from_series(s)
    assert_sets_same(res, IndexSet1D(['A', 'B', 'C'], name='LETTERS'))
    assert res.name == 'LETTERS'


def test_indexset1d_from_series_with_custom_name():
    s = pd.Series(['A', 'B', 'C'], name='LETTERS')
    res = IndexSet1D.from_series(s, name='CUSTOM')
    assert_sets_same(res, IndexSet1D(['A', 'B', 'C'], name='CUSTOM'))
    assert res.name == 'CUSTOM'


def test_indexset1d_from_series_empty_err():
    s = pd.Series(dtype=int)
    with pytest.raises(ValueError, match='Series is empty'):
        IndexSet1D.from_series(s)


def test_indexset1d_from_series_duplicate_err():
    s = pd.Series([1, 1, 2])
    with pytest.raises(ValueError):
        IndexSet1D.from_series(s)


def test_indexset1d_from_series_nonscalar_err():
    s = pd.Series([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        IndexSet1D.from_series(s)


# =============================================================================
# IndexSet1D.from_index
# =============================================================================


def test_indexset1d_from_index_basic():
    idx = pd.Index([10, 20, 30])
    res = IndexSet1D.from_index(idx)
    assert_sets_same(res, IndexSet1D([10, 20, 30]))
    assert res.name is None


def test_indexset1d_from_index_with_index_name():
    idx = pd.Index(['WH-A', 'WH-B'], name='WAREHOUSE')
    res = IndexSet1D.from_index(idx)
    assert_sets_same(res, IndexSet1D(['WH-A', 'WH-B'], name='WAREHOUSE'))
    assert res.name == 'WAREHOUSE'


def test_indexset1d_from_index_with_custom_name():
    idx = pd.Index(['WH-A', 'WH-B'], name='WAREHOUSE')
    res = IndexSet1D.from_index(idx, name='CUSTOM')
    assert_sets_same(res, IndexSet1D(['WH-A', 'WH-B'], name='CUSTOM'))
    assert res.name == 'CUSTOM'


def test_indexset1d_from_index_empty_err():
    idx = pd.Index([])
    with pytest.raises(ValueError, match='Index is empty'):
        IndexSet1D.from_index(idx)


def test_indexset1d_from_index_multiindex_err():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)])
    with pytest.raises(TypeError, match='MultiIndex is not supported by IndexSet1D'):
        IndexSet1D.from_index(mi)


def test_indexset1d_from_index_duplicate_err():
    idx = pd.Index([1, 1, 2])
    with pytest.raises(ValueError):
        IndexSet1D.from_index(idx)


def test_indexset1d_from_index_nonscalar_err():
    idx = pd.Index([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        IndexSet1D.from_index(idx)


# =============================================================================
# IndexSetND.from_dataframe
# =============================================================================


def test_indexsetnd_from_dataframe_basic():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'PERIOD': [0, 1]})
    res = IndexSetND.from_dataframe(df)
    assert_sets_same(res, IndexSetND([('chair', 0), ('desk', 1)], names=['PRODUCT', 'PERIOD']))
    assert res.names == ['PRODUCT', 'PERIOD']


def test_indexsetnd_from_dataframe_columns_subset():
    df = pd.DataFrame(
        {
            'PRODUCT': ['chair', 'desk'],
            'WH': ['WH-A', 'WH-B'],
            'PERIOD': [0, 1],
        }
    )
    res = IndexSetND.from_dataframe(df, columns=['PRODUCT', 'PERIOD'])
    assert_sets_same(res, IndexSetND([('chair', 0), ('desk', 1)], names=['PRODUCT', 'PERIOD']))
    assert res.names == ['PRODUCT', 'PERIOD']


def test_indexsetnd_from_dataframe_custom_names():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'PERIOD': [0, 1]})
    res = IndexSetND.from_dataframe(df, names=['P', 'T'])
    assert_sets_same(res, IndexSetND([('chair', 0), ('desk', 1)], names=['P', 'T']))
    assert res.names == ['P', 'T']


def test_indexsetnd_from_dataframe_none_column_names():
    df = pd.DataFrame([(1, 2), (3, 4)])
    df.columns = [None, 'B']
    res = IndexSetND.from_dataframe(df)
    assert res.names is None


def test_indexsetnd_from_dataframe_multiindex_none_column_names():
    df = pd.DataFrame([(1, 2), (3, 4)])
    df.columns = pd.MultiIndex.from_tuples([(None, 'X'), ('B', 'Y')])
    res = IndexSetND.from_dataframe(df)
    assert res.names is None


def test_indexsetnd_from_dataframe_empty_err():
    df = pd.DataFrame(columns=['A', 'B'])
    with pytest.raises(ValueError, match='DataFrame is empty'):
        IndexSetND.from_dataframe(df)


def test_indexsetnd_from_dataframe_duplicate_err():
    df = pd.DataFrame({'A': [1, 1], 'B': [2, 2]})
    with pytest.raises(ValueError):
        IndexSetND.from_dataframe(df)


def test_indexsetnd_from_dataframe_nonscalar_err():
    df = pd.DataFrame({'A': [[1, 2], [3, 4]], 'B': [1, 2]})
    with pytest.raises(TypeError, match='non-scalar value'):
        IndexSetND.from_dataframe(df)


# =============================================================================
# IndexSetND.from_index
# =============================================================================


def test_indexsetnd_from_index_basic():
    mi = pd.MultiIndex.from_tuples([('EAST', 'WH-A'), ('WEST', 'WH-B')], names=['ZONE', 'WH'])
    res = IndexSetND.from_index(mi)
    assert_sets_same(res, IndexSetND([('EAST', 'WH-A'), ('WEST', 'WH-B')], names=['ZONE', 'WH']))
    assert res.names == ['ZONE', 'WH']


def test_indexsetnd_from_index_custom_names():
    mi = pd.MultiIndex.from_tuples([('EAST', 'WH-A'), ('WEST', 'WH-B')], names=['ZONE', 'WH'])
    res = IndexSetND.from_index(mi, names=['Z', 'W'])
    assert_sets_same(res, IndexSetND([('EAST', 'WH-A'), ('WEST', 'WH-B')], names=['Z', 'W']))
    assert res.names == ['Z', 'W']


def test_indexsetnd_from_index_none_level_names():
    mi = pd.MultiIndex.from_tuples([('EAST', 'WH-A'), ('WEST', 'WH-B')])
    res = IndexSetND.from_index(mi)
    assert res.names is None


def test_indexsetnd_from_index_single_level_err():
    idx = pd.Index([1, 2, 3])
    with pytest.raises(TypeError, match='Single-level Index is not supported by IndexSetND'):
        IndexSetND.from_index(idx)


def test_indexsetnd_from_index_empty_err():
    mi = pd.MultiIndex.from_tuples([], names=['A', 'B'])
    with pytest.raises(ValueError, match='MultiIndex is empty'):
        IndexSetND.from_index(mi)


def test_indexsetnd_from_index_duplicate_err():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('A', 1)])
    with pytest.raises(ValueError):
        IndexSetND.from_index(mi)


# =============================================================================
# ParamDict1D.from_series
# =============================================================================


def test_paramdict1d_from_series_basic():
    s = pd.Series([200, 500], index=pd.Index(['chair', 'desk'], name='PRODUCT'), name='UNITS')
    res = ParamDict1D.from_series(s)
    assert res == ParamDict1D({'chair': 200, 'desk': 500})
    assert res.key_name == 'PRODUCT'
    assert res.value_name == 'UNITS'


def test_paramdict1d_from_series_custom_names():
    s = pd.Series([200, 500], index=['chair', 'desk'])
    res = ParamDict1D.from_series(s, key_name='ITEM', value_name='QTY')
    assert res == ParamDict1D({'chair': 200, 'desk': 500})
    assert res.key_name == 'ITEM'
    assert res.value_name == 'QTY'


def test_paramdict1d_from_series_empty_err():
    s = pd.Series(dtype=int)
    with pytest.raises(ValueError, match='Series is empty'):
        ParamDict1D.from_series(s)


def test_paramdict1d_from_series_duplicate_idx_err():
    s = pd.Series([1, 2], index=['A', 'A'])
    with pytest.raises(ValueError, match='duplicate index-label'):
        ParamDict1D.from_series(s)


def test_paramdict1d_from_series_multiindex_err():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)])
    s = pd.Series([10, 20], index=mi)
    with pytest.raises(TypeError, match='MultiIndex is not supported by ParamDict1D'):
        ParamDict1D.from_series(s)


def test_paramdict1d_from_series_nonscalar_key_err():
    s = pd.Series([10, 20], index=[['A', 'B'], 'C'])
    with pytest.raises(TypeError):
        ParamDict1D.from_series(s)


def test_paramdict1d_from_series_non_numeric_val_err():
    s = pd.Series(['x', 'y'], index=['A', 'B'])
    with pytest.raises(TypeError, match='values should be either int or float'):
        ParamDict1D.from_series(s)


# =============================================================================
# ParamDict1D.from_dataframe
# =============================================================================


def test_paramdict1d_from_dataframe_basic():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'UNITS': [200, 500]})
    res = ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')
    assert res == ParamDict1D({'chair': 200, 'desk': 500})
    assert res.key_name == 'PRODUCT'
    assert res.value_name == 'UNITS'


def test_paramdict1d_from_dataframe_custom_names():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'UNITS': [200, 500]})
    res = ParamDict1D.from_dataframe(
        df, key_col='PRODUCT', value_col='UNITS', key_name='ITEM', value_name='QTY'
    )
    assert res == ParamDict1D({'chair': 200, 'desk': 500})
    assert res.key_name == 'ITEM'
    assert res.value_name == 'QTY'


def test_paramdict1d_from_dataframe_empty_err():
    df = pd.DataFrame(columns=['PRODUCT', 'UNITS'])
    with pytest.raises(ValueError, match='DataFrame is empty'):
        ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')


def test_paramdict1d_from_dataframe_duplicate_keys_err():
    df = pd.DataFrame({'PRODUCT': ['chair', 'chair'], 'UNITS': [200, 500]})
    with pytest.raises(ValueError):
        ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')


def test_paramdict1d_from_dataframe_missing_col_err():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'UNITS': [200, 500]})
    with pytest.raises(KeyError):
        ParamDict1D.from_dataframe(df, key_col='MISSING', value_col='UNITS')


def test_paramdict1d_from_dataframe_nonscalar_key_err():
    df = pd.DataFrame({'PRODUCT': [['chair', 'stool'], 'desk'], 'UNITS': [200, 500]})
    with pytest.raises(TypeError):
        ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')


def test_paramdict1d_from_dataframe_non_numeric_val_err():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'UNITS': ['high', 'low']})
    with pytest.raises(TypeError):
        ParamDict1D.from_dataframe(df, key_col='PRODUCT', value_col='UNITS')


# =============================================================================
# ParamDictND.from_series
# =============================================================================


def test_paramdictnd_from_series_basic():
    mi = pd.MultiIndex.from_tuples([('Delhi', 'Seattle'), ('Delhi', 'Tokyo')], names=['ORI', 'DES'])
    s = pd.Series([11303, 5836], index=mi, name='DIST')
    res = ParamDictND.from_series(s)
    assert res == ParamDictND({('Delhi', 'Seattle'): 11303, ('Delhi', 'Tokyo'): 5836})
    assert res.key_names == ['ORI', 'DES']
    assert res.value_name == 'DIST'


def test_paramdictnd_from_series_custom_names():
    mi = pd.MultiIndex.from_tuples([('Delhi', 'Seattle'), ('Delhi', 'Tokyo')])
    s = pd.Series([11303, 5836], index=mi)
    res = ParamDictND.from_series(s, key_names=['ORIGIN', 'DEST'], value_name='MILES')
    assert res == ParamDictND({('Delhi', 'Seattle'): 11303, ('Delhi', 'Tokyo'): 5836})
    assert res.key_names == ['ORIGIN', 'DEST']
    assert res.value_name == 'MILES'


def test_paramdictnd_from_series_none_level_names():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)])
    s = pd.Series([10, 20], index=mi)
    res = ParamDictND.from_series(s)
    assert res.key_names is None
    assert res.value_name is None


def test_paramdictnd_from_series_empty_err():
    mi = pd.MultiIndex.from_tuples([], names=['A', 'B'])
    s = pd.Series(dtype=float, index=mi)
    with pytest.raises(ValueError, match='Series is empty'):
        ParamDictND.from_series(s)


def test_paramdictnd_from_series_duplicate_idx_err():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('A', 1)])
    s = pd.Series([10, 20], index=mi)
    with pytest.raises(ValueError, match='duplicate index-label'):
        ParamDictND.from_series(s)


def test_paramdictnd_from_series_single_level_err():
    s = pd.Series([10, 20], index=['A', 'B'])
    with pytest.raises(TypeError, match='Single-level index is not supported by ParamDictND'):
        ParamDictND.from_series(s)


def test_paramdictnd_from_series_single_level_key_err():
    s = pd.Series([10, 20], index=[(1, 2), (3, 4)])  # Index of tuples, but single-level
    with pytest.raises(TypeError, match='Single-level index is not supported by ParamDictND'):
        ParamDictND.from_series(s)


def test_paramdictnd_from_series_non_numeric_val_err():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)])
    s = pd.Series(['x', 'y'], index=mi)
    with pytest.raises(TypeError, match='values should be either int or float'):
        ParamDictND.from_series(s)


# =============================================================================
# ParamDictND.from_dataframe
# =============================================================================


def test_paramdictnd_from_dataframe_basic():
    df = pd.DataFrame(
        {
            'ORI': ['Delhi', 'Seattle'],
            'DES': ['Seattle', 'Tokyo'],
            'DIST': [11303, 7695],
        }
    )
    res = ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')
    assert res == ParamDictND({('Delhi', 'Seattle'): 11303, ('Seattle', 'Tokyo'): 7695})
    assert res.key_names == ['ORI', 'DES']
    assert res.value_name == 'DIST'


def test_paramdictnd_from_dataframe_custom_names():
    df = pd.DataFrame(
        {
            'ORI': ['Delhi', 'Seattle'],
            'DES': ['Seattle', 'Tokyo'],
            'DIST': [11303, 7695],
        }
    )
    res = ParamDictND.from_dataframe(
        df,
        key_cols=['ORI', 'DES'],
        value_col='DIST',
        key_names=['ORIGIN', 'DEST'],
        value_name='MILES',
    )
    assert res == ParamDictND({('Delhi', 'Seattle'): 11303, ('Seattle', 'Tokyo'): 7695})
    assert res.key_names == ['ORIGIN', 'DEST']
    assert res.value_name == 'MILES'


def test_paramdictnd_from_dataframe_empty_err():
    df = pd.DataFrame(columns=['ORI', 'DES', 'DIST'])
    with pytest.raises(ValueError, match='DataFrame is empty'):
        ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')


def test_paramdictnd_from_dataframe_empty_key_cols_err():
    df = pd.DataFrame({'ORI': ['Delhi'], 'DIST': [11303]})
    with pytest.raises(ValueError, match='key_cols'):
        ParamDictND.from_dataframe(df, key_cols=[], value_col='DIST')


def test_paramdictnd_from_dataframe_duplicate_keys_err():
    df = pd.DataFrame(
        {
            'ORI': ['Delhi', 'Delhi'],
            'DES': ['Seattle', 'Seattle'],
            'DIST': [11303, 7695],
        }
    )
    with pytest.raises(ValueError):
        ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')


def test_paramdictnd_from_dataframe_missing_col_err():
    df = pd.DataFrame({'ORI': ['Delhi'], 'DES': ['Seattle'], 'DIST': [11303]})
    with pytest.raises(KeyError):
        ParamDictND.from_dataframe(df, key_cols=['ORI', 'MISSING'], value_col='DIST')


def test_paramdictnd_from_dataframe_nonscalar_key_err():
    df = pd.DataFrame(
        {
            'ORI': [['Delhi', 'Agra'], 'Seattle'],
            'DES': ['Seattle', 'Tokyo'],
            'DIST': [11303, 7695],
        }
    )
    with pytest.raises(TypeError):
        ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')


def test_paramdictnd_from_dataframe_non_numeric_val_err():
    df = pd.DataFrame(
        {
            'ORI': ['Delhi', 'Seattle'],
            'DES': ['Seattle', 'Tokyo'],
            'DIST': ['far', 'very far'],
        }
    )
    with pytest.raises(TypeError):
        ParamDictND.from_dataframe(df, key_cols=['ORI', 'DES'], value_col='DIST')


# =============================================================================
# Direct Accessor Instantiations
# =============================================================================


def test_series_accessor_direct():
    s = pd.Series([10, 20, 30], name='VAL')
    acc = SeriesAccessor(s)
    iset = acc.to_indexset()
    assert_sets_same(iset, IndexSet1D([10, 20, 30], name='VAL'))
    pdict = acc.to_paramdict()
    assert pdict == ParamDict1D({0: 10, 1: 20, 2: 30}, value_name='VAL')


def test_series_accessor_multiindex_direct():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)], names=['L1', 'L2'])
    s = pd.Series([10.0, 20.0], index=mi, name='VAL')
    acc = SeriesAccessor(s)
    pdict = acc.to_paramdict()
    assert pdict == ParamDictND(
        {('A', 1): 10.0, ('B', 2): 20.0}, key_names=['L1', 'L2'], value_name='VAL'
    )


def test_index_accessor_direct_single_level():
    idx = pd.Index(['A', 'B', 'C'], name='LETTERS')
    acc = IndexAccessor(idx)
    iset = acc.to_indexset()
    assert_sets_same(iset, IndexSet1D(['A', 'B', 'C'], name='LETTERS'))


def test_index_accessor_direct_multiindex():
    mi = pd.MultiIndex.from_tuples([('A', 1), ('B', 2)], names=['L1', 'L2'])
    acc = IndexAccessor(mi)
    iset = acc.to_indexset()
    assert_sets_same(iset, IndexSetND([('A', 1), ('B', 2)], names=['L1', 'L2']))


def test_indexsetnd_from_dataframe_empty_columns_err():
    df = pd.DataFrame({'PRODUCT': ['chair', 'desk'], 'PERIOD': [0, 1]})
    with pytest.raises(ValueError, match='`columns` cannot be empty'):
        IndexSetND.from_dataframe(df, columns=[])


def test_paramdict1d_from_dataframe_key_col_equals_value_col():
    df = pd.DataFrame({'VAL': [10, 20]})
    res = ParamDict1D.from_dataframe(df, key_col='VAL', value_col='VAL')
    assert res == ParamDict1D({10: 10, 20: 20})
    assert res.key_name == 'VAL'
    assert res.value_name == 'VAL'


def test_paramdictnd_from_dataframe_value_col_in_key_cols():
    df = pd.DataFrame({'A': [1, 2], 'B': [10, 20]})
    res = ParamDictND.from_dataframe(df, key_cols=['A', 'B'], value_col='B')
    assert res == ParamDictND({(1, 10): 10, (2, 20): 20})
    assert res.key_names == ['A', 'B']
    assert res.value_name == 'B'


def test_paramdictnd_from_dataframe_single_key_col_err():
    df = pd.DataFrame({'A': [1, 2], 'B': [10, 20]})
    with pytest.raises(ValueError, match='should contain at least two column names'):
        ParamDictND.from_dataframe(df, key_cols=['A'], value_col='B')
