from bt_api_base.containers.orderbooks.orderbook import OrderBookData


class GeminiOrderBookData(OrderBookData):
    def __init__(
        self,
        orderbook_info,
        symbol: str | None = None,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol = symbol
        self.asset_type = asset_type
        self.bids: list[dict] = []
        self.asks: list[dict] = []
        self.timestamp: int | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.order_book_info, dict):
            if "bids" in self.order_book_info:
                self.bids = []
                for bid in self.order_book_info["bids"]:
                    if isinstance(bid, dict):
                        self.bids.append(
                            {
                                "price": float(bid.get("price", 0)),
                                "amount": float(bid.get("amount", 0)),
                            }
                        )
                    elif isinstance(bid, list) and len(bid) >= 2:
                        self.bids.append({"price": float(bid[0]), "amount": float(bid[1])})
            if "asks" in self.order_book_info:
                self.asks = []
                for ask in self.order_book_info["asks"]:
                    if isinstance(ask, dict):
                        self.asks.append(
                            {
                                "price": float(ask.get("price", 0)),
                                "amount": float(ask.get("amount", 0)),
                            }
                        )
                    elif isinstance(ask, list) and len(ask) >= 2:
                        self.asks.append({"price": float(ask[0]), "amount": float(ask[1])})
            self.timestamp = self.order_book_info.get("timestampms")
        self.has_been_json_encoded = True
        return self

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol,
            "asset_type": self.asset_type,
            "bids": self.bids,
            "asks": self.asks,
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        self.init_data()
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

    def get_bid_price_list(self) -> list[float]:
        self.init_data()
        return [bid["price"] for bid in self.bids]

    def get_ask_price_list(self) -> list[float]:
        self.init_data()
        return [ask["price"] for ask in self.asks]

    def get_bid_volume_list(self) -> list[float]:
        self.init_data()
        return [bid["amount"] for bid in self.bids]

    def get_ask_volume_list(self) -> list[float]:
        self.init_data()
        return [ask["amount"] for ask in self.asks]


class GeminiRequestOrderBookData(GeminiOrderBookData):
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
