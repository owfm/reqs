import { reqConstants } from '../_constants';
import moment from 'moment';

const initialState = {
  loading: false,
  isEditing: false,
  updatedOn: null,
  error: null,
  items: []
}

export function reqs(state = initialState, action) {
  switch (action.type) {
    case reqConstants.REQS_REQUEST:
      return {
        ...state,
        loading: true,
      };

    case reqConstants.REQS_SUCCESS:
      return {
        ...state,
        loading: false,
        updatedOn: moment(),
        items: [...state.items || [], ...action.items]
      }

    case reqConstants.REQS_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error,
        items: [...state.items]
      }

      case reqConstants.REQ_REQUEST:
        return {
          ...state,
          loading: true
        };

      case reqConstants.REQ_SUCCESS:
        return {
          ...state,
          loading: false,
          items: [...state.items, action.req]}


      case reqConstants.REQ_FAILURE:
        return {
          ...state,
          loading: false,
          error: action.error
        }

      case reqConstants.REQ_EDIT_TOGGLE:
        return {
          ...state,
          isEditing: !state.isEditing
        }

      default:
        return state;


  }
}
