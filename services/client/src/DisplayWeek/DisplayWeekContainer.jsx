import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import { withRouter } from 'react-router-dom';
import { Redirect } from 'react-router';

import { connect } from 'react-redux';

import { FilterSelect } from '../_components';
import { reqActions, filterActions } from '../_actions';
import { appConstants } from '../_constants';

import DisplayWeek from './DisplayWeek';


class DisplayWeekContainer extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      redirect: false,
      redirectTo: null,
    };

    this.props.history.listen(() => {
      this.setState({ redirect: false, redirectTo: null });
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
    if (reqActions.stale(lastupdated)) {
      this.props.dispatch(reqActions.getReqs(wb, false));
    }
  }

  componentDidUpdate(prevProps) {
    const { dispatch, lastupdated, currentWbStamp } = this.props;

    // if week has changed, fetch any new or edited reqs relating to the current week
    if (currentWbStamp !== prevProps.currentWbStamp) {
      if (reqActions.stale(lastupdated)) {
        dispatch(reqActions.getReqs(currentWbStamp, lastupdated, false));
      }
    }
  }

  goToCurrentWeek() {
    const currentWbStamp = filterActions.getWbStampFromDate(moment());
    this.setState({
      redirect: true,
      redirectTo: `/week/${moment(currentWbStamp).format(appConstants.dateFormat)}`,
    });
  }

  forwardWeek() {
    const { currentWbStamp } = this.props;

    this.setState({
      redirect: true,
      redirectTo: `/week/${moment(currentWbStamp).add(7, 'days').format(appConstants.dateFormat)}`,
    });
  }

  backWeek() {
    const { currentWbStamp } = this.props;

    this.setState({
      redirect: true,
      redirectTo: `/week/${moment(currentWbStamp).subtract(7, 'days').format(appConstants.dateFormat)}`,
    });
  }

  render() {
    const { redirect, redirectTo } = this.state;
    if (redirect) {
      return <Redirect push to={redirectTo} />;
    }

    const {
      sessions, reqsLoading, currentWbStamp, periods,
    } = this.props;

    return (

      <div>
        <button onClick={() => this.forwardWeek()}>Forward Week</button>
        <button onClick={() => this.backWeek()}>Backward Week</button>
        <button onClick={() => this.goToCurrentWeek()}>Current Week</button>
        <button onClick={() => this.props.dispatch(filterActions.setWeek(1))}>Set Week 1</button>
        <button onClick={() => this.props.dispatch(filterActions.setWeek(2))}>Set Week 2</button>

        {moment(this.props.currentWbStamp).format('Y-M-D')}
          Week number {this.props.filters.currentWeek}.


        {reqsLoading ?
          <div>Loading...</div> :
          <DisplayWeek currentWbStamp={currentWbStamp} sessions={sessions} periods={periods} />
        }

        <FilterSelect />

      </div>
    );
  }
}

function mapStateToProps(state, ownProps) {
  const { school, reqs, filters } = state;
  const { currentWbStamp } = ownProps.match.params;

  const periods = Object.keys(school.school.preferences.period_start_times)
    .map(p => parseInt(p, 10));

  const lastupdated = reqs[currentWbStamp] ?
    moment(reqs[currentWbStamp].lastupdated).format(appConstants.timeStampFormat) :
    null;

  return {
    periods,
    sessions: reqActions.getVisibleSessions(state, currentWbStamp),
    reqsLoading: reqs.loading,
    filters,
    lastupdated,
    currentWbStamp,
  };
}

export default withRouter(connect(mapStateToProps)(DisplayWeekContainer));

DisplayWeekContainer.defaultProps = {
  sessions: [],
  reqsLoading: false,
  lastupdated: null,
};

DisplayWeekContainer.propTypes = {
  dispatch: PropTypes.func.isRequired,
  periods: PropTypes.arrayOf(PropTypes.number).isRequired,
  sessions: PropTypes.arrayOf(PropTypes.shape({
    title: PropTypes.string.isRequired,
    equipment: PropTypes.string,
    notes: PropTypes.string,
  })),
  reqsLoading: PropTypes.bool,
  lastupdated: PropTypes.number,
  currentWbStamp: PropTypes.number.isRequired,


};
