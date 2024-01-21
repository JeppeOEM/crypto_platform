// import { createChart, CrosshairMode } from "lightweight-charts";

export class BottomChart {
  constructor(container) {
    this.container = container;
    this.chart = LightweightCharts.createChart(container, {
      layout: {
        textColor: "black",
        background: { type: "solid", color: "white" },
      },
      rightPriceScale: {
        scaleMargins: {
          top: 0.4, // leave some space for the legend
          bottom: 0.15,
        },
      },
      crosshair: {
        // hide the horizontal crosshair line
        horzLine: {
          visible: false,
          labelVisible: false,
        },
      },
      // hide the grid lines
      grid: {
        vertLines: {
          visible: false,
        },
        horzLines: {
          visible: false,
        },
      },
    });
    this.areaSeries = this.chart.addAreaSeries({
      topColor: "#2962FF",
      bottomColor: "rgba(41, 98, 255, 0.28)",
      lineColor: "#2962FF",
      lineWidth: 2,
      crossHairMarkerVisible: false,
    });
  }

  setData(data) {
    this.areaSeries.setData(data);
  }

  getLastBar(series) {
    const lastIndex = series.dataByIndex(Math.Infinity, -1);
    return series.dataByIndex(lastIndex);
  }

  formatPrice(price) {
    return (Math.round(price * 100) / 100).toFixed(2);
  }
  setTooltipHtml(name, date, price) {
    legend.innerHTML = `<div style="font-size: 24px; margin: 4px 0px;">${name}</div><div style="font-size: 22px; margin: 4px 0px;">${price}</div><div>${date}</div>`;
  }

  update(param) {
    this.param = param;
    const updateLegend = (param) => {
      const validCrosshairPoint = !(
        param === undefined ||
        param.time === undefined ||
        param.point.x < 0 ||
        param.point.y < 0
      );
      const bar = validCrosshairPoint ? param.seriesData.get(areaSeries) : getLastBar(areaSeries);
      // time is in the same format that you supplied to the setData method,
      // which in this case is YYYY-MM-DD
      const time = bar.time;
      const price = bar.value !== undefined ? bar.value : bar.close;
      const formattedPrice = formatPrice(price);
      setTooltipHtml(symbolName, time, formattedPrice);
    };
    return updateLegend;
    // this.param = param;
    // const validCrosshairPoint = !(
    //   this.param === undefined ||
    //   this.param.time === undefined ||
    //   this.param.point.x < 0 ||
    //   this.param.point.y < 0
    // );
    // const bar = validCrosshairPoint ? this.param.seriesData.get(areaSeries) : getLastBar(areaSeries);
    // // time is in the same format that you supplied to the setData method,
    // // which in this case is YYYY-MM-DD
    // const time = bar.time;
    // const price = bar.value !== undefined ? bar.value : bar.close;
    // const formattedPrice = this.formatPrice(price);
    // this.setTooltipHtml(symbolName, time, formattedPrice);
  }
}
