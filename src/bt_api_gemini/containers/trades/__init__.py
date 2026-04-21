from bt_api_base.containers.trades.trade import TradeData


class GeminiTradeData(TradeData):
    def __init__(
        self,
        trade_info,
        symbol: str | None = None,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(trade_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol = symbol
        self.asset_type = asset_type
        self.trade_id: int | None = None
        self.price: float | None = None
        self.amount: float | None = None
        self.side: str | None = None
        self.timestamp: int | None = None
        self.type: str | None = None
        self.fee: float | None = None
        self.fee_currency: str | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.trade_info, dict):
            if "tid" in self.trade_info:
                self.trade_id = self.trade_info.get("tid")
                self.price = float(self.trade_info.get("price", 0)) or 0
                self.amount = float(self.trade_info.get("amount", 0)) or 0
                self.side = self.trade_info.get("type")
                self.timestamp = self.trade_info.get("timestampms")
                self.type = "trade"
            elif "trade_id" in self.trade_info:
                self.trade_id = self.trade_info.get("trade_id")
                self.price = float(self.trade_info.get("price", 0)) or 0
                self.amount = float(self.trade_info.get("amount", 0)) or 0
                self.side = self.trade_info.get("side")
                self.timestamp = self.trade_info.get("timestampms")
                self.type = self.trade_info.get("execution_type")
                self.fee = float(self.trade_info.get("fee_amount", 0)) or 0
                self.fee_currency = self.trade_info.get("fee_currency")
        self.has_been_json_encoded = True
        return self

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "trade_id": self.trade_id,
            "price": self.price,
            "amount": self.amount,
            "side": self.side,
            "timestamp": self.timestamp,
            "type": self.type,
            "fee": self.fee,
            "fee_currency": self.fee_currency,
        }

    def to_dict(self):
        return self.get_all_data()

    def __str__(self) -> str:
        return str(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str | None:
        return self.symbol

    def get_asset_type(self) -> str | None:
        return self.asset_type

    def get_server_time(self) -> float | None:
        return self.timestamp

    def get_local_update_time(self) -> float | None:
        return self.timestamp


class GeminiRequestTradeData(GeminiTradeData):
    def __init__(self, data, symbol=None, asset_type=None, is_rest=True):
        super().__init__(data, symbol, asset_type or "SPOT", False)
        self.is_rest = is_rest
        if data:
            self.init_data()
