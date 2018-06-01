import { filterConstants, appConstants } from '../_constants';
import moment from 'moment';

export const filterActions = {
  getWbStampFromDate,
  setSiteFilter,
  setStatusFilter,
  clearSiteFilter,
  clearStatusFilter,
  clearAllFilters,
  clearAllSiteFilters,
  setWeek
}


function setWeek(weekNumber) {
  return {
    type: filterConstants.SET_WEEK,
    weekNumber
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

function clearSiteFilter(site) {
  return {
    type: filterConstants.CLEAR_SITE,
    site
  }
}

function clearStatusFilter() {
  return {
    type: filterConstants.CLEAR_STATUS
  }
}

function clearAllSiteFilters() {
  return {
    type: filterConstants.CLEAR_ALL_SITES
  }
}

function clearAllFilters() {
  return {
    type: filterConstants.CLEAR_ALL
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
