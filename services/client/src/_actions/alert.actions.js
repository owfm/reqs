
import { alertConstants } from '../_constants';

function showNotification(message) {
  return { type: alertConstants.FLASH, message };
}

function hideNotification() {
  return { type: alertConstants.CLEAR };
}

function flash(message) {
  return (dispatch) => {
    if (typeof message !== 'string') {
      return null;
    }

    dispatch(showNotification(message));

    setTimeout(() => {
      dispatch(hideNotification());
    }, 5000);
  };
}

export const alertActions = {
  flash,
	hideNotification,
};
