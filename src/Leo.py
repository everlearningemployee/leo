import korbit as API
from jsonpath_ng import jsonpath, parse
import time

currency_pair = 'xrp_krw'
env = API.constants()['exchange'][currency_pair]
env.update({'currency_pair': currency_pair})

# while True:
for i in range(1):
    myOrdrId = {o['id'] for o in myOrdr}  # <주문진행건> id 집합

    filledOrdr = API.transactions(**env)
    filledOrdrId = {o['id'] for o in filledOrdr}  # [체결된 주문내역] id 집합

    # <주문진행건> 중 [체결된 주문내역]이 없다면
    if not (myOrdrId & filledOrdrId):
        time.sleep(1)
        continue

    # <주문진행건> 중 [체결된 주문내역]이 있다면 (부분 체결 포함)

    openOrdr = API.open(**env)
    openOrdrId = {o['id'] for o in openOrdr}  # [미체결 주문내역] id 집합

    # <주문진행건> 중 [미 체결 주문내역] [주문 취소] (부분 체결 포함)
    toCancelId = myOrdrId & openOrdrId
    API.cancel(id=toCancelId, **env)

    # <주문진행건>에서 모든 내역 삭제
    myOrdr = []

    # [체결된 주문내역] 중 <주문진행건>의 매도 최대가 / 매수 최저가
    sellMax, buyMin = 0, int(env[coin]['max_price'])
    for id in myOrdrId & filledOrdrId:
        trns_type = filledOrdr[id]['type']
        price = int(filledOrdr[id]['fillsDetail']['price'])
        if trns_type == 'sell':
            sellMax = max(price, sellMax)
        elif trns_type == 'buy':
            buyMin = min(price, buyMin)

    balance = API.balances()
    # 보유현금
    cashValue = int(balance['krw']['available']) + \
        int(balance['krw']['trade_in_use'])

    detailed = API.detailed(**env)
    env.update({
        'bidMax': int(detailed['bid']),  # 최고 매수호가
        'askMin': int(detailed['ask'])  # 최저 매도호가
    })
