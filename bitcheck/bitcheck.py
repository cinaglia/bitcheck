import re
import sys
import argparse

from .async import get
from .parsers import ParserMercadoBitcoin, ParserCoinbase, ParserExchange
from .placeholders import default, cycle
from .utils import measure


class Bitcheck(object):

    # Fees
    COINBASE_FEE = 0.01
    MERCADO_BITCOIN_FEE = 0.02
    MERCADO_BITCOIN_BANK_FEE = 2.9
    MERCADO_BITCOIN_ORDER_FEE = 0.003
    IOF = 0.0038

    def __init__(self, args):
        self.args = args

    def run(self):
        """
        Retrieve relevant exchange rates, calculate arbitrage and output
        findings. This method, if otherwise specified, will perform three
        HTTP requests to gather information.

        Once all exchange rates are fetched, it will then crunch some numbers
        to find out how much can be made (or lost) by buying BTC in the US and
        selling it in a different market.
        """
        data = self.perform_async_requests()
        self.output(data)

    @measure
    def perform_async_requests(self):
        """
        Perform all requests asynchronously.
        """
        # Build list of URL and parsers for each exchange
        services = {
            '--mercadobitcoin': {
                'url': 'https://www.mercadobitcoin.com.br/api/ticker/',
                'parser': ParserMercadoBitcoin()
            },
            '--coinbase': {
                'url': 'https://coinbase.com/api/v1/prices/buy',
                'parser': ParserCoinbase()
            },
            '--exchange': {
                'url': 'http://www.cambioreal.com',
                'parser': ParserExchange()
            }
        }

        # Figure out services that were not overriden
        keys = [k for k in services.keys() if not self.args.get(k)]

        # Perform applicable requests in parallel
        r = get([(k, services.get(k)) for k in keys])

        # Add overriden values to dict
        overriden = set(services.keys()) - set(keys)
        r.update({k: float(self.args.get(k)) for k in overriden})

        # Calculate arbitrage based on values obtained
        return self.calculate(r['--coinbase'],
                              r['--mercadobitcoin'],
                              r['--exchange'])

    def calculate(self, coinbase, mercado_bitcoin, exchange):
        """
        Perform all relevant math calculations in order to figure out how much
        money can be made. It will then save its findings in a dictionary that
        will be used when displaying the data.
        """
        # Create data dict with relevant variables
        data = dict({'coinbase': coinbase, 'mercado_bitcoin': mercado_bitcoin,
                     'exchange': exchange})

        # Add investment amount
        data['investment'] = float(self.args.get('--investment'))

        # Calculate amount of bitcoins based on Coinbase price excluding fees.
        data['coinbase_fee'] = data['investment'] * self.COINBASE_FEE
        data['btc'] = (data['investment'] - data['coinbase_fee']) / coinbase
        data['coinbase_total'] = data['investment'] - data['coinbase_fee']

        # Calculate total amount of BRL based on MercadoBitcoin's prices
        # excluding applicable fees.
        data['brl'] = data['btc'] * mercado_bitcoin
        data['brl_excluding_fee'] = (data['brl'] * (1 - self.MERCADO_BITCOIN_FEE)) - \
            self.MERCADO_BITCOIN_BANK_FEE
        data['mercado_bitcoin_fee'] = data['brl'] - data['brl_excluding_fee']

        # Calculate gains
        data['brl_gain'] = data['brl_excluding_fee'] - (data['investment'] * exchange)
        data['percentage'] = (float(data['brl_gain']) / data['brl_excluding_fee']) * 100

        # If full cycle is enabled, calculate how much USD we can buy via bank.
        if self.args.get('--cycle'):
            data['iof_fee'] = data['brl_excluding_fee'] * self.IOF
            data['usd'] = ((data['brl_excluding_fee'] - data['iof_fee']) / exchange) - \
                data['investment']

        return data

    def output(self, data):
        """
        Display findings to the screen. Uses placeholders found in
        ``bitcheck.placeholders``.
        """
        print default.format(**data)

        if self.args.get('--cycle'):
            print cycle.format(**data).lstrip('\n')

        # Print empty line
        print
