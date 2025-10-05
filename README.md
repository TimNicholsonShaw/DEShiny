# DEShiny
## A pipeline for processing and visualization of Lexogen Quantseq Pool data

## Notes:
- The docker image is available from timnicholsonshaw/deshiny
- An example config file can be found in the tests folder
- The config file location (retrieved by wget) should be passed to the container via the CONFIG environment variable
- example: docker run -p 8080:8080 -e CONFIG=[config url] deshiny
- FASTQ, genome fasta, and genome annotation are retrieved via wget from the urls noted in the config file
- Shiny app will run on port 8080

## Features
- A dashboard for visualization of pipeline status
![Pipeline Status](tests/img/pipeline_status_example.png)
