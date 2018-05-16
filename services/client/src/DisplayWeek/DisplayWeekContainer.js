import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';

import { alertActions, reqActions } from '../_actions';
import { reqService } from '../_services';
import { DisplayWeek } from './DisplayWeek';

import moment from 'moment';

class DisplayWeekContainer extends React.Component {

  constructor(props) {
    super(props);

    const { dispatch } = this.props;
    history.listen((location, action) => {
        // clear alert on location change
        dispatch(alertActions.clear());
    });
  }

  componentDidMount() {

    // TODO: WORK OUT HOW TO CHECK IF IT IS NECESSARY TO FETCH MORE DATA

    if (reqService.reqsAreStale) {
      this.props.dispatch(reqActions.getReqs('01-09-17', '14-05-18', false));
    }

  }

  render() {


      const { reqs, lessons, school } = this.props;

      // school have different numbers of periods - get an array of period numbers from school preferences
      const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

      return (
        reqs.fetched ? <DisplayWeek reqs={reqs} periods={periods} /> : <div>Loading...</div>
      )
  }
}

function mapStateToProps(state) {
    const { reqs, school, lessons } = state;
    return {
      reqs,
      school,
      lessons
    };
}

const connectedDisplayWeekContainer = connect(mapStateToProps)(DisplayWeekContainer);
export { connectedDisplayWeekContainer as DisplayWeekContainer };
