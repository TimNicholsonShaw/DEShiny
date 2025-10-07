from datetime import datetime
from sys import argv
import pandas as pd

data_folder = "outputs/aligned/"

def parse_star_log(sample_name:str, 
                   data_folder=data_folder, 
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

if __name__=="__main__":
    out = {}
    for log in argv[1:]:
        out[log.replace(".Log.final.out", "")] = parse_star_log(log)
    df = pd.DataFrame(out).transpose().reset_index(names=["sample_name"])
    df.to_csv(f'{data_folder}align_summary.csv', index=False)

