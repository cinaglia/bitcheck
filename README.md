# Bitcheck

Calculate potential profitability by simulating [Bitcoin](http://www.bitcoin.org) transactions such as `USD` → `BTC` → `BRL` → `USD`. The script currently uses [Coinbase](https://www.coinbase.com)'s JSON API to fetch ```USD/BTC``` and [MercadoBitcoin](https://www.mercadobitcoin.com.br)'s to fetch ```BTC/BRL```.

Profit is calculated by making the assumption that bitcoin will be bought and sold whithin the shortest time frame possible.


Installation
-------
To install `bitcheck` follow the steps below. If you do not have `virtualenvwrapper`,
feel free to skip the environment creation step.
```bash
git clone https://github.com/cinaglia/bitcheck.git
cd bitcheck && mkvirtualenv bitcheck
pip install -r requirements.txt
python setup.py install
```

Usage
-------
```
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
```

Sample output
-------
```
$ bitcheck --verbose
Retrieving exchange rates ..  took 1.355609 seconds

    Bitcheck
    ==================
    Investment:  $1000
    USD/BRL:    R$2.70
    ------------------
         Coinbase
    ------------------
    USD/BTC:  $298.40
    Fee:      $10.00
    Total:    $990.00
    Bitcoin:  3.317694
    ------------------
      MercadoBitcoin
    ------------------
    BTC/BRL:  R$879.00
    Fee:      R$61.23
    BRL:      R$2855.03
    ------------------
      Exchange Gains
    ------------------
    BRL:      R$155.03
    Total:    %5.43
    ------------------

```

Dependencies
-------
This script uses the awesome lib `docopt` to handle argument parsing, `requests`
for HTTP requests, as well as `gevent` for asynchronous requests.
Optionally use `virtualenvwrapper` to handle dependencies.

TODO
-------
- [ ] Add support for multiple currencies and exchanges
- [ ] Handle request errors
- [x] Add support for parallel HTTP requests
- [x] Add setuptools support

(Un)license
-------
[Public domain](LICENSE)
