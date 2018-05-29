import { reqConstants, appConstants } from '../_constants';
import { filterActions } from '../_actions';
import { reqService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';
import moment from 'moment';

export const reqActions = {
  getReqs,
  getReq,
  reqToggleEdit,
  getVisibleSessions,
  getWbStamp,
  stale
};

const reqToggleEdit = () => {
  type: reqConstants.REQS_EDIT_TOGGLE
}

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
        dispatch(alertActions.flash(error.message))}
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
          dispatch(failure(error.message));
        }
      );
  };

  function request(id) { return { type: reqConstants.REQ_REQUEST, id } }
  function success(req) { return { type: reqConstants.REQ_SUCCESS, req } }
  function failure(error) { return { type: reqConstants.REQ_FAILURE, error } }
}

function stale(lastupdated){
  return lastupdated ? moment().diff(moment(lastupdated)) > appConstants.staleMilliseconds : true;
}


function getWbStamp(currentWbStamp){
  return moment(currentWbStamp).format(appConstants.dateFormat);
}


function getVisibleSessions(state) {
  const { filters, reqs, lessons } = state;
  const { currentWbStamp } = filters;

  const reqsSessions = reqs[currentWbStamp] ? [...reqs[currentWbStamp].items] : []
  const lessonSessions = lessons.items.filter(l => l.week === filters.weekNumber);
  return [...reqsSessions, ...lessonSessions];
}
