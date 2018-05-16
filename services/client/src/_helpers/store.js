import { createStore, applyMiddleware, compose } from 'redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from '../_reducers';
import throttle from 'lodash/throttle';

import { loadState, saveState } from './localStorage';

const loggerMiddleware = createLogger();

export const store = createStore(
    rootReducer,
    loadState(),
    compose(
      applyMiddleware(
        thunkMiddleware,
        loggerMiddleware
      ),
      window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()

    )
);

store.subscribe(throttle(() => {
  saveState(store.getState());
}, 1000))
