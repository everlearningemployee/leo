import yaml
import logging
import json
from os import path
from dao import *

# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

errorSymbol = {
    'name_unchecked': '본인인증을 하지 않은 사용자가 주문을 넣음',
    'not_enough_krw': '잔고가 부족하여 매수주문을 넣을 수 없음',
    'not_enough_btc': '잔고가 부족하여 매도주문을 넣을 수 없음',
    'too_many_orders': '사용자 당 최대 주문 건수를 초과함',
    'save_failure': '기타 다른 이유로 주문이 들어가지 않음',
    'not_found': '해당 주문이 존재하지 않음',
    'not_authorized': '다른 사용자의 주문을 취소하려고 함',
    'already_filled': '취소되기 전에 주문 수량 모두 체결됨',
    'already_canceled': '이미 취소된 주문'
}


def token_saver(token):
    # TODO
    pass


korbit = OAuth2Session(
    client=BackendApplicationClient(**iam),
    auto_refresh_kwargs=iam,
    token_updater=token_saver)

token = korbit.fetch_token(**iam, **{
    'token_url': 'https://api.korbit.co.kr/v1/oauth2/access_token',
    'auto_refresh_url': 'https://api.korbit.co.kr/v1/oauth2/access_token'
})


def detailed(currency_pair, **kwargs):
    ''' 시장 현황 상세정보 https://apidocs.korbit.co.kr/ko/#b5b542c8be
    returns the json-encoded content of a response, if any
      - timestamp 최종 체결 시각.
      - last 최종 체결 가격.
      - open 최근 24시간 시작 가격.
      - bid 매수호가. 현재 매수 주문 중 가장 높은 가격.
      - ask 매도호가. 현재 매도 주문 중 가장 낮은 가격.
      - low 최저가. 최근 24시간 동안의 체결 가격 중 가장 낮 가격.
      - high 최고가. 최근 24시간 동안의 체결 가격 중 가장 높은 가격.
      - volume 거래량.
      - change 시작 가격 대비 현재가 차이.
      - changePercent 시작 가격 대비 현재가 차이 변화 비율.    
    :param currency_pair: 요청할 통화쌍 '''
    r = korbit.get(
        url='https://api.korbit.co.kr/v1/ticker/detailed',
        params={'currency_pair': currency_pair})
    if r.ok:
        return r.json()


def orderbook(currency_pair, **kwargs):
    ''' 매수/매도 호가 https://apidocs.korbit.co.kr/ko/#b25e985961
    returns the json-encoded content of a response, if any
      - timestamp 가장 마지막으로 유입된 호가의 주문 유입시각.
      - asks [가격, 미체결잔량]으로 구성된 개별 호가를 나열한다. 3번째 값은 더이상 지원하지 않고 항상 "1"로 세팅된다.
      - bids [가격, 미체결잔량]으로 구성된 개별 호가를 나열한다. 3번째 값은 더이상 지원하지 않고 항상 "1"로 세팅된다.    
    :param currency_pair: 요청할 통화쌍 '''
    r = korbit.get(
        url='https://api.korbit.co.kr/v1/orderbook',
        params={'currency_pair': currency_pair})
    if r.ok:
        return r.json()


def constants():
    ''' 제약조건 https://apidocs.korbit.co.kr/ko/#6c6b9f83e3
    returns the json-encoded content of a response, if any
      - exchange 거래 제약조건
        - currency_pair 해당 거래의 통화쌍 (btc_krw, eth_krw, ...)
          - tick_size 호가단위
          - min_price 최소 주문가
          - max_price 최대 주문가
          - order_min_size 매수/매도 수량 최소 입력값
          - order_max_size 매수/매도 수량 최대 입력값
     '''
    r = korbit.get(
        url='https://api.korbit.co.kr/v1/constants')
    if r.ok:
        return r.json()


def balances():
    '''잔고 조회 https://apidocs.korbit.co.kr/ko/#ac7d6b6a6f
    returns the json-encoded content of a response, if any
      - available 현재 거래 가능한 화폐의 수량.
      - trade_in_use 현재 거래중인 화폐의 수량.
      - withdrawal_in_use 현재 출금이 진행중인 화폐의 수량.
      - avg_price 코인의 경우 평균 매수 단가
      - avg_price_updated_at 평균 매수 단가가 계산된 시각    
    '''
    r = korbit.get(
        url='https://api.korbit.co.kr/v1/user/balances')
    if r.ok:
        return r.json()


