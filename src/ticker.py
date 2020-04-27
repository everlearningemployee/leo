import korbit as API
import logging.config
import logging
import time

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(levelname)8s %(message)s',
        },
        'msg': {
            'class': 'logging.Formatter',
            'format': '%(message)s',
        },        
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        'ticker': {
            'class': 'logging.FileHandler',
            'filename': 'ticker.log',
            'mode': 'a',
            'formatter': 'msg',
            'encoding': 'utf-8',
            'level': 'INFO',
        },
    },
    'loggers': {
        'ticker': {
            'handlers': ['ticker']
        },
    },    
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
})

tickerLogging = logging.getLogger('ticker')

while True:
    ob = API.orderbook(currency_pair='xrp_krw')
    tickerLogging.info(ob)
    time.sleep(1)
