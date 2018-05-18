import { filterConstants } from '../_constants';

export const filterActions = {
  forwardWeek,
  backwardWeek,
  getWbNumberFromDate
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


function getWbNumberFromDate(date) {

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
