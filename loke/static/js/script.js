//Endpoints MUST NOT HAVE / to access URL id
//postIndicatorData(`add_indicator`);

class Field {
  constructor(field) {
    this.setField(field);
  }
  getField() {
    return this.field;
  }
  setField(newfield) {
    this.field = newfield;
  }
  addToField(element) {
    this.field.appendChild(element);
  }
}

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
});

async function build_page() {
  indicators_data = await update_chart("init_strategy");
  remove_element("buy_cond2");
  remove_element("sell_cond2");
  build_buttons(["<", ">", "==", "&", "or"], "compare", "button", "compare_cond");
  build_indicator_inputs(indicators_data.indicators);
  build_buttons(["or", "&"], "or_and", "button", "or_and_cond");
  build_conditions();
  build_optimization_results();
}

async function build_conditions() {
  const { sell_conds, buy_conds } = await getJson("load_conditions");

  remove_element("buy_cond2");
  remove_element("sell_cond2");
  insert_frontend(sell_conds, "sell_cond2");
  insert_frontend(buy_conds, "buy_cond2");
  optimizer_params(sell_conds, "_SELL");
  optimizer_params(buy_conds, "_BUY");
  function insert_frontend(cond, element) {
    // Reference to the ul element
    const myList = document.getElementById(element);

    // Loop through the array and insert list items
    for (let i = 0; i < cond.length; i++) {
      const listItem = document.createElement("li");
      listItem.textContent = cond[i];
      myList.appendChild(listItem);
    }
  }
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
function load_params() {
  let arr = [];
  rows = document.querySelectorAll(".param");
  rows.forEach((row) => {
    let indi = row.querySelector(".indicator");
    side = which_side(indi.innerText);
    let operator = row.querySelector(".operator");
    let min = row.querySelector(".min");
    let max = row.querySelector(".max");
    let type = "int";

    arr.push([indi.innerText, operator.innerText, type, min.value, max.value, side]);
  });
  data.optimizer_params = arr;
  data.params_class = "indicator";

  postJsonGetStatus(data, "optimizer_params");
}

function optimizer_params(sell_conds, suffix) {
  const title = document.querySelector("title");
  s_conds = [];
  sell_conds.forEach((cond) => {
    cond = JSON.parse(cond);
    s_conds.push(cond);
  });

  const tbody = document.querySelector("tbody");
  const opti_params = document.getElementById("optimize_params");
  s_conds.forEach((cond) => {
    cond.forEach((val) => {
      const clone = opti_params.content.cloneNode(true);
      clone.querySelector(".indicator").textContent = val[0]["ind"] + suffix;
      clone.querySelector(".operator").textContent = val[1]["cond"];
      clone.querySelector(".min").value = "1";
      clone.querySelector(".max").value = "1";
      tbody.appendChild(clone);
    });
  });
}

async function build_indicator_inputs(data) {
  //returns new array with parsed values
  indicators = data.map((indicator) => {
    let id = JSON.parse(indicator.id);
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

    return { id, indicator };
  });

  for (let i = 0; i < indicators.length; i++) {
    const form = await loadIndicator(
      indicators[i].indicator["kind"],
      "momentum",
      indicators[i].indicator,
      indicators[i].id
    );
    // form.submit();
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
  //remove name of indicator
  indi_data = indi_data.slice(1);
  const formContainer = document.getElementById("form-container");
  const form = document.createElement("form");
  form.classList.add("indicator_form");
  form.id = `form${form_id}`;
  let field = document.createElement("fieldset");
  const legend = document.createElement("legend");
  legend.textContent = name_indicator;
  formContainer.appendChild(form);
  form.appendChild(field);
  field.appendChild(legend);

  form.addEventListener("submit", gogo);
  //form.customParam = form;
  for (let i = 0; i < indi_data.length; i++) {
    //name type value forexample: lenght float 14
    input_params(indi_data[i][0], indi_data[i][1], indi_data[i][2], field);
  }

  const submitButton = document.createElement("input");
  submitButton.type = "submit";
  submitButton.id = "submitIndicator";
  submitButton.value = "Submit";
  field.appendChild(submitButton);

  async function gogo(event) {
    event.preventDefault();
    // remove "form" and get id
    let form_id = this.id;
    form_id = form_id.slice(4);
    // let formdata = event.currentTarget.customParam;
    const formData = new FormData(form);
    form_arr = [["kind", legend.innerText]];
    formData.forEach((value, key) => {
      form_arr.push([key, value]);
    });
    form_arr.push(form_id);
    //strategy_id = document.querySelector("#strategy_id");
    await postJsonGetStatus(form_arr, `convert_indicator`);
    let indicators_data = await update_chart("init_strategy");
    remove_element("indicator_form");
    build_indicator_inputs(indicators_data.indicators);
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
async function input_params(key, value, value, field) {
  console.log(key, value, value, field, "WHAT THE ACTUAL FUCK");
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
    remove_element("indicator_cond");
    build_buttons(responseData.cols, "conditions", "button", "indicator_cond");
    return responseData;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function getJson(endpoint) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  };
  let response = await fetch(endpoint, options);

  if (!response.ok) {
    throw new Error("Request failed");
  }

  const responseData = await response.json();
  return responseData;
}

async function postJsonGetData(data, endpoint, method = "POST") {
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

async function postJsonGetStatus(data, endpoint, method = "POST") {
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
  } else {
    console.log(response.status);
    return response;
  }
}

async function strategy_indicators(endpoint) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const responseData = await response.json();
    } else {
      console.error("Error:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function remove_element(class_name) {
  let elements = document.querySelectorAll(`.${class_name}`);

  elements.forEach(function (ele) {
    ele.parentNode.removeChild(ele);
  });
}
function build_buttons(array, element_id, element, class_name) {
  let container = document.getElementById(element_id);
  for (let i = 0; i < array.length; i++) {
    let button = document.createElement(element);
    button.innerText = array[i];
    button.classList.add(class_name);
    container.appendChild(button);
  }

  const buttons = container.querySelectorAll(`.${class_name}`);

  buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      let text = event.target.innerText;
      if (class_name == "indicator_cond") {
        cond.push({ ind: event.target.innerText });
      } else {
        cond.push({ cond: event.target.innerText });
      }
      document.getElementById("cond").textContent = `${show_string(cond)}`;
    });
  });
}

