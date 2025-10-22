from shiny import reactive, ui, render, module
from pathlib import Path
import pandas as pd



# hard coded resources
emoji_dict = { # emojis used to represent statuses in the progress tables
"not_started":" ",
    "running":"🏃",
    "finished":"✅"
}

################## ui ####################

@module.ui
def status_monitor_ui():
    return ui.page_fillable(
        ui.card(
            ui.card_header("Bulk Process Status"),
            ui.output_data_frame("bulk_status_table")
        ),
        ui.card(
            ui.card_header("Sample Progress Status"),
            ui.output_data_frame("sample_status_table")
        )
    )

################ server ###############
@module.server
def status_monitor_server(input, output, session, samples):

# FIXME sample progress and bulk progress should read from a stream

    ################### sample progress #####################
    sample_steps = ["extract", "trim", "align", "dedup"]
    sample_progress_df = reactive.value(pd.DataFrame())
    sample_progress_path = Path("logs/progress.log")

    @reactive.calc
    def populate_progress_df():
        sample_names = samples()
        with reactive.isolate():
            if sample_progress_df().empty:
                sample_progress_df.set( pd.DataFrame(
                    emoji_dict["not_started"],
                    index=sample_names,
                    columns=sample_steps
                ).reset_index().rename(columns={"index":"sample_name"})\
                .set_index("sample_name", drop=False))   
        
        return sample_progress_df
    
    def update_progress_df():
        for line in open(sample_progress_path):
            line = line.rstrip().split(",")
            sample_progress_df().loc[line[0], line[1]] = emoji_dict[line[2]]
        
        return sample_progress_df

    @render.data_frame
    @reactive.file_reader(sample_progress_path)
    def sample_status_table():
        populate_progress_df()
        return render.DataGrid(
            update_progress_df().get(),
            styles=[
                    {
                        "class":"text-center"
                    },
                    {
                        "names":True
                    },
                ]
            )  
    
    ################## bulk progress ####################

    bulk_steps = ["get_data", "demux", "make_index", "feature_counts"]
    bulk_progress_path = Path("logs/bulk_progress.log")
    bulk_progress_df = reactive.value(
        pd.DataFrame(
            emoji_dict["not_started"],
            index=["bulk_step"],
            columns=bulk_steps
        )
    )

    def update_bulk_status_table():
        for line in open(bulk_progress_path, "r"):
                line = line.rstrip().split(",")
                bulk_progress_df().loc["bulk_step", line[1]] = emoji_dict[line[2]]

        return bulk_progress_df

    @render.data_frame
    @reactive.file_reader(bulk_progress_path)
    def bulk_status_table():
        return render.DataGrid(
            update_bulk_status_table().get(),
            styles=[
                    {
                        "class":"text-center"
                    },
                    {
                        "names":True
                    },
                ]
            )