import requests

class Rocket(object):
    @staticmethod
    def get(callback):
        r = requests.get('http://lauzhack.sqpub.ch/prices', stream=True)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                callback(decoded_line)
