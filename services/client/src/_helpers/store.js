import { createStore, applyMiddleware } from 'redux';
import {composeWithDevTools} from 'redux-devtools-extension/developmentOnly';
import thunk from 'redux-thunk';
import { createLogger } from 'redux-logger';


import rootReducer from '../_reducers';
import throttle from 'lodash/throttle';

import { loadState, saveState } from './localStorage';

const logger = createLogger({
	collapsed: true,
	diff: true
});

export const store = createStore(
    rootReducer,
    loadState(),
    composeWithDevTools(
      applyMiddleware(thunk, logger)
    )
);

store.subscribe(throttle(() => {
  saveState(store.getState());
}, 1000))
