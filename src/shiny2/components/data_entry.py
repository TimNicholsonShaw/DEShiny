from shiny import ui, reactive


################ data entry page UI ###################

data_entry_ui = ui.page_fillable(
    ui.card( # Sample sheet and fastq location entry
        ui.card_header("Input Files"),
        ui.input_text("r1_loc", 
                        "Read 1 Location URL", 
                        value="https://github.com/TimNicholsonShaw/DEShiny/raw/refs/heads/main/tests/R1.fastq.gz",
                        width="100%"),
        ui.input_text("r2_loc", 
                        "Read 2 Location URL", 
                        value="https://github.com/TimNicholsonShaw/DEShiny/raw/refs/heads/main/tests/R2.fastq.gz",
                        width="100%"),

        # TODO add code to disable after pipeline kickoff
        ui.input_file("sample_sheet", "Sample Sheet"),
        fill=True
    ),

    ui.card( # Genome file entry
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
        ),

        # TODO add button to restart pipeline
        ui.layout_columns( # buttons to kick off and close pipeline
            ui.input_action_button(
                "start_pipeline", 
                "Start Pipeline", 
                width=1
                ),
            # TODO Put some kind of "are you sure?" confirmation
            ui.input_action_button(
                "shutdown_container",
                "Shutdown Container",
                width=1
            ),
            ui.div(width=10),
            col_widths=(3,3,6)
        )
)
