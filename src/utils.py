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

orderLogging = logging.getLogger('order')
tickerLogging = logging.getLogger('ticker')
transactionsLogging = logging.getLogger('trans')



