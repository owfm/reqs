import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { userActions, alertActions } from '../_actions';
import { userService } from '../_services'

class Logout extends React.Component {

  constructor(props) {
    super(props);
    this.state = {redirect: false};
  }

  componentDidMount(){
    const { dispatch } = this.props;
    userService.logout();
    dispatch(userActions.logout());
    this.setState({redirect: true})
  }

  render(){

    if ( this.state.redirect ) {
      return <Redirect push to='/login' />
    }

    return (
      <div>Logging out...</div>
    )
  }
}

function mapStateToProps(state) {
    const { authentication } = state;
    return {
      authentication
    };
}


const connectedLogout = connect(mapStateToProps)(Logout);
export { connectedLogout as Logout };
