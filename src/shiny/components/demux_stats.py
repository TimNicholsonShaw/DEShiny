from shiny import reactive, ui, module, render
from pathlib import Path
import pandas as pd
import plotly.express as px
from shinywidgets import render_widget, output_widget


demux_path = Path("outputs/idemultiplexed/demultipexing_stats.tsv")
demux_path.parents[0].mkdir(parents=True, exist_ok=True)
demux_path.touch()

@module.ui
def demux_stats_ui():
    return ui.page_fillable(
    ui.card(
        ui.card_header("Index Assignments"),
        ui.output_data_frame("index_assignment_table")
    ),
    ui.card(
        ui.card_header("Index Assignment Graph"),
        output_widget("index_assignment_graph")
    )

)


@module.server
def demux_stats_server(input, output, session, samples):
    
    @reactive.calc
    @reactive.file_reader(demux_path)
    def get_demux_df():
        try:
            df = pd.read_csv(demux_path, delimiter="\t")
            sample_order = list(samples()) +["undetermined"]
            df = df.set_index("sample_name", drop=False).reindex(sample_order)
            return df
        
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    

    @render.data_frame
    def index_assignment_table():
        return get_demux_df()
    
    @render_widget
    def index_assignment_graph():
        df = get_demux_df()
        if not df.empty: 
            return px.bar(get_demux_df(), x="sample_name", y="written_reads")
