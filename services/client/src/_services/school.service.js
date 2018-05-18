import { authHeader } from '../_helpers';
import axios from 'axios';
import handleResponse from './handle-response.js';


export const schoolService = {
  getWeekNumber
}


function getReq(id) {

  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${id}`;
  return axios.get(
    url,
    {headers: authHeader()},

  ).then(handleResponse);

}


function getWeekNumber(date) {

  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/schools/check?date=${date}`

  return axios.get(
    url,
    {headers: authHeader()}
  ).then(handleResponse);
};
