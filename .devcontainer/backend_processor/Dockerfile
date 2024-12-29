FROM python:3.9.21-bookworm

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# TODO: Breakout tweet_bot code from backend
COPY ./scripts /app

CMD ["sleep", "infinity"]