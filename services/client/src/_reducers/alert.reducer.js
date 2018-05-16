import { alertConstants } from '../_constants';

export function alert(state = {}, action) {
  switch (action.type) {
    case alertConstants.FLASH:
      return {
        open: true,
        message: action.message
      };

    case alertConstants.CLEAR:
      return {
        open: false
      };
    default:
      return state
  }
}
