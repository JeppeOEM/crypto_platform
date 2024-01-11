class StrategyController:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy
