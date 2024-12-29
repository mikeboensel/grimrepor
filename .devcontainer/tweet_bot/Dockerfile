FROM python:3.9.21-bookworm

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# TODO: Define some code listening or polling the DB to check for Tweets we should be sending
CMD ["sleep", "infinity"]