FROM python:3.10.6-slim


WORKDIR /prod

COPY requirements.txt requirements.txt

COPY project_walmart project_walmart
COPY setup.py setup.py
COPY models models
RUN pip install --upgrade pip
RUN pip install .


COPY Makefile Makefile


CMD uvicorn project_walmart.api.fast:app --host 0.0.0.0 --port $PORT
