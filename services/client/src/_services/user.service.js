import { authHeader } from '../_helpers';
import axios from 'axios';

export const userService = {
    login,
    logout,
    register,
    getAll,
    update,
    delete: _delete
};

function login(email, password) {

    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`

    return axios.post(url, {email, password})
        // .then(response => {
        //     console.log('----------------\n')
        //     console.log(response);
        //     console.log('----------------\n')
        //     if (response.status !== 200) {
        //         return Promise.reject("User not found.");
        //     }
        //     return response.data.user;
        // })
        .then((response) => {
            // login successful if there's a jwt token in the response
            if (response.data.user && response.data.user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }

            return response.data.user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch('/users', requestOptions).then(handleResponse);
}

function register(user) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch('/users/register', requestOptions).then(handleResponse);
}

function update(user) {
    const requestOptions = {
        method: 'PUT',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    };

    return fetch('/users/' + user.id, requestOptions).then(handleResponse);;
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    const requestOptions = {
        method: 'DELETE',
        headers: authHeader()
    };

    return fetch('/users/' + id, requestOptions).then(handleResponse);;
}

function handleResponse(response) {
    if (!response.ok) {
        return Promise.reject(response.statusText);
    }

    return response.json();
}
