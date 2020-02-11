import math, decimal

def getDcml(f):
    return decimal.Decimal(str(f))

def calcPrcAmt(
        balanceRate, 
        orderTrigeringPriceChagePercentPoint, 
        filledPrice, 
        coinAmount, 
        cashValue, 
        env
    ):

    '''
    - ve 평가액
    - vc 현금(예수금잔고)
    - vo 주문금액
    - po 주문가
    - ao 주문량
    - b  목표 밸런싱비율
    - t  주문트리거링가격변동포인트
    - ai 코인보유량
    - pf 최근내주문체결가
    - am 최소주문량
    '''

    b  = getDcml(balanceRate)
    t  = getDcml(orderTrigeringPriceChagePercentPoint)
    pf = getDcml(filledPrice)
    ai = getDcml(coinAmount)
    vc = getDcml(cashValue)
    am = getDcml(env['constans']['order_min_size']) # 최소주문량
    ts = getDcml(env['constans']['tick_size']) # 호가단위


    # 매수
    po = pf * (1 - t)
    ao = (b * vc - po * ai) / (po * (1 + b))
    # 최소주문량보다 작을 경우
    if ao < am: 
        ao = am
        po = b * vc / (ai + am * (1 + b))
    # 호가단위로 보정
    po = math.floor(po / ts) * ts 
    # 최소주문가보다 작을 경우
    if po < env['constans']['min_price']:
        print("안사: %s, %s" % (ao, po))
        po, ao = 0, 0    
    buyOrder = {"price": float(po), "amount": float(ao)}

    # 매도
    po = pf * (1 + t)
    ao = (po * ai - b * vc) / (po * (1 + b))
    # 최소주문량보다 작을 경우
    if ao < am: 
        ao = am
        po = b * vc / (ai - am * (1 + b))
    # 호가단위로 보정
    po = math.ceil(po / ts) * ts  
    # 최소주문가보다 작을 경우
    if po < env['constans']['min_price']:
        print("안팔아: %s, %s" % (ao, po))
        po, ao = 0, 0    
    sellOrder = {"price": float(po), "amount": float(ao)}    

    return {"buyOrder": buyOrder, "sellOrder": sellOrder}

env = {
        "constans": {
            "tick_size":0.100000000000000000,
            "min_price":10.000000000000000000,
            "max_price":100000000,
            "order_min_size":10.000000,
            "order_max_size":1000000.000000
        }
    }

filledPrice = 327.0
coinAmount = 1333.798114
cashValue = 436151.98327799997
balanceRate = 4
orderTrigeringPriceChagePercentPoint = 0.01

c = calcPrcAmt(
        balanceRate = balanceRate, 
        orderTrigeringPriceChagePercentPoint = orderTrigeringPriceChagePercentPoint, 
        filledPrice = filledPrice, 
        coinAmount = coinAmount, 
        cashValue = cashValue, 
        env = env)

print(c)

def calcBalance(coinAmount, cashValue, orderPrice, orderAmount, buyOrSell):
    try:
        vo = orderPrice * orderAmount
        if buyOrSell == "buy":
            coin = coinAmount * orderPrice + vo
            cash = cashValue - vo
        else:
            coin = coinAmount * orderPrice - vo
            cash = cashValue + vo
        print(coin / cash, coin, cash)
    except:
        import traceback
        traceback.print_exc()

calcBalance(
        coinAmount, 
        cashValue, 
        c['buyOrder']['price'], 
        c['buyOrder']['amount'], 
        "buy")


calcBalance(
        coinAmount, 
        cashValue, 
        c['sellOrder']['price'], 
        c['sellOrder']['amount'], 
        "sell")
