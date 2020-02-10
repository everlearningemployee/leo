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

    b  = balanceRate
    t  = orderTrigeringPriceChagePercentPoint
    pf = filledPrice
    ai = coinAmount
    vc = cashValue
    am = env['constans']['order_min_size']

    # 매수
    po = pf * (1 - t)
    ao = (b * vc - po * ai) / (po * (1 + b))
    if ao < am:
        ao = am
        po = b * vc / (ai + am * (1 + b))
    buyOrder = {"price": po, "amount": ao}    
    if po < env['constans']['min_price']:
        print("안사: %s" % buyOrder)
        buyOrder = {"price": 0, "amount": 0}    

    # 매도
    po = pf * (1 + t)
    ao = (po * ai - b * vc) / (po * (1 + b))
    if ao < am:
        ao = am
        po = b * vc / (ai - am * (1 + b))
    sellOrder = {"price": po, "amount": ao}    
    if po < env['constans']['min_price']:
        print("안팔아: %s" % sellOrder)
        buyOrder = {"price": 0, "amount": 0}    

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
cashValue = 10000

c = calcPrcAmt(
        balanceRate = 4, 
        orderTrigeringPriceChagePercentPoint = 0.03, 
        filledPrice = filledPrice, 
        coinAmount = coinAmount, 
        cashValue = cashValue, 
        env = env)

print(c)

def calcBalance(coinAmount, cashValue, orderPrice, orderAmount, buyOrSell):
    vo = orderPrice * orderAmount
    if buyOrSell == "buy":
        return (coinAmount * orderPrice + vo)  / (cashValue - vo)
    else:
        return (coinAmount * orderPrice - vo)  / (cashValue + vo)

b = calcBalance(
        coinAmount, 
        cashValue, 
        c['buyOrder']['price'], 
        c['buyOrder']['amount'], 
        "buy")
print(b)        

b = calcBalance(
        coinAmount, 
        cashValue, 
        c['sellOrder']['price'], 
        c['sellOrder']['amount'], 
        "sell")
print(b)        
