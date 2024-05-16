FROM python:3.8.12-buster


WORKDIR /prod

COPY requirements.txt requirements.txt

COPY project_walmart project_walmart
COPY setup.py setup.py
COPY models models
COPY logs logs
RUN pip install --upgrade pip
RUN pip install .
#RUN apt-get update && apt-get install -y libtbb2 libtbb-dev



COPY Makefile Makefile


CMD uvicorn project_walmart.api.fast:app --host 0.0.0.0 --port $PORT
