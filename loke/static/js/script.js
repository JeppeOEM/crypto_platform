function showValue(value) {
  alert("The value is: " + value);
}

function sendIndicator(indicator) {
  // Define the URL of your Flask endpoint
  const endpointUrl = "/add_indicator";

  // Create a data object to send as the POST request body
  const data = {
    indicator: indicator,
  };

  // Make a POST request to the Flask endpoint
  fetch(endpointUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      } else {
        throw new Error("Request failed");
      }
    })
    .then((responseData) => {
      // Handle the response from the Flask endpoint, if needed
      console.log("Response from Flask:", responseData);
    })
    .catch((error) => {
      // Handle any errors that occur during the request
      console.error("Error:", error);
    });
}
