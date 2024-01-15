import { createChart, CrosshairMode } from "lightweight-charts";
import { urlStringConversion } from "./url_string_conversion.js";
// import { postJsonGetData } from "../../loke/static/js/fetch";

export class Chart {
  constructor(container) {
    this.container = container;
    this.chart = createChart(container, {
      width: 1300,
      height: 500,
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
        borderColor: "rgba(197, 203, 206, 0.8)",
      },
    });
    this.candleSeries = this.chart.addCandlestickSeries({
      upColor: "rgba(255, 144, 0, 1)",
      downColor: "#000",
      borderDownColor: "rgba(255, 144, 0, 1)",
      borderUpColor: "rgba(155, 144, 0, 1)",
      wickDownColor: "rgba(55, 144, 0, 1)",
      wickUpColor: "rgba(255, 144, 0, 1)",
    });
    this.resizeChart();
  }
  setData(data) {
    this.candleSeries.setData(data);
  }

  async getCandlesticks(pair, timeframe, market_type) {
    const apiUrl = `load_pickled_df`;
    let coin_pair = pair.toUpperCase();
    console.log(market_type);

    const data_obj = {
      ticker: coin_pair,
      market_type: market_type,
      timeframes: [timeframe],
      timerange_start: 159810060000,
      timerange_end: "now",
    };
    console.log(data_obj);
    await fetch(apiUrl, {
      method: "POST", // or 'POST' if needed
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data_obj),
    })
      .then((response) => response.json())
      .then((jsonData) => {
        // Handle jsonData as a JSON object
        jsonData = JSON.parse(jsonData);

        // Now you can use jsonData in your frontend code
        // For example, pass it to your Chart class
        this.setData(jsonData);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }

  resizeChart() {
    new ResizeObserver((entries) => {
      if (entries.length === 0 || entries[0].target !== this.container) {
        return;
      }
      const newRect = entries[0].contentRect;
      this.chart.applyOptions({ height: newRect.height, width: newRect.width });
    }).observe(this.container);
  }
}

// Example usage:

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
// const requestOptions = {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify(jsonData),
// };

// try {
//   const response = await fetch(apiUrl, requestOptions);
//   if (!response.ok) {
//     throw new Error(`HTTP error! Status: ${response.status}`);
//   }

//   const data = await response.json();
//   const parsedData = JSON.parse(data);
//   console.log(parsedData);
//   return parsedData;
// } catch (error) {
//   console.error("Fetch error:", error);
// }
export async function postJsonGetData(data, endpoint, method = "POST") {
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  let response = await fetch(endpoint, options);

  if (!response.ok) {
    throw new Error("Request failed");
  }

  const responseData = await response.json();
  return responseData;
}
