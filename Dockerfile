FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir neat-python requests graphviz numpy matplotlib

COPY training training

CMD [ "python", "./training/bot-training-v1.py" ]
