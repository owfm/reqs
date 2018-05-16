import { reqConstants } from '../_constants';
import { reqService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';

export const reqActions = {
    getReqs,
    getReq
};

function getReqs(from, to, all=false) {

  return dispatch => {

    dispatch(request())

    reqService.getReqs(from, to, all)
      .then(
        response => {
          dispatch(success(response.data.data));
          dispatch(alertActions.flash('Reqs loaded successfully.'));
        },
        error => {dispatch(alertActions.flash(error.message))}
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
                    // TODO: BROWSER HISTORY HERE
                    // history.push(`/req/${id}`);
                },
                error => {
                    dispatch(failure(error.response.data.message));
                    dispatch(alertActions.error(error.response.data.message));
                }
            );
    };

    function request(id) { return { type: reqConstants.REQ_REQUEST, id } }
    function success(req) { return { type: reqConstants.REQ_SUCCESS, req } }
    function failure(error) { return { type: reqConstants.REQ_FAILURE, error } }
}
