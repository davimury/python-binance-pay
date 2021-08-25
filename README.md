# python-binance-pay v0.1
Updated 25th Aug 2021

This is an unofficial Python wrapper for the Binance Pay API V1.0.1. I am in no way affiliated with Binance, use at your own risk.

### Quick Start
```
pip install python-binance-pay
```

```Python
from binance_pay import Client

binance_pay = Client(merchant_api_key, merchant_api_secret)

create_order = binance_pay.create_order(
    merchantTradeNo = "9825382937292",
    totalFee = 25,
    productDetail = "Greentea ice cream cone",
    currency = "USDT",
    tradeType = "WEB",
    productType = "Food",
    productName = "Ice Cream"
)

query_order = binance_pay.query_order(prepayId = "987321472")
```