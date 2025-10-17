from shiny import ui, reactive


align_stats_ui = ui.page_fillable(
    ui.card(
        ui.card_header("Alignment Stats")
    ),
    ui.card(
        ui.card_header("Uniquely Mapped Reads Percentage")
    )
)



def align_stats_server(input, output, session):
    pass