def volume(currency_pair, **kwargs):
    '''거래량과 거래 수수료 정책 https://apidocs.korbit.co.kr/ko/#d491fe1497
    returns the json-encoded content of a response, if any
      - currency_pair 해당 통화쌍.
      - volume 해당 통화쌍의 30일간의 거래량(KRW).
      - maker_fee 베이시스 포인트(BPS - 1/100 퍼센트 기준)로 표기된 maker 거래 수수료율.
      - taker_fee 베이시스 포인트(BPS - 1/100 퍼센트 기준)로 표기된 taker 거래 수수료율.
      - total_volume 모든 통화쌍 거래의 거래량 총합(KRW).
      - timestamp 최종 거래량 및 거래 수수료 산정 시각(매시간에 한번씩 갱신).    
    :param currency_pair: 요청할 통화쌍 '''
    res = korbit.get(
        url='https://api.korbit.co.kr/v1/user/volume',
        params={'currency_pair': currency_pair})
    if res.ok:
        return res.json()


def buy(currency_pair, buy_type, price=None, coin_amount=None, fiat_amount=None, **kwargs):
    '''매수 주문 https://apidocs.korbit.co.kr/ko/#bf0145bc5d
    returns the json-encoded content of a response, if any
      - orderId 접수된 주문 ID
      - status 성공이면 "success", 실패할 경우 에러 심볼이 세팅된다.
      - currency_pair 해당 주문에 사용된 거래 통화    
    에러 심볼
      - name_unchecked 본인인증을 하지 않은 사용자가 주문을 넣은 경우.
      - not_enough_krw 잔고가 부족하여 매수주문을 넣을 수 없는 경우.
      - too_many_orders 사용자 당 최대 주문 건수를 초과한 경우.
      - save_failure 기타 다른 이유로 주문이 들어가지 않은 경우. 일반적으로 발생하지 않음.    
    :param currency_pair: 요청할 통화쌍. [제약조건]에 존재하는 통화쌍은 모두 사용할수 있으며, 이 외에 다른 통화쌍은 지원하지 않는다.
    :param buy_type: 주문 형태. "limit" : 지정가 주문, "market" : 시장가 주문.
    :param price: 가격. 지정가 주문(type=limit)인 경우에만 유효하다. [제약조건]을 참조하여 가격을 설정해야 한다.
    :param coin_amount: 매수하고자 하는 코인의 수량. 시장가 주문(type=market)일 경우 coin_amount와 fiat_amount중 하나만 설정해야 하며(둘 다 설정할 경우 HTTP Status Code 400 반환), coin_amount를 설정하는 경우 지정한 수량만큼 시장가로 매수한다.
    :param fiat_amount: 코인을 구매하는데 사용하고자 하는 금액을 지정. 원화 Market 일 경우 원화, 다른 통화 Market일 경우 해당 Market의 통화로 금액을 지정한다. 예를들어, currency_pair가 'eth_krw;인 경우 100만원 만큼의 ETH 를 구매하고 싶다면 fiat_amount에 1000000을 지정한다. 시장가 주문(type=market)일 때만 유효한 파라미터이며, coin_amount와 같이 사용할 수 없다.(둘 다 설정할 경우 HTTP Status Code 400 반환) '''
    res = korbit.post(
        url='https://api.korbit.co.kr/v1/user/orders/buy',
        data={'currency_pair': currency_pair,
              'type': buy_type,
              'price': price,
              'coin_amount': coin_amount,
              'fiat_amount': fiat_amount})
    if res.ok:
        resJson = res.json()
        status = resJson['status']
        if status == 'success':
            return resJson
        else:
            raise Exception(errorSymbol[status])
    raise Exception(f'{res.status_code} Error')


