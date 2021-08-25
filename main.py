from binance import client

binance_pay = client.Client('aknrinj0btitquuy4zgloglgrd4e3zxu4fbh5tgk25fxlvzw0aezwackn0354whz', 'ygwnnlqjn71loz1cjat049fntynqzjcizjfvstshzg8urvzez9uixmk2w2o3snui')
#return binance_pay.create_order(merchantTradeNo='982538293', tradeType="WEB", totalFee=1, currency="USDT", productType="Subscription", productName="BotBroker")
print(binance_pay.query_order(prepayId=111847015405993984))