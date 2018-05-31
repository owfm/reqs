import React from 'react';
import { withRouter } from 'react-router-dom';
import { Redirect } from 'react-router';

import { connect } from 'react-redux';

import { alertActions, reqActions, filterActions } from '../_actions';
import { appConstants } from '../_constants';

import { DisplayWeek } from './DisplayWeek';

import moment from 'moment';

class DisplayWeekContainer extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      redirect: false,
      redirectTo: null
    }

    const { dispatch } = this.props;

    this.props.history.listen((location, action) => {
        this.setState({redirect: false, redirectTo: null})
    });

    this.goToCurrentWeek = this.goToCurrentWeek.bind(this);
    this.forwardWeek = this.forwardWeek.bind(this);
    this.backWeek = this.backWeek.bind(this);
    this.goToCurrentWeek = this.goToCurrentWeek.bind(this);


  }

  componentDidMount() {

    const { lastupdated, currentWbStamp } = this.props;
    const wb = currentWbStamp;

    // fetch if reqs are stale
    if ( reqActions.stale(lastupdated) ) {
      this.props.dispatch(reqActions.getReqs(wb, false));
    }

  }

  componentDidUpdate(prevProps) {

    const { dispatch, lastupdated, currentWbStamp } = this.props;

    // if week has changed, fetch any new or edited reqs relating to the current week
    if ( currentWbStamp !== prevProps.currentWbStamp ) {
      if ( reqActions.stale(lastupdated) ) {
        dispatch(reqActions.getReqs(currentWbStamp, lastupdated, false));
      }
    }
  }

  goToCurrentWeek = () => {
    const currentWbStamp = filterActions.getWbStampFromDate(moment());
    this.setState({
      redirect: true,
      redirectTo: `/week/${moment(currentWbStamp).format(appConstants.dateFormat)}`
    })
  }

  forwardWeek = () => {

    const { currentWbStamp } = this.props;

    this.setState({
        redirect: true,
        redirectTo: `/week/${moment(currentWbStamp).add(7, 'days').format(appConstants.dateFormat)}`
    });
  }

  backWeek = () => {

    const { currentWbStamp } = this.props;

    this.setState({
        redirect: true,
        redirectTo: `/week/${moment(currentWbStamp).subtract(7, 'days').format(appConstants.dateFormat)}`
    });
  }


  render() {

      const { redirect, redirectTo } = this.state;

      if ( redirect ) {
        return <Redirect push to={redirectTo} />
      }

      const { school, sessions, reqsLoading, currentWbStamp } = this.props;

      // school have different numbers of periods - get an array of period numbers from school preferences
      const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

      return (


        <div>
          <button onClick={()=>this.forwardWeek()}>Forward Week</button>
          <button onClick={()=>this.backWeek()}>Backward Week</button>
          <button onClick={()=>this.goToCurrentWeek()}>Current Week</button>
          <button onClick={()=>this.props.dispatch(filterActions.setWeek(1))}>Set Week 1</button>
          <button onClick={()=>this.props.dispatch(filterActions.setWeek(2))}>Set Week 2</button>

          {moment(this.props.currentWbStamp).format('Y-M-D')}
          Week number {this.props.filters.currentWeek}.


          {reqsLoading ? <div>Loading...</div> : <DisplayWeek currentWbStamp={currentWbStamp} sessions={sessions} periods={periods} />}
        </div>
      )
  }
}

function mapStateToProps(state, ownProps) {

  const { school, reqs, filters } = state;
  const { currentWbStamp } = ownProps.match.params;

  const periods = Object.keys(school.school.preferences.period_start_times).map(p => parseInt(p))

  const lastupdated = reqs[currentWbStamp] ? moment(reqs[currentWbStamp].lastupdated).format(appConstants.timeStampFormat) : null;

  return {
    periods,
    school,
    sessions: reqActions.getVisibleSessions(state, currentWbStamp),
    reqsLoading: reqs.loading,
    filters,
    lastupdated,
    currentWbStamp
  };
}

const connectedDisplayWeekContainer = withRouter(connect(mapStateToProps)(DisplayWeekContainer));
export { connectedDisplayWeekContainer as DisplayWeekContainer };
