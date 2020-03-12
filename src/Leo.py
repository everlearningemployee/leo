import sys
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

    while True:
        LeoOrdrId = {str(o['orderId']) for o in getLeoOrder()}  # <주문진행건> id 집합
        logging.debug(f'<주문진행건> id 집합 {LeoOrdrId}')

        filledOrdr = API.transactions(**const, limit=10)  # [체결된 주문내역] # TODO 최근 몇개만... 몇개라는거 이거 설정으로 뺄까?
        filledOrdrId = {str(o['fillsDetail']['orderId']) for o in filledOrdr}  # [체결된 주문내역] id 집합
        # logging.debug(f'[체결된 주문내역] id 집합 {filledOrdrId}')

        if not(LeoOrdrId & filledOrdrId):
            logging.debug('<주문진행건> 중 [체결된 주문내역]이 없음')
            time.sleep(cfg['interval'])  # API call rate limit을 피한다 https://apidocs.korbit.co.kr/ko/#api-call-rate-limit
            continue

        # <주문진행건> 중 [체결된 주문내역]이 있다면 (부분 체결 포함)
        logging.info(f'체결 {LeoOrdrId & filledOrdrId}')
        for ordr in filledOrdr:
            if ordr['fillsDetail']['orderId'] in LeoOrdrId:
                transactionsLogging.info(ordr)

        # -------------------------------------------------------------------------
        openOrdrId = LeoOrdrId - filledOrdrId
        logging.info(f'<주문진행건> 중 [체결된 주문내역]을 제외한 {openOrdrId} [주문 취소] (부분 체결 포함)')
        if openOrdrId:
            API.cancel(id=openOrdrId, **const)
        # <주문진행건>에서 모든 내역 삭제
        resetLeoOrder()

        # -------------------------------------------------------------------------
        # [체결된 주문내역] 중 <주문진행건>의 매도 최대가 / 매수 최저가
        sellPrc, buyPrc = 0, sys.maxsize
        sellId, buyId = None, None  # TODO 로깅 위한 함수 파라미터 정리해야겠어
        for order in filledOrdr:
            orderId = order['fillsDetail']['orderId']
            if orderId in LeoOrdrId:
                price = float(order['fillsDetail']['price']['value'])
                if sellPrc < price: # 보다 비싸게 거래한걸 매도가의 기준으로
                    sellPrc = price
                    sellId = orderId
                elif buyPrc > price: # 보다 싸게 거래한걸 매수가의 기준으로
                    buyPrc = price
                    buyId = orderId

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
    # TODO 추이 파악하게 로그를 찍자
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
    logging.info(f'매수 주문: buyOrdr={buyOrdr}')
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
    else:
        logging.info('매수 주문 하지 않음')

    sellOrdr = calcSellOrder(
        filledPrice=sellPrice,
        coinAmount=coinAmount,
        cashValue=cashValue,
        **kwargs)
    logging.info(f'매도 주문: sellOrdr={sellOrdr}')
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
    else:
        logging.info('매도 주문 하지 않음')

    newLeoOrder([buyOrdrRslt, sellOrdrRslt])


if __name__ == '__main__':
    logging.debug('Leo 기동')
    run(coin='xrp', currency='krw')
