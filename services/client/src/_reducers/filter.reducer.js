import { filterConstants } from '../_constants';
import { filterActions } from '../_actions';
import moment from 'moment';

const initialState = {
  currentWbBeginningDate: filterActions.getWbNumberFromDate(moment())
}

export function filters(state = initialState, action) {

  switch (action.type) {

    case filterConstants.SET_WB_DATE:
      return {
        ...state
      };

    case filterConstants.FORWARD_WEEK:


      return {
        ...state,
        currentWbBeginningDate: moment(state.currentWbBeginningDate).add(7, 'days')
      };

    case filterConstants.BACKWARD_WEEK:
      return {
        ...state,
        currentWbBeginningDate: moment(state.currentWbBeginningDate).subtract(7, 'days')
      };

    default:
      return state
  }
}
