from pathlib import Path
import pandas as pd
from statistics import mode

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


class Sample_Sheet:
    def __init__(self, samples:dict[Sample]={}):
        self.samples = samples

    @staticmethod
    def from_csv(sample_sheet_path:Path):

        df = pd.read_csv(sample_sheet_path)

        return Sample_Sheet.from_pandas(df)
    
    @staticmethod
    def from_pandas(df:pd.DataFrame):
        Sample_Sheet._check_header(df.columns)

        out_samples = {}
        for i in range(len(df)):
            out_samples[df['sample_name'][i]] = Sample(df['sample_name'][i],
                       df['i7'][i],
                       df['i5'][i],
                       df['i1'][i]
            )
        sample_sheet = Sample_Sheet(out_samples)
        sample_sheet._check_index_lengths()
        return Sample_Sheet(out_samples)


    def _check_header(header:list[str]):
        correct_headers = ['sample_name', 'i7', 'i5', 'i1']
        if not all(col_name in header for col_name in correct_headers):
            raise(WrongHeader(header, f"Headers you provided were: {header}. Headers should be: {correct_headers}"))
        
    def add_sample(self, sample:Sample):
        self.samples[sample.name] = sample

    def remove_sample(self, sample:Sample|str):
        if type(sample) == str:
            del self.samples[sample]
        elif type(sample) == Sample:
    
            for index, value in self.samples.items():
                if value == sample:
                    del self.samples[index]
                    break
    
    def _check_index_lengths(self) -> bool:
        i7_length = mode([len(sample.i7) for _, sample in self.samples.items()])
        i5_length = mode([len(sample.i5) for _, sample in self.samples.items()])
        i1_length = mode([len(sample.i1) for _, sample in self.samples.items()])

        problem_samples = {}

        for name, sample in self.samples.items():
            if len(sample.i7) != i7_length:
                problem_samples[name] = problem_samples.get(name, []) + ["i7"]
            if len(sample.i5) != i5_length:
                problem_samples[name] = problem_samples.get(name, []) + ["i5"]
            if len(sample.i1) != i1_length:
                problem_samples[name] = problem_samples.get(name, []) + ["i1"]
        
        if len(problem_samples) > 0:
            raise(BarcodeError("Barcodes different lengths", problem_samples))
        
        return True


        
    def __len__(self):
        return len(self.samples)

if __name__ == "__main__":
    sample_sheet = Sample_Sheet.from_csv("tests/sample-sheet.csv")
    sample_sheet._check_index_lengths()