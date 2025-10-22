from shiny import ui, reactive, render, module
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget
from pathlib import Path

@module.ui
def align_stats_ui():
    return ui.page_fillable(
    ui.card(
        ui.card_header("Alignment Stats"),
        ui.output_data_frame("align_table")
    ),
    ui.card(
        ui.card_header("Uniquely Mapped Reads Percentage"),
        output_widget("align_graph")
    )
)


@module.server
def align_stats_server(input, output, session):
    align_summary_path = Path("outputs/aligned/align_summary.csv")
    
    # FIXME better error handling
    @reactive.calc
    @reactive.file_reader(align_summary_path)
    def get_align_df():
        try:
            return pd.read_csv(align_summary_path)
        except:
            return

    # FIXME better error handling
    @render.data_frame
    def align_table():
        try:
            return get_align_df()
        except:
            return
    
    # FIXME better error handling
    @render_widget
    def align_graph():
        try:
            df = get_align_df()
            df["Uniquely mapped reads %"] = df["Uniquely mapped reads %"].str.rstrip("%").astype('float')
            return px.bar(df, x="sample_name", y="Uniquely mapped reads %")
        except:
            return
