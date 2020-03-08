import yaml, json, logging
from os import path

with open(
        path.join(path.dirname(__file__), 'iam.yaml'),
        encoding='utf-8') as f:
    iam = yaml.load(f, Loader=yaml.FullLoader)

with open(
        path.join(path.dirname(__file__), 'propensity.yaml'),
        encoding='utf-8') as f:
    prpnst = yaml.load(f, Loader=yaml.FullLoader)
    # TODO 설정 출력할 것

with open(
        path.join(path.dirname(__file__), 'config.yaml'),
        encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    # TODO 설정 출력할 것


# LEO_ORDER = 'LeoOrder.yaml'
LEO_ORDER = 'LeoOrder.json'
# leoOrderLog = path.join(path.dirname(__file__), LEO_ORDER)
leoOrderLog = path.join('/leo/order', LEO_ORDER)

def getLeoOrder():
    try:
        with open(leoOrderLog, 'r') as f:
            # LeoOrdr = yaml.load(f, Loader=yaml.FullLoader)
            LeoOrdr = json.load(f)
    except:
        return None
    return LeoOrdr


def newLeoOrder(newOrder):
    toSave = list(filter(None, newOrder))
    with open(leoOrderLog, 'a') as f:
        # yaml.dump(toSave, f)
        json.dump(toSave, f)


def resetLeoOrder():
    logging.debug('reset LeoOrder')
    open(leoOrderLog, 'w').close()


