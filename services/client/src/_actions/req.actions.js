import { reqConstants, appConstants } from '../_constants';
import { reqService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';
import moment from 'moment';

export const reqActions = {
  getReqs,
  getReq,
  reqToggleEdit,
  reqsAreStale,
  getVisibleSessions,
  getWbStamp
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
        dispatch(success(wb, response.data.data));
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

function reqsAreStale(reqs) {

  return true;

  // if no items in reqs state, set stale to trigger fetch from server.
  if (reqs.items.length === 0) {
    return true;
  }
  return moment().diff(reqs.updatedOn, 'seconds') > 1000;
};


function getVisibleSessions(state) {

  const { reqs, lessons, filters } = state;
  const { currentWbStamp } = filters;
  const wbStamp = moment(currentWbStamp).format(appConstants.dateFormat);

  if (!reqs.hasOwnProperty(wbStamp)) {
    return [...lessons.items] || [];
  }

  const sessions = [...reqs[wbStamp].items, ...lessons.items]

  return sessions.filter(s => s.week === filters.currentWeek);

  // const reqSessions = reqs[wbStamp]['items'];
  // console.log(reqSessions);

  // return sessions.filter(s => s.week === filters.currentWeek)
  // return [];
}

function getWbStamp(currentWbStamp){
  return moment(currentWbStamp).format(appConstants.dateFormat);
}


function getVisibleSessions(state) {
  const { filters, reqs, lessons } = state;
  const { currentWbStamp } = filters;

  const reqsSessions = reqs[currentWbStamp] ? [...reqs[currentWbStamp].items] : []
  const lessonSessions = lessons.items.filter(l => l.week === filters.currentWeek);
  return [...reqsSessions, ...lessonSessions];
}


// function dateFilter (sessions) {
//   return sessions
//   .filter(session => {
//     if (session.type === 'requisition') {
//       const reqDate = parseReqTime(session.time, 'date');
//       const currentWbStamp = moment(this.state.currentWbStamp, 'DD-MM-YY');
//       return reqDate.isSameOrAfter(currentWbStamp) &&
//           reqDate.isSameOrBefore(currentWbStamp.add(5, 'days'))
//
//     } else if (session.type === 'lesson') {
//       return session.week === this.state.weekNumber;
//     }
//   })
// }
