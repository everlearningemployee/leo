import korbit as API
from decimal import Decimal
# import korbitMoc as API
from calc import *
from dao import *
from utils import *
import time
import logging


def run(coin, currency):
    currency_pair = f'{coin}_{currency}'
    const = API.constants()['exchange'][currency_pair]
    const.update({'currency_pair': currency_pair})

    LeoOrdr = getLeoOrder()
    if not LeoOrdr:
        logging.debug('주문 진행건이 없음')
        coinAmount, cashValue = getBalance(coin=coin, currency=currency)  # 코인보유량, 현금보유액
        ticker = API.detailed(**const)  # [시장 현황 상세정보]
        lastPrc = float(ticker['last'])  # 시장가 (최종 체결 가격)
        logging.debug(f'시장가 (최종 체결 가격) {lastPrc} 기반으로 산정하여 매도매수 주문')
        sureBet(buyPrice=lastPrc,
                sellPrice=lastPrc,
                coinAmount=coinAmount,
                cashValue=cashValue,
                **prpnst, **ticker, **const)
        LeoOrdr = getLeoOrder()

    while True:
        LeoOrdrId = {o['orderId'] for o in LeoOrdr}  # <주문진행건> id 집합

        filledOrdr = API.transactions(**const)  # [체결된 주문내역] # TODO 40개 이상
        logging.debug(f'filledOrdr: {filledOrdr[-3]}')
        filledOrdrId = {o['fillsDetail']['orderId'] for o in filledOrdr}  # [체결된 주문내역] id 집합

        if not(LeoOrdrId & filledOrdrId):
            logging.debug('<주문진행건> 중 [체결된 주문내역]이 없음')
            time.sleep(cfg['interval'])  # API call rate limit을 피한다 https://apidocs.korbit.co.kr/ko/#api-call-rate-limit
            continue

        # <주문진행건> 중 [체결된 주문내역]이 있다면 (부분 체결 포함)

        # -------------------------------------------------------------------------
        openOrdr = API.open(**const)  # [미 체결 주문내역] # TODO 40개 이상
        openOrdrId = {o['id'] for o in openOrdr}  # [미 체결 주문내역] id 집합
        logging.debug(f'<주문진행건> 중 [미 체결 주문내역] {(LeoOrdrId & openOrdrId)} [주문 취소] (부분 체결 포함)')
        API.cancel(id=(LeoOrdrId & openOrdrId), **const)
        # <주문진행건>에서 모든 내역 삭제
        resetLeoOrder()

        # -------------------------------------------------------------------------
        # [체결된 주문내역] 중 <주문진행건>의 매도 최대가 / 매수 최저가
        sellMax, buyMin = 0, float(const[coin]['max_price'])

        for order in filledOrdr:
            orderId = order['fillsDetail']['orderId']
            if orderId in LeoOrdrId:
                trns_type = order['type']
                price = float(order['fillsDetail']['price']['value'])
                if trns_type == 'sell':
                    sellPrc = max(price, sellPrc)
                    sellId = order['fillsDetail']['orderId']
                elif trns_type == 'buy':
                    buyPrc = min(price, buyPrc)
                    buyId = order['fillsDetail']['orderId']

        # -------------------------------------------------------------------------
        coinAmount, cashValue = getBalance(coin=coin, currency=currency)  # 코인보유량, 현금보유액
        ticker = API.detailed(**const)  # [시장 현황 상세정보]
        sureBet(buyPrice=buyPrc,
                buyId=buyId,
                sellPrice=sellPrc,
                sellId=sellId,
                coinAmount=coinAmount,
                cashValue=cashValue,
                **prpnst, **ticker, **const)

        time.sleep(cfg['interval'])  # API call rate limit을 피한다 https://apidocs.korbit.co.kr/ko/#api-call-rate-limit


def getBalance(currency, coin):
    balance = API.balances()  # [잔고 조회]
    balance_coin, balance_cash = balance[coin], balance[currency]
    coinAmount = float(balance_coin['available']) + float(balance_coin['trade_in_use'])  # 코인보유량
    cashValue = float(balance_cash['available']) + float(balance_cash['trade_in_use'])  # 현금보유액
    return coinAmount, cashValue


def sureBet(buyPrice, sellPrice, coinAmount, cashValue, buyId=None, sellId=None, **kwargs):
    buyOrdrRslt, sellOrdrRslt = None, None

    buyOrdr = calcBuyOrder(
        filledPrice=buyPrice,
        coinAmount=coinAmount,
        cashValue=cashValue,
        **kwargs)
    if buyOrdr['price'] != 0 and buyOrdr['amount'] != 0:
        buyOrdrRslt = API.buy(
            price=buyOrdr['price'],
            coin_amount=buyOrdr['amount'],
            buy_type='limit',
            **kwargs)
        buyOrdrRslt.update({'type': 'buy'})
        recordOrder([
            'buy', buyId, buyPrice, coinAmount, cashValue,
            buyOrdrRslt['orderId'], buyOrdr['price'], buyOrdr['amount'], ])

    sellOrdr = calcSellOrder(
        filledPrice=sellPrice,
        coinAmount=coinAmount,
        cashValue=cashValue,
        **kwargs)
    if sellOrdr['price'] != 0 and sellOrdr['amount'] != 0:
        sellOrdrRslt = API.sell(
            price=sellOrdr['price'],
            coin_amount=sellOrdr['amount'],
            sell_type='limit',
            **kwargs)
        sellOrdrRslt.update({'type': 'sell'})
        recordOrder([
            'sell', sellId, sellPrice, coinAmount, cashValue,
            sellOrdrRslt['orderId'], sellOrdr['price'], sellOrdr['amount'], ])

    newLeoOrder([buyOrdrRslt, sellOrdrRslt])


if __name__ == '__main__':
    logging.debug('Leo 기동')
    run(coin='xrp', currency='krw')
