"""
Bitcheck (Coinbase / MercadoBitcoin)

Check potential profitability by buying BTC from Coinbase and then selling
it at MercadoBitcoin. Profit is calculated by making the assumption that bitcoin
will be bought and sold whithin the shortest time frame possible.

Usage:
    bitcheck [--investment=I]
             [--coinbase=C]
             [--mercadobitcoin=M]
             [--exchange=E]
             [--verbose]
             [--cycle]
    bitcheck (-h | --help)
    bitcheck (-v | --version)

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

__title__ = 'bitcheck'
__version__ = '1.0'