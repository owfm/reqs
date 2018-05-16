import React from 'react';
import { Router, Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { history } from '../_helpers';

import { alertActions, reqActions } from '../_actions';

import { PrivateRoute, TestPage } from '../_components';

import { HomePage } from '../HomePage';
import { LoginPage } from '../LoginPage';
import { RegisterPage } from '../RegisterPage';
import { DisplayWeekContainer } from '../DisplayWeek';
import { ReqFullContainer } from '../ReqFull';
import { Navigation, Logout } from '../_components';

import Snackbar from 'material-ui/Snackbar';

class App extends React.Component {
    constructor(props) {
        super(props);

        const { dispatch } = this.props;
        history.listen((location, action) => {
            // clear alert on location change
            // dispatch(alertActions.clear());
        });
    }

    componentDidMount() {
    }

    render() {
        const { alerts, authentication } = this.props;

        return (
          <div>

            <Snackbar
              open={alerts.open}
              message={alerts.message}
              autoHideDuration={4000}
            />

            <Router history={history}>
                <div>
                    <PrivateRoute exact path="/" component={HomePage} />
                    <PrivateRoute exact path="/test" component={TestPage} />
                    <PrivateRoute exact path="/requisition/:id" component={ReqFullContainer} />
                    <PrivateRoute exact path="/week" component={DisplayWeekContainer} />

                    <Route path="/login" component={LoginPage} />
                    <Route path="/register" component={RegisterPage} />
                    <Route path="/logout" component={Logout} />

                </div>
            </Router>
          </div>
        );
    }
}

function mapStateToProps(state) {
    const { alerts, authentication } = state;
    return {
        alerts,
        authentication
    };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App };
