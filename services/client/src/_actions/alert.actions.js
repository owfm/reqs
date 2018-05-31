import { alertConstants } from '../_constants';

export const alertActions = {
  flash
};

function showNotification(message) {
  return { type: alertConstants.FLASH, message }
}

function hideNotification() {
  return { type: alertConstants.CLEAR }
}

function flash(message){

  return dispatch => {

    if (typeof message !== 'string') {
      return null;
      console.log('GOT WEIRD OBJCT AS MESSAGE')
    }

    dispatch(showNotification(message));

    setTimeout( () => {
      dispatch(hideNotification())
    }, 5000)
  }
};
