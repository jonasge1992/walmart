FROM tensorflow/tensorflow:2.10.0

WORKDIR /prod

COPY requirements.txt requirements.txt

COPY project_walmart project_walmart
COPY setup.py setup.py
RUN pip install .

COPY Makefile Makefile
RUN make reset_local_files


CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
