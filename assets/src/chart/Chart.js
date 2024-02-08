// import { createChart, CrosshairMode } from "lightweight-charts";
import { urlStringConversion } from "./url_string_conversion.js";
import { getJson } from "../functions/fetch.js";
// import { postJsonGetData } from "../../loke/static/js/fetch";
//https://www.youtube.com/watch?v=NlHjhmIe1EI&t=424s&ab_channel=DeKay

//www.youtube.com/watch?v=NlHjhmIe1EI&t=424s&ab_channel=DeKay
export class Chart {
  constructor(container, dataframe_column_names) {
    // this.dataframe_column_names = dataframe_column_names;
    // this.container = container;
    this.width = 1300;
    this.height = this.add_to_height(dataframe_column_names);
    this.chart = LightweightCharts.createChart(container, {
      width: this.width,
      height: this.height,
      layout: {
        background: {
          type: "solid",
          color: "#000000",
        },
        textColor: "rgba(13, 6, 6, 0.9)", // Set the font color to white
      },
      grid: {
        vertLines: {
          color: "rgba(107, 203, 206, 0.5)",
        },
        horzLines: {
          color: "rgba(197, 203, 206, 0.5)",
        },
      },
      crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
      },
      rightPriceScale: {
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
      timeScale: {
        timeVisible: true,
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
      pane: 0,
    });
    this.candleSeries = this.chart.addCandlestickSeries({
      upColor: "rgba(255, 144, 0, 1)",
      downColor: "#000",
      borderDownColor: "rgba(255, 144, 0, 1)",
      borderUpColor: "rgba(155, 144, 0, 1)",
      wickDownColor: "rgba(55, 144, 0, 1)",
      wickUpColor: "rgba(255, 144, 0, 1)",
    });
    // this.resizeChart();
  }
  setData(data) {
    this.candleSeries.setData(data);
  }

  add_to_height(dataframe_column_names) {
    const hei = dataframe_column_names.length;
    const new_height = 50 * hei;
    return new_height + 500;
  }

  // resizeChart() {
  //   new ResizeObserver((entries) => {
  //     if (entries.length === 0 || entries[0].target !== this.container) {
  //       return;
  //     }
  //     const newRect = entries[0].contentRect;
  //     this.chart.applyOptions({ height: newRect.height, width: newRect.width });
  //   }).observe(this.container);
  // }

  // add_histogram(indicator_data, pane, color1 = "green", color2 = "red") {
  //   const histogram = this.chart.addHistogramSeries({
  //     lineWidth: 2,
  //     pane,
  //   });
  //   histogram.setData(indicator_data);
  // }
  // add_histogram(volume_data, pane) {
  //   const volumeSeries = this.chart.addHistogramSeries({
  //     priceFormat: {
  //       type: "volume",
  //     },
  //     pane,
  //   });
  //   volumeSeries.priceScale().applyOptions({
  //     // set the positioning of the volume series
  //     scaleMargins: {
  //       top: 0.7, // highest point of the series will be 70% away from the top
  //       bottom: 0,
  //     },
  //   });
  //   volumeSeries.setData(volume_data);
  // }

  add_histogram(indicator_data, pane, params = { color: "red", lineWidth: 1 }) {
    // let custom_series = this.chart.addLineSeries(params);
    // custom_series.setData(indicator_data);
    params.pane = pane;
    const line_series = this.chart.addHistogramSeries(params);
    // line_series.priceScale().applyOptions({
    //   // set the positioning of the volume series
    //   scaleMargins: {
    //     top: 0.9, // highest point of the series will be 70% away from the top
    //     bottom: 0,
    //   },
    // });

    line_series.setData(indicator_data);
  }
  add_line_series(indicator_data, pane, params = { color: "red", lineWidth: 1 }) {
    // let custom_series = this.chart.addLineSeries(params);
    // custom_series.setData(indicator_data);
    params.pane = pane;
    const line_series = this.chart.addLineSeries(params);
    // line_series.priceScale().applyOptions({
    //   // set the positioning of the volume series
    //   scaleMargins: {
    //     top: 0.7, // highest point of the series will be 70% away from the top
    //     bottom: 0,
    //   },
    // });

    line_series.setData(indicator_data);
  }

  // add_histogram(volume_data, pane) {
  //   const volumeSeries = this.chart.addHistogramSeries({
  //     priceFormat: {
  //       color: (bar) => (bar.close > bar.open ? "green" : "red"),
  //       type: "volume",
  //     },
  //     pane,
  //   });
  //   volumeSeries.priceScale().applyOptions({
  //     // set the positioning of the volume series
  //     scaleMargins: {
  //       top: 0.7, // highest point of the series will be 70% away from the top
  //       bottom: 0,
  //     },
  //   });
  //   volumeSeries.setData(volume_data);
  // }
}
