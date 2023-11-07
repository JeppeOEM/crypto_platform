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

  createInputs(ind_props);
}

function createInputs(jsonData) {
  const name_indicator = jsonData.kind;
  const newJsonData = { ...jsonData };
  delete newJsonData.kind;
  const formContainer = document.getElementById("form-container");
  const form = document.createElement("form");
  const field = document.createElement("fieldset");
  const legend = document.createElement("legend");
  legend.textContent = name_indicator;
  formContainer.appendChild(form);
  form.appendChild(field);
  field.appendChild(legend);

  for (const key in newJsonData) {
    const value = newJsonData[key];
    createInput(key, value);
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

  const responseData = await response.json();

  return responseData;
}
