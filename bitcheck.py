"""
Bitcheck (Coinbase / MercadoBitcoin)

Check potential profitability by buying BTC from Coinbase and then selling
it at MercadoBitcoin. Profit is calculated by making the assumption that bitcoin
will be bought and sold whithin the shortest time frame possible.

Usage:
    bitcheck.py [--investment=I]
                [--coinbase=C]
                [--mercadobitcoin=M]
                [--exchange=E]
                [--verbose]
                [--cycle]
    bitcheck.py (-h | --help)
    bitcheck.py (-v | --version)

Options:
    -h --help           Show this screen.
    -v --version        Show version.
    --verbose           Print additional data about process.
    --cycle             Calculate full cycle. Transfer BRL back to USD.
    --investment=I      Total USD invested [default: 1000].
    --coinbase=C        Price paid at Coinbase.
    --mercadobitcoin=M  Price sold at MercadoBitcoin.
    --exchange=E        Exchange Rate.

"""

import re
import sys
import argparse
import requests

from docopt import docopt
from datetime import date, timedelta
from bitcheck.parsers import ParserMercadoBitcoin, ParserCoinbase, ParserExchange
from bitcheck.checker import Checker
from bitcheck.placeholders import default, cycle
from bitcheck.utils import measure


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
        # Fetch exchange rates
        mercado_bitcoin = self.check_mercado_bitcoin()
        coinbase = self.check_coinbase()
        exchange = self.check_exchange()
        # Calculate arbitrage based on values obtained
        data = self.calculate(coinbase, mercado_bitcoin, exchange)
        self.output(data)

    @measure
    def check_mercado_bitcoin(self):
        """
        Fetch and parse exchange rate from MercadoBitcoin.
        """
        # Return early if price is provided via args
        if self.args.get('--mercadobitcoin'):
            return float(self.args.get('--mercadobitcoin'))

        # Create a checker instance and retrieve data
        checker = Checker(url='https://www.mercadobitcoin.com.br/api/ticker/',
                          parser=ParserMercadoBitcoin())
        return checker.check()

    @measure
    def check_coinbase(self):
        """
        Fetch and parse exchange rate from Coinbase.
        """
        # Return early if price is provided via args
        if self.args.get('--coinbase'):
            return float(self.args.get('--coinbase'))

        # Create a checker instance and retrieve data
        checker = Checker(url='https://coinbase.com/api/v1/prices/buy',
                          parser=ParserCoinbase())
        return checker.check()

    @measure
    def check_exchange(self):
        """
        Fetch and parse exchange rate from CambioReal.

        Any other reliable source that provides USD/BRL rates could be used here.
        """
        # Return early if price is provided via args
        if self.args.get('--exchange'):
            return float(self.args.get('--exchange'))

        # Create a checker instance and retrieve data
        checker = Checker(url='http://www.cambioreal.com',
                          parser=ParserExchange())
        return checker.check()

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
            print cycle.format(**data)

        # Print empty line
        print


if __name__ == "__main__":
    args = docopt(__doc__, version='Bitcheck 1.0')
    check = Bitcheck(args)
    check.run()
    