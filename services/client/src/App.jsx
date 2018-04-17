import React from 'react';
import { Route, Switch } from 'react-router-dom';
import Snackbar from 'material-ui/Snackbar';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import MainController from './components/MainController';
import { getUser } from './utils/Helpers';
import './App.css';

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      user: null,
      snackbarOpen: false,
      snackbarMsg: '',
      isAuthenticated: false,
      drawerOpen: false
    };
    this.logoutUser = this.logoutUser.bind(this);
    this.loginUser = this.loginUser.bind(this);
    this.emitSnackbar = this.emitSnackbar.bind(this);
    this.openSideBarToggle = this.openSideBarToggle.bind(this);
  }

  componentWillMount() {
    if (window.localStorage.getItem('authToken')) {
      this.setState({ isAuthenticated: true });
    };
  };


  componentDidMount() {
    getUser().then((res) => {
      this.setState({
        user: res.data.data
      });
    })
    .catch((err) => { console.error(err) });
  };


  clearSnackbar = () => {
    this.setState({
      snackbarOpen: false
    })
  }

  emitSnackbar = (msg) => {
    this.setState({
      snackbarOpen: true,
      snackbarMsg: msg
    })

    setTimeout(this.clearSnackbar, 4000);
  }

  openSideBarToggle = () => {
    console.log('toggled');
    this.setState(
      {drawerOpen: !this.state.drawerOpen}
    )
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({});
  };

  loginUser(user, token) {
    window.localStorage.setItem('authToken', token);
    this.setState({
      isAuthenticated: true,
      user
     });
    this.emitSnackbar(`Wecome ${user.name}`);
  };


  render() {

    const isAuthenticated = this.state.isAuthenticated;
    const user = this.state.user;

    if (this.state.user === null) {
      getUser().then((res) => {
          this.setState({
            user: res.data.data
          });
        })
        .catch((err) => { console.error(err) });
      };

    return(



      <div>

        <Snackbar
          open={this.state.snackbarOpen}
          message={this.state.snackbarMsg}
        />

      <Switch>
        <Route exact path="/" render={() => (
          isAuthenticated && user ?
            <MainController
              user={this.state.user}
              emitSnackbar={this.emitSnackbar}
            />
           :
           <Form
             formType={'login'}
             isAuthenticated={this.state.isAuthenticated}
             loginUser={this.loginUser}
             emitSnackbar={this.emitSnackbar}

           />
        )}/>

        <Route exact path='/register' render={() => (
          <Form
            formType={'register'}
            isAuthenticated={this.state.isAuthenticated}
            loginUser={this.loginUser}
          />
        )} />

        <Route exact path='/login' render={() => (
          <Form
            formType={'login'}
            isAuthenticated={this.state.isAuthenticated}
            loginUser={this.loginUser}
            emitSnackbar={this.emitSnackbar}
          />
        )} />

        <Route exact path='/logout' render={() => (
          <Logout
            logoutUser={this.logoutUser}
            isAuthenticated={this.state.isAuthenticated}
            emitSnackbar={this.emitSnackbar}

          />
        )} />

      </Switch>
    </div>
    )
  }
  };


export default App;
