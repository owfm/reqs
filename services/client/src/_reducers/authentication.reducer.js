import { userConstants } from '../_constants';

let user = JSON.parse(localStorage.getItem('user'));

const initialState = user ? { loggedIn: true, loggingIn: false, user } : { loggedIn: false};

export function authentication(state = initialState, action) {
  switch (action.type) {
    case userConstants.LOGIN_REQUEST:
      return {
        loggingIn: true,
        user: action.user
      };
    case userConstants.LOGIN_SUCCESS:
      return {
        loggingIn: false,
        loggedIn: true,
        user: action.user
      };
    case userConstants.LOGIN_FAILURE:
      return {};
    default:
      return state

  }
}
