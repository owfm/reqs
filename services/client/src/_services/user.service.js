import axios from 'axios';
import { authHeader } from '../_helpers';
import handleResponse from './handle-response.js';

export const userService = {
  login,
  logout,
  register,
  update,
  delete: _delete,
};

function login(email, password) {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`;

  return axios.post(url, { email, password })
    .then((response) => {
      // login successful if there's a jwt token in the response
      if (response.data.user && response.data.school && response.data.user.token) {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return response.data;
      }
    });
}

function logout() {
  localStorage.clear();
}

function register(user) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  };

  return fetch('/users/register', requestOptions).then(handleResponse);
}

function update(user) {
  const requestOptions = {
    method: 'PUT',
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  };

  return fetch(`/users/${user.id}`, requestOptions).then(handleResponse);
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
  const requestOptions = {
    method: 'DELETE',
    headers: authHeader(),
  };

  return fetch(`/users/${id}`, requestOptions).then(handleResponse);
}
