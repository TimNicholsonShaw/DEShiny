from shiny import reactive, render, ui
from components.status_monitor import progress_log_buffer, bulk_progress_log_buffer
from components.data_entry import data_entry_server






def server(input, output, session):
    #return_new_progress_lines_local = return_new_progress_log_lines

    data_entry_server(input, output, session)
    