import { Chart } from "./Chart.js";
import { BottomChart } from "./BottomChart.js";
import { getJson, postJsonGetData } from "../functions/fetch.js";
import { createChart, CrosshairMode } from "lightweight-charts";
import { Histogram } from "./Histogram.js";
export async function insert_chart() {
  const chartDiv = document.querySelector(".chart");
  const customChart = new Chart(chartDiv);

  const volumeDiv = document.querySelector("#volume_chart");
  const volChart = new Histogram(volumeDiv);

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
  // let candlesticks = await customChart.getCandlesticks(data_obj);
  let candlesticks = await postJsonGetData(data_obj, "load_pickled_df");
  candlesticks = JSON.parse(candlesticks);

  function filter_candles(candlesticks, key) {
    return candlesticks.filter((d) => d[`${key}`]).map((d) => ({ time: d.time, value: d[`${key}`] }));
  }
  let indicator_data = filter_candles(candlesticks, "volume");

  customChart.setData(candlesticks);
  // customChart.add_indicator_ontop(indicator_data);
  customChart.add_volume(indicator_data);

  // volChart.setData(indicator_data);
}
