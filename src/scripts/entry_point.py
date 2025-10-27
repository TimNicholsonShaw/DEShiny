import subprocess, os, shutil
from pathlib import Path

test_logs = Path("tests/sample_files/logs/")
test_outputs = Path("tests/sample_files/outputs/")

if __name__=="__main__":

    if os.environ.get("TEST", False):
        shutil.move(test_logs, "./")
        shutil.move(test_outputs, "./")


    elif not os.environ.get("TEST", False):
        
        # create empty log files so shiny doesn't complain that they don't exist
        os.makedirs("logs/", exist_ok=True) 
        os.makedirs("res/", exist_ok=True) 
        os.makedirs("outputs/aligned/", exist_ok=True)
        os.makedirs("outputs/dedup/", exist_ok=True)
        open("logs/progress.log", "w").close()
        open("logs/bulk_progress.log", "w").close()
        open("outputs/aligned/align_summary.csv", "w").close()
        open("outputs/dedup/dedup_summary.csv", "w").close()
        open("outputs/gene_counts.tsv","w").close()
        open("outputs/gene_counts.tsv.summary","w").close()



    # run shiny app
    subprocess.Popen(
        [
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


