import decimal
import math
import logging
import sys


def dcml(f):
    return decimal.Decimal(str(f))

# TODO 나중에 검산해보게 로그를 찍자 

def calcBuyOrder(distributionRate,  # propensity
                 triggeringFluctuations,  # propensity
                 filledPrice,
                 coinAmount,
                 cashValue,
                 bid,  # ticker
                 order_min_size,  # const
                 tick_size,  # const
                 min_price,  # const
                 **kwargs):
    b = dcml(distributionRate)  # 배분비율
    t = dcml(triggeringFluctuations) / 100  # 주문 트리거링 가격변동%
    pf = dcml(filledPrice)  # 기준가
    ai = dcml(coinAmount)  # 코인보유량
    vc = dcml(cashValue)  # 현금보유액
    am = dcml(order_min_size)  # 최소주문량
    ts = dcml(tick_size)  # 호가단위
    bidMax = dcml(bid)  # 최고 매수호가
    logging.debug(f'calcBuyOrder: b={b}, t={t}, pf={pf}, ai={ai}, vc={vc}, am={am}, ts={ts}, bidMax={bidMax}')

    po = min(pf * (1 - t), bidMax)  # "최고 매수호가"보다 낮은 가격으로 주문해야 수수료가 싸다
    ao = (b * vc - po * ai) / (po * (1 + b))
    logging.debug(f'po={po}, ao={ao}')

    # 최소주문량보다 작을 경우
    if ao < am:
        logging.debug(f'ao(={ao}) < am(={am}): 다시계산!')
        ao = am
        # 이게 맞지만 거래가 발생 안해서 주석 처리함 TODO 나중에 주석 풀을 것
        # po = (b * vc) / (ai + am * (1 + b))
        logging.debug(f'po={po}, ao={ao}')

    # 호가단위로 보정
    po = math.floor(po / ts) * ts

    # 최소주문가보다 작거나 이거 저거 다 해도 "최고 매수호가" 보다 높은 가격일 경우
    if po > bidMax or po < int(min_price) or ao < int(order_min_size):
        logging.debug(f'안사: 주문량:{ao}, 최소주문량:{order_min_size}, 주문가:{po}, 최소주문가:{min_price}, 최고 매수호가:{bidMax}')
        po, ao = 0, 0

    return {"price": float(po), "amount": float(ao)}


def calcSellOrder(distributionRate,  # propensity
                  triggeringFluctuations,  # propensity
                  filledPrice,
                  coinAmount,
                  cashValue,
                  ask,  # ticker
                  order_min_size,  # const
                  tick_size,  # const
                  min_price,  # const
                  **kwargs):
    b = dcml(distributionRate)  # 밸런싱비율
    t = dcml(triggeringFluctuations) / 100  # 주문 트리거링 가격변동%
    pf = dcml(filledPrice)  # 기준가
    ai = dcml(coinAmount)  # 코인보유량
    vc = dcml(cashValue)  # 현금보유액
    am = dcml(order_min_size)  # 최소주문량
    ts = dcml(tick_size)  # 호가단위
    askMin = dcml(ask)  # 최저 매도호가
    logging.debug(f'calcSellOrder: b={b}, t={t}, pf={pf}, ai={ai}, vc={vc}, am={am}, ts={ts}, askMin={askMin}')

    po = max(pf * (1 + t), askMin)  # "최저 매도호가"보다 높은 가격으로 주문해야 수수료가 싸다
    ao = (po * ai - b * vc) / (po * (1 + b))
    logging.debug(f'po={po}, ao={ao}')

    # 최소주문량보다 작을 경우
    if ao < am:
        logging.debug(f'ao(={ao}) < am(={am}): 다시계산!')
        ao = am
        # 이게 맞지만 거래가 발생 안해서 주석 처리함 TODO 나중에 주석 풀을 것
        # po = (b * vc) / (ai - am * (1 + b))
        logging.debug(f'po={po}, ao={ao}')

    # 호가단위로 보정
    po = math.ceil(po / ts) * ts

    # 최소주문가보다 작거나 "최저 매도호가"보다 낮은 가격일 경우
    if po < askMin or po < int(min_price) or ao < int(order_min_size):
        logging.debug("안팔아: %s, %s" % (ao, po))
        logging.debug(f'안팔아: 주문량:{ao}, 최소주문량:{order_min_size}, 주문가:{po}, 최소주문가:{min_price}, 최저 매도호가:{askMin}')
        po, ao = 0, 0
    return {"price": float(po), "amount": float(ao)}

