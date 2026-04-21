from bt_api_base.containers.bars.bar import BarData


class GeminiBarData(BarData):
    def __init__(
        self,
        bar_info,
        symbol_name: str | None = None,
        asset_type: str = "SPOT",
        time_frame: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.time_frame = time_frame
        self.open: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.close: float | None = None
        self.volume: float | None = None
        self.timestamp: int | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.bar_info, list) and len(self.bar_info) > 0:
            if isinstance(self.bar_info[0], list):
                bar_data = self.bar_info[-1]
            else:
                bar_data = self.bar_info
            if len(bar_data) >= 6:
                self.timestamp = bar_data[0]
                self.open = float(bar_data[1])
                self.high = float(bar_data[2])
                self.low = float(bar_data[3])
                self.close = float(bar_data[4])
                self.volume = float(bar_data[5])
        elif isinstance(self.bar_info, dict):
            self.open = float(self.bar_info.get("open", 0)) or 0
            self.high = float(self.bar_info.get("high", 0)) or 0
            self.low = float(self.bar_info.get("low", 0)) or 0
            self.close = float(self.bar_info.get("close", 0)) or 0
            self.volume = float(self.bar_info.get("volume", 0)) or 0
            self.timestamp = self.bar_info.get("timestamp")
        self.has_been_json_encoded = True
        return self

    @property
    def symbol(self):
        return self.symbol_name

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "time_frame": self.time_frame,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        self.init_data()
        return str(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name or ""

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | None:
        return self.timestamp

    def get_local_update_time(self) -> float | None:
        return self.timestamp

    def get_open_time(self) -> float | int:
        return self.timestamp or 0

    def get_open_price(self) -> float:
        return self.open or 0.0

    def get_high_price(self) -> float:
        return self.high or 0.0

    def get_low_price(self) -> float:
        return self.low or 0.0

    def get_close_price(self) -> float:
        return self.close or 0.0

    def get_volume(self) -> float:
        return self.volume or 0.0

    def get_amount(self) -> float:
        return self.volume or 0.0

    def get_close_time(self) -> float | None:
        return None

    def get_quote_asset_volume(self) -> float | None:
        return None

    def get_base_asset_volume(self) -> float | None:
        return None

    def _parse_single_bar(self, bar_data):
        if not isinstance(bar_data, list) or len(bar_data) < 6:
            return None
        return bar_data


class GeminiRequestBarData(GeminiBarData):
    def __init__(
        self,
        data,
        symbol: str | None = None,
        asset_type: str | None = None,
        time_frame: str | None = None,
        is_rest: bool = True,
        extra_data: dict | None = None,
        status: bool = False,
        normalize_func=None,
    ) -> None:
        if extra_data is None:
            extra_data = {}
        extra_data.setdefault("exchange_name", "GEMINI")
        if symbol:
            extra_data.setdefault("symbol_name", symbol)
        if asset_type:
            extra_data.setdefault("asset_type", asset_type)
        super().__init__(data, symbol, asset_type or "SPOT", time_frame, False)
        self.is_rest = is_rest
        if data:
            self.init_data()
