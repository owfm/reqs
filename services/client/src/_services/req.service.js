import { authHeader } from '../_helpers';
import axios from 'axios';
import moment from 'moment';
import handleResponse from './handle-response.js';

export const reqService = {
  getReq,
  getReqs,
  reqsAreStale,
  postNewReq,
  postReqUpdate,
  deleteReq,
};

function getReq(id) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${id}`;
  return axios.get(
    url,
    { headers: authHeader() },

  ).then(handleResponse);
}

function getReqs(wb, lastupdated, all) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;
  const params = { wb, all };
  if (lastupdated) {
    params.lastupdated = lastupdated;
  }
  return axios.get(
    url,
    {
      headers: authHeader(),
      params,
    },
  )
    .then(handleResponse);
}

function postNewReq(reqData) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;

  return axios.post(
    url, reqData,
    {
      headers: authHeader(),
    },
  )
    .then(handleResponse);
}

function postReqUpdate(updatedReq) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${updatedReq.id}`;

  const dontPatch = ['id', 'currentWbStamp'];

  const patch = Object.keys(updatedReq)
    .filter(key => !dontPatch.includes(key))
    .map(
    key => {
        return { op: 'replace', path: `/${key}`, value: `${updatedReq[key] || ''}` }
    });

  return axios.patch(
    url,
    patch,
    {
      headers: authHeader(),
    },
  )
    .then(handleResponse);
}

function deleteReq(id) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${id}`;
  return axios.delete(
    url,
    {
      headers: authHeader(),
    },
  )
    .then(handleResponse);
}

function reqsAreStale(reqs) {
  // if no items in reqs state, set stale to trigger fetch from server.
  if (reqs.items.length === 0) {
    return true;
  }

  return moment().diff(reqs.updatedOn, 'seconds') > 1000;
}
