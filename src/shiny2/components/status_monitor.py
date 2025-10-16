from shiny import reactive
from pathlib import Path


# hard coded log locations
progress_log_loc = Path("logs/progress.log")
bulk_progress_log_loc =Path("logs/bulk_progress.log")

# monitor last known position of read in progress logs
progress_log_pos = reactive.value(0)
bulk_progress_log_pos = reactive.value(0)

# makes progress monitors
def make_progress_monitor(reactive_file_loc, reactive_pos):
    @reactive.file_reader(reactive_file_loc,)
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
    


progress_log_buffer = make_progress_monitor(progress_log_loc, progress_log_pos)
bulk_progress_log_buffer = make_progress_monitor(bulk_progress_log_loc, bulk_progress_log_pos)



