import { filterConstants, appConstants } from '../_constants';

export const filterActions = {
  forwardWeek,
  backwardWeek,
  getWbStampFromDate,
  setSiteFilter,
  setStatusFilter,
  clearSiteFilter,
  clearStatusFilter,
  clearAllFilters,
  setWeek
}

function fetchWeekNumber(date) {

}

function setWeek(week) {
  return {
    type: filterConstants.SET_WEEK,
    week
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

  // if in week, go back to monday.
  // if weekend, jump to next Monday

  // isoweekday, 1=Monday, 2=Tuesday.... 6=Saturday, 7=Sunday

  const weekdayNo = date.isoWeekday();

  if (weekdayNo === 6 || weekdayNo === 7) {
    const shift = 8 - weekdayNo;
    return date.add(shift, 'days').format(appConstants.dateFormat);

  } else {
    const shift = weekdayNo - 1;
    return date.subtract(shift, 'days').format(appConstants.dateFormat);
  }

}
