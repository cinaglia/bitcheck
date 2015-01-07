import requests

class Checker(object):
    def __init__(self, url, parser):
        self.url = url
        self.parser = parser

    def check(self):
        try:
            result = requests.get(self.url)
        except Exception, e:
            raise
        return self.parser.parse(result.text)
