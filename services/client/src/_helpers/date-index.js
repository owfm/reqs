import { appConstants } from '../_constants';
import { filterActions } from '../_actions';
import moment from 'moment';

export function getWbStamp(date=null) {

  if (!date || !date.isValid()) {
    const date = moment()
  }

  return filterActions.getWbStampFromDate(moment(date)).format(appConstants.dateFormat);
}
