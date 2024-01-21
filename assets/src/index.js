//Endpoints MUST NOT HAVE / to access URL id
//postIndicatorData(`add_indicator`);
import { selected_cond } from "./classes/globals.js";
import { strategyDataInstance } from "./classes/StrategyData.js";
// import { CondController } from "./cond_list.js";

import { show_string } from "./functions/show_string.js";
import { optimizer_params } from "./strategy_page/optimize.js";
import { postJsonGetData, getJson } from "./functions/fetch.js";
import { postJsonGetStatus } from "./functions/fetch.js";
import { build_strategy_page } from "./strategy_page/build_strategy_page.js";
import { build_optimization_results } from "./strategy_page/build_strategy_page.js";
import { condListController } from "./strategy_page/cond_list.js";
import { load_indicator } from "./strategy_page/load_indicator";
import { build_conds } from "./strategy_page/conditions.js";

window.optimize = optimize;
window.value_cond = value_cond;
window.select_indicator = select_indicator;
window.backtest = backtest;
window.drop_here = drop_here;
window.drop = drop;

const strategyData = strategyDataInstance;
let conditions = [];
let conditions_sell = [];

document.addEventListener("DOMContentLoaded", function () {
  // Your code here
  build_strategy_page().then(() => {
    build_conds();
    build_optimization_results();
  });

  document.querySelector("#testbtn").addEventListener("click", () => {
    console.log(condListController.getKey(29));
  });
});

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

function drop_here(event) {
  const element = event.target.closest(".dropzone");
  console.log(element);
  if (!element.classList.contains("expand_dropzone")) {
    element.classList.add("expand_dropzone");
    console.log("dropzone");
  }
}

function drop(event) {
  console.log("here");
}

// function unpack(cond) {
//   return (
//     cond
//       .flat()
//       // each obj returns as array, with values joined together in a string
//       // there is only 1 val pr array.
//       .map((obj) => Object.values(obj).join("")) //* implicit return *
//       .join(" ")
//   );
// }

// function init_indicators(indicators) {

//   for (let i = 0; i < indicators.length; i ++){

//   }

// }

// export async function save_cond_buy() {
//   //indicators
//   conditions.push(cond);
//   // reset global cond
//   cond = [];
//   document.querySelectorAll("cond").forEach((condbuy) => {
//     condbuy.textContent = `${show_string(cond)}`;
//   });
//   document.querySelectorAll("saved_conds").forEach((saved_cond) => {
//     saved_cond.textContent = `${show_string(conditions)}`;
//   });
//   data.buy_cond = JSON.stringify(conditions);
//   data.side = "buy";
//   data.primary_key = selected_cond.get();
//   console.log(data.buy_cond);
//   let response = await postJsonGetStatus(data, "condition");
//   console.log(response);
//   let build_conds = await build_conditions();
//   document.querySelectorAll("buy_cond2").forEach((bconds) => {
//     bconds.textContent = `${build_conds}`;
//   });
//   console.log(build_conds, "build_conds");
//   conditions = [];
//   selected_cond.set_string("");
// }

// export async function save_cond_sell() {
//   //indicators
//   //cond_sell is global variable
//   conditions_sell.push(cond);
//   // reset global cond
//   cond = [];
//   document.querySelectorAll("cond").forEach((cond) => {
//     cond.textContent = `${show_string(cond_sell)}`;
//   });

//   document.querySelectorAll("saved_conds_sell").forEach((saved_cond) => {
//     saved_cond.textContent = `${show_string(conditions_sell)}`;
//   });
//   data.sell_cond = JSON.stringify(conditions_sell);
//   data.side = "sell";
//   data.primary_key = selected_cond.get();

//   let response = await postJsonGetStatus(data, "condition");
//   console.log(response);
//   let build_conds = await build_conditions();
//   document.querySelectorAll("sell_cond2").forEach((sellcond2) => {
//     sellcond2.textContent = `${build_conds}`;
//   });
//   conditions_sell = [];
//   console.log(build_conds, "build_conds");
//   selected_cond.set_string("");
// }

// ##################################################################################
// ##################################################################################
// ##################################################################################
// ##################################################################################