function value_cond() {
  let value_cond = document.getElementById("value_cond").value;
  cond.push({ val: parseFloat(value_cond) });
  document.getElementById("cond").textContent = `${show_string(cond)}`;
}

async function save_cond_buy() {
  //indicators
  conditions.push(cond);
  cond = [];

  document.getElementById("cond").textContent = `${show_string(cond)}`;
  document.getElementById("saved_conds").textContent = `${show_string(conditions)}`;
  data.buy_cond = JSON.stringify(conditions);
  data.side = "buy";
  console.log(data.buy_cond);
  let response = await postJsonGetStatus(data, "condition");
  console.log(response);
  console.log(response);
  let build_conds = await build_conditions();
  document.getElementById("buy_cond2").textContent = `${build_conds}`;
  conditions = [];
}

async function save_cond_sell() {
  //indicators
  conditions_sell.push(cond);
  cond = [];
  document.getElementById("cond").textContent = `${show_string(cond_sell)}`;
  document.getElementById("saved_conds_sell").textContent = `${show_string(conditions_sell)}`;
  data.sell_cond = JSON.stringify(conditions_sell);
  data.side = "sell";
  console.log(data.sell_cond);
  let response = await postJsonGetStatus(data, "condition");
  console.log(response);
  let build_conds = await build_conditions();
  document.getElementById("sell_cond2").textContent = `${build_conds}`;
  conditions_sell = [];
}

function del_last() {
  cond.pop();
  document.getElementById("cond").textContent = `${show_string(cond)}`;
}

function del_last_sell_cond() {
  conditions_sell.pop();
  document.getElementById("conditions_sell").textContent = `${show_string(cond)}`;
}
function del_last_buy_cond() {
  conditions.pop();
  document.getElementById("conditions").textContent = `${show_string(cond)}`;
}

function show_string(array_objs) {
  let arr_strings = [];
  for (let i = 0; i < array_objs.length; i++)
    for (const [key, value] of Object.entries(array_objs[i])) {
      arr_strings.push(value);
    }
  return JSON.stringify(arr_strings);
}

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
