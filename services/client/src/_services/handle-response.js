export default function handleResponse(response) {
  console.log(response);
    if (response.status > 300) {
        return Promise.reject(response.statusText);
    }
    return response;
}
