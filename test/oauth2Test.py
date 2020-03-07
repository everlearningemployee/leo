# https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import yaml
import time
# from korbit import *


def token_saver(token):
    pass


def getSession():
    return OAuth2Session(
        # client_id=iam['client_id'],
        client=client,
        token=token,
        auto_refresh_url=authUrl['auto_refresh_url'],
        auto_refresh_kwargs=iam,
        token_updater=token_saver)


def work():
    # korbit = getSession()
    res = korbit.get(
        url='https://api.korbit.co.kr/v1/user/transactions',
        params={'currency_pair': 'xrp_krw',
                'offset': 0,
                'limit': 2})
    logging.info(res.json())
    time.sleep(2)


if __name__ == '__main__':
    import sys
    sys.path.append('../src')

    from utils import *
    from dao import *

    authUrl = {
        'token_url': 'https://api.korbit.co.kr/v1/oauth2/access_token',
        'auto_refresh_url': 'https://api.korbit.co.kr/v1/oauth2/access_token'}
    korbit = OAuth2Session(
        client=BackendApplicationClient(**iam),
        auto_refresh_url=authUrl['auto_refresh_url'],
        auto_refresh_kwargs=iam,
        token_updater=token_saver)
    token = korbit.fetch_token(
        **iam,
        token_url=authUrl['token_url'])

    while True:
        # for i in range(3):
        work()
