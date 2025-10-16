from shiny import ui
from components.data_entry import data_entry_ui

app_ui = ui.page_fluid(
    ui.navset_pill(
        ui.nav_panel("data_entry", "Data Entry", data_entry_ui),
        ui.nav_panel("pipeline_status", "Pipeline Status"),
        ui.nav_panel("demux_stats", "Demux Stats"),
        ui.nav_panel("align_stats", "Align Stats"),
        ui.nav_panel("dedup_stats", "Dedup Stats"),
        ui.nav_panel("tpm", "TPM"),
        id="tab"
    ),
    ui.output_text_verbatim("text")
)
