//Endpoints MUST NOT HAVE / to access URL id
//postIndicatorData(`add_indicator`);
import { selected_cond_instance } from "./classes/globals.js";
// import { CondController } from "./cond_list.js";
import { condController } from "./cond_list.js";
import { show_string } from "./functions/show_string.js";
import { getJson } from "./fetch.js";
import { postJsonGetData } from "./fetch.js";
import { postJsonGetStatus } from "./fetch.js";
import { build_conds } from "./conditions.js";
window.optimize = optimize;
window.value_cond = value_cond;

window.select_indicator = select_indicator;

// window.save_cond_sell = save_cond_sell;
// window.save_cond_buy = save_cond_buy;

const selected_cond = selected_cond_instance;

// const condController = condController;

const data = {
  exchange: "binance",
  init_candles: 100,
  symbol: "BTCUSDT",
  name: "test",
  description: "description",
};

let conditions = [];
let conditions_sell = [];
let cond = [];
let cond_sell = [];

document.addEventListener("DOMContentLoaded", function () {
  // Your code here
  build_page();
  let todo_b = document.querySelector("#new_todo_buy");

  todo_b.addEventListener("click", () => {
    create_list("buy");
    location.reload();
    // remove_element("cond_list");
    // build_condition_lists();
  });

  let todo_s = document.querySelector("#new_todo_sell");

  todo_s.addEventListener("click", () => {
    create_list("sell");
    location.reload();
    // remove_element("cond_list");
    // build_condition_lists();
  });
});

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

async function create_list(side) {
  const status = postJsonGetStatus(data, "cond_list?side=" + side);
  // remove_element("cond_list");
  // build_condition_lists();
}

async function build_page() {
  // init strategy gets the indicators saved in indicator_strategies
  const strategy_data = await update_chart("init_strategy");
  console.log(strategy_data, "strategy_data!!!!!!!!!!!!!!!!!!!!!");
  remove_element("indicator_cond");
  build_buttons(strategy_data.cols, "condition_btns", "button", "indicator_cond");
  remove_element("buy_cond2");
  remove_element("sell_cond2");
  //build buttons also build indicator strategy_dataframe related buttons
  //params: array, element_id, element, class_name

  console.log(strategy_data, "strategy_data.indicators");
  build_indicator_inputs(strategy_data.indicators);
  // await build_conditions();
  build_optimization_results();
  build_condition_lists();
  build_buttons(["<", ">", "==", "&", "or"], "compare_btns", "button", "compare_cond");
  build_buttons(["or", "&"], "or_and_btns", "button", "or_and_cond");
  build_buttons(strategy_data.cols, "condition_btns", "button", "indicator_cond");
  build_conds();
}

//
async function build_condition_lists() {
  // const taskManager1 = condController.createCondManager("buy_cond_list1");
  // const taskManager2 = condController.createCondManager("sell_cond_list2");
  const json_buy = await getJson("cond_list?side=buy");
  const json_sell = await getJson("cond_list?side=sell");
  console.log(json_buy, json_sell, "lists");
  const sell_clones = document.querySelector(".sell_clones");
  const buy_clones = document.querySelector(".buy_clones");
  const clone_template = document.querySelector(".clone_template");
  await clone_list(json_buy, buy_clones, "buy");
  await clone_list(json_sell, sell_clones, "sell");

  async function clone_list(json, container, side) {
    let primary_key;
    json.forEach((data) => {
      let element_name = `${side}_cond_list_${data.frontend_id}`;
      const clone = clone_template.content.cloneNode(true);
      let insert_name = clone.querySelector(".single_list");
      let cond_modal = clone.querySelector(".currentTask");
      cond_modal.dataset.side = "buy";
      insert_name.classList.add(element_name);
      insert_name.classList.add(`${side}_side`);
      if (side == "buy") {
        insert_name.dataset.primary_key = data.list_id;
        primary_key = data.list_id;
        console.log(data.list_id, "data.list_id");
      } else {
        insert_name.dataset.primary_key = data.list_id;
        primary_key = data.list_id;
      }
      console.log(primary_key, "primary_key");
      insert_name.dataset.frontend_id = data.frontend_id;
      // const cond_wrapper = clone.querySelector(`.clone_${side}`);
      // cond_wrapper.dataset.id = data.list_id;
      container.appendChild(clone);
      //cond_list.js controller
      condController.createCondManager(element_name, primary_key);
    });
  }
}

