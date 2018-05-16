import { schoolConstants } from '../_constants';
import moment from 'moment';

export function school(state = {}, action) {
  switch (action.type) {
    case schoolConstants.SCHOOL_REQUEST:
      return {
        loading: true,
      };

    case schoolConstants.SCHOOL_SUCCESS:
      return {
        school: action.school
      }

    case schoolConstants.SCHOOL_FAILURE:
      return {
        loading: false,
        fetched: false,
        error: action.error
      }

    default:
      return state;


  }
}
