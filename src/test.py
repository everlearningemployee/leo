import json
import requests
import math
import decimal
from calc import *


const = {
    "tick_size": 0.100000000000000000,
    "min_price": 10.000000000000000000,
    "max_price": 100000000,
    "order_min_size": 10.000000,
    "order_max_size": 1000000.000000,
    'currency_pair': 'xrp_krw'
}

ticker = {

}

prpnst = {
    'distributionRate': 1,  # 배분비율
    'triggeringFluctuations': 3  # = 0.03 # 주문 트리거링 가격변동%
}

filledOrdr = [
    {
        "timestamp": 1383707746000,
        "completedAt": 1383797746000,
        "id": "599",
        "type": "sell",
        "fee": {"currency": "krw", "value": "1500"},
        "fillsDetail": {
            "price": {"currency": "krw", "value": "1000000"},
            "amount": {"currency": "btc", "value": "1"},
            "native_amount": {"currency": "krw", "value": "1000000"},
            "orderId": "1002"
        }
    },
    {
        "timestamp": 1383705741000,
        "completedAt": 1383797746200,
        "id": "597",
        "type": "buy",
        "fee": {"currency": "btc", "value": "0.0015"},
        "fillsDetail": {
            "price": {"currency": "krw", "value": "1000000"},
            "amount": {"currency": "btc", "value": "1"},
            "native_amount": {"currency": "krw", "value": "1000000"},
            "orderId": "1002"
        }
    }
]

openOrdr = [
    {
        "timestamp": 1389173297000,
        "id": "58726",
        "type": "ask",
        "price": {"currency": "krw", "value": "800000"},
        "total": {"currency": "btc", "value": "1.00000000"},
        "open": {"currency": "btc", "value": "0.75000000"}
    },
    {
        "timestamp": 1386419377000,
        "id": "37499",
        "type": "bid",
        "price": {"currency": "krw", "value": "700000"},
        "total": {"currency": "btc", "value": "1.50000000"},
        "open": {"currency": "btc", "value": "0.41200000"}
    }
]


def calcBalance(coinAmount, cashValue, price, amount, buyOrSell, **kwargs):
    '''검증용 함수'''
    try:
        vo = orderPrice * orderAmount
        if buyOrSell == "buy":
            coin = coinAmount * orderPrice + vo
            cash = cashValue - vo
        else:
            coin = coinAmount * orderPrice - vo
            cash = cashValue + vo
        print(coin / cash, coin, cash, coin + cash)
    except:
        import traceback
        traceback.print_exc()


def testCalc():
    testData = {
        'filledPrice': 327.0,
        'coinAmount': 1333.798114,
        'cashValue': 436151.98327799997,
        # 'cashValue': 0,
        'balanceRate': 1,
        'orderTrigeringPriceChagePercentPoint': 0.02,
        'env': env
    }

    order = calcBuyOrder(**testData)
    print(order)
    calcBalance(**order, **testData, buyOrSell="buy")

    order = calcSellOrder(**testData)
    print(order)
    calcBalance(**order ** testData, buyOrSell="sell")


def t1():
    id = ["11111", 22222]
    # id = [11111,22222]
    # id = [1111]
    # id = 1111

    r = requests.post('http://www.google.com', data={'id': id})  # OK

    # r = requests.post('http://www.google.com', data=json.dumps('{"id": ["1","2"]}'))
    # r = requests.post('http://www.google.com', params=json.dumps({'id': id}))

    # r = requests.post('http://www.google.com', params={'id': [1,2]}) # OK
    r = requests.post('http://www.google.com', data={'id': {1, 2}})  # OK
    # r = requests.post('http://www.google.com', params={'id': id}) # OK

    print(r.request.url)
    print(r.request.body)

def f1(aa, bb, ff, **kwargs):
    print(f'aa=[{aa}], bb=[{bb}], ff=[{ff}]')

def f2(**g):
    f1(**g)

def t2():
    haha = {
        'aa': 'a1111',
        'dd': 'd1111'
    }
    hoho = {
        'cc': 'c1111',
        'bb': 'b1111'
    }
    hihi = {
        'ee': 'ec1111',
        'ff': 'f1111'
    }
    f2(**haha, **hoho, **hihi)

t2()
