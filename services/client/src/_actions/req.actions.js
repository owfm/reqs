import { reqConstants, appConstants } from '../_constants';
import { filterActions } from '../_actions';
import { reqService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';
import moment from 'moment';

export const reqActions = {
  getReqs,
  getReq,
  postNewReq,
  postReqUpdate,
  stale,
  getWbStamp,
  getVisibleSessions,
};


function getReqs(wb, lastupdated=null, all=false) {

  return dispatch => {

    dispatch(request())

    reqService.getReqs(wb, lastupdated, all)
    .then(
      response => {
        dispatch(success(wb, response.data.items));

        // TODO HANDLE HOLIDAYS

        dispatch(filterActions.setWeek(response.data.weeknumber));

      },
      error => {
        dispatch(failure(error));
        dispatch(alertActions.flash(error.response.data.message))}
    );

  }

  function request() { return { type: reqConstants.REQS_REQUEST } }

  function success(wbStamp, items) {
    return {
      type: reqConstants.REQS_SUCCESS,
      timestamp: moment(),
      wbStamp,
      items,
    }
  }
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
          dispatch(failure(error.response.data.message));
        }
      );
  };

  function request(id) { return { type: reqConstants.REQ_REQUEST, id } }
  function success(req) { return { type: reqConstants.REQ_SUCCESS, req } }
  function failure(error) { return { type: reqConstants.REQ_FAILURE, error } }
}

function postNewReq(reqData) {


    return dispatch => {

        dispatch(request());

        reqService.postNewReq(reqData)
            .then(
                response => {

                    dispatch(success(reqData.currentWbStamp, response.data.data));
                    dispatch(alertActions.flash(response.data.message))
                    history.goBack();
                },
                error => {
                    dispatch(failure(error.message));
                    dispatch(alertActions.flash(error.data.message || 'Something went wrong.'));
                }
            );
    };

    function request() { return { type: reqConstants.POST_REQUEST } }
    function success(currentWbStamp, newReq) { return { type: reqConstants.POST_SUCCESS, currentWbStamp, newReq } }
    function failure(error) {return { type: reqConstants.POST_FAILURE, error } }

}

function postReqUpdate(updatedReqInfo) {
  return function(dispatch){
    dispatch(request());

    reqService.postReqUpdate(updatedReqInfo)
      .then(
        response => {
          dispatch(success(updatedReqInfo.currentWbStamp, response.data.data));
          dispatch(alertActions.flash(response.data.message))
          history.goBack();
        },
        error => {
          console.log(error);
          dispatch(failure());
          dispatch(alertActions.flash(error.response.data.message || 'Something went wrong.'));
        }
      );
  }
  function request() { return { type: reqConstants.UPDATE_REQUEST } }
  function success(currentWbStamp, updatedReq) { return { type: reqConstants.UPDATE_SUCCESS, currentWbStamp, updatedReq } }
  function failure() {return { type: reqConstants.UPDATE_FAILURE } }

}

function stale(lastupdated){
  return lastupdated ? moment().diff(moment(lastupdated)) > appConstants.staleMilliseconds : true;
}

function getWbStamp(currentWbStamp){
  return moment(currentWbStamp).format(appConstants.dateFormat);
}

function getVisibleSessions(state, currentWbStamp) {

  const { filters, reqs, lessons } = state;
  const { sites, status } = filters;

  const reqsSessions = reqs[currentWbStamp] ? [...reqs[currentWbStamp].items] : []
  const lessonSessions = lessons.items.filter(l => l.week === filters.weekNumber);

  // remove lessons that have reqs assigned
  const reqLessonIds = reqsSessions.map(req => req.lesson_id);
  const lessonsToReturn = lessonSessions.filter(s => !reqLessonIds.includes(s.id));

  let reqsToReturn = [...reqsSessions];

  // apply filters if necessary
  if ( status ) {
    // active reqs are those that are not done and not marked as having problems
    if ( status === 'active' ) {
      reqsToReturn = reqsToReturn.filter(s => (s.isDone === false && s.hasIssue === false))
    } else {
      reqsToReturn = reqsToReturn.filter(s => s[status] === true)
    }
  }

  const sessions = [...reqsToReturn, ...lessonsToReturn]

  if ( sites.length > 0 ) {
    return sessions.filter(s => sites.includes(s.room.site.name))
  }

  return sessions;


  // return [...toReturn, ...lessonsReqsAssignedRemoved];
}
