from shiny import ui
from components.data_entry import data_entry_ui
from components.status_monitor import status_monitor_ui
from components.demux_stats import demux_stats_ui
from components.align_stats import align_stats_ui
from components.dedup_stats import dedup_stats_ui
from components.tpm import tpm_ui
import os

app_ui = ui.page_navbar(
            ui.nav_panel(
                "Data Entry", 
                data_entry_ui
            ),
            ui.nav_panel(
                "Pipeline Status",
                status_monitor_ui
            ),
            ui.nav_panel(
                "Demux Stats",
                demux_stats_ui
            ),
            ui.nav_panel(
                "Align Stats",
                align_stats_ui
                ),
            ui.nav_panel(
                "Dedup Stats",
                dedup_stats_ui
                ),
            ui.nav_panel(
                "TPM",
                tpm_ui
                ),
            ui.nav_spacer(),
            id="page",
            title="TEST "*10 if os.environ.get("TEST", False) else "DE Shiny"

)
