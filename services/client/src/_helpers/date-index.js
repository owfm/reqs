import { appConstants } from '../_constants';
import { filterActions } from '../_actions';
import moment from 'moment';

export function getWbStamp(date=null) {

	let dateCpy = date;

  if (!date || !date.isValid()) {
    dateCpy = moment()
  }

  return filterActions.getWbStampFromDate(moment(dateCpy)).format(appConstants.dateFormat);
}
