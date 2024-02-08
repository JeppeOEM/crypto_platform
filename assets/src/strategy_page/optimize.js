import { postJsonGetData, postJsonGetStatus } from "../functions/fetch.js";
import { selected_cond } from "../classes/globals.js";

//save the optimization params to the database
export function load_params() {
  const arr = [];
  const rows = document.querySelectorAll(".param");
  rows.forEach((row) => {
    let list_id = row.dataset.id;
    let condition_id = row.dataset.condition_id;
    console.log(list_id, "LIST ID");
    const indi = row.querySelector(".indicator");
    let side = which_side(indi.innerText);
    const operator = row.querySelector(".operator");
    const min = row.querySelector(".min");
    const max = row.querySelector(".max");
    const type = "int";

    arr.push([indi.innerText, operator.innerText, type, min.value, max.value, side, list_id, condition_id]);
  });
  let data = {};
  data.optimizer_params = arr;
  data.params_class = "indicator";

  const status = postJsonGetStatus(data, "optimizer_params");
  console.log(status);
}

window.load_params = load_params;

//creating the input fields and are NOT saved to the database
export function optimizer_params(conditions, suffix) {
  const title = document.querySelector("title");
  const cond_arr = [];
  console.log(conditions, "optimizer params conditions");
  //global conditions arrayy

  conditions.forEach((cond) => {
    let placement = {
      list_id: cond.fk_list_id,
      list_row: cond.list_row,
    };
    console.log(cond.condition_id);
    console.log(cond, "COND");
    let condition_id = cond.condition_id;
    cond = JSON.parse(cond.indicator_json);
    cond_arr.push([cond, placement, condition_id]);
  });

  // const tbody = document.querySelector(`.${element}`);
  const opti_params = document.getElementById("optimize_params");
  cond_arr.forEach((cond) => {
    cond[0].forEach((val) => {
      let list_id = cond[1].list_id;
      let list_row = cond[1].list_row;
      let condition_id = cond[2];
      // let opti_data = postJsonGetData({ condition_id: condition_id }, "get_opti_params");
      const clone = opti_params.content.cloneNode(true);
      clone.querySelector(".indicator").textContent = val[0]["ind"] + suffix;
      clone.querySelector(".operator").textContent = val[1]["cond"];
      clone.querySelector(".min").value = "1";
      clone.querySelector(".max").value = "1";
      let table_row = clone.querySelector(".param");
      table_row.dataset.condition_id = condition_id;
      table_row.dataset.id = list_id;
      table_row.dataset.row = list_row;
      console.log(list_id, list_row, suffix, "APPEND HEREEEEEEEEEEEEEEE");
      let append_here = insert_opti_where(list_id, list_row, suffix);
      console.log(append_here, "APPEND HEREEEEEEEEEEEEEEE");
      append_here.appendChild(clone);
    });
  });
}

function insert_opti_where(list_id, list_row, side) {
  if (side === "_BUY") {
    let container = document.querySelector(".buy_clones");
    const the_list = container.querySelector(`[data-primary_key="${list_id}"]`);
    let row = the_list.querySelector(`.opti_list_${list_row}`);

    return row;
  } else {
    let container = document.querySelector(".sell_clones");

    console.log(container.querySelector(`[data-primary_key="${list_id}"]`));
    const the_list = container.querySelector(`[data-primary_key="${list_id}"]`);
    let row = the_list.querySelector(`.opti_list_${list_row}`);
    return row;
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

// export function optimizer_params(conditions, suffix) {

//   const cond_arr = [];

//   //global conditions arrayy

//   conditions.forEach((cond) => {
//     let placement = {
//       list_id: cond.fk_list_id,
//       list_row: cond.list_row,
//     };
//     cond = JSON.parse(cond.indicator_json);

//     cond_arr.push([cond, placement]);
//   });

//   // const tbody = document.querySelector(`.${element}`);
//   const opti_params = document.getElementById("optimize_params");
//   cond_arr.forEach((cond) => {
//     cond[0].forEach((val) => {
//       let list_id = cond[1].list_id;
//       let list_row = cond[1].list_row;
//       const clone = opti_params.content.cloneNode(true);
//       clone.querySelector(".indicator").textContent = val[0]["ind"] + suffix;
//       clone.querySelector(".operator").textContent = val[1]["cond"];
//       clone.querySelector(".min").value = "1";
//       clone.querySelector(".max").value = "1";
//       let table_row = clone.querySelector(".param");
//       table_row.dataset.id = list_id;
//       table_row.dataset.row = list_row;
//       console.log(list_id, list_row, suffix, "APPEND HEREEEEEEEEEEEEEEE");
//       let append_here = insert_opti_where(list_id, list_row, suffix);
//       console.log(append_here, "APPEND HEREEEEEEEEEEEEEEE");
//       append_here.appendChild(clone);
//     });
//   });
// }

// export function optimizer_params(conditions, suffix) {
//   const cond_arr = [];

//   conditions.forEach((cond) => {
//     let placement = {
//       list_id: cond.fk_list_id,
//       list_row: cond.list_row,
//     };
//     cond = JSON.parse(cond.indicator_json);
//     cond_arr.push([cond, placement]);
//   });

//   const opti_params = document.getElementById("optimize_params");
//   //fragment kills the flicker
//   const fragment = document.createDocumentFragment();

//   cond_arr.forEach((cond) => {
//     cond[0].forEach((val) => {
//       let list_id = cond[1].list_id;
//       let list_row = cond[1].list_row;

//       const clone = opti_params.content.cloneNode(true);
//       clone.querySelector(".indicator").textContent = val[0]["ind"] + suffix;
//       clone.querySelector(".operator").textContent = val[1]["cond"];
//       clone.querySelector(".min").value = "1";
//       clone.querySelector(".max").value = "1";
//       let table_row = clone.querySelector(".param");
//       table_row.dataset.id = list_id;
//       table_row.dataset.row = list_row;

//       let append_here = insert_opti_where(list_id, list_row, suffix);

//       // Append the clone to the fragment instead of the actual document
//       fragment.appendChild(clone);
//     });
//   });

//   // Append the fragment to the actual document in one go
//   opti_params.appendChild(fragment);
// }
