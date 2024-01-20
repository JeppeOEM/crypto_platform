import { postJsonGetStatus } from "../functions/fetch.js";

export function load_params() {
  const arr = [];
  const rows = document.querySelectorAll(".param");
  rows.forEach((row) => {
    const indi = row.querySelector(".indicator");
    let side = which_side(indi.innerText);
    const operator = row.querySelector(".operator");
    const min = row.querySelector(".min");
    const max = row.querySelector(".max");
    const type = "int";

    arr.push([indi.innerText, operator.innerText, type, min.value, max.value, side]);
  });
  let data = {};
  data.optimizer_params = arr;
  data.params_class = "indicator";

  const status = postJsonGetStatus(data, "optimizer_params");
}

window.load_params = load_params;

export function optimizer_params(conditions, suffix, element) {
  const title = document.querySelector("title");
  const cond_arr = [];

  //global conditions arrayy
  conditions.forEach((cond) => {
    cond = JSON.parse(cond.indicator_json);
    cond_arr.push(cond);
  });

  const tbody = document.querySelector(`.${element}`);
  const opti_params = document.getElementById("optimize_params");
  cond_arr.forEach((cond) => {
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