def sell(currency_pair, sell_type, price=None, coin_amount=None, **kwargs):
    '''매도 주문 https://apidocs.korbit.co.kr/ko/#95fdcac640
    returns the json-encoded content of a response, if any
      - orderId 접수된 주문 ID
      - status 성공이면 "success", 실패할 경우 에러 심볼이 세팅된다.
      - currency_pair 해당 주문에 사용된 거래 통화    
    에러 심볼
      - name_unchecked 본인인증을 하지 않은 사용자가 주문을 넣은 경우.
      - not_enough_btc 잔고가 부족하여 매도주문을 넣을 수 없는 경우.
      - too_many_orders 사용자 당 최대 주문 건수를 초과한 경우.
      - save_failure 기타 다른 이유로 주문이 들어가지 않은 경우. 일반적으로 발생하지 않음.      
    :param currency_pair: 요청할 통화쌍. [제약조건]에 존재하는 통화쌍은 모두 사용할수 있으며, 이 외에 다른 통화쌍은 지원하지 않는다.
    :param sell_type: 주문 형태. "limit" : 지정가 주문, "market" : 시장가 주문.
    :param price: 주문 가격. 지정가 주문(type=limit)인 경우에만 유효하다. [제약조건]을 참조하여 가격을 설정해야 한다.
    :param coin_amount: 매도하고자 하는 코인의 수량 '''
    res = korbit.post(
        url='https://api.korbit.co.kr/v1/user/orders/sell',
        data={'currency_pair': currency_pair,
              'type': sell_type,
              'price': price,
              'coin_amount': coin_amount})
    if res.ok:
        resJson = res.json()
        status = resJson['status']
        if status == 'success':
            return resJson
        else:
            raise Exception(errorSymbol[status])
    raise Exception(f'{res.status_code} Error')


def cancel(currency_pair, id, **kwargs):
    '''주문 취소 https://apidocs.korbit.co.kr/ko/#9019a1d4df
    returns the json-encoded content of a response, if any
      - orderId id 파라미터로 넘긴 주문 일련번호.
      - status 성공이면 "success", 실패할 경우 에러 심볼이 세팅된다.    
    에러 심볼
      - not_found 해당 주문이 존재하지 않는 경우. 잘못된 주문 일련번호를 지정하면 이 에러가 발생한다.
      - not_authorized 다른 사용자의 주문을 취소하려고 한 경우.
      - already_filled 취소되기 전에 주문 수량 모두 체결된 경우.
      - already_canceled 이미 취소된 주문인 경우.     
    :param currency_pair: 요청할 통화쌍. [제약조건]에 존재하는 통화쌍은 모두 사용할수 있으며, 이 외에 다른 통화쌍은 지원하지 않는다.
    :param id: 취소할 주문의 ID. string 또는 list. list의 경우는 여러 건의 주문을 한 번에 취소. v1/user/orders/open의 응답에 들어있는 id 필드의 값이나, v1/user/orders/buy 혹은 v1/user/orders/sell의 결과로 받은 orderId를 사용할 수 있다.   '''
    if not id:
        return
    res = korbit.post(
        url='https://api.korbit.co.kr/v1/user/orders/cancel',
        data={'currency_pair': currency_pair,
              'id': id}
    )
    if res.ok:
        resJson = res.json()
        status = resJson['status']
        if status == 'success':
            return resJson
        else:
            raise Exception(errorSymbol[status])
    raise Exception(f'{res.status_code} Error')


def open(currency_pair, offset=0, limit=40, **kwargs):
    '''미 체결 주문내역 https://apidocs.korbit.co.kr/ko/#19c18e900d
    returns the json-encoded content of a response, if any
      - timestamp 주문 시각
      - id 주문 일련번호
      - type 매수/매도 구분. "bid"는 매수주문, "ask"은 매도주문
      - price 가격
        - currency 거래에 사용한 통화
        - value 주문 가격
      - total 주문 수량
        - currency 거래에 사용한 통화
        - value 주문한 수량
      - open 주문 수량 중 아직 체결되지 않은 수량. 
        - currency 거래에 사용한 통화
        - value 아직 체결되지 않은 수량
    :param currency_pair: 요청할 통화쌍
    :param offset: 전체 데이터 중 offset(0부터 시작) 번 째 데이터부터 가져옴
    :param limit: 전체 데이터 중 limit개를 가져옴. 최대값은 40   '''
    res = korbit.get(
        url='https://api.korbit.co.kr/v1/user/orders/open',
        params={'currency_pair': currency_pair,
                'offset': offset,
                'limit': limit})
    if res.ok:
        return res.json()


