from shiny import ui, reactive, render, module
from pathlib import Path
import pandas as pd

@module.ui
def dedup_stats_ui(): 
    return ui.page_fillable(
    ui.card(
        ui.card_header("Deduplication Summary"),
        ui.output_data_frame("dedup_table")
    )
)


@module.server
def dedup_stats_server(input, output, session):
    dedup_summary_path = Path("outputs/dedup/dedup_summary.csv")

    @reactive.calc
    @reactive.file_reader(dedup_summary_path)
    def get_dedup_df():
        try:
            df = pd.read_csv(dedup_summary_path)
            return df
        except:
            return

    
    @render.data_frame
    def dedup_table():
        try:
            return get_dedup_df()
        except:
            return