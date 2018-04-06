import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


import App from './App.jsx';
import AdminPreferences from './components/AdminPreferences';

ReactDOM.render((
  <Router>

  <MuiThemeProvider>
      <App/>
  </MuiThemeProvider>
</Router>
), document.getElementById('root'))
