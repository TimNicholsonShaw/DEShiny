# DEShiny
## A pipeline for processing and visualization of Lexogen Quantseq Pool data

## Notes:
- The docker image is available from timnicholsonshaw/deshiny
- Shiny app will run on port 8080
- Example sample sheet is available in the tests folder, default URLs should work for testing

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


