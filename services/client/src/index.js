import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import { store } from './_helpers';

import { Provider } from 'react-redux';

import { App } from './App/App';
import AdminPreferences from './components/AdminPreferences';

render((
  <Provider store={store}>
    <Router>
    <MuiThemeProvider>
        <App/>
    </MuiThemeProvider>
  </Router>
</Provider>
), document.getElementById('root'))
