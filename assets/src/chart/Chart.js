import { createChart, CrosshairMode } from "lightweight-charts";
import { urlStringConversion } from "./url_string_conversion.js";
import { getJson } from "../functions/fetch.js";
// import { postJsonGetData } from "../../loke/static/js/fetch";

export class Chart {
  constructor(container) {
    this.container = container;
    this.chart = createChart(container, {
      width: 1300,
      height: 500,
      layout: {
        background: {
          type: "solid",
          color: "#000000",
        },
        textColor: "rgba(255, 255, 255, 0.9)",
      },
      grid: {
        vertLines: {
          color: "rgba(197, 203, 206, 0.5)",
        },
        horzLines: {
          color: "rgba(197, 203, 206, 0.5)",
        },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
      },
      rightPriceScale: {
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
      timeScale: {
        timeVisible: true,
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
    });
    this.candleSeries = this.chart.addCandlestickSeries({
      upColor: "rgba(255, 144, 0, 1)",
      downColor: "#000",
      borderDownColor: "rgba(255, 144, 0, 1)",
      borderUpColor: "rgba(155, 144, 0, 1)",
      wickDownColor: "rgba(55, 144, 0, 1)",
      wickUpColor: "rgba(255, 144, 0, 1)",
    });
    this.resizeChart();
  }
  setData(data) {
    this.candleSeries.setData(data);
  }

  resizeChart() {
    new ResizeObserver((entries) => {
      if (entries.length === 0 || entries[0].target !== this.container) {
        return;
      }
      const newRect = entries[0].contentRect;
      this.chart.applyOptions({ height: newRect.height, width: newRect.width });
    }).observe(this.container);
  }

  add_histogram(indicator_data, color1 = "green", color2 = "red") {
    const histogram = this.chart.addHistogramSeries({
      color: (bar) => (bar.close > bar.open ? color1 : color2),
      lineWidth: 2,
    });
    histogram.setData(indicator_data);
  }

  add_indicator_ontop(indicator_data, params = { color: "red", lineWidth: 1 }) {
    let custom_series = this.chart.addLineSeries(params);
    custom_series.setData(indicator_data);
  }

  add_volume(volume_data) {
    const volumeSeries = this.chart.addHistogramSeries({
      priceFormat: {
        type: "volume",
      },
      priceScaleId: "", // set as an overlay by setting a blank priceScaleId
    });
    volumeSeries.priceScale().applyOptions({
      // set the positioning of the volume series
      scaleMargins: {
        top: 0.7, // highest point of the series will be 70% away from the top
        bottom: 0,
      },
    });
    volumeSeries.setData(volume_data);
  }
}
