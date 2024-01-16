// import { download_form } from "./download_data";
import { postJsonGetData } from "../fetch.js";

document.addEventListener("DOMContentLoaded", function () {
  download_form();
});

let data = {
  exchange: "binance",
  coin: "ETHUSDT",
};

export function download_form() {
  const d_form = document.querySelector("#download_form");
  console.log(d_form);
  d_form.addEventListener("submit", async function (event) {
    event.preventDefault();
    console.log("hit");
    let response = await postJsonGetData(data, "marketdata");
    console.log(data, response);
  });
}
