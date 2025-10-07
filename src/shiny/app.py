from shiny import render, reactive, req
from shiny.express import input, ui
import pandas as pd
from pathlib import Path
from resource_entry import enter_resources, make_snakemake_config
import subprocess, os
from shiny_validate import InputValidator, check
import plotly.express as px
from shinywidgets import render_widget 


################ full app options ################
ui.page_opts(
     title="Differential Expression Shiny" 
 )

############## reference ##############

emoji_dict = { # emojis used to represent statuses in the progress tables
"not_started":" ",
    "running":"🏃",
    "finished":"✅"
}

sample_steps = ["extract", "trim", "align", "dedup"]

bulk_steps = ["get_data", "demux", "make_index", "feature_counts"]

################# reactive log monitoring ####################
progress_log_loc = Path("logs/progress.log")
global_progress_file_position = 0

bulk_progress_log_loc =Path("logs/bulk_progress.log")
global_bulk_progress_file_position = 0


############# reactive values ####################

@reactive.file_reader(progress_log_loc)
def return_new_progress_log_lines(progress_log_loc=progress_log_loc):
    global global_progress_file_position
    buffer = []

    while True:
        try:
            with open(progress_log_loc, 'r') as log:
                log.seek(global_progress_file_position)
                line=log.readline().rstrip()
                global_progress_file_position = log.tell()
                if line:
                    buffer.append(line)
                else:
                    break
        except:
            return buffer
    return buffer

@reactive.file_reader(bulk_progress_log_loc)
def return_new_bulk_progress_log_lines(progress_log_loc=bulk_progress_log_loc):
    global global_bulk_progress_file_position
    buffer = []

    while True:
        try:
            with open(progress_log_loc, 'r') as log:
                log.seek(global_bulk_progress_file_position)
                line=log.readline().rstrip()
                global_bulk_progress_file_position = log.tell()
                if line:
                    buffer.append(line)
                else:
                    break
        except:
            return buffer
    return buffer

individual_progress_df = reactive.value(pd.DataFrame())
bulk_progress_df = reactive.value(pd.DataFrame())
sample_sheet = reactive.value(pd.DataFrame())
samples = reactive.value([])


################# UI ###################
################# data entry ############
with ui.nav_panel("Data Entry"):

    ########### validation #############
    enter_resources() 
    # Unfortunate workaround to get InputValidator to work in Express
    input_validator = None

    @reactive.effect
    def _validator():
        # Add validation rules for each input that requires validation
        global input_validator
        input_validator = InputValidator()
        input_validator.add_rule("r1_loc", check.required())
        input_validator.add_rule("r1_loc", check.url())
        input_validator.add_rule("r2_loc", check.required())
        input_validator.add_rule("r2_loc", check.url())
        input_validator.add_rule("sample_sheet", check.required())
        input_validator.add_rule("genome_fasta_loc", check.required())
        input_validator.add_rule("genome_fasta_loc", check.url())        
        input_validator.add_rule("annotation_loc", check.required())
        input_validator.add_rule("annotation_loc", check.url())
    
    ###################################
    @render.text
    @reactive.calc
    def set_sample_df() -> None:
        if not input.sample_sheet():
            return
        
        try:
            sample_sheet_loc = input.sample_sheet()[0]["datapath"]
            sample_sheet.set(pd.read_csv(sample_sheet_loc))

        except IndexError:
            return

    @render.text
    @reactive.calc
    def set_sample_names() -> None:
        if not input.sample_sheet():
            return
        try:
            samples.set(
                sample_sheet.get()["sample_name"].values
            ) 
        except IndexError:
            return
    
    with ui.layout_columns(col_widths=(3,3,6)):
        ui.input_action_button(
            "start_pipeline", 
            "Start Pipeline", 
            width=1
            )
        ui.input_action_button(
            "shutdown_container",
            "Shutdown Container",
            width=1
        )
        ui.div(width=10)
    
    @render.text
    @reactive.event(input.start_pipeline)
    def run_snakemake(sample_steps=sample_steps, bulk_steps=bulk_steps):
        input_validator.enable()
        req(input_validator.is_valid())
        if len(samples.get()) == 0:
            return "Invalid sample sheet"
        
        individual_progress_df.set(
            pd.DataFrame(
                emoji_dict["not_started"],
                index=samples.get(),
                columns=sample_steps
            ).reset_index().rename(columns={"index":"sample_name"})\
            .set_index("sample_name", drop=False)
        )

        bulk_progress_df.set(
            pd.DataFrame(
                emoji_dict["not_started"],
                index=["bulk_step"],
                columns=bulk_steps
            )
        )

        make_snakemake_config(
            demux_r1_loc = input.r1_loc(),
            demux_r2_loc = input.r2_loc(),
            demux_sample_sheet = input.sample_sheet()[0]["datapath"],
            align_genome = input.genome_fasta_loc(),
            align_annotation = input.annotation_loc()
        )

        ui.update_action_button("start_pipeline", disabled=True)

        # kick off pipeline
        subprocess.Popen(["conda", "run", "--no-capture-output", "-n", "test-env",
            "snakemake", "--snakefile", "src/Snakefile", "--configfile","res/snakemakeconfig.yaml",
            "--cores", "all", "--keep-incomplete"])
        
    @render.text
    @reactive.event(input.shutdown_container)
    def click_shutdown_container():
        cmd = "ps -afx | grep tail | awk '{print $1}' | xargs kill -9"
        subprocess.run(cmd, shell=True)


    with ui.card():
        ui.card_header("Sample Sheet")
        @render.data_frame
        def blah():
            return sample_sheet.get()
        
