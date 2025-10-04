from shiny import render, ui
from shiny.express import input
import pandas as pd

ui.panel_title("Differential Expression Shiny")

@render.data_frame
def sample_table():
    return pd.read_csv("res/sample_sheet.csv")
