import { alertConstants } from '../_constants';

export function alerts(state = {open: false, message: ''}, action) {
  switch (action.type) {
    case alertConstants.FLASH:
      return {
        open: true,
        message: action.message
      };

    case alertConstants.CLEAR:
      return {
        open: false,
        message: ''
      };
    default:
      return state
  }
}
