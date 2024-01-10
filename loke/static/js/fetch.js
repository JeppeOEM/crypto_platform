export async function postJsonGetStatus(data, endpoint, method = "POST") {
  // Create an options object for the fetch request
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  // Make the POST request using the fetch API
  let response = await fetch(endpoint, options);

  if (!response.ok) {
    throw new Error("Request failed");
  } else {
    console.log(response.status);
    return response;
  }
}

export async function getJson(endpoint) {
  const options = {
    method: "GET",
  };
  let response = await fetch(endpoint, options);

  if (!response.ok) {
    throw new Error("Request failed");
  }

  const responseData = await response.json();
  return responseData;
}
