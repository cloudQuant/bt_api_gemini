# Gemini Documentation

## English

Welcome to the Gemini documentation for bt_api.

### Quick Start

```bash
pip install bt_api_gemini
```

```python
from bt_api_gemini import GeminiRequestDataSpot
feed = GeminiRequestDataSpot(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSD")
```

## 中文

欢迎使用 bt_api 的 Gemini交易所 文档。

### 快速开始

```bash
pip install bt_api_gemini
```

```python
from bt_api_gemini import GeminiRequestDataSpot
feed = GeminiRequestDataSpot(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSD")
```

## API Reference

See source code in `src/bt_api_gemini/` for detailed API documentation.
