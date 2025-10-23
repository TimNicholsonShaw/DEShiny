from pathlib import Path
import pandas as pd

class WrongHeader(Exception):
    def __init__(self, header, message):
        self.header=header
        self.message=message
        super().__init__(self.message)


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


class Sample_Sheet:
    def __init__(self, samples:list[Sample]=[]):
        self.samples = samples

    @staticmethod
    def from_csv(sample_sheet_path:Path):

        df = pd.read_csv(sample_sheet_path)
        Sample_Sheet.check_header(df.columns)


        out_samples = []
        for i in range(len(df)):
            out_samples.append(
                Sample(df['sample_name'][i],
                       df['i7'][i],
                       df['i5'][i],
                       df['i1'][i]
                )
            )
        return Sample_Sheet(out_samples)
    
    @staticmethod
    def from_pandas(df:pd.DataFrame):
        Sample_Sheet.check_header(df.columns)

        out_samples = []
        for i in range(len(df)):
            out_samples.append(
                Sample(df['sample_name'][i],
                       df['i7'][i],
                       df['i5'][i],
                       df['i1'][i]
                )
            )
        return Sample_Sheet(out_samples)

    @staticmethod
    def check_header(header:list[str]):
        correct_headers = ['sample_name', 'i7', 'i5', 'i1']
        if not all(col_name in correct_headers for col_name in header):
            raise(WrongHeader(header, f"Headers you provided were: {header}. Headers should be: {correct_headers}"))
        

    
    def add_sample(self, sample:Sample):
        self.samples.append(sample)
    
    def __len__(self):
        return len(self.samples)