def orders(currency_pair, status, id, offset=0, limit=40, **kwargs):
    '''거래소 주문 조회 https://apidocs.korbit.co.kr/ko/#1cfc61cd9b
    returns the json-encoded content of a response, if any
      - id 주문의 ID 식별번호.
      - currency_pair 해당 통화쌍.
      - side 매수/매도 구분. 매수 주문일 시에는 'bid', 매도 주문일 시에는 'ask'.
      - avg_price 체결 가격의 가중 평균치.
      - price 주문 시에 설정한 지정가. 시장가 주문일 경우에는 기본값인 0으로 나온다.
      - order_amount 주문 시에 지정한 코인의 수량. 시장가 주문의 경우, 체결된 수량이 나온다.
      - filled_amount 현재까지 체결된 코인의 수량. filledAmount와 orderAmount가 같을 때 주문이 체결 완료된다.
      - order_total 주문 금액. 시장가 매도 주문의 경우 이 필드는 표시되지 않는다.
      - filled_total 체결 금액.
      - created_at 거래를 주문한 시각. Unix timestamp(milliseconds)로 제공된다.
      - last_filled_at 거래가 부분 체결된 최종 시각. Unix timestamp(milliseconds)로 제공된다. 부분적으로도 전혀 체결되지 않은 주문(unfilled)에서는 이 필드는 표시되지 않는다.
      - status 현재 주문의 상태. 상태에 따라 'unfilled', 'partially_filled', 'filled' 값으로 나오게 된다.
      - fee 거래 수수료. 매수 주문일 시에는 해당 매수 코인으로 수수료가 적용되며, 매도 주문일 시에는 원화(KRW)로 수수료가 적용된다. 부분적으로도 전혀 체결되지 않은 주문(unfilled)에서는 이 필드는 표시되지 않는다.    
    :param currency_pair: 요청할 통화쌍
    :param status: 'unfilled', 'partially_filled', 'filled' 값 중의 하나, 또는 조합(list)
    :param id: 조회할 주문의 ID. string 또는 list. list의 경우는 여러 건의 주문을 한 번에 조회
    :param offset: 전체 데이터 중 offset(0부터 시작) 번 째 데이터부터 가져옴
    :param limit: 전체 데이터 중 limit개를 가져옴. 최대값은 40    '''
    res = korbit.get(
        url='https://api.korbit.co.kr/v1/user/orders',
        params={'currency_pair': currency_pair,
                'status': status,
                'id': id,
                'offset': offset,
                'limit': limit})
    if res.ok:
        return res.json()


def transactions(currency_pair, offset=0, limit=40, **kwargs):
    '''체결된 주문내역 https://apidocs.korbit.co.kr/ko/#3dc3ae9243
      - timestamp 체결, 입출금이 발생한 시각
      - completedAt 완료 시각. 체결의 경우 항상 세팅되며, KRW입출금, BTC입출금의 경우 아직 완료되지 않은 상태로 처리 중인 경우 이 필드가 들어오지 않는다.
      - id 고유 일련번호. 각 카테고리 안에서만 일련번호가 고유하다. 예를 들어, 체결내역 안에서의 일련번호는 고유하지만, 체결내역과 KRW입출금 내역 간에는 동일한 일련번호가 사용될 수 있다.
      - type "buy"/"sell"
      - fee 수수료
        - currency
        - value
      - fillsDetail
        - price 체결된 가격. 현재는 currency가 항상 krw로 들어온다.
          - currency
          - value
        - amount 체결된 수량. currency 필드 값에는 currency_pair에 따라 "btc", "etc" 혹은 "eth"로 들어오며, value 필드에는 선택 화폐의 체결된 수량이 들어온다.
          - currency
          - value
        - native_amount 체결된 가격과 수량을 계산한 총 거래된 액수.
        - orderId 원 주문의 ID. 해당 체결 건이 발생하기 전에 사용자가 실행한 주문의 ID이다.        
    :param currency_pair: 요청할 통화쌍
    :param offset: 전체 데이터 중 offset(0부터 시작) 번 째 데이터부터 가져옴
    :param limit: 전체 데이터 중 limit개를 가져옴. 최대값은 40   '''
    res = korbit.get(
        url='https://api.korbit.co.kr/v1/user/transactions',
        params={'currency_pair': currency_pair,
                'offset': offset,
                'limit': limit})
    if res.ok:
        return res.json()
