import logging.config

def recordOrder(log):    
    orderLogging.info(','.join([str(i) for i in log]))


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
        'order': {
            'class': 'logging.FileHandler',
            'filename': 'order.log',
            'mode': 'a',
            'formatter': 'csv',
            'level': 'INFO',
        },
        'ticker': {
            'class': 'logging.FileHandler',
            'filename': 'ticker.log',
            'mode': 'a',
            'formatter': 'csv',
            'level': 'INFO',
        },
        'trans': {
            'class': 'logging.FileHandler',
            'filename': 'trans.log',
            'mode': 'a',
            'formatter': 'csv',
            'level': 'INFO',
        },
        'errors': {
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'mode': 'a',
            'level': 'ERROR',
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
        'handlers': ['console', 'errors'],
        'level': 'DEBUG',
    },
})

orderLogging = logging.getLogger('order')
tickerLogging = logging.getLogger('ticker')
transactionsLogging = logging.getLogger('trans')



