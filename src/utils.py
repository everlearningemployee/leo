import sys
import traceback
import logging.config


logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-6s %(levelname)8s %(message)s',
            # 'datefmt': '%Y-%m-%d %H:%M:%S.%f'
            'datefmt': '%Y-%m-%d,%H:%M:%S'
        },
        'csv': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s,%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        'out': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/leo/out.log',
            'mode': 'a',
            'formatter': 'detailed',
            'encoding': 'utf-8',
        },
        'order': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/leo/order.log',
            'mode': 'a',
            'formatter': 'csv',
            'encoding': 'utf-8',
            'level': 'INFO',
        },
        'ticker': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/leo/ticker.log',
            'mode': 'a',
            'formatter': 'csv',
            'encoding': 'utf-8',
            'level': 'INFO',
        },
        'trans': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/leo/trans.log',
            'mode': 'a',
            'formatter': 'csv',
            'encoding': 'utf-8',
            'level': 'INFO',
        },
        'errors': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/leo/errors.log',
            'mode': 'a',
            'level': 'ERROR',
            'encoding': 'utf-8',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'ticker': {
            'handlers': ['ticker']
        },
        'order': {
            'handlers': ['order']
        },
        'trans': {
            'handlers': ['trans']
        },
        'errors': {
            'handlers': ['errors']
        },
    },
    'root': {
        'handlers': ['console', 'out', 'errors'],
        'level': 'DEBUG',
    },
})


def recordOrder(log):
    orderLogging.info(','.join([str(i) for i in log]))


def exception_hook(type, value, tb):
    logging.error('='*80)
    t = traceback.format_exception(type, value, tb)
    t = [i.rstrip().split('\n') for i in t]
    for i in sum(t, []):
        logging.error(i)
    logging.error('-'*80)


sys.excepthook = exception_hook


orderLogging = logging.getLogger('order')
tickerLogging = logging.getLogger('ticker')
transactionsLogging = logging.getLogger('trans')