async function build_buttons(array, element_id, element, class_name) {
  // adds all types of buttons to frontend(also the indicators)
  document.querySelectorAll(`.${element_id}`).forEach((container) => {
    for (let i = 0; i < array.length; i++) {
      let button = document.createElement(element);
      button.innerText = array[i];
      button.classList.add(class_name);
      button.classList.add("smallbtn");
      container.appendChild(button);
    }

    // dataframe column buttons functionality
    const buttons = container.querySelectorAll(`.${class_name}`);
    buttons.forEach(function (button) {
      button.addEventListener("click", function (event) {
        let text = event.target.innerText;
        //USES GLOBAL COND ARRAY
        if (class_name == "indicator_cond") {
          // cond.push({ ind: event.target.innerText });
          selected_cond.add_cond({ ind: event.target.innerText });
          console.log(cond);
        } else {
          selected_cond.add_cond({ cond: event.target.innerText });
          // cond.push({ cond: event.target.innerText });
        }
        //UPDATES THE CURRENT UNSAVED CONDITION STRING
        document.querySelectorAll(".cond").forEach((cond_string) => {
          // cond_string.textContent = `${show_string(cond)}`;
          cond_string.textContent = `${show_string(selected_cond.get_cond())}`;
        });
      });
    });
  });
}

