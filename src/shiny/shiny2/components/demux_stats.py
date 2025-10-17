from shiny import reactive, ui


demux_stats_ui = ui.page_fillable(
    ui.card(
        ui.card_header("Index Assignments")
    ),
    ui.card(
        ui.card_header("Index Assignment Graph")
    )

)



def demux_stats_server(input, output, session):
    pass