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
