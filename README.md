# Bitcheck

Calculate potential profitability by simulating [Bitcoin](http://www.bitcoin.org) transactions such as `USD` → `BTC` → `BRL` → `USD`. The script currently uses [Coinbase](https://www.coinbase.com)'s JSON API to fetch ```USD/BTC``` and [MercadoBitcoin](https://www.mercadobitcoin.com)'s to fetch ```BTC/BRL```.

Total gains are calculated by making the assumption that bitcoin will be bought and sold whithin the shortest time frame possible.


##### Usage
```
python bitcheck.py [--investment=I]
            [--coinbase=C]
            [--mercadobitcoin=M]
            [--exchange=E]
            [--verbose]
            [--cycle]
python bitcheck.py (-h | --help)
python bitcheck.py (-v | --version)
```

##### Sample output
```
$ python bitcheck.py --verbose
Retrieving exchange // check_mercado_bitcoin ..  took 1.81531 seconds
Retrieving exchange // check_coinbase ..  took 1.266546 seconds
Retrieving exchange // check_exchange ..  took 2.522646 seconds

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

##### Dependencies
---
This script uses the awesome lib `docopt` to handle argument parsing and `requests`
for HTTP requests.

##### Roadmap
---
* Add setuptools support.
* Update app so that it can be easily extended to be used with multiple currencies and exchanges.


##### (Un)license
-------
[Public domain](LICENSE)