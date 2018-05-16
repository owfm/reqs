import { authHeader } from '../_helpers';
import axios from 'axios';
import moment from 'moment';

export const reqService = {
  getReq,
  getReqs,
  reqsAreStale
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
    .then(handleResponse);
};


function reqsAreStale(state) {
  return moment().diff(state.reqs.updatedOn, 'seconds') > 1000;
}


function handleResponse(response) {
    if (response.status !== 200) {
        return Promise.reject(response.statusText);
    }

    return response;
}
