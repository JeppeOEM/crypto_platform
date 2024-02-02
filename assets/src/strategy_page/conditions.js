import { selected_cond } from "../classes/globals.js";
import { last_cond_dom } from "../classes/globals.js";
import { postJsonGetData } from "../functions/fetch.js";
import { getJson } from "../functions/fetch.js";
import { remove_element } from "../functions/remove_element.js";
import { show_string } from "../functions/show_string.js";
import { condListController } from "./cond_list.js";
import { optimizer_params } from "./optimize.js";

// const condListController = condListController
window.save_cond_sell = save_cond_sell;
window.save_cond_buy = save_cond_buy;
window.del_last_buy_cond = del_last_buy_cond;
window.del_last_sell_cond = del_last_sell_cond;
window.del_last = del_last;

let conditions = [];
let conditions_sell = [];
// let cond = [];
const data = {
  exchange: "binance",
  init_candles: 100,
  symbol: "BTCUSDT",
  name: "test",
  description: "description",
};

function which_row_string(string) {
  switch (string) {
    case "toDo":
      return 1;
    case "onGoing":
      return 2;
    case "done":
      return 3;
  }
}

export async function remove_conds() {}

export async function build_conds() {
  const json = await getJson("load_conditions");

  const buy_conds = json.buy_conds;
  const sell_conds = json.sell_conds;
  optimizer_params(buy_conds, "_BUY");
  optimizer_params(sell_conds, "_SELL");
  remove_element("single_condition");
  load_cond_managers(buy_conds, "buy");
  load_cond_managers(sell_conds, "sell");
  function load_cond_managers(arr, side) {
    for (let i = 0; i < arr.length; i++) {

      //CODE FAILS HERE
      let condManager = condListController.getKey(arr[i].fk_list_id);
      //text, column, id, side;
      condManager.insert_cond(arr[i].indicator_json, which_row(arr[i].list_row), arr[i].condition_id, side);
    }
  }
}
function which_row(number) {
  switch (number) {
    case 1:
      return "toDo";
    case 2:
      return "ongoing";
    case 3:
      return "done";
  }
}

export async function save_cond_buy() {
  //indicators
  conditions.push(selected_cond.get_cond());
  // reset global cond
  selected_cond.set_string();
  selected_cond.reset_cond();
  // cond = [];
  document.querySelectorAll("cond").forEach((condbuy) => {
    condbuy.textContent = `${show_string(cond)}`;
  });
  document.querySelectorAll("saved_conds").forEach((saved_cond) => {
    saved_cond.textContent = `${show_string(conditions)}`;
  });
  data.buy_cond = JSON.stringify(conditions);

  data.side = "buy";
  data.primary_key = selected_cond.get();
  let response = await postJsonGetData(data, "condition");
  //assign id to last cond inserted in the dom
  let last_dom = last_cond_dom.get();
  last_dom.dataset.cond_key = response.id;
  last_cond_dom.set(last_dom);

  // const json = await getJson("load_conditions");
  // const buy_conds = json.buy_conds;

  // optimizer_params(buy_conds, "_BUY", "param_buy");

  conditions = [];
}

export async function save_cond_sell() {
  conditions_sell.push(selected_cond.get_cond());
  // reset global cond
  selected_cond.set_string();
  selected_cond.reset_cond();
  document.querySelectorAll("cond").forEach((cond) => {
    cond.textContent = `${show_string(cond_sell)}`;
  });

  document.querySelectorAll("saved_conds_sell").forEach((saved_cond) => {
    saved_cond.textContent = `${show_string(conditions_sell)}`;
  });
  data.sell_cond = JSON.stringify(conditions_sell);
  data.side = "sell";
  //get primary key of the current list
  data.primary_key = selected_cond.get();

  let response = await postJsonGetData(data, "condition");

  //assign id to last condition inserted in the dom
  let last_dom = last_cond_dom.get();
  last_dom.dataset.cond_key = response.id;
  last_cond_dom.set(last_dom);

  // const json = await getJson("load_conditions");
  // const sell_conds = json.sell_conds;

  // optimizer_params(sell_conds, "_SELL", "sell");
  // optimizer_params(sell_conds, "_SELL", "param_sell");

  conditions_sell = [];

  selected_cond.reset_cond();
}

function del_last() {
  selected_cond.del_last();
  document.querySelectorAll(".cond").forEach((unsaved_cond) => {
    unsaved_cond.textContent = `${show_string(cond)}`;
  });
  selected_cond.set_string(show_string(cond));
}

function del_last_sell_cond() {
  conditions_sell.pop();
  document.querySelectorAll("conditions_sell").forEach((cond_sell) => {
    cond_sell.textContent = `${show_string(cond_sell)}`;
  });
  selected_cond.set_string(show_string(cond));
}

function del_last_buy_cond() {
  conditions.pop();
  document.querySelectorAll("conditions").forEach((cond) => {
    cond.textContent = `${show_string(cond)}`;
  });
  selected_cond.set_string(show_string(cond));
}
