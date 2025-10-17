from pathlib import Path
from shiny import reactive
import pandas as pd
from shiny import reactive, render

emoji_dict = { # emojis used to represent statuses in the progress tables
"not_started":" ",
    "running":"🏃",
    "finished":"✅"
}
sample_steps = ["extract", "trim", "align", "dedup"]
bulk_steps = ["get_data", "demux", "make_index", "feature_counts"]

def make_funcs():
    @render.text
    def text():
        return "blorpazorp"






