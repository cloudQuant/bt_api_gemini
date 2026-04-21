from bt_api_base.containers.balances.balance import BalanceData


class GeminiBalanceData(BalanceData):
    def __init__(
        self,
        balance_info,
        symbol: str | None = None,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "GEMINI"
        self.symbol = symbol
        self.asset_type = asset_type
        self.currency: str | None = None
        self.amount: float | None = None
        self.available: float | None = None
        self.available_for_withdrawal: float | None = None
        self.timestamp: int | None = None

    def init_data(self):
        if self.has_been_json_encoded:
            return self
        if isinstance(self.balance_info, dict):
            self.currency = self.balance_info.get("currency")
            self.amount = float(self.balance_info.get("amount", 0)) or 0
            self.available = float(self.balance_info.get("available", 0)) or 0
            self.available_for_withdrawal = (
                float(self.balance_info.get("availableForWithdrawal", 0)) or 0
            )
            self.timestamp = self.balance_info.get("timestampms")
        elif isinstance(self.balance_info, list) and self.balance_info:
            first = self.balance_info[0]
            if isinstance(first, dict):
                self.currency = first.get("currency")
                self.amount = float(first.get("amount", 0)) or 0
                self.available = float(first.get("available", 0)) or 0
                self.available_for_withdrawal = float(first.get("availableForWithdrawal", 0)) or 0
                self.timestamp = first.get("timestampms")
        self.has_been_json_encoded = True
        return self

    def get_all_data(self):
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "currency": self.currency,
            "amount": self.amount,
            "available": self.available,
            "available_for_withdrawal": self.available_for_withdrawal,
            "timestamp": self.timestamp,
        }


class GeminiRequestBalanceData(GeminiBalanceData):
    def __init__(
        self,
        data,
        extra_data=None,
        status=False,
        normalize_func=None,
        symbol=None,
        asset_type=None,
        is_rest=True,
    ):
        if extra_data is None:
            extra_data = {}
        extra_data.setdefault("exchange_name", "GEMINI")
        if asset_type:
            extra_data.setdefault("asset_type", asset_type)
        super().__init__(data, symbol, asset_type or "SPOT", False)
        self.is_rest = is_rest
        if data:
            self.init_data()
