from shiny import reactive, render, ui
from components.status_monitor import status_monitor_server
from components.data_entry import data_entry_server






def server(input, output, session):
    global_sample_names = reactive.value([])

    data_entry_server("data_entry_module", global_sample_names)
    status_monitor_server("status_monitor_module", global_sample_names)
    