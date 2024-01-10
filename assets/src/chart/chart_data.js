import { createChart, ColorType, CrosshairMode } from "lightweight-charts";
import React, { useState, useEffect, useRef } from "react";
import { urlStringConversion } from "./urlStringConversion";
import s from "./ticker.module.css";

const Chart = ({ chart_data }) => {
  const [chartData, setChartData] = useState([]);
  const chartRef = useRef();

  useEffect(() => {
    var chart = createChart(chartRef.current, {
      width: 600,
      height: 300,
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
        // secondsVisible: false,
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
    });

    var candleSeries = chart.addCandlestickSeries({
      upColor: "rgba(255, 144, 0, 1)",
      downColor: "#000",
      borderDownColor: "rgba(255, 144, 0, 1)",
      borderUpColor: "rgba(155, 144, 0, 1)",
      wickDownColor: "rgba(55, 144, 0, 1)",
      wickUpColor: "rgba(255, 144, 0, 1)",
    });

    // candleSeries.setData([
    //   { time: Date.parse("2019-04-11 09:43"), open: 107.2, high: 207.3, low: 207.1, close: 207.1 },
    //   { time: Date.parse("2019-04-11 12:43"), open: 407.2, high: 207.3, low: 207.1, close: 207.1 },
    //   { time: Date.parse("2019-04-11 13:43"), open: 307.2, high: 407.3, low: 207.1, close: 207.1 },
    //   { time: Date.parse("2019-04-11 14:43"), open: 107.2, high: 207.3, low: 207.1, close: 207.1 },
    // ]);
    candleSeries.setData(chart_data);
  }, []);

  return (
    <div className='chart-container'>
      <h2>Interactive 5 Years Historical Daily Chart</h2>
      <div ref={chartRef} />
    </div>
  );
};
export default Chart;

export async function getServerSideProps(context) {
  //const ticker = context.params.ticker;
  const query = context.query;
  console.log(query);
  const apiUrl = `http://127.0.0.1:8000/loaddfs/`;
  const { market_type, pair } = urlStringConversion(query.ticker);
  let pair2 = pair;
  pair2 = pair2.toUpperCase();
  const jsonData = {
    ticker: pair2,
    market_type: market_type,
    timeframes: [query.timeframe],
    timerange_start: 159810060000,
    timerange_end: "now",
  };
  let chart_data;
  const requestOptions = {
    method: "POST", // You can use 'GET', 'POST', 'PUT', 'DELETE', etc.
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
  };

  chart_data = await fetch(apiUrl, requestOptions)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      data = JSON.parse(data);
      console.log(data);
      return data;
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });

  let lol = "lol";
  return {
    props: { chart_data },
  };
}

// function nextBusinessDay(time) {
//   var d = new Date();
//   d.setUTCFullYear(time.year);
//   d.setUTCMonth(time.month - 1);
//   d.setUTCDate(time.day + 1);
//   d.setUTCHours(0, 0, 0, 0);
//   return {
//     year: d.getUTCFullYear(),
//     month: d.getUTCMonth() + 1,
//     day: d.getUTCDate(),
//   };
// }
// setInterval(function () {
//   var deltaY = targetPrice - lastClose;
//   var deltaX = targetIndex - lastIndex;
//   var angle = deltaY / deltaX;
//   var basePrice = lastClose + (currentIndex - lastIndex) * angle;
//   var noise = 0.1 - Math.random() * 0.1 + 1.0;
//   var noisedPrice = basePrice * noise;
//   mergeTickToBar(noisedPrice);
//   if (++ticksInCurrentBar === 5) {
//     // move to next bar
//     currentIndex++;
//     currentBusinessDay = nextBusinessDay(currentBusinessDay);
//     currentBar = {
//       open: null,
//       high: null,
//       low: null,
//       close: null,
//       time: currentBusinessDay,
//     };
//     ticksInCurrentBar = 0;
//     if (currentIndex === 5000) {
//       reset();
//       return;
//     }
//     if (currentIndex === targetIndex) {
//       // change trend
//       lastClose = noisedPrice;
//       lastIndex = currentIndex;
//       targetIndex = lastIndex + 5 + Math.round(Math.random() + 30);
//       targetPrice = getRandomPrice();
//     }
//   }
// }, 200);
