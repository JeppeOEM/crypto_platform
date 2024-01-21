import { createChart, CrosshairMode } from "lightweight-charts";
import { urlStringConversion } from "./url_string_conversion.js";
import { getJson } from "../functions/fetch.js";
// import { postJsonGetData } from "../../loke/static/js/fetch";

export class Histogram {
  constructor(container) {
    this.container = container;
    this.chart = createChart(container, {
      width: 1300,
      height: 500,
      layout: { textColor: "black", background: { type: "solid", color: "white" } },
    });
    this.histogramSeries = this.chart.addHistogramSeries({ color: "#26a69a" });
  }
  setData(data) {
    this.histogramSeries.setData(data);
    this.chart.timeScale().fitContent();
  }
}
