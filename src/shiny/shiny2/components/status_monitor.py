from shiny import reactive, ui, render
from pathlib import Path
import pandas as pd
from components.data_entry import samples

# hard coded resources
emoji_dict = { # emojis used to represent statuses in the progress tables
"not_started":" ",
    "running":"🏃",
    "finished":"✅"
}
sample_steps = ["extract", "trim", "align", "dedup"]
bulk_steps = ["get_data", "demux", "make_index", "feature_counts"]


# hard coded log locations
progress_log_loc = Path("logs/progress.log")
bulk_progress_log_loc =Path("logs/bulk_progress.log")

# monitor last known position of read in progress logs
progress_log_pos = reactive.value(0)
sample_progress_df = reactive.value(
    pd.DataFrame(
        emoji_dict["not_started"],
        index=["bulk_step"],
        columns=bulk_steps
    )
)

bulk_progress_log_pos = reactive.value(0)
bulk_progress_df = reactive.value(
    pd.DataFrame(
        emoji_dict["not_started"],
        index=["bulk_step"],
        columns=bulk_steps
    )
)

# makes progress monitor functions
def make_progress_monitor(reactive_file_loc:Path, reactive_pos:reactive.value):
    @reactive.file_reader(reactive_file_loc)
    def return_new_progress_log_lines(loc=reactive_file_loc, pos=reactive_pos):
        buffer = []
        while True:
            try:
                with open(loc, 'r') as log:
                    log.seek(pos.get())
                    line=log.readline().rstrip()
                    pos.set(log.tell())
                    if line:
                        buffer.append(line)
                    else:
                        break
            except:
                return buffer
        return buffer
    return return_new_progress_log_lines
    

# instantiated progress monitor functions
sample_progress_log_buffer = make_progress_monitor(progress_log_loc, progress_log_pos)
bulk_progress_log_buffer = make_progress_monitor(bulk_progress_log_loc, bulk_progress_log_pos)



################## ui ####################

status_monitor_ui = ui.page_fillable(
    ui.card(
        ui.card_header("Bulk Process Status"),
        ui.output_data_frame("bulk_status_table")
    ),
    ui.card(
        ui.card_header("Sample Progress Status"),
        ui.output_data_frame("sample_progress_table")
    )
)


def status_monitor_server(input, output, session):
    @render.data_frame
    def bulk_status_table():
        df = bulk_progress_df()
        for line in bulk_progress_log_buffer():
            line = line.rstrip().split(",")
            df.loc["bulk_step", line[1]] = emoji_dict[line[2]]

        bulk_progress_df.set(df)

        return render.DataTable(df)