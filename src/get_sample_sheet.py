import yaml
import subprocess
import pandas as pd 

with open('src/snakemakeconfig.yaml', 'r') as file:
    config = yaml.safe_load(file)
    subprocess.run(["mkdir", "-p", "res"])
    subprocess.run(["wget", 
                    "-O",
                    "res/sample_sheet.csv",
                    config["demux"]["sample_sheet"]
                    ])

    
