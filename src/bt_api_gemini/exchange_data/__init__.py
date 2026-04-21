from bt_api_base.containers.exchanges.exchange_data import ExchangeData
from bt_api_base.logging_factory import get_logger

logger = get_logger("gemini_exchange_data")


class GeminiExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "GEMINI"
        self.rest_url = "https://api.gemini.com"
        self.wss_url = "wss://api.gemini.com/v1/marketdata"
        self.account_wss_url = "wss://api.gemini.com/v1/order/events"

        self.rest_paths = {
            "get_symbols": "/v1/symbols",
            "get_symbol_details": "/v1/symbols/details/{symbol}",
            "get_ticker": "/v1/pubticker/{symbol}",
            "get_depth": "/v1/book/{symbol}",
            "get_trades": "/v1/trades/{symbol}",
            "get_kline": "/v2/candles/{symbol}/{time_frame}",
            "get_system_time": "/v1/timestamp",
            "get_price_feed": "/v1/pricefeed",
            "get_balance": "/v1/balances",
            "get_open_orders": "/v1/orders",
            "get_order_history": "/v1/mytrades",
            "make_order": "/v1/order/new",
            "cancel_order": "/v1/order/cancel",
            "cancel_orders": "/v1/order/cancel/all",
            "query_order": "/v1/order/status",
            "get_transfers": "/v1/transfers",
        }

        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "6h": "6h",
            "1d": "1d",
            "7d": "7d",
            "14d": "14d",
            "30d": "30d",
        }

        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        self.legal_currency = ["USD", "BTC", "ETH"]

    def get_symbol(self, symbol: str) -> str:
        if symbol:
            return symbol.replace("/", "").replace("-", "").lower()
        return symbol

    def get_period(self, period: str) -> str:
        return self.reverse_kline_periods.get(period, period)

    def get_rest_path(self, request_type: str, **kwargs) -> str:
        if request_type in self.rest_paths:
            return self.rest_paths[request_type]
        return ""


class GeminiExchangeDataSpot(GeminiExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.exchange_name = "GEMINI___SPOT"
