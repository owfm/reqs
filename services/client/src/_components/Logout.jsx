import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { userActions } from '../_actions';
import { userService } from '../_services';


class Logout extends React.Component {
  componentDidMount() {
    const { dispatch } = this.props;
    userService.logout();
    dispatch(userActions.logout());
  }

  render() {
    return <Redirect push to="/login" />;
  }
}

function mapStateToProps(state) {
  const { authentication } = state;
  return {
    authentication,
  };
}


const connectedLogout = connect(mapStateToProps)(Logout);
export { connectedLogout as Logout };


Logout.propTypes = {
  dispatch: PropTypes.func.isRequired,
};
