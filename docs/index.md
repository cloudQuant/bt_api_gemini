# Gemini Documentation

## English

Welcome to the Gemini documentation for bt_api.

### Quick Start

```bash
pip install bt_api_gemini
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "GEMINI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("GEMINI___SPOT", "BTCUSD")
print(ticker)
```

## 中文

欢迎使用 bt_api 的 Gemini交易所 文档。

### 快速开始

```bash
pip install bt_api_gemini
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "GEMINI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("GEMINI___SPOT", "BTCUSD")
print(ticker)
```

## API Reference

See source code in `src/bt_api_gemini/` for detailed API documentation.
