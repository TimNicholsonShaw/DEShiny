from shiny import reactive, render, ui
from components.status_monitor import progress_log_buffer, bulk_progress_log_buffer







def server(input, output, session):
    #return_new_progress_lines_local = return_new_progress_log_lines

    

    @render.text
    def text():
        return progress_log_buffer()
    
        global global_bulk_progress_file_position
        buffer = []

        while True:
            try:
                with open(progress_log_loc, 'r') as log:
                    log.seek(global_bulk_progress_file_position)
                    line=log.readline().rstrip()
                    global_bulk_progress_file_position = log.tell()
                    if line:
                        buffer.append(line)
                    else:
                        break
            except:
                return buffer
        return buffer