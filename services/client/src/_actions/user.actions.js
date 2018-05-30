import { userConstants, schoolConstants, lessonConstants } from '../_constants';
import { userService } from '../_services';
import { alertActions } from './';
import { history } from '../_helpers';


export const userActions = {
    login,
    logout,
    register,
    delete: _delete
};

function login(email, password) {
    return dispatch => {

        dispatch(request({ email }));

        userService.login(email, password)
            .then(
                response => {

                    dispatch(success_user(response.user));
                    dispatch(success_school(response.school));

                    // lessons only returned if user is teacher
                    if (response.lessons) {
                      dispatch(success_lessons(response.lessons));
                    }

                    history.push('/');
                },
                error => {
                    dispatch(failure());
                    dispatch(alertActions.error(error.message || 'Something went wrong.'));
                }
            );
    };

    function request(user) { return { type: userConstants.LOGIN_REQUEST, user } }
    function success_user(user) { return { type: userConstants.LOGIN_SUCCESS, user } }
    function success_school(school) {return { type: schoolConstants.SCHOOL_SUCCESS, school } }
    function success_lessons(items) { return { type: lessonConstants.LESSONS_SUCCESS, items } }

    function failure() { return { type: userConstants.LOGIN_FAILURE } }
}

function logout() {
    userService.logout();
    return { type: userConstants.LOGOUT };
}

function register(user) {
    return dispatch => {
        dispatch(request(user));

        userService.register(user)
            .then(
                user => {
                    dispatch(success());
                    history.push('/login');
                    dispatch(alertActions.success('Registration successful'));
                },
                error => {
                    dispatch(failure(error));
                    dispatch(alertActions.error(error.message || 'Something went wrong'));
                }
            );
    };

    function request(user) { return { type: userConstants.REGISTER_REQUEST, user } }
    function success(user) { return { type: userConstants.REGISTER_SUCCESS, user } }
    function failure(error) { return { type: userConstants.REGISTER_FAILURE, error } }
}


// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    return dispatch => {
        dispatch(request(id));

        userService.delete(id)
            .then(
                user => {
                    dispatch(success(id));
                },
                error => {
                    dispatch(failure(id, error));
                }
            );
    };

    function request(id) { return { type: userConstants.DELETE_REQUEST, id } }
    function success(id) { return { type: userConstants.DELETE_SUCCESS, id } }
    function failure(id, error) { return { type: userConstants.DELETE_FAILURE, id, error } }
}
