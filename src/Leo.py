import korbit as API
from calc import *
from dao import *
import time

coin = 'xrp'
currency = 'krw'


def run():
    currency_pair = f'{coin}_{currency}'

    const = API.constants()['exchange'][currency_pair]
    const.update({'currency_pair': currency_pair})

    # 레오가 주문한게 없다면
    if not LeoOrdr:
        # 시장가 (최종 체결 가격) 기반으로 산정하여 매도매수 주문한다
        ticker = API.detailed(**const)  # [시장 현황 상세정보]
        lastPrc = int(ticker['last'])  # 시장가 (최종 체결 가격)
        sureBet(buyPrice=lastPrc,
                sellPrice=lastPrc,
                coinAmount=coinAmount,
                cashValue=cashValue,
                **prpnst, **ticker, **const)

    # while True:
    for i in range(1):
        LeoOrdrId = {o['orderId'] for o in LeoOrdr}  # <주문진행건> id 집합

        filledOrdr = API.transactions(**const)  # [체결된 주문내역] # TODO 40개 이상
        filledOrdrId = {o['fillsDetail']['orderId'] for o in filledOrdr}  # [체결된 주문내역] id 집합

        # <주문진행건> 중 [체결된 주문내역]이 없다면
        if not(LeoOrdrId & filledOrdrId):
            time.sleep(cfg['interval'])
            continue

        # <주문진행건> 중 [체결된 주문내역]이 있다면 (부분 체결 포함)

        # -------------------------------------------------------------------------
        openOrdr = API.open(**const)  # [미 체결 주문내역] # TODO 40개 이상
        openOrdrId = {o['id'] for o in openOrdr}  # [미 체결 주문내역] id 집합
        # <주문진행건> 중 [미 체결 주문내역] [주문 취소] (부분 체결 포함)
        API.cancel(id=(LeoOrdrId & openOrdrId), **const)
        # <주문진행건>에서 모든 내역 삭제
        LeoOrdr, LeoOrdrId = [], []

        # -------------------------------------------------------------------------
        # [체결된 주문내역] 중 <주문진행건>의 매도 최대가 / 매수 최저가
        sellMax, buyMin = 0, int(const[coin]['max_price'])
        for orderId in LeoOrdrId & filledOrdrId:   
            trns_type = filledOrdr[id]['type']  # 이거아님 TODO orderId로 구해야함 JSONPath로 할 것
            price = int(filledOrdr[id]['fillsDetail']['price']) # 이거아님 TODO orderId로 구해야함 JSONPath로 할 것
            if trns_type == 'sell':
                sellPrc = max(price, sellPrc)
            elif trns_type == 'buy':
                buyPrc = min(price, buyPrc)

        # -------------------------------------------------------------------------
        balance = API.balances()  # [잔고 조회]
        cash, coin = balance[currency], balance[coin]
        coinAmount = int(coin['available']) + \
            int(coin['trade_in_use'])  # 코인보유량
        cashValue = int(cash['available']) + int(cash['trade_in_use'])  # 현금보유액

        ticker = API.detailed(**const)  # [시장 현황 상세정보]

        sureBet(buyPrice=buyPrc,
                sellPrice=sellPrc,
                coinAmount=coinAmount,
                cashValue=cashValue,
                **prpnst, **ticker, **const)

        time.sleep(cfg['interval'])
        continue


def sureBet(buyPrice, sellPrice, coinAmount, cashValue, **kwargs):

    buyOrdr = calcBuyOrder(
        filledPrice=buyPrice,
        coinAmount=coinAmount,
        cashValue=cashValue,
        **kwargs)

    buyOrdrRslt = API.buy(
        price=buyOrdr['price'],
        coin_amount=buyOrdr['amount'],
        buy_type='limit',
        **kwargs)

    sellOrdr = calcSellOrder(
        filledPrice=sellPrice,
        coinAmount=coinAmount,
        cashValue=cashValue,
        **kwargs)

     sellOrdrRslt = API.sell(
        price=sellOrdr['price'],
        coin_amount=sellOrdr['amount'],
        sell_type='limit',
        **kwargs)

    return [buyOrdrRslt, sellOrdrRslt]


if __name__ == '__main__':
    run()
