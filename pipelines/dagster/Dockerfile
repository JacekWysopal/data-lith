FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt /tmp/requirements-dagster.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dagster.txt
RUN mkdir -p /dagster_home
RUN printf "telemetry:\n  enabled: false\n" > /dagster_home/dagster.yaml

ENV DAGSTER_HOME=/dagster_home

CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "/workspace/pipelines/dagster/definitions.py"]
