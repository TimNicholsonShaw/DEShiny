from shiny import reactive, render, ui
from components.status_monitor import status_monitor_server
from components.data_entry import data_entry_server






def server(input, output, session):


    data_entry_server(input, output, session)
    status_monitor_server(input, output, session)
    