################## progress monitoring ##################
with ui.nav_panel("Pipeline Status"):
    with ui.card():
        ui.card_header("Pipeline Sample Status")
        
        @render.data_frame
        @reactive.calc
        def render_progress_df():
            if len(samples.get()) == 0:
                return
            
            df = individual_progress_df.get()

            for line in return_new_progress_log_lines():
                line = line.rstrip().split(",")
                df.loc[line[0], line[1]] = emoji_dict[line[2]]

                individual_progress_df.set(df)


            return render.DataTable(
                individual_progress_df(),
                styles=[
                    {
                        "class":"text-center"
                    },
                    {
                        "names":True
                    },
                ]
                )
    with ui.card():
        ui.card_header("Bulk Process Status")



        @render.data_frame
        @reactive.calc
        def render_bulk_progress_df():
            if len(samples()) == 0:
                return
            df = bulk_progress_df()
            for line in return_new_bulk_progress_log_lines():
                line = line.rstrip().split(",")
                df.loc["bulk_step", line[1]] = emoji_dict[line[2]]

                bulk_progress_df.set(df)



            return render.DataTable(
                bulk_progress_df(),
                styles=[
                    {
                        "class":"text-center"
                    },
                    {
                        "names":True
                    },
                ]
                )
        
############## demux stats ##################
with ui.nav_panel("Demux Stats"):
    demux_path = Path("outputs/idemultiplexed/demultipexing_stats.tsv")
    demux_path.parents[0].mkdir(parents=True, exist_ok=True)
    demux_path.touch()


    @reactive.calc
    @reactive.file_reader(demux_path)
    def get_demux_df():
        try:
            df = pd.read_csv(demux_path, delimiter="\t")
            sample_order = list(samples()) +["undetermined"]
            df = df.set_index("sample_name", drop=False).reindex(sample_order)

            return df
        except:
            return
    
    @render.data_frame
    def render_demux_stats():
        return get_demux_df()
    
    @render_widget
    def render_demux_bar():
        try:
            return px.bar(get_demux_df(), x="sample_name", y="written_reads")
        except:
            return


    # @render.data_frame
    # @reactive.file_reader(demux_path)
    # def render_demux_stats_table():
    #     try:
    #         df = pd.read_csv(demux_path, delimiter="\t")
    #         sample_order = list(samples()) +["undetermined"]

    #         df = df.set_index("sample_name", drop=False).reindex(sample_order)
            
    #         return df
    #     except:
    #         return
        
    # @render_widget
    # @reactive.file_reader(demux_path)
    # def render_demux_bar():
    #     try:
    #         df = pd.read_csv(demux_path, delimiter="\t")

    #         return px.bar(df, x="sample_name", y="written_reads")
    #     except:
    #         return
    




