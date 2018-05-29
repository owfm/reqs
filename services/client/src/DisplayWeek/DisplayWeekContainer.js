import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';
import { alertActions, reqActions, filterActions } from '../_actions';
import { reqService } from '../_services';
import { appConstants } from '../_constants';

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

    this.goToCurrentWeek = this.goToCurrentWeek.bind(this);
  }

  componentDidMount() {

    const { lastupdated, filters } = this.props;

    const wb = moment(filters.currentWbStamp).format(appConstants.dateFormat);

    // fetch if reqs are stale
    if ( reqActions.stale(lastupdated) ) {
      this.props.dispatch(reqActions.getReqs(wb, false));
    }

  }

  componentDidUpdate(prevProps){

    const { filters, dispatch, lastupdated } = this.props;
    const { currentWbStamp } = filters;

    // if week has changed, fetch any new or edited reqs relating to the current week
    if ( currentWbStamp !== prevProps.filters.currentWbStamp ) {
      if ( reqActions.stale(lastupdated) ) {
        dispatch(reqActions.getReqs(currentWbStamp, lastupdated, false));
      }

    }

  }

  goToCurrentWeek = () => {
    const { dispatch } = this.props;
    const now = moment();
    dispatch(filterActions.setCurrentWeek(now));
  }

  render() {

      const { school, sessions, reqsLoading } = this.props;

      // school have different numbers of periods - get an array of period numbers from school preferences
      const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

      const sites = ['Walthamstow', 'Wiseman Upstairs', 'Wiseman Downstairs'];

      return (


        <div>
          <button onClick={()=>this.goToCurrentWeek()}>Go To Current Week</button>
          <button onClick={()=>this.props.dispatch(filterActions.backwardWeek())}>Backward Week</button>
          <button onClick={()=>this.props.dispatch(filterActions.forwardWeek())}>Forward Week</button>

          <button onClick={()=>this.props.dispatch(filterActions.setWeek(1))}>Set Week 1</button>
          <button onClick={()=>this.props.dispatch(filterActions.setWeek(2))}>Set Week 2</button>

          {sites.map(s => {
            <button onClick={()=>this.props.dispatch(filterActions.setSiteFilter(s))}>{s}</button>
          })}
          <button onClick={()=>this.props.dispatch(filterActions.clearSiteFilter())}>Clear Site Filter</button>


          {moment(this.props.filters.currentWbStamp).format('Y-M-D')}


          {reqsLoading ? <div>Loading...</div> : <DisplayWeek sessions={sessions} periods={periods} />}
        </div>
      )
  }
}

function mapStateToProps(state) {

  const { school, reqs, filters } = state;
  const { currentWbStamp } = filters;

  const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

  const lastupdated = reqs[currentWbStamp] ? moment(reqs[currentWbStamp].lastupdated).format(appConstants.timeStampFormat) : null;

  return {
    periods,
    school,
    sessions: reqActions.getVisibleSessions(state),
    reqsLoading: reqs.loading,
    filters,
    lastupdated
  };
}

const connectedDisplayWeekContainer = connect(mapStateToProps)(DisplayWeekContainer);
export { connectedDisplayWeekContainer as DisplayWeekContainer };
