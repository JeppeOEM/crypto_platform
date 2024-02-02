import { remove_element } from "../functions/remove_element.js";
import { insert_chart } from "../chart/insert_chart.js";
import { getJson, postJsonGetData, postJsonGetStatus } from "../functions/fetch.js";
import { condListController } from "./cond_list.js";
import { load_indicator } from "./load_indicator.js";
import { selected_cond } from "../classes/globals.js";
import { strategyDataInstance } from "../classes/StrategyData.js";
import { show_string } from "../functions/show_string.js";

const strategyData = strategyDataInstance;

export async function build_strategy_page() {
  // init strategy gets the indicators saved in indicator_strategies
  // const data = strategyData.getData();
  let data = {};
  const strategy_data = await postJsonGetData(data, "init_strategy");
  // const datasets_available = strategyData.dataset_pairs;
  let dataset_pairs = await strategy_data.dataset_pairs;

  await build_dataset_pair_selector(dataset_pairs, strategy_data.cols);
  // console.log(datasets_available, "datasets_available");
  let edited_data = strategyData.getData();
  edited_data.cols = strategy_data.cols;
  strategyData.setData(edited_data);
  console.log(strategyData.getData(), "strategyData.getData()");
  remove_element("indicator_cond");
  await build_buttons(strategy_data.cols, "condition_btns", "button", "indicator_cond");
  remove_element("buy_cond2");
  remove_element("sell_cond2");
  //build buttons also build indicator strategy_dataframe related buttons
  //params: array, element_id, element, class_name

  await build_indicator_inputs(strategy_data.indicators);
  // await build_conditions();

  await build_condition_lists();
  await build_buttons(["<", ">", "==", "&", "or"], "compare_btns", "button", "compare_cond");
  await build_buttons(["or", "&"], "or_and_btns", "button", "or_and_cond");
  await build_buttons(strategy_data.cols, "condition_btns", "button", "indicator_cond");

  console.log(strategy_data.cols, "COLUUUUUUUUUUUMns");

  insert_chart(strategy_data.cols);

  let todo_b = document.querySelector("#new_list_buy");

  todo_b.addEventListener("click", () => {
    create_list("buy");
    // location.reload();
    remove_element("cond_list");
    build_condition_lists();
  });

  let todo_s = document.querySelector("#new_list_sell");

  todo_s.addEventListener("click", () => {
    create_list("sell");
    location.reload();
    remove_element("cond_list");
    build_condition_lists();
  });
}

async function create_list(side) {
  const status = postJsonGetStatus({}, "cond_list?side=" + side);
  // remove_element("cond_list");
  // build_condition_lists();
}

export async function build_optimization_results() {
  const data = strategyData.getData();
  const response = await postJsonGetData(data, "optimization_results");
  console.log(response, "response");

  const resultList = document.querySelector("#optimization_results");
  console.log(resultList, "resultList");
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

    const listItem = document.createElement("li");
    listItem.textContent = `PNL: ${parsed[0]["pnl"]}% max drawdown: ${
      parsed[0]["max_drawdown"]
    }% params: ${JSON.stringify(parsed[0]["params"])}`;
    console.log(listItem.textContent);
    resultList.appendChild(listItem);
  });
}

export async function build_indicator_inputs(data, category = null) {
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
      const form = await load_indicator(
        indicators[i].indicator["kind"],
        indicators[i].category,
        indicators[i].indicator, //values
        indicators[i].id
      );
    }
  }
}
async function build_dataset_pair_selector(dataset_pairs, dataframe_column_names) {
  // Create select element
  const selectElement = document.createElement("select");
  selectElement.id = "dataset_pair_selector";
  const data = await getJson("strategy_pair");
  const current_pair = data.pair;
  // Iterate through the keys of the first object to get the options
  dataset_pairs.forEach((dataset_pair) => {
    for (let key in dataset_pair) {
      const optionElement = document.createElement("option");
      optionElement.value = key;
      optionElement.text = key;
      selectElement.appendChild(optionElement);

      // Set the option as selected if it matches the current strategy pair value
      if (key === current_pair) {
        optionElement.selected = true;
      }
    }
  });

  document.querySelector("#strategy_dataset_selector").appendChild(selectElement);

  document.querySelector("#dataset_pair_selector").addEventListener("change", async function (event) {
    const pair = event.target.value;
    let status = await postJsonGetStatus({ pair: pair }, "strategy_pair");
    // location.reload();
    let data = await postJsonGetData({}, "init_strategy");
    remove_chart();
    insert_chart(dataframe_column_names);
  });
}
function remove_chart() {
  const chartDiv = document.querySelector(".chart");
  chartDiv.innerHTML = "";
}

export async function build_condition_lists() {
  // const taskManager1 = condListController.createCondManager("buy_cond_list1");
  // const taskManager2 = condListController.createCondManager("sell_cond_list2");
  const json_buy = await getJson("cond_list?side=buy");
  const json_sell = await getJson("cond_list?side=sell");
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
      } else {
        insert_name.dataset.primary_key = data.list_id;
        primary_key = data.list_id;
      }

      insert_name.dataset.frontend_id = data.frontend_id;
      // const cond_wrapper = clone.querySelector(`.clone_${side}`);
      // cond_wrapper.dataset.id = data.list_id;
      container.appendChild(clone);
      //cond_list.js controller
      condListController.createCondManager(element_name, primary_key);
      window.scrollTo(0, document.body.scrollHeight);
    });
  }
}
export async function build_buttons(array, element_id, element, class_name) {
  remove_element(class_name);
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
