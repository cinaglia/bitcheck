default = """
    Bitcheck
    ==================
    Investment:  ${investment:.0f}
    USD/BRL:    R${exchange:.2f}
    ------------------
         Coinbase
    ------------------
    USD/BTC:  ${coinbase:.2f}
    Fee:      ${coinbase_fee:.2f}
    Total:    ${coinbase_total:.2f}
    Bitcoin:  {btc:.6f}
    ------------------
      MercadoBitcoin
    ------------------
    BTC/BRL:  R${mercado_bitcoin:.2f}
    Fee:      R${mercado_bitcoin_fee:.2f}
    BRL:      R${brl_excluding_fee:.2f}
    ------------------
      Exchange Gains
    ------------------
    BRL:      R${brl_gain:.2f}
    Total:    %{percentage:.2f}
    ------------------"""

cycle = """
        BRL to USD
    ------------------
    IOF:     R${iof_fee:.4f}
    USD:      ${usd:.2f}
    ------------------
"""