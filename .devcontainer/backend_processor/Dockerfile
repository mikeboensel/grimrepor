FROM python:3.12.8-bullseye

COPY requirements.txt /tmp
# Use 3.12 for all the stuff we care about (older versions for attempting remediating builds)
RUN python -m pip install -r /tmp/requirements.txt

# TODO: Define code that runs the backend (currently its scripts expected to be run 1 after another manually)
CMD ["sleep", "infinity"]