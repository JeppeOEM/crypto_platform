import { Chart } from "./Chart.js";
import { getJson } from "../functions/fetch.js";

export async function insert_chart() {
  const chartDiv = document.querySelector(".chart");
  const customChart = new Chart(chartDiv);

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
  customChart.getCandlesticks(data_obj);
}
