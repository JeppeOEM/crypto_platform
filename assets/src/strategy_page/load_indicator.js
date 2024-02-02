import { postJsonGetStatus, postJsonGetData } from "../functions/fetch.js";
import { remove_element } from "../functions/remove_element.js";
import { build_buttons } from "./build_strategy_page.js";
import { build_indicator_inputs } from "./build_strategy_page.js";
import { strategyDataInstance } from "../classes/StrategyData.js";

const strategyData = strategyDataInstance;

export async function load_indicator(name, category, values = undefined, form_id) {
  // Create a new input field element
  const data = {
    indicator: name,
    category: category,
  };
  let output = [];
  const strat_id = document.getElementById("strategy_id");
  const id = strat_id.dataset.info;
  let indi_data = await postIndicatorData(`add_indicator`);
  console.log(indi_data,"load indicator")
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

    //strategy_id = document.querySelector("#strategy_id");
    await postJsonGetStatus(form_arr, `convert_indicator`);

    let indicators_data = await postJsonGetData(data, "init_strategy");

    remove_element("indicator_cond");
    build_buttons(indicators_data.cols, "condition_btns", "button", "indicator_cond");
    let edited_data = strategyData.getData();
    edited_data.cols = indicators_data.cols;
    strategyData.setData(edited_data);
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
