
from typing import Dict
import hashlib
import hmac
import requests
import time
import uuid
import json
from .exceptions import BinanceAPIException, BinanceRequestException

class Client:
    API_URL = 'https://bpay.binanceapi.com/binancepay/openapi'

    def __init__(self, api_key: str, api_secret: str):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.session()
        return session
    
    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not (200 <= response.status_code < 300):
            raise BinanceAPIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException('Invalid Response: %s' % response.text)

    def _request_api(self, method, path: str, **kwargs):
        uri = self._create_api_uri(path)
        return self._request(method, uri, **kwargs)

    def _create_api_uri(self, path: str) -> str:
        url = self.API_URL
        return url + '/' + path

    def _request(self, method, uri: str, **kwargs):
        data = json.dumps(kwargs['data'])

        # Create the request header
        headers = {
            'Content-Type': 'application/json',
            'BinancePay-Certificate-SN': self.API_KEY,
            'BinancePay-Timestamp': str(int(time.time() * 1000)),
            'BinancePay-Nonce': str(uuid.uuid4().hex),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',  # noqa
        }

        # Make the signer for the request header
        payload = headers['BinancePay-Timestamp'] + "\n" + headers['BinancePay-Nonce'] + "\n" + data + "\n"
        sign = hmac.new(self.API_SECRET.encode('utf-8'), payload.encode('utf-8'), hashlib.sha512).hexdigest().upper()
        headers['BinancePay-Signature'] = sign

        # Update the session header and make the request in the Binance API
        self.session.headers.update(headers)
        self.response = getattr(self.session, method)(uri, data=data)
        return self._handle_response(self.response)

    def _post(self, path, **kwargs) -> Dict:
        return self._request_api('post', path, **kwargs)

    def create_order(self, **params):
        """Create order API used for merchant/partner to initiate acquiring order.

        https://developers.binance.com/docs/binance-pay/api-order-create

        :param merchantId:
        :type merchantId: int
        :param subMerchantId:
        :type subMerchantId: int
        :param merchantTradeNo: required
        :type merchantTradeNo: str
        :param tradeType: required
        :type tradeType: str
        :param totalFee: required
        :type totalFee: float
        :param currency: required
        :type currency: str
        :param productType: required
        :type productType: str
        :param productName: required
        :type productName: str
        :param returnUrl:
        :type returnUrl: str

        :returns: API response

        :code-block:: python
            {
                "merchantId": "98765987",
                "subMerchantId": "98765987",
                "merchantTradeNo": "9825382937292",
                "totalFee": 25.17,
                "productDetail": "Greentea ice cream cone",
                "currency": "EUR",
                "returnUrl": "",
                "tradeType": "APP",
                "productType": "Food",
                "productName": "Ice Cream"
            }
        """

        return self._post('order', data=params)

    def query_order(self, **params):
        """Query order API used for merchant/partner to query order status

        https://developers.binance.com/docs/binance-pay/api-order-query

        :param merchantId:
        :type merchantId: int
        :param subMerchantId:
        :type subMerchantId: int
        :param merchantTradeNo: required
        :type merchantTradeNo: str
        :param prepayId: required
        :type prepayId: str

        :returns: API response

        :code-block:: python
            {
                "merchantId": 987321472,
                "subMerchantId": 987321472,
                "merchantTradeNo": "9825382937292",
                "prepayId": None
            }
        """

        return self._post('order/query', data=params)

    def close_order(self, **params):
        """Close order API used for merchant/partner to close order without any prior payment activities triggered by user.
           The successful close result will be notified asynchronously through Order Notification Webhook with bizStatus = "PAY_CLOSED"

        https://developers.binance.com/docs/binance-pay/api-order-create

        :param merchantId:
        :type merchantId: int
        :param subMerchantId:
        :type subMerchantId: int
        :param merchantTradeNo: required
        :type merchantTradeNo: str
        :param prepayId: required
        :type prepayId: str

        :returns: API response

        :code-block:: python
            {
                "merchantId": 987321472,
                "subMerchantId": 987321472,
                "merchantTradeNo": "9825382937292",
                "prepayId": None
            }
        """

        return self._post('order/close', data=params)

    def transfer_fund(self, **params):
        """Fund transfer API used for merchant/partner to initiate Fund transfer between wallets.

        https://developers.binance.com/docs/binance-pay/api-wallet-transfer

        :param requestId: required
        :type requestId: str
        :param merchantId: required
        :type merchantId: int
        :param currency: required
        :type currency: str
        :param amount: required
        :type amount: str
        :param transferType: required
        :type transferType: str

        :returns: API response

        :code-block:: python
            {
                "requestId": "100002021071407140001",
                "merchantId": "98765987",
                "currency": "BNB",
                "amount": "0.01",
                "transferType": "TO_MAIN"
            }
        """

        return self._post('wallet/transfer', data=params)

    def query_transfer_fund(self, **params):
        """Query Transfer Result API used for merchant/partner to query transfer result.

        https://developers.binance.com/docs/binance-pay/api-wallet-transfer-query

        :param requestId: required
        :type requestId: str
        :param merchantId: required
        :type merchantId: int
        :param currency: required
        :type currency: str
        :param amount: required
        :type amount: str
        :param transferType: required
        :type transferType: str
        :param tranId: required
        :type tranId: str

        :returns: API response

        :code-block:: python
            {
                "requestId": "100002021071407140001",
                "merchantId": "98765987",
                "currency": "BNB",
                "amount": "0.01",
                "transferType": "TO_MAIN",
                "tranId": "4069044573"
            }
        """

        return self._post('wallet/transfer/query', data=params)

    def create_submerchant(self, **params):
        """Create Sub-merchant API used for merchant/partner.

        https://developers.binance.com/docs/binance-pay/api-submerchant-add

        :param mainMerchantId: required
        :type mainMerchantId: str
        :param merchantName: required
        :type merchantName: str
        :param merchantType: required
        :type merchantType: int
        :param merchantMcc: required
        :type merchantMcc: str
        :param brandLogo: 
        :type brandLogo: str
        :param country: required
        :type country: str
        :param address: 
        :type address: str
        :param companyName: 
        :type companyName: str
        :param registrationNumber:
        :type registrationNumber: str
        :param registrationCountry:
        :type registrationCountry: str
        :param registrationAddress: 
        :type registrationAddress: str
        :param incorporationDate: 
        :type incorporationDate: int
        :param storeType: 
        :type storeType: int
        :param siteType: 
        :type siteType: int
        :param siteUrl: 
        :type siteUrl: str
        :param siteName:
        :type siteName: str
        :param certificateType:
        :type certificateType: int
        :param certificateCountry: 
        :type certificateCountry: str
        :param certificateNumber: 
        :type certificateNumber: str
        :param certificateValidDate: 
        :type certificateValidDate: int
        :param contractTimeIsv: 
        :type contractTimeIsv: int

        :returns: API response

        :code-block:: python
            {
                "mainMerchantId":350945884,
                "merchantName":"Individual",
                "merchantType":1,
                "merchantMcc":"5511",
                "brandLogo":null,
                "country":"CN,US",
                "address":null,
                "companyName":null,
                "registrationNumber":null,
                "registrationCountry":null,
                "registrationAddress":null,
                "incorporationDate":null,
                "storeType":null,
                "siteType":null,
                "siteUrl":null,
                "siteName":null,
                "certificateType":1,
                "certificateCountry":"US",
                "certificateNumber":"123456X",
                "certificateValidDate":1752422400000,
                "contractTimeIsv":1594656000000
            }
        """

        return self._post('submerchant/add', data=params)
    
    def refund_order(self, **params):
        """Refund order API used for Marchant/Partner to refund for a successful payment.

        https://developers.binance.com/docs/binance-pay/api-order-refund

        :param refundRequestId: required
        :type refundRequestId: str
        :param prepayId: required
        :type prepayId: int
        :param refundAmount: required
        :type refundAmount: float
        :param refundReason: 
        :type refundReason: str

        :returns: API response

        :code-block:: python
            {
                "refundRequestId": "68711039982968832",
                "prepayId": "383729303729303",
                "refundAmount": 25.17,
                "refundReason": ""
            }
        """

        return self._post('order/refund', data=params)

    def query_refund_order(self, **params):
        """Refund order API used for Marchant/Partner to refund for a successful payment.

        https://developers.binance.com/docs/binance-pay/api-order-refund

        :param refundRequestId: required
        :type refundRequestId: str

        :returns: API response

        :code-block:: python
            {
                "refundRequestId": "68711039982968832"
            }
        """

        return self._post('order/refund/query', data=params)