import { filterActions } from '../_actions';
import { reqConstants } from '../_constants';
import moment from 'moment';
const wbStamp = filterActions.getWbStampFromDate(moment());

const initialState = {
  loading: false,
  deleting: false,
  isEditing: false,
  error: null,
};

initialState[wbStamp] = {
  items: [],
  lastupdated: null,
};


export function reqs(state = initialState, action) {

  switch (action.type) {
    case reqConstants.REQS_REQUEST:
    case reqConstants.REQ_REQUEST:
    case reqConstants.EDIT_REQUEST:
    case reqConstants.POST_REQUEST:

      return {
        ...state,
        loading: true,
      };
    case reqConstants.DELETE_REQUEST:
      return {
        ...state,
        deleting: action.id,
      }

    case reqConstants.REQS_SUCCESS:

      // copy state
      const newState = { ...state };
      newState.loading = false;

      const { wbStamp } = action;
      const extantItems = state[wbStamp] ? state[wbStamp].items : [];

      newState[wbStamp] = {};
      newState[wbStamp]['items'] = merge(extantItems, action.items);
      newState[wbStamp]['lastupdated'] = action.timestamp;

      return newState;

    case reqConstants.REQ_SUCCESS:
        return {
          ...state,
          loading: false,
          items: [...state.items, action.req]}


    case reqConstants.REQ_FAILURE:
    case reqConstants.REQS_FAILURE:
    case reqConstants.POST_FAILURE:
    case reqConstants.UPDATE_FAILURE:

        return {
          ...state,
          loading: false
        }

    case reqConstants.DELETE_FAILURE:
        return {
          ...state,
          deleting: false,
        }
    case reqConstants.POST_SUCCESS:

        let stateWithNewReq = { ...state };
        stateWithNewReq.loading = false;

        const { newReq, currentWbStamp } = action;

        stateWithNewReq[currentWbStamp].items = [...state[currentWbStamp].items, newReq]

        return stateWithNewReq;

    case reqConstants.UPDATE_SUCCESS:

      const newItems = [...state[action.currentWbStamp].items.filter(s => s.id !== action.updatedReq.id), action.updatedReq]

      return {
        ...state,
        loading: false,
        [action.currentWbStamp]: {'items': [...newItems]}
      }

    case reqConstants.DELETE_SUCCESS:

      return {
        ...state,
        deleting: false,
        [action.currentWbStamp]: {
          items: [...state[action.currentWbStamp].items.filter(s => s.id !== action.id)],
        }
      }




    default:
      return state;


  }
}

function merge(old = [],updated) {
  var o = {};

  old.forEach(function(v) {
    o[v.id] = v;
  })

  updated.forEach(function(v) {
    o[v.id] = v;
  })

  var r = [];

  for(var p in o) {
    if(o.hasOwnProperty(p))
      r.push(o[p]);
  }

  return r;
}
