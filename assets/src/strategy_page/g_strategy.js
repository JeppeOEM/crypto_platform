import { load_indicator } from "./load_indicator";
import { strategyDataInstance } from "../classes/StrategyData.js";
const strategyData = strategyDataInstance;

window.optimize = optimize;
window.value_cond = value_cond;
window.select_indicator = select_indicator;
window.backtest = backtest;

async function backtest() {
  // let conditions_copy = [[{ ind: "AO_14_14" }, { cond: ">" }, { val: 50 }]];
  // let conditions_sell_copy = [[{ ind: "AO_14_14" }, { cond: "<" }, { val: 11 }]];
  let conditions_copy = conditions;
  let conditions_sell_copy = conditions_sell;

  data.conds_buy = conditions_copy;
  data.conds_sell = conditions_sell_copy;
  console.log(data.conds_buy);
  console.log(data.conds_sell);

  let response = await postJsonGetData(data, "backtest");
  document.getElementById("cond").textContent = JSON.stringify(response.message);
}

function value_cond(btn) {
  const parentDiv = btn.parentElement;
  const inputElement = parentDiv.querySelector(".value_cond");
  var value = inputElement.value;
  // cond.push({ val: parseFloat(value) });
  selected_cond.add_cond({ val: parseFloat(value) });
  // Assuming you have an element with class 'unsaved_cond'

  document.querySelectorAll(".cond").forEach((cond_string) => {
    // cond_string.textContent = `${show_string(cond)}`;
    cond_string.textContent = `${show_string(selected_cond.get_cond())}`;
  });
}

function select_indicator(category, id) {
  const dropdown = document.getElementById(id);
  const selectedValue = dropdown.value;

  // Call the load_indicator function with the selected value
  load_indicator(selectedValue, category);
}

async function optimize() {
  const data = strategyData.getData();
  const response = await postJsonGetData(data, "optimize");
}
