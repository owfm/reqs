import { reqConstants } from '../_constants';

export function reqs(state = {}, action) {
  switch (action.type) {
    case reqConstants.REQ_GET_REQUEST:
      return {
        loading: true
      };

    case reqConstants.REQ_GET_SUCCESS:
      return {
        loading: false,
        ...state,
        reqSessions: [...state.reqSessions, action.req]
      }

    case reqConstants.REQ_GET_FAILURE:
      return {
        loading: false,
        error: action.error
      }

      case reqConstants.REQS_GET_REQUEST:
        return {
          loading: true
        };

      case reqConstants.REQS_GET_SUCCESS:
        return {
          loading: false,
          ...state,
          reqSessions: [...state.reqSessions, ...action.reqs]
        }

      case reqConstants.REQS_GET_FAILURE:
        return {
          loading: false,
          error: action.error
        }

      default:
        return state;


  }
}
