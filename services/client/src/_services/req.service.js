import { authHeader } from '../_helpers';
import axios from 'axios';

export const reqService = {
  getReq,
  getReqs
}

function getReq(id) {

  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${id}`;

  return axios.get(
    url,
    {headers: authHeader()},

  ).then(handleResponse);

}


function getReqs(from, to, all) {


  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;

  const params = { from, to, all }

  return axios.get(
    url,
    {
      headers: authHeader(),
      params
    },
  )
  .then((response) => {
    if (response.data.data) {
      localStorage.setItem('reqs', JSON.stringify(response.data.data));
    }
    return response;
  })
  .then(handleResponse);
};


function handleResponse(response) {
    if (response.status !== 200) {
        return Promise.reject(response.statusText);
    }

    return response;
}
