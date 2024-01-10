export function urlStringConversion(urlString) {
  let string = urlString.toLowerCase();
  const split = string.split("_");
  let market_type = "";
  if (split[0] === "margin") {
    string = `${split[1]}/${split[2]}:${split[3]}`;
    market_type = "margin";
  } else {
    string = `${split[1]}/${split[2]}`;
    market_type = "spot";
  }

  return { market_type: market_type, pair: string };
}
