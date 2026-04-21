from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class GeminiErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        "InvalidSignature": (UnifiedErrorCode.INVALID_SIGNATURE, "Invalid signature"),
        "InvalidNonce": (UnifiedErrorCode.EXPIRED_TIMESTAMP, "Invalid nonce"),
        "MissingPayloadHeader": (UnifiedErrorCode.MISSING_PARAMETER, "Missing payload header"),
        "InvalidPayload": (UnifiedErrorCode.INVALID_PARAMETER, "Invalid payload"),
        "InvalidAPIKey": (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        "RateLimit": (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded"),
        "InsufficientFunds": (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient funds"),
        "InvalidPrice": (UnifiedErrorCode.INVALID_PRICE, "Invalid price"),
        "InvalidQuantity": (UnifiedErrorCode.INVALID_VOLUME, "Invalid quantity"),
        "InvalidSide": (UnifiedErrorCode.INVALID_PARAMETER, "Invalid side"),
        "InvalidOrderType": (UnifiedErrorCode.INVALID_ORDER, "Invalid order type"),
        "OrderNotFound": (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        "ClientOrderIdNotFound": (UnifiedErrorCode.ORDER_NOT_FOUND, "Client order ID not found"),
        "SystemError": (UnifiedErrorCode.INTERNAL_ERROR, "System error"),
        "MarketNotOpen": (UnifiedErrorCode.MARKET_CLOSED, "Market not open"),
        "MaintenanceError": (UnifiedErrorCode.EXCHANGE_OVERLOADED, "Exchange under maintenance"),
    }
