import { schoolConstants } from '../_constants';
import moment from 'moment';

const initialState = {
  school: null,
  weekNumber: null,
  loading: false,
  error: null
}

export function school(state = initialState, action) {
  switch (action.type) {
    case schoolConstants.SCHOOL_REQUEST:
      return {
        ...state,
        loading: true,
      };

    case schoolConstants.SCHOOL_SUCCESS:
      return {
        ...state,
        loading: false,
        school: action.school
      }

    case schoolConstants.SCHOOL_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      }

    case schoolConstants.WEEK_SUCCESS:
      return {
        ...state,
        weekNumber: action.weekNumber
      }

    case schoolConstants.WEEK_SUCCESS:
      return {
        ...state,
        weekNumber: action.weekNumber
      }

    case schoolConstants.SITES_SUCCESS:
      return {
        ...state,
        sites: [...action.sites]
      }

    default:
      return state;


  }
}
