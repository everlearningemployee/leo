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
    logging.info(f'calcBuyOrder: b={b}, t={t}, pf={pf}, ai={ai}, vc={vc}, am={am}, ts={ts}')

    po = pf * (1 - t)
    ao = (b * vc - po * ai) / (po * (1 + b))
    logging.info(f'po={po}, ao={ao}')

    # 최소주문량보다 작을 경우
    if ao < am:
        logging.info(f'ao(={ao}) < am(={am}): 다시계산!')
        ao = am
        po = (b * vc) / (ai + am * (1 + b))  # 이게 맞지만 거래가 잘 발생 안함. 지겨우면 주석으로 막을 것
        logging.info(f'po={po}, ao={ao}')

    # 호가단위로 보정
    po = math.floor(po / ts) * ts

    # 최소주문가보다 작은 가격일 경우
    if po < int(min_price) or ao < int(order_min_size):
        logging.info(f'안사: 주문량:{ao}, 최소주문량:{order_min_size}, 주문가:{po}, 최소주문가:{min_price}')
        po, ao = 0, 0

    return {"price": float(po), "amount": float(ao)}


def calcSellOrder(distributionRate,  # propensity
                  triggeringFluctuations,  # propensity
                  filledPrice,
                  coinAmount,
                  cashValue,
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
    logging.info(f'calcSellOrder: b={b}, t={t}, pf={pf}, ai={ai}, vc={vc}, am={am}, ts={ts}')

    po = pf * (1 + t)
    ao = (po * ai - b * vc) / (po * (1 + b))
    logging.info(f'po={po}, ao={ao}')

    # 최소주문량보다 작을 경우
    if ao < am:
        logging.info(f'ao(={ao}) < am(={am}): 다시계산!')
        ao = am
        po = (b * vc) / (ai - am * (1 + b))  # 이게 맞지만 거래가 잘 발생 안함. 지겨우면 주석으로 막을 것
        logging.info(f'po={po}, ao={ao}')

    # 호가단위로 보정
    po = math.ceil(po / ts) * ts

    # "최저 매도호가"보다 낮은 가격일 경우
    if po < int(min_price) or ao < int(order_min_size):
        logging.info("안팔아: %s, %s" % (ao, po))
        logging.info(f'안팔아: 주문량:{ao}, 최소주문량:{order_min_size}, 주문가:{po}, 최소주문가:{min_price}')
        po, ao = 0, 0
    return {"price": float(po), "amount": float(ao)}