// async function build_optimization_results() {
//   const data = strategyData.getData();
//   const response = await postJsonGetData(data, "optimization_results");
//   const resultList = document.querySelector(".opti_results");

//   response.forEach((opti) => {
//     let result = JSON.parse(opti.result);
//     for (let i = 0; i < result.length; i++) {
//       // Convert python math Infinity to "Infinity"
//       result[i] = result[i].replace("Infinity", '"Infinity"');
//     }
//     const parsed = result.map((res) => {
//       res = JSON.parse(res);
//       return res;
//     });

//     const listItem = document.createElement("li");
//     listItem.textContent = `PNL: ${parsed[0]["pnl"]}% max drawdown: ${
//       parsed[0]["max_drawdown"]
//     }% params: ${JSON.stringify(parsed[0]["params"])}`;
//     resultList.appendChild(listItem);
//   });
// }

// async function getJson(endpoint) {
//   try {
//     // Make a GET request to the Flask app
//     const response = await fetch(endpoint);

//     // Check if the request was successful
//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }

//     // Parse the JSON in the response
//     const data = await response.json();
//     // Use the JSON data
//     console.log(data);
//     return data;
//   } catch (error) {
//     // Handle errors
//     console.error("Fetch error:", error);
//   }
// }
// async function update_chart(data, endpoint) {
//   try {
//     const response = await fetch(endpoint, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(data),
//     });

//     const responseData = await response.json();

//     return responseData;
//   } catch (error) {
//     console.error("Error:", error);
//   }
// }

// async function postJsonGetStatus(data, endpoint, method = "POST") {
//   // Create an options object for the fetch request
//   const options = {
//     method: method,
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(data),
//   };

//   // Make the POST request using the fetch API
//   let response = await fetch(endpoint, options);

//   if (!response.ok) {
//     throw new Error("Request failed");
//   } else {
//     console.log(response.status);
//     return response;
//   }
// }
// async function createList(side, element) {
//   const newId = await newList(side, element);
//   console.log(newId);
//   condListController.createCondManager(newId);
// }

// function newList(side, element) {
//   const cloneContainer = document.querySelector(`.clone_template`);
//   const append_here = document.querySelector(`${side}_clones`);
//   console.log(cloneContainer, "clone_container");
//   const clone = cloneContainer.cloneNode(true);
//   append_here.appendChild(clone);
//   return newId;
// }

// let test = getJson("/current_df");

// async function build_buttons(array, element_id, element, class_name) {
//   // adds all types of buttons to frontend(also the indicators)
//   document.querySelectorAll(`.${element_id}`).forEach((container) => {
//     for (let i = 0; i < array.length; i++) {
//       let button = document.createElement(element);
//       button.innerText = array[i];
//       button.classList.add(class_name);
//       button.classList.add("smallbtn");
//       container.appendChild(button);
//     }

//     // dataframe column buttons functionality
//     const buttons = container.querySelectorAll(`.${class_name}`);
//     buttons.forEach(function (button) {
//       button.addEventListener("click", function (event) {
//         let text = event.target.innerText;
//         //USES GLOBAL COND ARRAY
//         if (class_name == "indicator_cond") {
//           // cond.push({ ind: event.target.innerText });
//           selected_cond.add_cond({ ind: event.target.innerText });
//         } else {
//           selected_cond.add_cond({ cond: event.target.innerText });
//           // cond.push({ cond: event.target.innerText });
//         }
//         //UPDATES THE CURRENT UNSAVED CONDITION STRING
//         document.querySelectorAll(".cond").forEach((cond_string) => {
//           // cond_string.textContent = `${show_string(cond)}`;
//           cond_string.textContent = `${show_string(selected_cond.get_cond())}`;
//         });
//       });
//     });
//   });
// }
// function insert_frontend(cond, element) {
//   const conds_db = document.querySelectorAll(`.${element}`).forEach((saved_conds) => {
//     for (let i = 0; i < cond.length; i++) {
//       const listItem = document.createElement("li");

//       listItem.textContent = unpack(JSON.parse(cond[i]));
//       saved_conds.appendChild(listItem);
//     }
//   });
// }
