import React from 'react';
import Drawer from 'material-ui/Drawer';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import AppBar from 'material-ui/AppBar';

import { Redirect } from 'react-router-dom';

import { connect } from 'react-redux';

import { appConstants } from '../_constants';

class Navigation extends React.Component {

  constructor(props) {
    super(props);
    this.state = {open: false};
  }

  handleToggle = () => this.setState({open: !this.state.open});
  handleClose = () => this.setState({open: false});

  render() {

    const { authentication } = this.props;
    const { user } = authentication;

    return (
      <div>

        <AppBar
          style={{zIndex: '0'}}
          title={authentication.loggedIn ? user.name : 'Welcome'}
          iconClassNameRight="muidocs-icon-navigation-expand-more"
          onLeftIconButtonClick={this.handleToggle}
        />

        <Drawer
          style={{zIndex: '0'}}
          docked={false}
          width={200}
          open={this.state.open}
          onRequestChange={(open) => this.setState({open})}
        >
        </Drawer>

      </div>
    );
  }
}

function mapStateToProps(state) {
    const { authentication } = state;
    return {
        authentication
    };
}

const connectedNavigation = connect(mapStateToProps)(Navigation);
export { connectedNavigation as Navigation };
