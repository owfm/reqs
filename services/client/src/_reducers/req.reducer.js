import { reqConstants } from '../_constants';

export function reqs(state = {}, action) {
  switch (action.type) {
    case reqConstants.REQS_REQUEST:
      return {
        loading: true
      };

    case reqConstants.REQS_SUCCESS:
      return {
        ...state,
        loading: false,
        items: [...state.items || [], ...action.items]
      }

    case reqConstants.REQS_FAILURE:
      return {
        loading: false,
        error: action.error
      }

      case reqConstants.REQ_REQUEST:
        return {
          loading: true
        };

      case reqConstants.REQ_SUCCESS:
        return
          // loading: false,
          // ...state,
          // reqSessions: [...state.reqSessions, ...action.reqs]
          [...state, ...action.reqs]


      // case reqConstants.REQ_FAILURE:
      //   return {
      //     loading: false,
      //     error: action.error
      //   }

      default:
        return state;


  }
}
