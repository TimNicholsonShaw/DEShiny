# syntax=docker/dockerfile:1

FROM mambaorg/micromamba:2.3.3

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

WORKDIR /app

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

COPY . .



CMD ["/usr/local/bin/_entrypoint.sh", "&&",  "python", "src/scripts/entry_point.py", "&", "tail", "-f", "/dev/null"]