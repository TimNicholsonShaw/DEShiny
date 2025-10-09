from shiny import ui, reactive, render
from shiny.express import input
import yaml

def make_snakemake_config(output:str="res/snakemakeconfig.yaml",
                          **kwargs) -> None:
    
    config = {}
    
    # set demux options
    config['demux'] = {
        "r1":kwargs['demux_r1_loc'], # required
        "r2":kwargs["demux_r2_loc"], # required
        "sample_sheet":kwargs["demux_sample_sheet"] # required
    }

    # set alignment options
    config['align'] = {
        "threads":kwargs.get("align_threads", 12), 
        "genome_fasta_location":kwargs["align_genome"], # required
        "genome_annotation_location":kwargs["align_annotation"], # required
        "sjdb_overhang":kwargs.get("align_sjdb_overhang", 99)
    }

    with open(output, 'w') as file:
        yaml.safe_dump(config, file)

def enter_resources():
    return(
        ui.card(
            ui.card_header("Input Files"),
            ui.input_text("r1_loc", 
                          "Read 1 Location URL", 
                          value="https://github.com/TimNicholsonShaw/DEShiny/raw/refs/heads/main/tests/R1.fastq.gz",
                          width="100%"),
            ui.input_text("r2_loc", 
                          "Read 2 Location URL", 
                          value="https://github.com/TimNicholsonShaw/DEShiny/raw/refs/heads/main/tests/R2.fastq.gz",
                          width="100%"),
            ui.input_file("sample_sheet", "Sample Sheet"),
            fill=True
        ),
        ui.card(
            ui.card_header("Genome Files"),
            ui.input_text("genome_fasta_loc", 
                          "Genome fasta.gz URL",
                          value="https://github.com/TimNicholsonShaw/DEShiny/raw/refs/heads/main/tests/GRCh38_chr20.fa.gz",
                          width="100%"
                          ),
            ui.input_text("annotation_loc",
                          "Genome Annotation URL",
                          value="https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_49/gencode.v49.basic.annotation.gtf.gz",
                          width="100%"
                          )
        )


    )

if __name__=="__main__":
    make_snakemake_config(output="res/snakemakeconfig_test.yaml", 
                          align_threads=12, 
                          demux_r1_loc="r1 boop", 
                          demux_r2_loc="r2 boop",
                          align_genome="align genome",
                          align_annotation="annotation")