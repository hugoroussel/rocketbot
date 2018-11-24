FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir neat-python requests graphviz numpy matplotlib

COPY test test

CMD [ "python", "./test/evolve-feedforward.py" ]
