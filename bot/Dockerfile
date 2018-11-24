FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir neat-python requests graphviz numpy matplotlib

COPY . .

CMD [ "python", "./bot.py"]
