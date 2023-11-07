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
  console.log("HEEEEEEEEEYAAAAAAAAAAA");
  console.log(data, category);

  ind_props = await postJsonString(data, "/add_indicator");
  console.log("indi", ind_props);
  // Get the container for new inputs
  var container = document.getElementById("input-container");

  // Append the newly created input field to the container
  container.appendChild(inputField);
}

async function postJsonString(data, endpoint) {
  // Define the URL of your Flask endpoint

  // Create a data object to send as the POST request body

  let response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Request failed");
  }

  const responseData = await response.text();

  return responseData;
}
