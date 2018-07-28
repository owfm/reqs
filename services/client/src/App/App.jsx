import React from 'react';
import { Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';

import Snackbar from 'material-ui/Snackbar';
import DisplayWeekContainer from '../DisplayWeek';
import ReqFullContainer from '../ReqFull';

import { history } from '../_helpers';
import {
  PrivateRoute,
  TestPage,
  Navigation,
  Logout,
} from '../_components';

import { alertActions } from '../_actions';

import { HomePage } from '../HomePage';
import { LoginPage } from '../LoginPage';
import { RegisterPage } from '../RegisterPage';


class App extends React.Component {
  constructor(props) {
    super(props);

    history.listen((location, action) => {
      // clear alert on location change
      const { dispatch } = this.props;
      dispatch(alertActions.hideNotification());
    });
  }

  componentDidMount() {

  }

  render() {
    const { alerts } = this.props;

    return (
      <div>

        <Snackbar
          open={alerts.open}
          message={alerts.message}
          autoHideDuration={4000}
        />

        <Router history={history}>
          <div>
            <Navigation />

            <PrivateRoute exact path="/" component={HomePage} />
            <PrivateRoute exact path="/test" component={TestPage} />
            <PrivateRoute exact path="/week/:currentWbStamp/" component={DisplayWeekContainer} />
            <PrivateRoute exact path="/week/:currentWbStamp/:type/:id" component={ReqFullContainer} />


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
    authentication,
  };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App };
