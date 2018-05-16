import React from 'react';
import { connect } from 'react-redux';
import { userActions, alertActions } from '../_actions';
import { userService } from '../_services'

class Logout extends React.Component {

  componentDidMount(){
    const { dispatch } = this.props;
    userService.logout();
    dispatch(userActions.logout());
    dispatch(alertActions.flash('Logged out!'))
  }

  render(){
    return (
      <div>Logging out...</div>
    )
  }
}

const connectedLogout = connect()(Logout);
export { connectedLogout as Logout };
