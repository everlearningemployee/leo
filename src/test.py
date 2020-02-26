import json
import requests
import math
import decimal


def dcml(f):
    return decimal.Decimal(str(f))


def calcBuyOrder(balanceRate,
                 orderTrigeringPriceChagePercentPoint,
                 filledPrice,
                 coinAmount,
                 cashValue,
                 order_min_size,
                 tick_size,
                 min_price,
                 **kwargs):
    b = dcml(balanceRate)  # 밸런싱비율
    t = dcml(orderTrigeringPriceChagePercentPoint)  # 주문트리거링가격변동포인트
    pf = dcml(filledPrice)  # 최근내주문체결가
    ai = dcml(coinAmount)  # 코인보유량
    vc = dcml(cashValue)  # 주문금액
    am = dcml(order_min_size)  # 최소주문량
    ts = dcml(tick_size)  # 호가단위

    po = pf * (1 - t)
    ao = (b * vc - po * ai) / (po * (1 + b))
    # 최소주문량보다 작을 경우
    if ao < am:
        ao = am
        po = b * vc / (ai + am * (1 + b))
    # 호가단위로 보정
    po = math.floor(po / ts) * ts
    # 최소주문가보다 작을 경우
    if po < int(min_price):
        print("안사: %s, %s" % (ao, po))
        po, ao = 0, 0
    return {"price": float(po), "amount": float(ao)}


def calcSellOrder(balanceRate,
                  orderTrigeringPriceChagePercentPoint,
                  filledPrice,
                  coinAmount,
                  cashValue,
                  order_min_size,
                  tick_size,
                  min_price,
                 **kwargs):
    b = dcml(balanceRate)  # 밸런싱비율
    t = dcml(orderTrigeringPriceChagePercentPoint)  # 주문트리거링가격변동포인트
    pf = dcml(filledPrice)  # 최근내주문체결가
    ai = dcml(coinAmount)  # 코인보유량
    vc = dcml(cashValue)  # 주문금액
    am = dcml(order_min_size)  # 최소주문량
    ts = dcml(tick_size)  # 호가단위

    po = pf * (1 + t)
    ao = (po * ai - b * vc) / (po * (1 + b))
    # 최소주문량보다 작을 경우
    if ao < am:
        ao = am
        po = b * vc / (ai - am * (1 + b))
    # 호가단위로 보정
    po = math.ceil(po / ts) * ts
    # 최소주문가보다 작을 경우
    if po < int(min_price):
        print("안팔아: %s, %s" % (ao, po))
        po, ao = 0, 0
    return {"price": float(po), "amount": float(ao)}


env = {
    "tick_size": 0.100000000000000000,
    "min_price": 10.000000000000000000,
    "max_price": 100000000,
    "order_min_size": 10.000000,
    "order_max_size": 1000000.000000
}


def calcBalance(a, buyOrSell):
    coinAmount = a['coinAmount']
    cashValue = a['cashValue']
    orderPrice = a['price']
    orderAmount = a['amount']
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
    calcBalance(dict(**order, **testData), buyOrSell="buy")

    order = calcSellOrder(**testData)
    print(order)
    calcBalance(dict(**order, **testData), buyOrSell="sell")


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


t1()
