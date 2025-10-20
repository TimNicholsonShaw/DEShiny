from shiny import ui, module

@module.ui
def tpm_ui():
    return ui.page_sidebar(
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

def tpm_server(input, output, server):
    pass
