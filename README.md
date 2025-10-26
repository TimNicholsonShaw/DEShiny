# DEShiny
## A pipeline for processing and visualization of Lexogen Quantseq Pool data

# basic useage
```
docker run -p 8080:8080 timnicholsonshaw/deshiny:latest
```
- Navigate to localhost:8080 in your browser
- An example sample sheet is available [here](https://github.com/TimNicholsonShaw/DEShiny/blob/main/tests/sample-sheet.csv)
- Other default values will work for a test run with the above sample sheet

## Features
- A page for setting pipeline options with input validation. Sample sheet validation coming soon.
![Pipeline Options](tests/img/data_entry_example.png)

- A dashboard for visualization of pipeline status
![Pipeline Status](tests/img/pipeline_status_example.png)

- Visualization of demultiplexed counts
![Demux Stats](tests/img/demux_stats_example.png)

- Alignment quality metrics
![Align Stats](tests/img/align_stats_example.png)

- Deduplication quality metrics
![Dedup Stats](tests/img/dedup_stats_example.png)

- Table views of gene counts with visualizations coming soon
![Gene Counts](tests/img/gene_counts_example.png)


