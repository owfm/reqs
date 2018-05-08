import { combineReducers } from 'redux';
import { reqs } from './req.reducer';
import { authentication } from './authentication.reducer';
import { registration } from './registration.reducer';
import { alert } from './alert.reducer';

const rootReducer = combineReducers({
  authentication,
  registration,
  reqs,
  alert
});

export default rootReducer;
