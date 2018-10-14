FROM python:3.6-stretch

COPY . /app
WORKDIR /app
RUN pip install -e .

ENTRYPOINT ["TBD"]
