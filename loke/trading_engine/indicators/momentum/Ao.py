

class Ao:

    def __init__(self):
        self.fast = None
        self.slow = None
        self.offset = None

    def get(self):
        return {
            "kind": self.__class__.__name__.lower(),
            "fast": self.fast,
            "slow": self.slow,
            "offset": self.offset
        }

    def set(self, fast, slow, offset):
        self.fast = fast
        self.slow = slow
        self.offset = offset

    def type_dict(self):
        return [("kind", self.__class__.__name__.lower()), ("fast", "int", 5), ("slow", "int", 34), ("offset", "int", 0),]

    def type_only(self):
        return [{"kind": self.__class__.__name__.lower(), "fast": "int", "slow": "int", "offset": "int"}]

    def default_values(self):
        return [("kind", self.__class__.__name__.lower()), ("fast", 5), ("slow", 34), ("offset", 0),]

    def chart_info(self):
        return "histogram"

    def __repr__(self):
        description = """Awesome Oscillator (AO)

    The Awesome Oscillator is an indicator used to measure a security's momentum.
    AO is generally used to affirm trends or to anticipate possible reversals.

    Sources:
        https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)
        https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator

    Calculation:
        Default Inputs:
            fast=5, slow=34
        SMA = Simple Moving Average
        median = (high + low) / 2
        AO = SMA(median, fast) - SMA(median, slow)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        fast (int): The short period. Default: 5
        slow (int): The long period. Default: 34
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
        return description
