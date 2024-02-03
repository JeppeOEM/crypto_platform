class ChartIndicators {
  constructor() {
    this.indicators = [];
  }

  add(indicator) {
    this.indicators.push(indicator);
  }

  get() {
    return this.indicators;
  }
}

const chart_indicators = new ChartIndicators();
export { chart_indicators };