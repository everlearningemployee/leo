def detailed(currency_pair, **kwargs):
    return {
        "timestamp": 1558590089274,
        "last": "9198500",
        "open": "9500000",
        "bid": "9192500",
        "ask": "9198000",
        "low": "9171500",
        "high": "9599000",
        "volume": "1539.18571988",
        "change": "-301500",
        "changePercent": "-3.17"
    }


def orderbook(currency_pair, **kwargs):
    return {
        "timestamp": 1386135077000,
        "bids": [
            [
                "1100000",
                "0.0103918",
                "1"
            ],
            [
                "1000000",
                "0.01000000",
                "1"
            ]
        ],
        "asks": [
            [
                "569000",
                "0.50000000",
                "1"
            ],
            [
                "568500",
                "2.00000000",
                "1"
            ]
        ]
    }


def constants():
    return {
        "exchange": {
            "btc_krw": {
                "tick_size": 500,
                "min_price": 1000,
                "max_price": 100000000,
                "order_min_size": 0.00100000,
                "order_max_size": 100.00000000
            },
            "eth_krw": {
                "tick_size": 50,
                "min_price": 1000,
                "max_price": 100000000,
                "order_min_size": 0.01000000,
                "order_max_size": 1000.00000000
            }
        }
    }


def balances():
    return {
        "krw": {
            "available": "123000",
            "trade_in_use": "13000",
            "withdrawal_in_use": "0"
        },
        "btc": {
            "available": "1.50200000",
            "trade_in_use": "0.42000000",
            "withdrawal_in_use": "0.50280000",
            "avg_price": "7115500",
            "avg_price_updated_at": 1528944850000
        },
        "eth": {
            "available": "4.80200000",
            "trade_in_use": "1.23238000",
            "withdrawal_in_use": "0.00000000",
            "avg_price": "529000",
            "avg_price_updated_at": 1528944250000
        },
        "etc": {
            "available": "10.00000000",
            "trade_in_use": "2.00000000",
            "withdrawal_in_use": "0.00000000",
            "avg_price": "14770",
            "avg_price_updated_at": 1528945850000
        },
        "xrp": {
            "available": "134524.657899",
            "trade_in_use": "2332.000000",
            "withdrawal_in_use": "0.000000",
            "avg_price": "594",
            "avg_price_updated_at": 1528944340000
        }
    }


def volume(currency_pair, **kwargs):
    return {
        "btc_krw": {
            "volume": "17570000",
            "maker_fee": "0.00100000",
            "taker_fee": "0.00200000"
        },
        "eth_krw": {
            "volume": "0",
            "maker_fee": "0.00100000",
            "taker_fee": "0.00200000"
        },
        "etc_krw": {
            "volume": "6570000",
            "maker_fee": "0.00100000",
            "taker_fee": "0.00200000"
        },
        "total_volume": "24140000",
        "timestamp": 1386418990000
    }


def buy(currency_pair, buy_type, price=None, coin_amount=None, fiat_amount=None, **kwargs):
    return {
        "orderId": "58738",
        "status": "success",
        "currency_pair": "btc_krw"
    }


def sell(currency_pair, sell_type, price=None, coin_amount=None, **kwargs):
    return {
        "orderId": "12513",
        "status": "success",
        "currency_pair": "btc_krw"
    }


def cancel(currency_pair, id, **kwargs):
    return [
        {"orderId": "1000", "status": "success"},
        {"orderId": "1001", "status": "not_found"},
        {"orderId": "1002", "status": "success"}
    ]


def open(currency_pair, offset=0, limit=40, **kwargs):
    return [
        {
            "timestamp": 1389173297000,
            "id": "58726",
            "type": "ask",
            "price": {
                "currency": "krw",
                "value": "800000"
            },
            "total": {
                "currency": "btc",
                "value": "1.00000000"
            },
            "open": {
                "currency": "btc",
                "value": "0.75000000"
            }
        },
        {
            "timestamp": 1386419377000,
            "id": "37499",
            "type": "bid",
            "price": {
                "currency": "krw",
                "value": "700000"
            },
            "total": {
                "currency": "btc",
                "value": "1.50000000"
            },
            "open": {
                "currency": "btc",
                "value": "0.41200000"
            }
        }
    ]


def orders(currency_pair, status, id, offset=0, limit=40, **kwargs):
    return [
        {
            "id": "89999",
            "currency_pair": "btc_krw",
            "side": "bid",
            "avg_price": "2900000",
            "price": "3000000",
            "order_amount": "0.81140000",
            "filled_amount": "0.33122200",
            "order_total": "2434200",
            "filled_total": "960543",
            "created_at": "1500033942638",
            "last_filled_at": "1500533946947",
            "status": "partially_filled",
            "fee": "0.00000500"
        },
        {
            "id": "90002",
            "currency_pair": "btc_krw",
            "side": "ask",
            "avg_price": "0",
            "price": "5000000",
            "order_amount": "0.71140000",
            "filled_amount": "0",
            "order_total": "3557000",
            "filled_total": "0",
            "created_at": "1500533946947",
            "status": "unfilled"
        },
        {
            "id": "90003",
            "currency_pair": "btc_krw",
            "side": "bid",
            "avg_price": "3000000",
            "price": "3000000",
            "order_amount": "0.81140000",
            "filled_amount": "0.81140000",
            "order_total": "2434200",
            "filled_total": "2434200",
            "created_at": 1400533933748,
            "last_filled_at": "1500510381038",
            "status": "filled",
            "fee": "0.00001000"
        }
    ]


def transactions(currency_pair, offset=0, limit=40, **kwargs):
    return [
        {
            "timestamp": 1383707746000,
            "completedAt": 1383797746000,
            "id": "599",    
            "type": "sell",
            "fee": {
                "currency": "krw",
                "value": "1500"
            },
            "fillsDetail": {
                "price": {
                    "currency": "krw",
                    "value": "1000000"
                },
                "amount": {
                    "currency": "btc",
                    "value": "1"
                },
                "native_amount": {
                    "currency": "krw",
                    "value": "1000000"
                },
                "orderId": "1002" 
            }
        },
        {
            "timestamp": 1383705741000,
            "completedAt": 1383797746200,
            "id": "597",
            "type": "buy",
            "fee": {
                "currency": "btc",
                "value": "0.0015"
            },
            "fillsDetail": {
                "price": {
                    "currency": "krw",
                    "value": "1000000"
                },
                "amount": {
                    "currency": "btc",
                    "value": "1"
                },
                "native_amount": {
                    "currency": "krw",
                    "value": "1000000"
                },
                "orderId": "1002" // 이거이거
            }
        }
    ]
