# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# add wget to image
RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y procps \
  && rm -rf /var/lib/apt/lists/*
  

# install conda
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH



# install conda dependencies
RUN --mount=type=cache,target=/root/.cache/conda \
    --mount=type=bind,source=environment.yaml,target=environment.yaml \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda env create -f environment.yaml

# install pip dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    conda run --no-capture-output -n test-env pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# use this command to stop the container from shutting down


EXPOSE 8080

#CMD ["tail", "-f", "/dev/null"]
# CMD touch logs/progress.log \
# && touch logs/bulk_progress.log \
# && wget -O src/snakemakeconfig.yaml $CONFIG \
# && conda run --no-capture-output -n test-env python src/get_sample_sheet.py \
# # && conda run --no-capture-output -n test-env snakemake --snakefile src/Snakefile \
# # --configfile src/snakemakeconfig.yaml --cores 4 --keep-incomplete \
# & sleep 2 \
# && conda run --no-capture-output -n test-env shiny run src/shiny/app.py --host 0.0.0.0 --port 8080 -r

# CMD ["conda", "run," "--no-capture-output", "-n", "test-env", "python", "src/scripts/entry_point.py"]
CMD conda run --no-capture-output -n test-env python src/scripts/entry_point.py & tail -f /dev/null