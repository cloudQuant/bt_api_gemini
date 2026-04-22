from bt_api_base.containers.tickers.ticker import TickerData


class GeminiTickerData(TickerData):

    def __init__(
        self,
        ticker_info,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.last_price: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.volume: float | None = None
        self.bid: float | None = None
        self.ask: float | None = None
        self.timestamp: int | None = None
        self.change_24h: float | None = None
        self.change_percent_24h: float | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.ticker_info, dict):
            self.last_price = float(
                self.ticker_info.get("close", self.ticker_info.get("last", 0)) or 0
            )
            self.high = float(self.ticker_info.get("high", 0)) or 0
            self.low = float(self.ticker_info.get("low", 0)) or 0
            vol = self.ticker_info.get("volume", {})
            if isinstance(vol, dict):
                self.volume = float(vol.get(self.symbol_name.lower(), 0)) if vol else None
            else:
                self.volume = float(vol) if vol else None
            self.bid = float(self.ticker_info.get("bid", 0)) or 0
            self.ask = float(self.ticker_info.get("ask", 0)) or 0
            self.timestamp = self.ticker_info.get("timestampms")
            changes = self.ticker_info.get("changes") or {}
            if isinstance(changes, dict):
                self.change_24h = float(changes.get("24h", 0))
                self.change_percent_24h = float(changes.get("24h_percent", 0))
        self.has_been_json_encoded = True
        return self

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "last_price": self.last_price,
            "high": self.high,
            "low": self.low,
            "volume": self.volume,
            "bid": self.bid,
            "ask": self.ask,
            "timestamp": self.timestamp,
            "change_24h": self.change_24h,
            "change_percent_24h": self.change_percent_24h,
        }


class GeminiRequestTickerData(GeminiTickerData):

    def __init__(
        self,
        data,
        symbol=None,
        asset_type=None,
        is_rest=True,
        extra_data=None,
        status=False,
        normalize_func=None,
    ) -> None:
        if extra_data is None:
            extra_data = {}
        extra_data.setdefault("exchange_name", "GEMINI")
        if symbol:
            extra_data.setdefault("symbol_name", symbol)
        if asset_type:
            extra_data.setdefault("asset_type", asset_type)
        super().__init__(data, symbol, asset_type, False)
        self.is_rest = is_rest
        if data:
            self.init_data()
