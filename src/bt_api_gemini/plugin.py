try:
    from bt_api_base.plugins.metadata import PluginMetadata
except ImportError:
    PluginMetadata = None
try:
    from bt_api_base.plugins.protocol import PluginInfo
except ImportError:
    PluginInfo = None

from bt_api_gemini.feeds.live_gemini import GeminiRequestDataSpot

if PluginMetadata is not None and PluginInfo is not None:
    GEMINI_PLUGIN_INFO = PluginInfo(
        name="bt_api_gemini",
        metadata=PluginMetadata(
            display_name="Gemini",
            description="Gemini exchange plugin for spot trading",
            version="0.1.0",
            tags=["gemini", "exchange", "spot"],
        ),
        feed_classes=[GeminiRequestDataSpot],
        container_classes=[],
    )
else:
    GEMINI_PLUGIN_INFO = None
