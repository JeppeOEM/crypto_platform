class StrategyData {
  constructor() {
    this._exchange = "binance";
    this._name = "test";
    this._description = "description";
    this._init_candles = 100;
  }

  getExchange() {
    return this._exchange;
  }

  setExchange(value) {
    this._exchange = value;
  }

  setName(value) {
    this._name = value;
  }
  getName() {
    return this._name;
  }
  setDescription(value) {
    this._description = value;
  }
  getDescription() {
    return this._description;
  }
  setInitCandles(value) {
    this._init_candles = value;
  }
  getInitCandles() {
    return this._init_candles;
  }

  getDataObject() {
    return {
      exchange: this._exchange,
      pair: this._pair,
      name: this._name,
      description: this._description,
      init_candles: this._init_candles,
    };
  }
}
const strategyDataInstance = new StrategyData();

export { strategyDataInstance };

// const data = {
//   exchange: "binance",
//   init_candles: 100,
//   symbol: "BTCUSDT",
//   name: "test",
//   description: "description",
// };
