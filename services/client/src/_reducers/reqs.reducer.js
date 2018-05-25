import { filterActions } from '../_actions';
import { reqConstants, appConstants } from '../_constants';
import { getWbStamp } from '../_helpers';
import moment from 'moment';

const wbStamp = filterActions.getWbStampFromDate(moment());

const initialState = {
  loading: false,
  isEditing: false,
  error: null
};

initialState[wbStamp] = {
  items: [],
  'lastupdated': null
}
// create key for current week of reqs, populate with empty array of items
// const wbStamp = getWbStamp(moment());
// initialState[wbStamp]['items'] = [];
// initialState[wbStamp]['lastupdated'] = null;


export function reqs(state = initialState, action) {
  switch (action.type) {
    case reqConstants.REQS_REQUEST:
      return {
        ...state,
        loading: true,
      };

    case reqConstants.REQS_SUCCESS:

      // copy state
      const newState = { ...state };
      newState.loading = false;

      const { wbStamp, items, timestamp } = action;
      const extantItems = state[wbStamp] ? state[wbStamp].items : [];

      newState[wbStamp] = {};
      newState[wbStamp]['items'] = merge(extantItems, action.items);
      newState[wbStamp]['lastupdated'] = action.timestamp;

      return newState;

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
