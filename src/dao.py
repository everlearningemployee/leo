import yaml

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

with open(
        path.join(path.dirname(__file__), 'LeoOrdr.yaml'),
        'w', encoding='utf-8') as f:
    LeoOrdr = yaml.load(f, Loader=yaml.FullLoader)
