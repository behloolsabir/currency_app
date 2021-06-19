class trade:
    """
    Trade object.
    """
    def __init__(self, base, quote, timestamp, provider, rate, operation):
        self.base = base
        self.quote = quote
        self.timestamp = timestamp
        self.provider = provider
        self.rate = rate
        self.operation = operation
    