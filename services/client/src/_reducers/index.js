import { combineReducers } from 'redux';
import { authentication } from './authentication.reducer';
import { registration } from './registration.reducer';
import { reqs } from './reqs.reducer';
import { alerts } from './alerts.reducer';
import { lessons } from './lessons.reducer';
import { school } from './school.reducer';


const rootReducer = combineReducers({
  authentication,
  registration,
  reqs,
  school,
  alerts,
  lessons
});

export default rootReducer;
