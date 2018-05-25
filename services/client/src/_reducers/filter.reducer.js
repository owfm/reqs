import { filterConstants, appConstants } from '../_constants';
import { filterActions } from '../_actions';
import moment from 'moment';

const initialState = {
  currentWbStamp: filterActions.getWbStampFromDate(moment()),
  site: null,
  status: null,
  currentWeek: 1
}

export function filters(state = initialState, action) {

  switch (action.type) {

    case filterConstants.SET_WEEK:
      return {
        ...state,
        currentWeek: action.week
      }

    case filterConstants.SET_WB_DATE:
      return {
        ...state
      };

    case filterConstants.FORWARD_WEEK:


      return {
        ...state,
        currentWbStamp: moment(state.currentWbStamp).add(7, 'days').format(appConstants.dateFormat)
      };

    case filterConstants.BACKWARD_WEEK:
      return {
        ...state,
        currentWbStamp: moment(state.currentWbStamp).subtract(7, 'days').format(appConstants.dateFormat)
      };

    case filterConstants.SET_SITE:
      return {
        ...state,
        site: action.site
      }

      case filterConstants.SET_STATUS:
        return {
          ...state,
          status: action.status
        }

      case filterConstants.CLEAR_SITE:
        return {
          ...state,
          site: null
        }

    default:
      return state
  }
}
