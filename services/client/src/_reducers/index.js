import { combineReducers } from 'redux';
import { authentication } from './authentication.reducer';
import { registration } from './registration.reducer';
import { reqs } from './reqs.reducer';
import { alerts } from './alerts.reducer';
import { lessons } from './lessons.reducer';
import { school } from './school.reducer';
import { filters } from './filter.reducer';




const appReducer = combineReducers({
  authentication,
  registration,
  reqs,
  school,
  alerts,
  lessons,
  filters
});

const rootReducer = (state, action) => {
  if (action.type === 'USERS_LOGOUT') {
    state = undefined
  }
  return appReducer(state, action)
}

export default rootReducer;
