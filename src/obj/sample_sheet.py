from pathlib import Path
import pandas as pd
from statistics import mode
from collections import Counter

class WrongHeader(Exception):
    def __init__(self, message, bad_header):
        super().__init__(message)
        self.bad_header=bad_header
        self.message=message

class BarcodeError(Exception):
    def __init__(self, message, problem_samples):
        super().__init__(message)
        self.problem_samples = problem_samples

class SampleError(Exception):
    def __init__(self, message, bad_sample):
        super().__init__(message)
        self.bad_sample = bad_sample
        

# TODO refactor with custom exceptions
class Sample:
    def __init__(self, name:str, i7:str, i5:str, i1:str):
        self.name=name
        self.i7=i7
        self.i5=i5
        self.i1=i1

        if self.is_valid():
            self._make_upper()
    
    def is_valid(self):
        if self._check_properties_are_strings() == False:
            return False
        
        if self._check_correct_bases() == False:
            return False
        
        return True
    
    def _check_properties_are_strings(self):
        for variable in vars(self).values(): # everything should be a strin
            if type(variable) != str:
                return False
            
        return True
    
    def _make_upper(self):
        self.i7 = self.i7.upper()
        self.i5 = self.i5.upper()
        self.i1 = self.i1.upper()


    def _check_correct_bases(self):
        for seq in (self.i1, self.i5, self.i7):
            for base in seq:
                if base not in "ATGCatgc":
                    return False
        return True
    
    def __repr__(self):
        return f'{self.name} -> i7:{self.i7} i5:{self.i5} i1:{self.i1}'
    
    def __eq__(self, other):
        return all([self.name==other.name,
                   self.i7==other.i7,
                   self.i5==other.i5,
                   self.i1==other.i1])
    
    def get_smashed_barcode(self):
        return f'{self.i7}{self.i5}{self.i1}'


class Sample_Sheet:
    def __init__(self, samples:list[Sample]):
        self.samples = samples # dict version

    @staticmethod
    def from_csv(sample_sheet_path:Path):

        df = pd.read_csv(sample_sheet_path)

        return Sample_Sheet.from_pandas(df)
    
    @staticmethod
    def from_pandas(df:pd.DataFrame):
        Sample_Sheet._check_header(df.columns)

        out_samples = []
        for i in range(len(df)):
            out_samples.append(Sample(df['sample_name'][i],
                       df['i7'][i],
                       df['i5'][i],
                       df['i1'][i]
                        )
            )
        sample_sheet = Sample_Sheet(out_samples)
        sample_sheet._check_valid_samples()
        sample_sheet._check_index_lengths()
        sample_sheet._check_duplicate_barcodes_and_sample_names()
        return Sample_Sheet(out_samples)


    def _check_header(header:list[str]):
        correct_headers = ['sample_name', 'i7', 'i5', 'i1']
        if not all(col_name in header for col_name in correct_headers):
            raise(WrongHeader(header, f"Headers you provided were: {header}. Headers should be: {correct_headers}"))
        
    def add_sample(self, sample:Sample):
        if sample.name in [s.name for s in self.samples]:
            raise(SampleError("Sample name already in use", sample.name))
        if sample.get_smashed_barcode() in [s.get_smashed_barcode() for s in self.samples]:
            raise(BarcodeError("Barcode already in use", sample.name))
        self.samples.append(sample)
        try:
            self._check_index_lengths()
        except BarcodeError as e:
            self.remove_sample(sample)
            raise(e)

    def remove_sample(self, remove_sample:Sample|str):
        if type(remove_sample) == Sample: remove_sample = remove_sample.name
        
        self.samples = [sample for sample in self.samples if sample.name != remove_sample]
    
    def _check_index_lengths(self) -> bool:
        i7_length = mode([len(sample.i7) for sample in self.samples])
        i5_length = mode([len(sample.i5) for sample in self.samples])
        i1_length = mode([len(sample.i1) for sample in self.samples])

        problem_samples = {}

        for sample in self.samples:
            if len(sample.i7) != i7_length:
                problem_samples[sample.name] = problem_samples.get(sample.name, []) + ["i7"]
            if len(sample.i5) != i5_length:
                problem_samples[sample.name] = problem_samples.get(sample.name, []) + ["i5"]
            if len(sample.i1) != i1_length:
                problem_samples[sample.name] = problem_samples.get(sample.name, []) + ["i1"]
        
        if len(problem_samples) > 0:
            raise(BarcodeError("Barcodes different lengths", problem_samples))
        
        return True
    
    def _check_valid_samples(self):
        for sample in self.samples:
            if not sample.is_valid():
                raise(SampleError("invalid sample", sample))
            
    def _check_duplicate_barcodes_and_sample_names(self):
        barcodes = []
        sample_names = []
        for sample in self.samples:
            sample_names.append(sample.name)
            barcodes.append(f'{sample.i7}{sample.i5}{sample.i1}')

        sample_name_duplicates = [item for item, count in Counter(sample_names).items() if count > 1]
        barcode_duplicates = [item for item, count in Counter(barcodes).items() if count > 1]


        if len(sample_name_duplicates) > 0:
            raise(SampleError("Duplicate sample names", sample_name_duplicates))
        
        if len(barcode_duplicates) > 0:
            bad_samples = []
            # TODO make this less slow and dumb
            for barcode in barcode_duplicates:
                for i in range(len(barcodes)):
                    if barcodes[i] == barcode: bad_samples.append(sample_names[i])
            
            raise(BarcodeError("Duplicate Barcodes", bad_samples))

        
    def __len__(self):
        return len(self.samples)
    
    def __repr__(self):
        return "\n".join([sample.__repr__() for sample in self.samples])

if __name__ == "__main__":

    df = pd.read_csv(Path("tests/sample-sheet.csv"))
    duplicate_barcode = pd.DataFrame({"sample_name":["sample_009"], 
                        "i7":["CGGGAACCCGCA"],
                        "i5":["GTCTTTGGCCCG"],
                        "i1":["AGTCTCAGCAAA"]})
    

    s_sheet = Sample_Sheet.from_pandas(pd.concat([df,
                                            duplicate_barcode],
                                            ignore_index=True)
        )
    
    
    print(s_sheet)