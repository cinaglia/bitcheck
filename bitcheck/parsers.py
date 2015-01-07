import re
import json

class Parser(object):
    def parse_json(self, data):
        return json.loads(data)

    def parse_regex(self, regex, data):
        c = re.compile(regex)
        return c.findall(data)


class ParserMercadoBitcoin(Parser):
    """Parses a ticker json response from MercadoBitcoin's API."""
    def parse(self, data):
        j = self.parse_json(data)
        return float(j['ticker']['last'])


class ParserCoinbase(Parser):
    """Parses a ticker json response from Coinbase's API."""
    def parse(self, data):
        j = self.parse_json(data)
        return float(j['subtotal']['amount'])

class ParserExchange(Parser):
    """Parses the exchange rate by extracting it from an HTML response."""
    def parse(self, data):
        d = self.parse_regex(r'"usd":"([\d.]*)"', data)
        return float(d[0])
