from flask import g


class StrategyController:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy


def get_strategy_controller():
    if 'strategy_controller' not in g:
        g.strategy_controller = StrategyController()
        print("StrategyController created", g.strategy_controller)
    return g.strategy_controller
