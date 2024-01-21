import { Chart } from "./Chart.js";
import { BottomChart } from "./BottomChart.js";
import { getJson, postJsonGetData } from "../functions/fetch.js";
// import { createChart, CrosshairMode } from "lightweight-charts";
import { Histogram } from "./Histogram.js";
export async function insert_chart() {
  const chartDiv = document.querySelector(".chart");
  const MainChart = new Chart(chartDiv);

  let current_strategy = await getJson("get_strategy");
  console.log(current_strategy, "current_strategy!!!!!!!!!!!");
  let coin_pair = current_strategy.pair;
  let market_type = "spot";
  let timeframe = "1m";
  let name = current_strategy.strategy_name;
  let description = current_strategy.info;
  const data_obj = {
    name: name,
    description: description,
    ticker: coin_pair,
    market_type: market_type,
    timeframes: [timeframe],
    timerange_start: 159810060000,
    timerange_end: "now",
  };
  // let candlesticks = await chart.getCandlesticks(data_obj);
  let candlesticks = await postJsonGetData(data_obj, "load_pickled_df");
  candlesticks = JSON.parse(candlesticks);

  function filter_candles(candlesticks, key) {
    return candlesticks.filter((d) => d[`${key}`]).map((d) => ({ time: d.time, value: d[`${key}`] }));
  }
  let indicator_data = filter_candles(candlesticks, "volume");
  let adx = filter_candles(candlesticks, "ADX_14");
  MainChart.setData(candlesticks);
  MainChart.add_indicator_ontop(adx);

  // MainChart.add_indicator_ontop(indicator_data);
  MainChart.add_indicator_ontop(indicator_data);

  // volChart.setData(indicator_data);

  function generateLineData(minValue, maxValue, maxDailyGainLoss = 1000) {
    var res = [];
    var time = new Date(Date.UTC(2018, 0, 1, 0, 0, 0, 0));
    for (var i = 0; i < 500; ++i) {
      var previous = res.length > 0 ? res[res.length - 1] : { value: 0 };
      var newValue = previous.value + (Math.random() * maxDailyGainLoss * 2 - maxDailyGainLoss);

      res.push({
        time: time.getTime() / 1000,
        value: Math.max(minValue, Math.min(maxValue, newValue)),
      });

      time.setUTCDate(time.getUTCDate() + 1);
    }

    return res;
  }

  function generateHistogramData(minValue, maxValue) {
    var res = [];
    var time = new Date(Date.UTC(2018, 0, 1, 0, 0, 0, 0));
    for (var i = 0; i < 500; ++i) {
      res.push({
        time: time.getTime() / 1000,
        value: minValue + Math.random() * (maxValue - minValue),
      });

      time.setUTCDate(time.getUTCDate() + 1);
    }

    return res;
  }

  var chart = LightweightCharts.createChart(document.getElementById("container"), {
    timeScale: {
      borderColor: "rgb(225, 226, 227)",
    },
    overlayPriceScales: {
      scaleMargins: {
        top: 0.6,
        bottom: 0,
      },
    },
    rightPriceScale: {
      autoScale: true,
      scaleMargins: {
        top: 0.1,
        bottom: 0.08,
      },
    },
  });

  var mainSeries = chart.addLineSeries({
    title: "primary",
    priceFormat: {
      minMove: 1,
      precision: 0,
    },
  });

  mainSeries.setData(generateLineData(1000, 300000, 1500));

  var secondSeries = chart.addLineSeries({
    title: "second",
    priceFormat: {
      minMove: 1,
      precision: 0,
    },
    color: "#ff0000",
    pane: 1,
  });
  secondSeries.setData(generateLineData(0, 100, 20));

  var thirdSeries = chart.addLineSeries({
    title: "third",
    priceFormat: {
      minMove: 1,
      precision: 0,
    },
    color: "#00ff00",
    pane: 1,
  });
  thirdSeries.setData(generateLineData(0, 100, 20));

  var fourthSeries = chart.addLineSeries({
    title: "fourth",
    priceFormat: {
      minMove: 1,
      precision: 0,
    },
    color: "#ea6622",
    pane: 2,
  });
  fourthSeries.setData(generateLineData(0, 100, 20));

  var volumeSeries = chart.addHistogramSeries({
    secondary: "volume",
    priceScaleId: "",
    pane: 0,
  });
  volumeSeries.setData(generateHistogramData(100000, 3000000));
}

console.log(LightweightCharts);

// candleseries.setMarkers(
//   klinedata
//     .filter((d) => d.long || d.short)
//     .map((d) =>
//       d.long
//         ? {
//             time: d.time,
//             position: "belowBar",
//             color: "green",
//             shape: "arrowUp",
//             text: "LONG",
//           }
//         : {
//             time: d.time,
//             position: "aboveBar",
//             color: "red",
//             shape: "arrowDown",
//             text: "SHORT",
//           }
//     )
// );
