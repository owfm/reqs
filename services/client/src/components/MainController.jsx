import React from 'react';
import { getReqs, getSchool, getWeekNumber } from '../utils/Helpers';
import MainDisplay from './MainDisplay';
import ReqFull from './ReqFull';
import Loading from './Loading';
import Modal from 'react-modal';
import { shadowHoverStyle } from './Styles';
import moment from 'moment';
import Navigation from './Navigation';


class MainController extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      modalOpen: false,
      currentWbDate: null,
      modalSessionObj: null,
      school: null,
      sessions: null,
      filters: {
        isDone: true,
        hasIssue: true,
        sites: null
      }
    }

    this.handleFilterToggle = this.handleFilterToggle.bind(this);
    this.handleModalOpen = this.handleModalOpen.bind(this);
    this.handleModalClose = this.handleModalClose.bind(this);
    this.handleSetModalObject = this.handleSetModalObject.bind(this);
    this.handleWeekChange = this.handleWeekChange.bind(this);
    this.handleRemoveFilter = this.handleRemoveFilter.bind(this);
    this.updateStateWithNewOrEditedReq = this.updateStateWithNewOrEditedReq.bind(this);
  }

  componentDidMount(){
    const now = moment();
    const monday = getWbNumberFromDate(now);
    const monday_str = monday.format('DD-MM-YY');
    this.setState({
      currentWbDate: monday_str
    });

    getWeekNumber(monday.format("DD-MM-YY"))
    .then((res) => {
      this.setState({
        weekNumber: res.data.data
      })
    })
    .catch((err) => console.error(err))

    getReqs().then((res) => {
      this.setState({
        sessions: res.data.data.sessions
      });
    })
    .catch((err) => { console.error(err)});

    getSchool()
    .then((res) => {
      this.setState({
        school: res.data.data
      });
      if (this.state.school.preferences.sites) {
        const siteFilters = {};
        for (let site in this.state.school.sites){
          siteFilters[this.state.school.sites[site].name] = true;
        }
        const state = {...this.state};
        state.filters["sites"] = siteFilters;
        this.setState(
          state
        )
      }

      if (window.localStorage.getItem('filters')) {
        this.setState({
          filters: getFilterStateFromLocalStorage()
        })
      }

    })
    .catch((err) => { console.error(err) });
  };

  handleFilterToggle = (e) => {

    const value = e.target.checked;
    const name = e.target.name;
    var filters = {...this.state.filters};
    (name in filters.sites) ? filters.sites[name] = value : filters[name] = value;

    this.setState({
      filters
    })

    saveFilterStateToLocalStorage(filters);
  }

  handleRemoveFilter (target) {
    var filters = {...this.state.filters};

    if (target === 'ALL') {
      for (var f in filters) {if (f !== 'sites') {filters[f] = true}};
      for (var s in filters.sites) {filters.sites[s] = true};
    } else {
      (target in this.state.filters.sites) ? filters.sites[target] = false : filters[target] = false;
    }

    this.setState({
      filters
    })

    saveFilterStateToLocalStorage(filters);

  }


  dateFilter (sessions) {
    return sessions
    .filter(session => {
      if (session.type === 'requisition') {
        const reqDate = parseReqTime(session.time, 'date');
        const currentWbDate = moment(this.state.currentWbDate, 'DD-MM-YY');
        return reqDate.isSameOrAfter(currentWbDate) &&
            reqDate.isSameOrBefore(currentWbDate.add(5, 'days'))

      } else if (session.type === 'lesson') {
        return session.week === this.state.weekNumber;
      }
    })
  }

  statusFilter (sessions) {
    return sessions
    .filter((session) => {
      if (session.type === 'requisition') {

        if (this.state.filters.isDone && session.isDone){
          return true;
        } else if (this.state.filters.hasIssue && session.hasIssue) {
          return true;
        } else if (!session.hasIssue && !session.isDone ){
          return true;
        }
        return false;
      }     else {
        return true;
      }
    })
  };

  siteFilter (sessions) {
    return sessions.filter(session => {
      const siteName = session.room.site.name;
      const sitesFilter = {...this.state.filters.sites};
      return sitesFilter[siteName];}
    )}

  assignmentFilter (sessions) {
    const reqLessonIds = sessions
    .filter(session => session.type === 'requisition')
    .map(session => session.lesson_id);

    const sessionsWithoutAssignedLessons = sessions.
    filter(session => {
      const check = session.type === 'lesson' && reqLessonIds.includes(session.id);
      return !check;
    })
    return sessionsWithoutAssignedLessons;
  };

  filterController (sessions) {
    const DateFiltered = this.dateFilter(sessions);
    const SiteFiltered = this.siteFilter(DateFiltered);
    const StatusFiltered = this.statusFilter(SiteFiltered);
    const AssignmentFiltered = this.assignmentFilter(StatusFiltered);
    return AssignmentFiltered;
  }

  handleModalOpen = () => {
    this.setState({
      modalOpen: true
    })
  };

  handleModalClose = () => {
    this.setState({
      modalOpen: false
    })
  };

  handleSetModalObject = (modalSessionId, modalSessionType) => {

    const modalSessionObj = this.state.sessions.find(
      session => session.id === modalSessionId && session.type === modalSessionType
    )
    this.setState({
      modalSessionObj
    })

  }

  handleWeekChange = (change) => {

    const oldDateStr = this.state.currentWbDate.toString();
    const newDate = moment(oldDateStr, 'DD-MM-YY').add(change, 'days');
    const newDateStr = newDate.format("DD-MM-YY");
    getWeekNumber(newDateStr)
    .then((res) => {
      this.setState({
        weekNumber: res.data.data
      })
    })
    .catch((err) => console.error(err))

    this.setState({
      currentWbDate: newDateStr
    })
  }

  updateStateWithNewOrEditedReq = (req) => {

    const new_sessions = this.state.sessions.filter(session =>
    !(session.id === req.id && session.type === req.type))

    new_sessions.push(req);
    this.setState({sessions: new_sessions});
  }


  render() {

    if (!(this.props.user && this.state.sessions && this.state.school)) {
      return (
        <div>
            <p>loading in main controller</p>
        <Loading />
      </div>
      )
    }

    const viewFilteredSessions = this.filterController(this.state.sessions);

    return (
      <div>
        <Navigation
          user={this.props.user}
          logoutUser={this.props.logoutUser}
        />

        <Modal
          style={shadowHoverStyle}
          isOpen={this.state.modalOpen}
          >
            <ReqFull
              updateStateWithNewOrEditedReq={this.updateStateWithNewOrEditedReq}
              currentWbDate={this.state.currentWbDate}
              emitSnackbar={this.props.emitSnackbar}
              roleCode={this.props.user.role_code}
              req={this.state.modalSessionObj}
              handleModalClose={this.handleModalClose}
            />
        </Modal>

        <MainDisplay
          filters={this.state.filters}
          weekNumber={this.state.weekNumber}
          school={this.state.school}
          sessions={viewFilteredSessions}
          user={this.props.user}
          handleRemoveFilter={this.handleRemoveFilter}
          handleFilterToggle={this.handleFilterToggle}
          handleSetModalObject={this.handleSetModalObject}
          handleModalOpen={this.handleModalOpen}
          handleSetModalType={this.handleSetModalType}
          handleWeekChange={this.handleWeekChange}
          emitSnackbar={this.props.emitSnackbar}
          currentWbDate={this.state.currentWbDate}
        />

        </div>
      )
    }

  }


  export default MainController;

  const getWbNumberFromDate = (date) => {

    // if in week, go back to monday.
    // if weekend, jump to next Monday

    // isoweekday, 1=Monday, 2=Tuesday.... 6=Saturday, 7=Sunday

    const weekdayNo = date.isoWeekday();

    if (weekdayNo === 6 || weekdayNo === 7) {
      const shift = 8 - weekdayNo;
      return date.add(shift, 'days');

    } else {
      const shift = weekdayNo - 1;
      return date.subtract(shift, 'days');
    }

  }

  const parseReqTime = (time, which) => {

    const date_and_time = time.split(' ');

    switch(which) {
      case 'date':
      return moment(date_and_time[0])
      case 'time':
      return moment(date_and_time[1])
      default:
      console.error('parseReqTime called with wrong arguments.');
    }

  }

  const saveFilterStateToLocalStorage = (filters) => {
    window.localStorage.setItem('filters', JSON.stringify(filters));
  }

  const getFilterStateFromLocalStorage = () => {
    return JSON.parse(window.localStorage.getItem('filters'));
  }
