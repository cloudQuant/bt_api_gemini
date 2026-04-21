from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from bt_api_base.functions.utils import update_extra_data

from bt_api_gemini.exchange_data import GeminiExchangeDataSpot
from bt_api_gemini.feeds.live_gemini.request_base import GeminiRequestData
from bt_api_gemini.containers.orders import GeminiRequestOrderData


class GeminiRequestDataSpot(GeminiRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "GEMINI___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = GeminiExchangeDataSpot()

    def _make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        request_symbol = self._params.get_symbol(symbol)
        side, order_type = order_type.split("-")
        gemini_order_type = "exchange limit" if order_type != "market" else "exchange market"
        params = {
            "symbol": request_symbol,
            "side": side.upper(),
            "amount": str(vol),
            "price": str(price) if price else None,
            "type": gemini_order_type,
        }
        if client_order_id is not None:
            params["client_order_id"] = client_order_id
        options = []
        if post_only:
            options.append("maker-or-cancel")
        if kwargs.get("time_in_force") == "IOC":
            options.append("immediate-or-cancel")
        elif kwargs.get("time_in_force") == "FOK":
            options.append("fill-or-kill")
        if options:
            params["options"] = options
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "make_order",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._make_order_normalize_function,
            },
        )
        return self._params.get_rest_path("make_order"), params, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [GeminiRequestOrderData(i, symbol_name, asset_type, True) for i in input_data]
        elif isinstance(input_data, dict):
            data = [GeminiRequestOrderData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_balance(self, symbol=None, extra_data=None, **kwargs):
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_balance",
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_balance_normalize_function,
            },
        )
        return self._params.get_rest_path("get_balance"), {}, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        return [input_data], True

    def _get_account(self, extra_data=None, **kwargs):
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_account",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_account_normalize_function,
            },
        )
        return self._params.get_rest_path("get_balance"), {}, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        return [input_data], True

    def _get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_open_orders")
        params = {}
        if symbol:
            params["symbol"] = self._params.get_symbol(symbol)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_open_orders",
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            },
        )
        return path, params, extra_data

    def _query_order(self, symbol, order_id, extra_data=None, **kwargs):
        params = {"order_id": order_id}
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "query_order",
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "order_id": order_id,
            },
        )
        return self._params.get_rest_path("query_order"), params, extra_data

    def _get_ticker(self, symbol, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol) if symbol else None
        path = self._params.get_rest_path("get_ticker").format(symbol=request_symbol)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_tick",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            },
        )
        return path, {}, extra_data

    _get_tick = _get_ticker

    @staticmethod
    def _get_tick_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        return [input_data], True

    def _get_depth(self, symbol, limit_bids=50, limit_asks=50, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_depth").format(symbol=request_symbol)
        params = {"limit_bids": limit_bids, "limit_asks": limit_asks}
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_depth",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        return [input_data], True

    def _get_trades(self, symbol, limit_trades=50, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_trades").format(symbol=request_symbol)
        params = {"limit_trades": limit_trades}
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_trades",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            },
        )
        return path, params, extra_data

    def _get_kline(self, symbol, time_frame, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        gemini_time_frame = self._params.get_period(time_frame)
        path = self._params.get_rest_path("get_kline").format(
            symbol=request_symbol, time_frame=gemini_time_frame
        )
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_kline",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            },
        )
        return path, {}, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if isinstance(input_data, list):
            return [input_data], True
        return [input_data], True

    def _get_symbols(self, extra_data=None, **kwargs):
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_symbols",
                "symbol_name": "ALL",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            },
        )
        return self._params.get_rest_path("get_symbols"), {}, extra_data

    def _get_symbol_details(self, symbol, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_symbol_details").format(symbol=request_symbol)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_symbol_details",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
            },
        )
        return path, {}, extra_data

    def get_balance(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def get_account(self, symbol="ALL", extra_data=None, **kwargs):
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def query_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra_data = self._query_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def get_ticker(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_ticker(symbol, extra_data, **kwargs)
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    get_tick = get_ticker

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, method="GET", params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_depth(self, symbol, limit_bids=50, limit_asks=50, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(
            symbol, limit_bids, limit_asks, extra_data, **kwargs
        )
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    def async_get_depth(self, symbol, limit_bids=50, limit_asks=50, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(
            symbol, limit_bids, limit_asks, extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, method="GET", params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_trades(self, symbol, limit_trades=50, extra_data=None, **kwargs):
        path, params, extra_data = self._get_trades(symbol, limit_trades, extra_data, **kwargs)
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    def get_kline(self, symbol, time_frame, extra_data=None, **kwargs):
        path, params, extra_data = self._get_kline(symbol, time_frame, extra_data, **kwargs)
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    def async_get_kline(self, symbol, time_frame, extra_data=None, **kwargs):
        path, params, extra_data = self._get_kline(symbol, time_frame, extra_data, **kwargs)
        self.submit(
            self.async_request(path, method="GET", params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def get_symbols(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_symbols(extra_data, **kwargs)
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    def get_symbol_details(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_symbol_details(symbol, extra_data, **kwargs)
        return self.request(path, method="GET", params=params, extra_data=extra_data)

    def make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, params, extra_data = self._make_order(
            symbol, vol, price, order_type, offset, post_only, client_order_id, extra_data, **kwargs
        )
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        path = self._params.get_rest_path("cancel_order")
        params = {"order_id": order_id}
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "cancel_order",
                "order_id": order_id,
            }
        )
        return self.request(path, method="POST", params=params, extra_data=extra_data)

    def cancel_all_orders(self, symbol=None, extra_data=None, **kwargs):
        path = self._params.get_rest_path("cancel_orders")
        params = {}
        if symbol:
            params["symbol"] = self._params.get_symbol(symbol)
        return self.request(path, method="POST", params=params, extra_data=extra_data)
