window.save_cond_sell = save_cond_sell;
window.save_cond_buy = save_cond_buy;

import { postJsonGetStatus } from "./fetch.js";
import { build_conditions } from "./script.js";

const data = {
  exchange: "binance",
  init_candles: 100,
  symbol: "BTCUSDT",
  name: "test",
  description: "description",
};

export async function save_cond_buy() {
  //indicators
  conditions.push(cond);
  // reset global cond
  cond = [];
  document.querySelectorAll("cond").forEach((condbuy) => {
    condbuy.textContent = `${show_string(cond)}`;
  });
  document.querySelectorAll("saved_conds").forEach((saved_cond) => {
    saved_cond.textContent = `${show_string(conditions)}`;
  });
  data.buy_cond = JSON.stringify(conditions);
  data.side = "buy";
  data.primary_key = selected_cond.get();
  console.log(data.buy_cond);
  let response = await postJsonGetStatus(data, "condition");
  console.log(response);
  let build_conds = await build_conditions();
  document.querySelectorAll("buy_cond2").forEach((bconds) => {
    bconds.textContent = `${build_conds}`;
  });
  console.log(build_conds, "build_conds");
  conditions = [];
  selected_cond.set_string("");
}

export async function save_cond_sell() {
  //indicators
  //cond_sell is global variable
  conditions_sell.push(cond);
  // reset global cond
  cond = [];
  document.querySelectorAll("cond").forEach((cond) => {
    cond.textContent = `${show_string(cond_sell)}`;
  });

  document.querySelectorAll("saved_conds_sell").forEach((saved_cond) => {
    saved_cond.textContent = `${show_string(conditions_sell)}`;
  });
  data.sell_cond = JSON.stringify(conditions_sell);
  data.side = "sell";
  data.primary_key = selected_cond.get();

  let response = await postJsonGetStatus(data, "condition");
  console.log(response);
  let build_conds = await build_conditions();
  document.querySelectorAll("sell_cond2").forEach((sellcond2) => {
    sellcond2.textContent = `${build_conds}`;
  });
  conditions_sell = [];
  console.log(build_conds, "build_conds");
  selected_cond.set_string("");
}
