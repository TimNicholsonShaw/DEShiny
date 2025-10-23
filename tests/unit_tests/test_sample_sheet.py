import pytest
from src.obj.sample_sheet import Sample, Sample_Sheet, WrongHeader
from pathlib import Path
import pandas as pd

# Sample object tests

def test_make_valid_sample():
    assert Sample("sample_001", "ATGCATGC", "TGCATGCA", "GCATGCAT").is_valid() == True


def test_wrong_base_index():
    assert Sample("sample_001", "ATGZATGC", "TGCATGCA", "GCATGCAT").is_valid() == False
    assert Sample("sample_001", "ATGCATGC", "TGCATGCQ", "GCATGCAT").is_valid() == False
    assert Sample("sample_001", "ATGCATGC", "TGCATGCA", "GPATGCAT").is_valid() == False


def test_numbers_instead_of_bases():
    assert Sample(15, "ATGCATGC", "TGCATGCA", "GCATGCAT").is_valid() == False
    assert Sample("sample_001", 12, "TGCATGCA", "GCATGCAT").is_valid() == False
    assert Sample("sample_001", "ATGCATGC", 124, "GCATGCAT").is_valid() == False
    assert Sample("sample_001", "ATGCATGC", "TGCATGCA", 500).is_valid() == False


def test_lowercase_inputs_handled():
    test_sample = Sample("sample_001", "atgcatgc", "tgcatgca", "gcatgcat")
    test_sample._make_upper
    assert test_sample.i7.isupper()
    assert test_sample.i5.isupper()
    assert test_sample.i1.isupper()

# sample sheet

def test_read_in_from_csv():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))

    assert len(test_sample_sheet) == 8
    for sample in test_sample_sheet.samples:
        assert type(sample) == Sample

def test_read_in_from_pandas_df():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    test_sample_sheet = Sample_Sheet.from_pandas(df)
    assert len(test_sample_sheet) == 8

def test_add_sample_to_sample_sheet():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    test_sample_sheet.add_sample(Sample("sample_009", "ATGCATGG", "TGCATGCA", "GCATGCAT"))
    assert len(test_sample_sheet) == 9

def test_remove_sample_from_sample_sheet():
    pass

def test_different_index_lengths_not_valid():
    pass

def test_with_invalid_samples():
    pass

def test_repeated_barcodes_invalid():
    pass

def test_repeated_sample_names_invalid():
    pass

def test_wrong_header_names():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    df = df.rename(columns={"sample_name":"simple_nom"})

    with pytest.raises(WrongHeader):
        Sample_Sheet.from_pandas(df)
    
    
def test_extra_columns_in_sample_sheet_ok():
    pass