function insert_frontend(cond, element) {
  const conds_db = document.querySelectorAll(`.${element}`).forEach((saved_conds) => {
    console.log(saved_conds, element, "saved_conds");
    for (let i = 0; i < cond.length; i++) {
      const listItem = document.createElement("li");

      listItem.textContent = unpack(JSON.parse(cond[i]));
      saved_conds.appendChild(listItem);
      console.log(saved_conds, "saved_conds!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    }
  });
}

//runs if there is saved indicators in the db that belongs to the strategy
async function build_indicator_inputs(data, category = null) {
  //returns new array with parsed values
  let indicators = data.map((indicator) => {
    let id = JSON.parse(indicator.id);
    let category = indicator.category;
    indicator = JSON.parse(indicator.settings);
    //convert to numeric values
    for (let key in indicator) {
      if (indicator.hasOwnProperty(key)) {
        if (key === "talib") {
          continue;
        }
        if (key === "offset") {
          indicator[key] = parseInt(indicator[key]);
        } else if (key != "kind") {
          indicator[key] = parseFloat(indicator[key]);
        }
      }
    }

    return { id, indicator, category };
  });

  load();

  async function load() {
    for (let i = 0; i < indicators.length; i++) {
      const form = await loadIndicator(
        indicators[i].indicator["kind"],
        indicators[i].category,
        indicators[i].indicator, //values
        indicators[i].id
      );
    }
  }
}

async function loadIndicator(name, category, values = undefined, form_id) {
  // Create a new input field element
  const data = {
    indicator: name,
    category: category,
  };
  let output = [];
  const strat_id = document.getElementById("strategy_id");
  const id = strat_id.dataset.info;
  let indi_data = await postIndicatorData(`add_indicator`);
  //gets values saved in indicator_strategies otherwise default values from Indicator Classes
  if (values) {
    for (const key in values) {
      if (values.hasOwnProperty(key)) {
        const value = values[key];
        if (typeof value === "number") {
          output.push([key, "float", value]);
        }
        if (typeof value === "string") {
          output.push([key, value]);
        }
      }
    }
    indi_data = output;
  }
  const name_indicator = indi_data[0][1];
  console.log(name_indicator, "name_indicator");
  //remove name of indicator
  indi_data = indi_data.slice(1);
  const formContainer = document.getElementById("form-container");
  const form = document.createElement("form");
  const delbtn = document.createElement("button");
  delbtn.innerText = "X";
  delbtn.classList = "smallbtn_blue mr5";
  form.classList.add("indicator_form");
  form.id = `form${form_id}`;
  form.classList.add("flex_horizontal");
  form.dataset.category = category;
  let field = document.createElement("fieldset");
  const legend = document.createElement("span");
  legend.textContent = name_indicator;
  formContainer.appendChild(form);
  form.appendChild(delbtn);
  form.appendChild(field);
  field.appendChild(legend);

  form.addEventListener("submit", submit_to_db);
  // get values in the form submitted
  for (let i = 0; i < indi_data.length; i++) {
    //name type value forexample: lenght, float, 14, html element
    input_params(indi_data[i][0], indi_data[i][1], indi_data[i][2], field);
  }

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.classList = "smallbtn ml10";
  submitButton.innerText = "Submit";
  field.appendChild(submitButton);

  //build input fields of indicator on click
  async function submit_to_db(event) {
    event.preventDefault();
    // remove "form" and get id
    let form_id = this.id;
    form_id = form_id.slice(4);
    // let formdata = event.currentTarget.customParam;
    const formData = new FormData(form);
    let form_arr = [["kind", legend.innerText]];
    formData.forEach((value, key) => {
      form_arr.push([key, value]);
    });
    form_arr.push(form_id);
    form_arr.unshift(event.target.dataset.category);
    console.log(form_arr);
    //strategy_id = document.querySelector("#strategy_id");
    await postJsonGetStatus(form_arr, `convert_indicator`);

    let indicators_data = await update_chart("init_strategy");
    console.log(indicators_data, "indicators_data!!!!!!!!!!!!!!!!!!!!");
    remove_element("indicator_cond");
    build_buttons(indicators_data.cols, "condition_btns", "button", "indicator_cond");
    remove_element("indicator_form");
    build_indicator_inputs(indicators_data.indicators, category);
  }

  // var container = document.getElementById("input-container");
  async function postIndicatorData(endpoint, method = "POST") {
    // Create an options object for the fetch request
    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };

    // Make the POST request using the fetch API
    let response = await fetch(endpoint, options);

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const responseData = await response.json();
    return responseData;
  }
}

function select_indicator(category, id) {
  console.log(category, id);
  const dropdown = document.getElementById(id);
  const selectedValue = dropdown.value;

  // Call the loadIndicator function with the selected value
  loadIndicator(selectedValue, category);
}

async function input_params(key, type, value, field) {
  if (value != "bool") {
    const label = document.createElement("label");
    label.innerText = key;
    const input = document.createElement("input");
    input.type = "text";
    input.name = key;
    input.value = value;
    field.appendChild(label);
    field.appendChild(input);
  } else {
    const label2 = document.createElement("label");
    label2.innerText = key;
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = key;
    // checkbox.value = value;
    checkbox.value = false;
    field.appendChild(label2);
    field.appendChild(checkbox);
  }
}

// function init_indicators(indicators) {

//   for (let i = 0; i < indicators.length; i ++){

//   }

// }

function remove_element(class_name) {
  let elements = document.querySelectorAll(`.${class_name}`);

  elements.forEach(function (ele) {
    ele.parentNode.removeChild(ele);
  });
}

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

async function optimize() {
  const response = await postJsonGetData(data, "optimize");
  console.log(response);
}

async function build_optimization_results() {
  const response = await postJsonGetData(data, "optimization_results");
  const resultList = document.querySelector(".opti_results");

  response.forEach((opti) => {
    let result = JSON.parse(opti.result);
    for (let i = 0; i < result.length; i++) {
      // Convert python math Infinity to "Infinity"
      result[i] = result[i].replace("Infinity", '"Infinity"');
    }
    const parsed = result.map((res) => {
      res = JSON.parse(res);
      return res;
    });
    console.log(parsed, "parsedddd");
    const listItem = document.createElement("li");
    listItem.textContent = `PNL: ${parsed[0]["pnl"]}% max drawdown: ${
      parsed[0]["max_drawdown"]
    }% params: ${JSON.stringify(parsed[0]["params"])}`;
    resultList.appendChild(listItem);
  });
}

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
async function update_chart(endpoint) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const responseData = await response.json();

    return responseData;
  } catch (error) {
    console.error("Error:", error);
  }
}

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
//   condController.createCondManager(newId);
// }

// function newList(side, element) {
//   const cloneContainer = document.querySelector(`.clone_template`);
//   const append_here = document.querySelector(`${side}_clones`);
//   console.log(cloneContainer, "clone_container");
//   const clone = cloneContainer.cloneNode(true);
//   append_here.appendChild(clone);
//   return newId;
// }
function unpack(cond) {
  return (
    cond
      .flat()
      // each obj returns as array, with values joined together in a string
      // there is only 1 val pr array.
      .map((obj) => Object.values(obj).join("")) //* implicit return *
      .join(" ")
  );
}

function which_side(inputString) {
  let str = inputString.toUpperCase().includes("BUY");
  let side;
  if (str) {
    side = "BUY";
  } else {
    side = "SELL";
  }

  return side;
}
let test = getJson("/current_df");
console.log(test, "test");
