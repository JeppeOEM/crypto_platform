import { Chart } from "./chart/Chart";

const chartDiv = document.querySelector(".chart");
const customChart = new Chart(chartDiv);
const chartData = await customChart.getCandlesticks("BTC/USD", "1h");
customChart.setData(chartData.chart_data);
