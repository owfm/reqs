import { filterConstants, appConstants } from '../_constants';
import { filterActions } from '../_actions';
import moment from 'moment';

const initialState = {
  currentWbStamp: filterActions.getWbStampFromDate(moment()),
  sites: [],
  status: null,
  currentWeek: 1,
  holiday: false
}

export function filters(state = initialState, action) {

  switch (action.type) {

    case filterConstants.SET_WB_STAMP:
      return {
        ...state,
        currentWbStamp: action.currentWbStamp
      }

    case filterConstants.SET_WEEK:
      return {
        ...state,
        holiday: false,
        weekNumber: action.weekNumber
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
      // console.log(state);
      // return state;
      if (state.sites.includes(action.site)) {
        return { ...state }
      }

      return {
        ...state,
        sites: [...state.sites, action.site]
      }

    case filterConstants.SET_STATUS:
      return {
        ...state,
        status: action.status
      }

    case filterConstants.CLEAR_SITE:
      return {
        ...state,
        sites: state.sites.filter(s => s !== action.site)
      }

    case filterConstants.CLEAR_ALL_SITES:
      return {
        ...state,
        sites: []
      }

    case filterConstants.CLEAR_STATUS:
      return {
        ...state,
        status: null
      }

    case filterConstants.CLEAR_ALL:
      return {
        ...state,
        status: null,
        sites: []
      }


    default:
      return state
  }
}
