FROM python:3.12.8-bullseye

COPY requirements.txt /tmp
RUN python -m pip install -r /tmp/requirements.txt

# TODO: Define some code listening or polling the DB to check for Tweets we should be sending
CMD ["sleep", "infinity"]