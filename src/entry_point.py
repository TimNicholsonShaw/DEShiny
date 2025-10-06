import subprocess
import os


if __name__=="__main__":

    # create empty log files so shiny doesn't complain that they don't exist
    os.makedirs("logs/", exist_ok=True) 
    os.makedirs("res/", exist_ok=True) 
    open("logs/progress.log", "w").close()
    open("logs/bulk_progress.log", "w").close()

    # run shiny app
    subprocess.Popen(
        [
            "conda",
            "run",
            "--no-capture-output",
            "-n",
            "test-env",
            "shiny",
            "run",
            "src/shiny/app.py",
            "--host",
            "0.0.0.0",
            "--port",
            "8080",
            "-r"
        ]
    )