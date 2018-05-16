import React from 'react';
import { Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import { history } from '../_helpers';

import { alertActions, reqActions } from '../_actions';

import { PrivateRoute } from '../_components';

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
            dispatch(alertActions.clear());
        });
    }

    componentDidMount() {
    }

    render() {
        const { alert, dispatch } = this.props;
        return (
          <div>

            <Snackbar
              open={alert.open}
              message={alert.message}
              autoHideDuration={4000}
            />

            <Navigation />


            <Router history={history}>
                <div>
                    <PrivateRoute exact path="/" component={HomePage} />
                    <PrivateRoute path="/week" component={DisplayWeekContainer} />

                    <Route path="/login" component={LoginPage} />
                    <Route path="/register" component={RegisterPage} />
                    <Route path="/logout" component={Logout} />
                    <Route path="/requisition/:id" component={ReqFullContainer} />

                </div>
            </Router>
          </div>
        );
    }
}

function mapStateToProps(state) {
    const { alert, reqs } = state;
    return {
        alert,
        reqs
    };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App };
