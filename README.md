# bt_api_gemini

Gemini exchange plugin for `bt_api`, supporting Spot trading.

## Installation

```bash
pip install bt_api_gemini
```

## Usage

```python
from bt_api_gemini import GeminiRequestDataSpot

feed = GeminiRequestDataSpot(public_key="your_key", private_key="your_secret")
ticker = feed.get_ticker("BTCUSD")
```

## Architecture

```
bt_api_gemini/
├── exchange_data/         # Exchange configuration and REST/WSS paths
├── errors/                # Error translator
├── tickers/               # Ticker data container
├── feeds/live_gemini/     # REST API implementation
├── containers/            # Data containers (balance, bar, orderbook, order, trade)
└── plugin.py              # PluginInfo registration
```
