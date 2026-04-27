APP_NAME = "Baya Empire Pro"

DB_NAME = "baya_empire.db"

INITIAL_CASH = 10000.0
PAPER_FEE_RATE = 0.001  # 0.1% رسوم افتراضية للتجربة

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "ADAUSDT",
]

INTERVALS = {
    "1 دقيقة": "1m",
    "5 دقائق": "5m",
    "15 دقيقة": "15m",
    "1 ساعة": "1h",
    "4 ساعات": "4h",
    "1 يوم": "1d",
}

DATA_SOURCES = {
    "Binance US": "https://api.binance.us",
    "Binance Global": "https://api.binance.com",
}
