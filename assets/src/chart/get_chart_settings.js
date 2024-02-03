export function chart_settings(indi) {
  indi = remove_underscore(indi);
  switch (indi) {
    case "RSI":
    case "AO":
    case "ADX":
      return { type: "line_add_pane" };
    case "volume":
      return { type: "histogram" };
    default:
      console.log("################# Unknown indicator ################ ::::: " + indi);
  }
}

function remove_underscore(inputString) {
  return inputString.split("_")[0];
}
