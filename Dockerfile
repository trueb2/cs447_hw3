FROM python:3.5

RUN apt-get update && \
  pip install --upgrade pip && \
  pip install nltk==3.2.2

CMD '/bin/bash'
