import React from 'react';
import { connect } from 'react-redux';


const Profile = (props) => {

  const { user } = props;

  return (
    <div>{user.name} Profile Page.</div>
  )
}

function mapStateToProps(state) {
    const { authentication } = state;
    const { user } = authentication;
    return {
      user
    };
}

const connectedProfile = connect(mapStateToProps)(Profile);
export { connectedProfile as Profile };
