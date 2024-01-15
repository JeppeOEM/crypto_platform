import { Chart } from "./chart/Chart";
import { postJsonGetData } from "../../loke/static/js/fetch";

function insert_chart() {
  const chartDiv = document.querySelector(".chart");
  const customChart = new Chart(chartDiv);
  customChart.getCandlesticks("ETH/USD", "1m", "spot");
}
insert_chart();
