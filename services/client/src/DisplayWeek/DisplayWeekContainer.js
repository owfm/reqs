import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';
import { alertActions, reqActions, filterActions } from '../_actions';
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

    const { reqsAreStale } = this.props;

    if (reqsAreStale) {
      this.props.dispatch(reqActions.getReqs('01-09-17', '14-05-18', false));
    }

  }

  render() {

      const { sessions = [], school, reqsLoading } = this.props;


      // school have different numbers of periods - get an array of period numbers from school preferences
      const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

      return (


        <div>
          <button onClick={()=>this.props.dispatch(filterActions.forwardWeek())}>Forward Week</button>
          <button onClick={()=>this.props.dispatch(filterActions.backwardWeek())}>Backward Week</button>
          {moment(this.props.filters.currentWbBeginningDate).format('Y-M-D')}

          {reqsLoading ? <div>Loading...</div> : <DisplayWeek sessions={sessions} periods={periods} />}
        </div>
      )
  }
}

function mapStateToProps(state) {

  const { school, reqs, filters } = state;

  const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))


  return {
    periods,
    school: school,
    sessions: reqActions.getVisibleSessions(state),
    reqsAreStale: reqActions.reqsAreStale(reqs),
    reqsLoading: reqs.loading,
    filters
  };
}

const connectedDisplayWeekContainer = connect(mapStateToProps)(DisplayWeekContainer);
export { connectedDisplayWeekContainer as DisplayWeekContainer };
