FROM python:3.10-slim-bookworm
LABEL Name=openbbscreener Version=0.0.1

WORKDIR /app
RUN pip install openbb[all]

WORKDIR /app/widgets/table
COPY main.py /app/widgets/table/
COPY widgets.json /app/widgets/table/

