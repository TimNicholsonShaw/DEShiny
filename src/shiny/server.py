from shiny import reactive, render, ui
from components.status_monitor import status_monitor_server
from components.data_entry import data_entry_server
from components.demux_stats import demux_stats_server
from components.align_stats import align_stats_server
from components.dedup_stats import dedup_stats_server
from components.tpm import tpm_server






def server(input, output, session):
    global_sample_names = reactive.value([])

    data_entry_server("data_entry_module", global_sample_names)
    status_monitor_server("status_monitor_module", global_sample_names)
    demux_stats_server("demux_stats_module", global_sample_names)
    align_stats_server("align_stats_module")
    dedup_stats_server("dedup_stats_module")
    tpm_server("tpm_module", global_sample_names)
    