from datetime import datetime
from sys import argv
import pandas as pd

alignment_data_folder = "outputs/aligned/"
dedup_data_folder = "outputs/dedup/"

def parse_star_log(sample_name:str, 
                   data_folder=alignment_data_folder, 
                   file_extension=".Log.final.out") -> dict:
    out_dict={}
    datetime_fmt = "%b %d %H:%M:%S"
    

    with open(f'{data_folder}{sample_name}{file_extension}', "r") as log:
        for line in log:
            line = line.strip().replace("\t", "").split("|")
            line[0] = line[0].strip()
            if len(line) != 2: continue
            out_dict[line[0]] = line[1]
    start = datetime.strptime(out_dict["Started job on"], datetime_fmt)
    finish = datetime.strptime(out_dict["Finished on"], datetime_fmt)
    out_dict["time_minutes"] = (finish - start).total_seconds()/60

    return out_dict

def parse_dedup_log(sample_name:str,
                    data_folder=dedup_data_folder,
                    file_extension="_dedup.log") -> dict:
    
    out = {}
    
    with open(f'{data_folder}{sample_name}{file_extension}', "r") as log:
        for line in log:
            if line.startswith("#"): continue
            line=line.strip().split("INFO")[-1]
            line = line.split(":")
            if len(line) == 1:
                line=line[0].split(" ")
            if line[0] == " command": continue
            out[line[-2].lstrip()] = line[-1]
    
    return out

if __name__=="__main__":
    if len(argv) == 1:
        print(parse_dedup_log("sample_001"))

    elif argv[1] == "align":
        out = {}
        for log in argv[2:]:
            out[log] = parse_star_log(log)
        df = pd.DataFrame(out).transpose().reset_index(names=["sample_name"])
        df.to_csv(f'{alignment_data_folder}align_summary.csv', index=False)
    
    elif argv[1] == "dedup":
        out = {}
        for log in argv[2:]:
            out[log] = parse_dedup_log(log)
        df = pd.DataFrame(out).transpose().reset_index(names="sample_name")
        df.to_csv(f'{dedup_data_folder}dedup_summary.csv', index=False)
