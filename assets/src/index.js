import { Chart } from "./chart/Chart";
import { getJson } from "../../loke/static/js/fetch";

async function insert_chart() {
  const chartDiv = document.querySelector(".chart");
  const customChart = new Chart(chartDiv);

  const response = await getJson("current_chart");
  console.log(response, "fuckinging response");
  customChart.getCandlesticks("BTC/USD", "1m", "spot");
}
insert_chart();
