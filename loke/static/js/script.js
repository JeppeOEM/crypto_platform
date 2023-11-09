class Condition {
  constructor(cond) {
    this.setCondition(cond);
  }
  getCondition() {
    return this.cond;
  }
  setCondition(newCond) {
    newCond = newCond.trim();
    if (newCond === "") {
      throw "Cond cant be empty";
    }
    this.name = newCond;
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

async function loadIndicator(indicatorValue, category) {
  // Create a new input field element
  const data = {
    indicator: indicatorValue,
    category: category,
  };

  let inputField = document.createElement("input");
  inputField.type = "text"; // You can change this to the desired input type
  inputField.setAttribute("name", indicatorValue);
  console.log("Load Indicator");
  console.log(data, category);

  ind_props = await postJsonGetData(data, "/add_indicator");
  console.log("after postJsonGetData", ind_props);

  // Get the container for new inputs
  var container = document.getElementById("input-container");

  // Append the newly created input field to the container
  container.appendChild(inputField);

  createInputs(ind_props);
}

function createInputs(data) {
  console.log(data);
  const name_indicator = data[0][1];
  //remove name
  data = data.slice(1);
  console.log(name_indicator);
  const formContainer = document.getElementById("form-container");
  const form = document.createElement("form");
  const field = document.createElement("fieldset");
  const legend = document.createElement("legend");
  legend.textContent = name_indicator;
  formContainer.appendChild(form);
  form.appendChild(field);
  field.appendChild(legend);

  form.addEventListener("submit", gogo);
  //form.customParam = form;
  for (let i = 0; i < data.length; i++) {
    console.log(i);
    console.log(data[i]);
    createInput(data[i][0], data[i][1]);
  }

  const submitButton = document.createElement("input");
  submitButton.type = "submit";
  submitButton.id = "submitButton";
  submitButton.value = "Submit";
  field.appendChild(submitButton);

  function createInput(key, value) {
    if (value != "bool") {
      const label = document.createElement("label");
      label.innerText = key;
      const input = document.createElement("input");
      input.type = "text";
      input.value = "14";
      input.name = key;
      field.appendChild(label);
      field.appendChild(input);
    } else {
      const label2 = document.createElement("label");
      label2.innerText = key;
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = key;
      field.appendChild(label2);
      field.appendChild(checkbox);
    }
  }

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

    console.log("Form Data as JSON:", JSON.stringify(form_arr));
  }
}

async function postJsonGetData(data, endpoint) {
  console.log(endpoint);
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
  console.log(reponse);
  if (!reponse.ok) {
    throw new Error("Request failed");
  } else {
    console.log(reponse.status);
  }
}

async function update_chart(endpoint) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      console.log("response ok");
      const responseData = await response.json();
      console.log(responseData);
      build_buttons(responseData, "conditions", "button", "indicator_cond");
      build_buttons(["<", ">", "==", "&", "or"], "compare", "button", "compare_cond");
      build_buttons(["or", "&"], "compare", "button", "or_and_cond");
    } else {
      console.error("Error:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
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
      console.log(text);
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
  console.log(cond);
  console.log(conditions);
  console.log(conditions_sell);
  let arr_strings = [];
  for (let i = 0; i < array_objs.length; i++)
    for (const [key, value] of Object.entries(array_objs[i])) {
      console.log(`${key}: ${value}`);
      arr_strings.push(value);
    }
  return arr_strings;
}

async function backtest() {
  // let conditions_copy = conditions;
  // let conditions_sell_copy = conditions_sell;
  // conditions_copy[0].splice(0, 0, "buy first");
  // conditions_sell_copy[0].splice(0, 0, "sell first");
  // data.conds_buy = [conditions_copy];
  // data.conds_sell = [conditions_sell_copy];
  data.conds_buy = [
    [
      "buy first",
      {
        ind: "RSI_14",
      },
      {
        cond: "<",
      },
      {
        val: 33,
      },
    ],
  ];
  data.conds_sell = [
    [
      [
        "sell first",
        {
          ind: "open",
        },
        {
          cond: "<",
        },
        {
          val: 1,
        },
      ],
    ],
  ];
  console.log(data.conds_buy);
  console.log(data.conds_sell);
  let response = await postJsonGetData(data, "/backtest");
  console.log(response);
}
