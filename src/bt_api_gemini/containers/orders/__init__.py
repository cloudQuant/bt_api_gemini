from bt_api_base.containers.orders.order import OrderData


class GeminiOrderData(OrderData):
    def __init__(
        self,
        order_info,
        symbol: str | None = None,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol = symbol
        self.asset_type = asset_type
        self.order_id: str | None = None
        self.client_order_id: str | None = None
        self.side: str | None = None
        self.type: str | None = None
        self.status: str | None = None
        self.price: float | None = None
        self.original_amount: float | None = None
        self.executed_amount: float | None = None
        self.timestamp: int | None = None
        self.avg_price: float | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.order_info, dict):
            if "order_id" in self.order_info:
                self.order_id = str(self.order_info.get("order_id"))
                self.client_order_id = self.order_info.get("client_order_id")
                self.symbol = self.order_info.get("symbol")
                self.side = self.order_info.get("side")
                self.type = self.order_info.get("type")
                self.status = self.order_info.get("status", "new")
                self.price = float(self.order_info.get("price", 0)) or 0
                self.original_amount = float(self.order_info.get("original_amount", 0)) or 0
                self.executed_amount = float(self.order_info.get("executed_amount", 0)) or 0
                self.timestamp = self.order_info.get("timestampms")
                avg = self.order_info.get("avg_execution_price")
                self.avg_price = float(avg) if avg else None
            elif "id" in self.order_info:
                self.order_id = str(self.order_info.get("id"))
                self.client_order_id = self.order_info.get("client_order_id")
                self.symbol = self.order_info.get("symbol")
                self.side = self.order_info.get("side")
                self.type = self.order_info.get("type")
                is_live = self.order_info.get("is_live")
                self.status = "active" if is_live else "filled"
                self.price = float(self.order_info.get("price", 0)) or 0
                self.original_amount = float(self.order_info.get("original_amount", 0)) or 0
                self.executed_amount = float(self.order_info.get("executed_amount", 0)) or 0
                self.timestamp = self.order_info.get("timestampms")
                avg = self.order_info.get("avg_execution_price")
                self.avg_price = float(avg) if avg else None
        self.has_been_json_encoded = True
        return self

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "order_id": self.order_id,
            "client_order_id": self.client_order_id,
            "side": self.side,
            "type": self.type,
            "status": self.status,
            "price": self.price,
            "original_amount": self.original_amount,
            "executed_amount": self.executed_amount,
            "timestamp": self.timestamp,
            "avg_price": self.avg_price,
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


class GeminiRequestOrderData(GeminiOrderData):
    def __init__(
        self,
        data,
        symbol=None,
        asset_type=None,
        is_rest=True,
        extra_data=None,
        status=False,
        normalize_func=None,
    ):
        if extra_data is None:
            extra_data = {}
        extra_data.setdefault("exchange_name", "GEMINI")
        if symbol:
            extra_data.setdefault("symbol_name", symbol)
        if asset_type:
            extra_data.setdefault("asset_type", asset_type)
        super().__init__(data, symbol, asset_type or "SPOT", False)
        self.is_rest = is_rest
        if data:
            self.init_data()
