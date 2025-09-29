import pandas as pd 
import yaml

with open("src/snakemakeconfig.yaml") as file:
    config_data=yaml.safe_load(file)

print(config_data)

df = pd.read_csv(config_data["sample_sheet"])
print(list(df["sample_name"]))