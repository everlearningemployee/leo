import yaml, logging
from os import path

with open(
        path.join(path.dirname(__file__), 'iam.yaml'),
        encoding='utf-8') as f:
    iam = yaml.load(f, Loader=yaml.FullLoader)

with open(
        path.join(path.dirname(__file__), 'propensity.yaml'),
        encoding='utf-8') as f:
    prpnst = yaml.load(f, Loader=yaml.FullLoader)

with open(
        path.join(path.dirname(__file__), 'config.yaml'),
        encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


LEO_ORDER = 'LeoOrder.yaml'


def getLeoOrder():
    try:
        with open(path.join(path.dirname(__file__), LEO_ORDER), 'r') as f:
            LeoOrdr = yaml.load(f, Loader=yaml.FullLoader)
    except:
        return None
    return LeoOrdr


def newLeoOrder(newOrder):
    toSave = list(filter(None, newOrder))
    with open(path.join(path.dirname(__file__), LEO_ORDER), 'a') as f:
        yaml.dump(toSave, f)


def resetLeoOrder():
    open(LEO_ORDER, 'w').close()


