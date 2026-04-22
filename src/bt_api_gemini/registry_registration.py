from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from bt_api_gemini import __version__
from bt_api_gemini.exchange_data import GeminiExchangeDataSpot
from bt_api_gemini.feeds.live_gemini import GeminiRequestDataSpot

if TYPE_CHECKING:
    pass


def _gemini_subscribe_handler(
    data_queue,
    exchange_params,
    topics,
    bt_api,
):
    from bt_api_gemini.feeds.live_gemini import GeminiRequestDataSpot

    feed = GeminiRequestDataSpot(
        data_queue=data_queue,
        public_key=exchange_params.get("public_key", ""),
        private_key=exchange_params.get("private_key", ""),
        testnet=exchange_params.get("testnet", False),
    )
    feed.start()
    return feed


def register_plugin(
    registry: type[ExchangeRegistry], runtime_factory: type[GatewayRuntimeRegistrar]
) -> PluginInfo | None:
    try:
        from bt_api_base.plugins.metadata import PluginMetadata  # noqa: F401
        from bt_api_base.plugins.protocol import PluginInfo
    except ImportError:
        return None

    registry.register_feed("GEMINI___SPOT", GeminiRequestDataSpot)
    registry.register_exchange_data("GEMINI___SPOT", GeminiExchangeDataSpot)

    return PluginInfo(
        name="bt_api_gemini",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("GEMINI___SPOT",),
        supported_asset_types=("SPOT",),
    )


def register_gemini():
    try:
        from bt_api_base.plugins.metadata import PluginMetadata  # noqa: F401
        from bt_api_base.plugins.protocol import PluginInfo  # noqa: F401
    except ImportError:
        return

    class MockRuntimeFactory:
        def register_adapter(self, *args, **kwargs):
            pass

    register_plugin(ExchangeRegistry, MockRuntimeFactory)


register_gemini()
