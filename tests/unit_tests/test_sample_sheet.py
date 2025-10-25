import pytest
from src.obj.sample_sheet import Sample, Sample_Sheet, WrongHeader, BarcodeError, SampleError
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

def test_sample_equivalence():
    s1 = Sample("sample_001", "ATGCATGC", "TGCATGCA", "GCATGCAT")
    s2 = Sample("sample_001", "ATGCATGC", "TGCATGCA", "GCATGCAT")
    assert s1 == s2

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
    test_sample_sheet.add_sample(Sample("sample_009", "CGGGAACCCGCT","GTCTTTGGCCCT","CGGGAACCCGCA"))
    assert len(test_sample_sheet) == 9

def test_remove_sample_from_sample_sheet_by_name():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    test_sample_sheet.remove_sample("sample_008")
    assert len(test_sample_sheet) == 7

def test_remove_sample_from_sample_sheet_by_object():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    test_sample = Sample("sample_001", "CGGGAACCCGCA", "GTCTTTGGCCCT", "CGGGAACCCGCA")
    test_sample_sheet.remove_sample(test_sample)
    assert len(test_sample_sheet) == 7

def test_different_index_lengths_not_valid():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    new_incorrect_row_short = pd.DataFrame({"sample_name":["sample_009"], 
                        "i7":["CGGGAACCCGCA"],
                        "i5":["GTCTTTGGCC"], # too short
                        "i1":["CGGGAACCCGCA"]})
    
    new_incorrect_row_long = pd.DataFrame({"sample_name":["sample_010"], 
                        "i7":["CGGGAACCCGCA"],
                        "i5":["GTCTTTGGCCCTTA"], # too long
                        "i1":["CGGGAACCCGCA"]})
    
    more_incorrect_row_short = pd.DataFrame({"sample_name":["sample_011"], 
                        "i7":["CGGGAACC"], # too short
                        "i5":["GTCTTTGGCCCT"], 
                        "i1":["CGGGAACC"]}) # too short

    with pytest.raises(BarcodeError) as exc_info:
        Sample_Sheet.from_pandas(pd.concat([df, 
                                            new_incorrect_row_long,
                                            new_incorrect_row_short,
                                            more_incorrect_row_short], ignore_index=True))

    problems = exc_info.value.problem_samples
    assert len(problems) == 3
    assert problems["sample_010"] == ['i5']
    assert problems["sample_009"] == ['i5']
    assert problems["sample_011"] == ['i7', 'i1']

def test_cant_add_index_wrong_length():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    with pytest.raises(BarcodeError):
        test_sample_sheet.add_sample(Sample("sample_009", "ATGCATGCGCATGAC", "TGCATGCA", "GCATGCAT"))

def test_with_invalid_samples():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    bad_row1 = pd.DataFrame({"sample_name":["sample_009"], 
                        "i7":["CGGGAQACCGCA"],
                        "i5":["GTCTTTCCCCCT"],
                        "i1":["CGGGAACCCGCA"]})
    bad_row2 = pd.DataFrame({"sample_name":["sample_009"], 
                        "i7":["CGGGAGACCGCA"],
                        "i5":[7],
                        "i1":["CGGGAACCCGCA"]})

    with pytest.raises(SampleError) as exc_info:
        Sample_Sheet.from_pandas(pd.concat([df,
                                            bad_row1,], ignore_index=True))
        Sample_Sheet.from_pandas(pd.concat([df,
                                            bad_row2,], ignore_index=True))
    
def test_repeated_barcodes_invalid():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    duplicate_barcode = pd.DataFrame({"sample_name":["sample_009"], 
                        "i7":["CGGGAACCCGCA"],
                        "i5":["GTCTTTGGCCCT"],
                        "i1":["AGTCTCAGCAAA"]})
    
    with pytest.raises(BarcodeError):
        Sample_Sheet.from_pandas(pd.concat([df,
                                            duplicate_barcode],
                                            ignore_index=True)
        )

def test_repeated_sample_names_invalid():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    duplicate_name = pd.DataFrame({"sample_name":["sample_002"], 
                        "i7":["CGGGAACCCGCA"],
                        "i5":["GTCTTTGGCCCT"],
                        "i1":["AGTCTCAGCAGG"]})
    
    df = pd.concat([df, duplicate_name], ignore_index=True)

    print(df)
    
    with pytest.raises(SampleError):
        Sample_Sheet.from_pandas(pd.concat([df,
                                            duplicate_name],
                                            ignore_index=True)
        )
    
def test_cant_add_sample_name_already_present():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    repeat_sample_name = Sample("sample_001","CGGGAACCCGCC","GTCTTTGGCGCT","AGTCTCAGCATA")
    
    with pytest.raises(SampleError):
        test_sample_sheet.add_sample(repeat_sample_name)

def test_cant_add_barcode_already_present():
    test_sample_sheet = Sample_Sheet.from_csv(Path("tests/sample-sheet.csv"))
    repeat_sample_name = Sample("sample_009","CGGGAACCCGCA","GTCTTTGGCCCT","TCCTCTCTTCTA")
    
    with pytest.raises(BarcodeError):
        test_sample_sheet.add_sample(repeat_sample_name)

def test_wrong_header_names():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    df = df.rename(columns={"sample_name":"simple_nom"})

    with pytest.raises(WrongHeader):
        Sample_Sheet.from_pandas(df)
    
def test_extra_columns_in_sample_sheet_ok():
    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    df["blurp"] = 5

    Sample_Sheet.from_pandas(df)


