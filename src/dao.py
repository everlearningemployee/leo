import yaml
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
    with open(path.join(path.dirname(__file__), LEO_ORDER), 'r') as f:
        LeoOrdr = yaml.load(f, Loader=yaml.FullLoader)
    return LeoOrdr


def newLeoOrder(newOrder):
    with open(path.join(path.dirname(__file__), LEO_ORDER), 'a') as f:
        yaml.dump(newOrder, f)


def resetLeoOrder():
    open(LEO_ORDER, 'w').close()
