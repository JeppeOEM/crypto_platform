import { Chart } from "./Chart.js";
import { BottomChart } from "./BottomChart.js";
import { getJson, postJsonGetData } from "../functions/fetch.js";
// import { createChart, CrosshairMode } from "lightweight-charts";

import { chart_indicators } from "../classes/ChartIndicators.js";
import { chart_settings } from "./get_chart_settings.js";

export async function insert_chart(dataframe_column_names) {
  const chartDiv = document.querySelector(".chart");
  dataframe_column_names = dataframe_column_names.slice(4);
  const MainChart = new Chart(chartDiv, dataframe_column_names);

  const current_strategy = await getJson("get_strategy");

  const coin_pair = current_strategy.pair;
  const market_type = "spot";
  const timeframe = "1m";
  const name = current_strategy.strategy_name;
  const description = current_strategy.info;
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

  MainChart.setData(candlesticks);

  // MainChart.add_indicator_ontop(volume);
  // MainChart.add_line_series(adx);
  // MainChart.add_histogram(volume, 1);

  //remove open,high,close so only cols that need to be inserted in chart remains

  add_all_indicators(MainChart, dataframe_column_names, candlesticks);
}

function add_all_indicators(MainChart, col_names, candlesticks) {
  for (let i = 0; i < col_names.length; i++) {
    let pane_level = i + 1;

    let data = filter_candles(candlesticks, col_names[i]);
    let setting = chart_settings(col_names[i]);
    console.log(setting, "setting");
    if (setting.type === "histogram") {
      MainChart.add_histogram(data, pane_level);
    } else if (setting.type === "line_add_pane") {
      MainChart.add_line_series(data, pane_level);
    }
  }
}
function filter_candles(candlesticks, key) {
  // filter values by key
  return candlesticks.filter((d) => d[`${key}`]).map((d) => ({ time: d.time, value: d[`${key}`] }));
}

//DONT DELETE THIS CODE
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
