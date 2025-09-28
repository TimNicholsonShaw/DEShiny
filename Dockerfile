# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# add wget to image
RUN  apt-get update \
  && apt-get install -y wget \
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

SHELL ["conda", "run","--no-capture-output", "-n", "test-env", "/bin/bash", "-c" ]
# RUN STAR
# RUN samtools --version
# Switch to the non-privileged user to run the application.
# USER appuser

# Copy the source code into the container.
COPY . .

# Run the application.
# CMD ["tail", "-f", "/dev/null"]
CMD  conda run --no-capture-output -n test-env umi_tools --version && tail -f /dev/null
