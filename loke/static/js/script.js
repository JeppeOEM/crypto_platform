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
    const data = {
      exchange: "binance",
      init_candles: 100,
      symbol: "BTCUSDT",
      name: "test",
      description: "description",
    };

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const responseData = await response.json();
      document.getElementById("content-div").textContent = responseData.content;
    } else {
      console.error("Error:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
