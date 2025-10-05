from shiny import render, reactive
from shiny.express import input, ui
import pandas as pd
from shiny.ui import page_navbar
from functools import partial
from pathlib import Path


ui.page_opts(
    title="Differential Expression Shiny" 
)

############################
# read samples in from the sample sheet, downloaded by entry point of docker file
samples = pd.read_csv("res/sample_sheet.csv")["sample_name"]

emoji_dict = { # emojis used to represent statuses in the progress tables
"not_started":" ",
    "running":"🏃",
    "finished":"✅"
}

################# individual step progress monitoring ##################
steps = ["extract", "trim", "align", "dedup"]
progress_df = pd.DataFrame(emoji_dict["not_started"], index=samples, columns=steps)\
    .reset_index().set_index("sample_name", drop=False)
progress_log_loc = Path("logs/progress.log")
global_progress_file_position = 0

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

################# bulk step progress monitoring #####################
bulk_steps = ["get_data", "demux", "make_index", "feature_counts"]
bulk_progress_df = pd.DataFrame(emoji_dict["not_started"], index=["bulk_step"], columns=bulk_steps)
bulk_progress_log_loc =Path("logs/bulk_progress.log")
global_bulk_progress_file_position = 0

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

################# UI ###################

with ui.nav_panel("Pipeline Status"):
    with ui.card():
        ui.card_header("Pipeline Sample Status")
        @render.data_frame
        def render_progress_df():
            for line in return_new_progress_log_lines():
                line = line.rstrip().split(",")
                try:
                    progress_df.loc[line[0], line[1]] = emoji_dict[line[2]]
                except:
                    continue

            return render.DataTable(
                progress_df,
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
        def render_bulk_progress_df():
            for line in return_new_bulk_progress_log_lines():
                line = line.rstrip().split(",")
                try:
                    bulk_progress_df.loc["bulk_step", line[1]] = emoji_dict[line[2]]
                except:
                    continue

            return render.DataTable(
                bulk_progress_df,
                styles=[
                    {
                        "class":"text-center"
                    },
                    {
                        "names":True
                    },
                ]
                )
        

