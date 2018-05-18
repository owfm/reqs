import { reqConstants } from '../_constants';
import { reqService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';
import moment from 'moment';

export const reqActions = {
  getReqs,
  getReq,
  reqToggleEdit,
  reqsAreStale,
  getVisibleSessions
};

const reqToggleEdit = () => {
  type: reqConstants.REQS_EDIT_TOGGLE
}

function getReqs(from, to, all=false) {

  return dispatch => {

    dispatch(request())

    reqService.getReqs(from, to, all)
    .then(
      response => {
        console.log('ACTIONS RESPONSE OK');
        dispatch(success(response.data.data));
        dispatch(alertActions.flash('Reqs loaded successfully.'));
      },
      error => {
        console.error(error);
        console.log('ACTIONS RESPONSE FAIL');

        dispatch(alertActions.flash(error.message))}
    );

  }

  function request() { return { type: reqConstants.REQS_REQUEST } }
  function success(items) { return { type: reqConstants.REQS_SUCCESS, items } }
  function failure(error) { return { type: reqConstants.REQS_FAILURE, error } }

}

function getReq(id) {
  return dispatch => {

    dispatch(request({ id }));

    reqService.getReq(id)
      .then(
        req => {
          dispatch(success(req));
        },
        error => {
          console.log(error);
          dispatch(failure(error.message));
        }
      );
  };

  function request(id) { return { type: reqConstants.REQ_REQUEST, id } }
  function success(req) { return { type: reqConstants.REQ_SUCCESS, req } }
  function failure(error) { return { type: reqConstants.REQ_FAILURE, error } }
}

function reqsAreStale(reqs) {

  return true;

  // if no items in reqs state, set stale to trigger fetch from server.
  if (reqs.items.length === 0) {
    return true;
  }
  return moment().diff(reqs.updatedOn, 'seconds') > 1000;
};


function getVisibleSessions(state) {
  const { reqs, lessons } = state;

  return [];
  return [...reqs.items, ...lessons.items]
  // return [...state.reqs.items, ...state.lessons.items];
}
