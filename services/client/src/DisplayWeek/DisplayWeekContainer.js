import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';

import { alertActions, reqActions } from '../_actions';
import { DisplayWeek } from './DisplayWeek';

import moment from 'moment';

class DisplayWeekContainer extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      reqsFromLocalStorage: null
    }

    const { dispatch } = this.props;
    history.listen((location, action) => {
        // clear alert on location change
        dispatch(alertActions.clear());
    });
  }

  componentDidMount() {

    const reqsFromLocalStorage = JSON.parse(localStorage.getItem('reqs'))

    if (reqsFromLocalStorage) {
      this.setState({reqsFromLocalStorage})
    }

    const { reqs } = this.props;

    // TODO: WORK OUT HOW TO CHECK IF IT IS NECESSARY TO FETCH MORE DATA

    if (!reqs.items) {
      this.props.dispatch(reqActions.getReqs('01-09-17', '14-05-18', false));
    }

  }

  render() {
      let { reqs } = this.props;
      let { reqsFromLocalStorage } = this.state;

      const school = JSON.parse(localStorage.getItem('school'));
      const periods = Object.keys(school.preferences.period_start_times).map(p => parseInt(p))

      return (
        reqs.fetched ? <DisplayWeek reqs={reqs} periods={periods} /> : <div>Loading...</div>
      )
  }
}

function mapStateToProps(state) {
    const { reqs } = state;
    return {
      reqs
    };
}

const connectedDisplayWeekContainer = connect(mapStateToProps)(DisplayWeekContainer);
export { connectedDisplayWeekContainer as DisplayWeekContainer };
