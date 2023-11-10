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

function showValue(value) {
  alert("The value is: " + value);
}

document.addEventListener("DOMContentLoaded", function () {
  // Your code here
  build_page();
});

async function build_page() {
  indicatordata = await update_chart("init_strategy");
  console.log(indicatordata.indicators);
  try {
    build_buttons(["<", ">", "==", "&", "or"], "compare", "button", "compare_cond");
  } catch (error) {
    console.log(error);
  }
  build_indicator_inputs(indicatordata.indicators);
  build_buttons(["or", "&"], "compare", "button", "or_and_cond");
}

function build_indicator_inputs(data) {
  indicators = data.map((indicator) => {
    indicator = JSON.parse(indicator);

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
    return indicator;
  });
  console.log(indicators);

  for (let i = 0; i < indicators.length; i++) {
    loadIndicator(indicators[i]["kind"], "momentum", indicators[i]);
  }
}

async function loadIndicator(indicatorValue, category, values = undefined) {
  // Create a new input field element
  const data = {
    indicator: indicatorValue,
    category: category,
  };
  console.log(values);
  let output = [];
  let indi_data = await postJsonGetData(data, "/add_indicator");
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
    //asign default values
    indi_data = output;
  }

  const name_indicator = indi_data[0][1];
  //remove name of indicator
  indi_data = indi_data.slice(1);
  const formContainer = document.getElementById("form-container");
  const form = document.createElement("form");
  var field = document.createElement("fieldset");
  const legend = document.createElement("legend");
  legend.textContent = name_indicator;
  formContainer.appendChild(form);
  form.appendChild(field);
  field.appendChild(legend);

  form.addEventListener("submit", gogo);
  //form.customParam = form;
  for (let i = 0; i < indi_data.length; i++) {
    input_params(indi_data[i][0], indi_data[i][1], indi_data[i][2], field);
  }

  const submitButton = document.createElement("input");
  submitButton.type = "submit";
  submitButton.id = "submitIndicator";
  submitButton.value = "Submit";
  field.appendChild(submitButton);

  async function gogo(event) {
    event.preventDefault();
    // let formdata = event.currentTarget.customParam;
    const formData = new FormData(form);
    form_arr = [["kind", legend.innerText]];
    formData.forEach((value, key) => {
      form_arr.push([key, value]);
    });
    //strategy_id = document.querySelector("#strategy_id");
    await postJsonGetStatus(form_arr, `convert_indicator`);
    await update_chart("init_strategy");
  }

  // var container = document.getElementById("input-container");
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
    remove_buttons("indicator_cond");
    build_buttons(responseData.cols, "conditions", "button", "indicator_cond");
    return responseData;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function postJsonGetData(data, endpoint) {
  const options = {
    method: "POST",
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

async function postJsonGetStatus(data, endpoint) {
  // Create an options object for the fetch request
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  // Make the POST request using the fetch API
  let reponse = await fetch(endpoint, options);

  if (!reponse.ok) {
    throw new Error("Request failed");
  } else {
    console.log(reponse.status);
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

function remove_buttons(class_name) {
  let buttons = document.querySelectorAll(`.${class_name}`);

  buttons.forEach(function (button) {
    button.parentNode.removeChild(button);
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

function save_cond_buy() {
  //indicators
  conditions.push(cond);
  cond = [];
  document.getElementById("cond").textContent = `${show_string(cond)}`;
  document.getElementById("saved_conds").textContent = `${show_string(conditions)}`;
}

function save_cond_sell() {
  //indicators
  conditions_sell.push(cond);
  cond = [];
  document.getElementById("cond").textContent = `${show_string(cond_sell)}`;
  document.getElementById("saved_conds_sell").textContent = `${show_string(conditions_sell)}`;
}

function del_last() {
  cond.pop();
  document.getElementById("cond").textContent = `${show_string(cond)}`;
}

function show_string(array_objs) {
  let arr_strings = [];
  for (let i = 0; i < array_objs.length; i++)
    for (const [key, value] of Object.entries(array_objs[i])) {
      arr_strings.push(value);
    }
  return arr_strings;
}

async function optimize() {
  let response = await postJsonGetData(data, "/optimize");
  console.log(response);
}

async function backtest() {
  // let conditions_copy = [[{ ind: "AO_14_14" }, { cond: ">" }, { val: 50 }]];
  // let conditions_sell_copy = [[{ ind: "AO_14_14" }, { cond: "<" }, { val: 11 }]];
  let conditions_copy = conditions;
  let conditions_sell_copy = conditions_sell;

  data.conds_buy = conditions_copy;
  data.conds_sell = conditions_sell_copy;

  let response = await postJsonGetData(data, "backtest");
}
async function input_params(key, value, value, field) {
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
