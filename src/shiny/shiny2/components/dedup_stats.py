from shiny import ui


dedup_stats_ui = ui.page_fillable(
    ui.card(
        ui.card_header("Deduplication Summary")
    ),
    ui.card(
        ui.card_header("Deduplication Graph")
    )
)


def dedup_stats_server(input, output, session):
    pass