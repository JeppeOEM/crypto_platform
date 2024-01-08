#           high (pd.Series): Series of 'high's


class Adx:

    def __init__(self):
        self.length = None
        self.lensig = None
        self.scalar = None
        self.mamode = None
        self.drift = None
        self.offset = None

    def get(self):
        return {
            "kind": self.__class__.__name__.lower(),
            "fast": self.length,
            "lensig": self.lensig,
            "scalar": self.scalar,
            "mamode": self.mamode,
            "drift": self.drift,
            "offset": self.offset,
        }

    def set(self, length, lensig, scalar, mamode, drift, offset):
        self.length = length
        self.lensig = lensig
        self.scalar = scalar
        self.mamode = mamode
        self.drift = drift
        self.offset = offset

    def type_dict(self):
        return [("kind", self.__class__.__name__.lower()), ("fast", "int", 14), ("lensig", "int", 14), ("scalar", "float", 100), ("mamode", "str", "rma"), ("drift", "int", 1), ("offset", "int", 0),]

    def type_only(self):
        return [{"kind": self.__class__.__name__.lower(), "fast": "int", "lensig": "int", "scalar": "float", "mamode": "str", "drift": "int", "offset": "int"}]

        # [{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {
        #     'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]

    def default_values(self):
        return [("kind", self.__class__.__name__.lower()), ("fast", 14), ("lensig", 14), ("scalar", 100), ("mamode", "rma"), ("drift", 1), ("offset", 0),]

    def __repr__(self):
        description = """
    Average Directional Movement (ADX)

    adx(high, low, close, length=None, lensig=None, scalar=None, mamode=None, drift=None, offset=None, **kwargs)

    Average Directional Movement is meant to quantify trend strength by measuring       
    the amount of movement in a single direction.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/average-directional-movement-adx/
        TA Lib Correlation: >99%

    Calculation:
        DMI ADX TREND 2.0 by @TraderR0BERT, NETWORTHIE.COM
            //Created by @TraderR0BERT, NETWORTHIE.COM, last updated 01/26/2016
            //DMI Indicator
            //Resolution input option for higher/lower time frames
            study(title="DMI ADX TREND 2.0", shorttitle="ADX TREND 2.0")

            adxlen = input(14, title="ADX Smoothing")
            dilen = input(14, title="DI Length")
            thold = input(20, title="Threshold")

            threshold = thold

            //Script for Indicator
            dirmov(len) =>
                up = change(high)
                down = -change(low)
                truerange = rma(tr, len)
                plus = fixnan(100 * rma(up > down and up > 0 ? up : 0, len) / truerange)
                minus = fixnan(100 * rma(down > up and down > 0 ? down : 0, len) / truerange)
                [plus, minus]

            adx(dilen, adxlen) =>
                [plus, minus] = dirmov(dilen)
                sum = plus + minus
                adx = 100 * rma(abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)      
                [adx, plus, minus]

            [sig, up, down] = adx(dilen, adxlen)
            osob=input(40,title="Exhaustion Level for ADX, default = 40")
            col = sig >= sig[1] ? green : sig <= sig[1] ? red : gray

            //Plot Definitions Current Timeframe
            p1 = plot(sig, color=col, linewidth = 3, title="ADX")
            p2 = plot(sig, color=col, style=circles, linewidth=3, title="ADX")
            p3 = plot(up, color=blue, linewidth = 3, title="+DI")
            p4 = plot(up, color=blue, style=circles, linewidth=3, title="+DI")
            p5 = plot(down, color=fuchsia, linewidth = 3, title="-DI")
            p6 = plot(down, color=fuchsia, style=circles, linewidth=3, title="-DI")    
            h1 = plot(threshold, color=black, linewidth =3, title="Threshold")

            trender = (sig >= up or sig >= down) ? 1 : 0
            bgcolor(trender>0?black:gray, transp=85)

            //Alert Function for ADX crossing Threshold
            Up_Cross = crossover(up, threshold)
            alertcondition(Up_Cross, title="DMI+ cross", message="DMI+ Crossing Threshold")
            Down_Cross = crossover(down, threshold)
            alertcondition(Down_Cross, title="DMI- cross", message="DMI- Crossing Threshold")

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        lensig (int): Signal Length. Like TradingView's default ADX. Default: length    
        scalar (float): How much to magnify. Default: 100
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: adx, dmp, dmn columns.
    """
        return description
