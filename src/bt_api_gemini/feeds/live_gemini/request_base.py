from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_base.logging_factory import get_logger

from bt_api_base.rate_limiter import RateLimiter, RateLimitRule, RateLimitScope, RateLimitType

from bt_api_gemini.exchange_data import GeminiExchangeDataSpot
from bt_api_gemini.errors import GeminiErrorTranslator


class GeminiRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.MARKET_STREAM,
            Capability.ACCOUNT_STREAM,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.public_key = kwargs.get("public_key") or kwargs.get("api_key")
        self.private_key = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.exchange_name = kwargs.get("exchange_name", "GEMINI___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.logger_name = kwargs.get("logger_name", "gemini_spot_feed.log")
        self._params = GeminiExchangeDataSpot()
        self.request_logger = get_logger("gemini_spot_feed")
        self.async_logger = get_logger("gemini_spot_feed")
        self._error_translator = GeminiErrorTranslator()
        self._rate_limiter = kwargs.get("rate_limiter", self._create_default_rate_limiter())
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    @staticmethod
    def _create_default_rate_limiter():
        rules = [
            RateLimitRule(
                name="public_api",
                type=RateLimitType.SLIDING_WINDOW,
                limit=120,
                interval=60,
                scope=RateLimitScope.GLOBAL,
            ),
            RateLimitRule(
                name="private_api",
                type=RateLimitType.SLIDING_WINDOW,
                limit=600,
                interval=60,
                scope=RateLimitScope.GLOBAL,
            ),
            RateLimitRule(
                name="order",
                type=RateLimitType.SLIDING_WINDOW,
                limit=100,
                interval=60,
                scope=RateLimitScope.GLOBAL,
            ),
        ]
        return RateLimiter(rules)

    def _sign_request(self, path, params=None):
        if params is None:
            params = {}
        payload = {"request": path, "nonce": int(time.time() * 1000)}
        payload.update(params)
        payload_json = json.dumps(payload, separators=(",", ":"))
        payload_b64 = base64.b64encode(payload_json.encode("utf-8"))
        signature = hmac.new(
            self.private_key.encode("utf-8"), payload_b64, hashlib.sha384
        ).hexdigest()
        return payload_b64, signature

    def _build_headers(self, path, params=None):
        payload_b64, signature = self._sign_request(path, params)
        return {
            "X-GEMINI-APIKEY": self.public_key,
            "X-GEMINI-PAYLOAD": payload_b64.decode("utf-8"),
            "X-GEMINI-SIGNATURE": signature,
            "Content-Type": "text/plain",
            "Content-Length": "0",
            "Cache-Control": "no-cache",
        }

    def _normalize_response(self, response, extra_data):
        status = response is not None
        if extra_data and "normalize_function" in extra_data:
            return extra_data["normalize_function"](response, extra_data)
        return response, status

    def request(self, path, method="POST", params=None, data=None, extra_data=None):
        if method == "POST":
            headers = self._build_headers(path, params)
            url = f"{self._params.rest_url}{path}"
            with self._rate_limiter:
                response = self.http_request(method=method, url=url, headers=headers, body=data)
                normalized_response, status = self._normalize_response(response, extra_data)
                return normalized_response
        elif method == "GET":
            if params:
                query_string = urlencode(params)
                url = f"{self._params.rest_url}{path}?{query_string}"
            else:
                url = f"{self._params.rest_url}{path}"
            headers = {"Content-Type": "application/json"}
            with self._rate_limiter:
                response = self.http_request(method=method, url=url, headers=headers, body=data)
                normalized_response, status = self._normalize_response(response, extra_data)
                return normalized_response

    async def async_request(self, path, method="GET", params=None, extra_data=None, timeout=5):
        if method == "POST":
            headers = self._build_headers(path, params)
            url = f"{self._params.rest_url}{path}"
        else:
            if params:
                query_string = urlencode(params)
                url = f"{self._params.rest_url}{path}?{query_string}"
            else:
                url = f"{self._params.rest_url}{path}"
            headers = {"Content-Type": "application/json"}
        try:
            response = await self._http_client.async_request(
                method=method, url=url, headers=headers
            )
            normalized, status = self._normalize_response(response, extra_data)
            return normalized
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)
