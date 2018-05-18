import { schoolConstants } from '../_constants';
import { schoolService } from '../_services';
import { alertActions } from './';

export const schoolActions = {
  getWeekNumber,
  reqToggleEdit
};

const reqToggleEdit = () => {
  type: reqConstants.REQS_EDIT_TOGGLE
}


function getWeekNumber(date) {

  return dispatch => {

    dispatch(request())

    schoolService.getWeekNumber(date)
    .then(
      response => {
        dispatch(success(response.data.data));
        dispatch(alertActions.flash('Reqs loaded successfully.'));
      },
      error => {dispatch(alertActions.flash(error.message))}
    );

  }
  function request() { return { type: schoolConstants.SCHOOL_REQUEST } }
  function success(weekNumber) { return { type: schoolConstants.WEEK_SUCCESS, weekNumber } }
  function failure(error) { return { type: schoolConstants.WEEK_FAILURE, error } }

}
