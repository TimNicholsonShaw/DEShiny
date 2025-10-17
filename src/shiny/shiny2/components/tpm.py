from shiny import ui

tpm_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "sample_selectize",
            "Select Sample(s)",
            choices=["A", "B", "C"], # TODO update to samples
            multiple=True
        )
    ),
    ui.card(
        ui.card_header("Gene Counts Summary")
    ),
    ui.card(
        ui.card_header("Gene Counts")
    )
)
