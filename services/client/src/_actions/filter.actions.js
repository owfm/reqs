import { filterConstants, appConstants } from '../_constants';
import moment from 'moment';

export const filterActions = {
  forwardWeek,
  backwardWeek,
  getWbStampFromDate,
  setSiteFilter,
  setCurrentWeek,
  setStatusFilter,
  clearSiteFilter,
  clearStatusFilter,
  clearAllFilters,
  setWeek
}

function fetchWeekNumber(date) {

}

function setCurrentWeek(date) {

  if ( !moment(date).isValid() ) {
    throw new Error('Expected date in setCurrentWeek')
  }

  const currentWbStamp = getWbStampFromDate(moment(date));

  return {
    type: filterConstants.SET_WB_STAMP,
    currentWbStamp
  }

}

function setWeek(weekNumber) {
  return {
    type: filterConstants.SET_WEEK,
    weekNumber
  }

}

function forwardWeek() {

  return {
    type: filterConstants.FORWARD_WEEK
  }
}

function backwardWeek() {
  return {
    type: filterConstants.BACKWARD_WEEK
  }
}

function setSiteFilter(site) {
  return {
    type: filterConstants.SET_SITE,
    site
  }
}

function setStatusFilter(status) {
  return {
    type: filterConstants.SET_STATUS,
    status
  }
}

function clearSiteFilter() {
  return {
    type: filterConstants.CLEAR_SITE,
  }
}

function clearStatusFilter() {
  return {
    type: filterConstants.CLEAR_STATUS,
  }
}

function clearAllFilters() {
  return {
    type: filterConstants.CLEAR_ALL,
  }
}


function getWbStampFromDate(date) {

  const weekdayNo = date.isoWeekday();

  if (weekdayNo === 6 || weekdayNo === 7) {
    const shift = 8 - weekdayNo;
    return date.add(shift, 'days').format(appConstants.dateFormat);

  } else {
    const shift = weekdayNo - 1;
    return date.subtract(shift, 'days').format(appConstants.dateFormat);
  }

}
