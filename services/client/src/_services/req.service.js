import { authHeader } from '../_helpers';
import axios from 'axios';

export const reqService = {
  getReq,
  getReqs
}

function getReq(id) {

  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${id}`;

  return axios.get(url).then(handleResponse);

}


function getReqs(from, to) {

  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;

  const params = { from, to };

  return axios.get(
    url,
    {
      headers: authHeader(),
      params
    },
  )
  .then(handleResponse);
};

// function getLesson(id)
//
//
// function getLessons(userId)
//
//
// function postReq(req)
// title
// equipment
// notes
// lesson id
// filenames
// week beginning date


function handleResponse(response) {
    if (response.status !== 200) {
        return Promise.reject(response.statusText);
    }

    return response;
}
