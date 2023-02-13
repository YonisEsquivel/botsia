import requests
import json
import config
from urllib import parse
import time
import base64
import hashlib
import hmac

class UrlParamsBuilder(object):
    def __init__(self):
        self.param_map = dict()
        self.post_map = dict()
    
    def build_url(self):
        if len(self.param_map) == 0:
            return ""
        encoded_param = parse.urlencode(self.param_map)
        return encoded_param

    def put_url(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.param_map[name] = json.dumps(value)
            elif isinstance(value, float):
                self.param_map[name] = ('%.20f' % (value))[slice(0, 16)].rstrip('0').rstrip('.')
            else:
                self.param_map[name] = str(value)
    
class RestApiRequest(object):
    def __init__(self):
        self.method = ""
        self.url = ""
        self.host = ""
        self.post_body = ""
        self.header = dict()
        self.json_parser = None

class BinanceApiClient():
    def __init__(self, api_key, secret_key, server_url="https://api.binance.com"):
        self._api_key = api_key
        self._secret_key = secret_key
        self._server_url = server_url


    def builderRequest(self, params=None):
        builder = UrlParamsBuilder()
        if params != None:
            for index in params:       
                builder.put_url(index, params[index])
        return builder


    def create_signature(self, secret_key, builder):
        if secret_key is None or secret_key == "":
            raise "Error se requiere secret_key"
        keys = builder.param_map.keys()
        query_string = '&'.join(['%s=%s' % (key, parse.quote(builder.param_map[key], safe='')) for key in keys])
        signature = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
        builder.put_url("signature", signature)
        

    def _create_request(self, method, endpoint, params):
        builder = self.builderRequest(params)
        request = RestApiRequest()
        request.method = method
        request.host = self._server_url
        request.header.update({'Content-Type': 'application/json'})
        request.url = endpoint + "?" + builder.build_url()
        return request

    def _create_request_with_signature(self, method, endpoint, params):
        builder = self.builderRequest(params)
        request = RestApiRequest()
        request.method = method
        request.host = self._server_url
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self._api_key})
        self.create_signature(self._secret_key, builder)

        request.url = endpoint + "?" + builder.build_url()
        return request


    def __create_request_with_apikey(self, url, builder):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self._server_url
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({"X-MBX-APIKEY": self._api_key})
        request.url = url + "?" + builder.build_url()
         # For develop
        print("====== Request ======")
        print(request)
        print("=====================")
        return request
    
    
        
    def _call_sync(self, request):
        resp = {}
        if request.method == "GET":
            response = requests.get(request.host + request.url, headers = request.header)
            resp['data'] =  response.json()
        elif request.method == "POST":
            pass
        elif request.method == "DELETE":
            pass
        elif request.method == "PUT":
            pass

        return resp

    def get_servertime(self) -> any:
        request = self._create_request('GET', '/time', None)
        response = self._call_sync(request)
        return response['data']

    def get_current_timestamp(self):
        return int(round(time.time() * 1000))

    def json_parse(self, json_data):
        data = list()
        for i in range(0,len(json_data)):
            data.append({
                'openTime':json_data[i][0],
                'open':json_data[i][1],
                'high':json_data[i][2],
                'low':json_data[i][3],
                'close':json_data[i][4],
                'volume':json_data[i][5],
                'closeTime':json_data[i][6],
                'quoteAssetVolume':json_data[i][7],
                'numTrades':json_data[i][8],
                'takerBuyBaseAssetVolume':json_data[i][9],
                'takerBuyQuoteAssetVolume':json_data[i][10],
                'ignore':json_data[i][11]
            })
        return data

    def get_price_symbol(self, symbol) -> any:
        request = self._create_request('GET', '/ticker/price', {"symbol":symbol})
        response = self._call_sync(request)
        return response['data']

    def get_book_ticker(self, symbol) -> any:
        request = self._create_request('GET', '/ticker/bookTicker', {"symbol":symbol})
        response = self._call_sync(request)
        return response['data']

    def get_klines_data(self, symbol, interval, limit) -> any:
        request = self._create_request('GET', '/klines', {"symbol":symbol, "interval": interval, "limit": limit})
        response = self._call_sync(request)
        return self.json_parse(response['data'])

    def get_balance(self) -> any:
        timestamp = str(self.get_current_timestamp() - 1000)
        request = self._create_request_with_signature('GET', '/balance', {"recvWindow":6000, "timestamp": timestamp})
        response = self._call_sync(request)
        return response['data']
    
    def get_balance_account(self) -> any:
        timestamp = str(self.get_current_timestamp() - 1000)
        request = self._create_request_with_signature('GET', '/account', {"recvWindow":6000, "timestamp": timestamp})
        response = self._call_sync(request)
        return response['data']['balances']

    def get_open_orders(self, symbol) -> any:
        timestamp = str(self.get_current_timestamp() - 1000)
        request = self._create_request_with_signature('GET', '/openOrders', {"symbol":symbol, "recvWindow":6000, "timestamp": timestamp})
        response = self._call_sync(request)
        return response['data']

    def get_order_book(self, symbol, interval, depth):
        request = self._create_request('GET', '/depth', {"symbol":symbol, "interval": interval, "limit": depth})
        response = self._call_sync(request)
        return response['data']

    def get_position_risk(self, symbol) -> any:
        timestamp = str(self.get_current_timestamp() - 1000)
        request = self._create_request_with_signature('GET', '/positionRisk', {"symbol":symbol, "recvWindow":6000, "timestamp": timestamp})
        response = self._call_sync(request)
        return response['data']

#ab = BinanceApiClient(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

#Obtiene la hora actual der serverr
#resp = ab.get_servertime()

#Obtiene el pecio actual del simbolo
#resp = ab.get_book_ticker('BNBUSDT')

#resp = ab.get_klines_data('BNBUSDT','5m', 1000)

#print(resp)
