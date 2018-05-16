import React from 'react';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import AppBar from 'material-ui/AppBar';

import { Link } from 'react-router-dom';

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
    const { UserCode } = appConstants;

    const title = `${user.name} (${UserCode[user.role_code]})`

    return (
      <div>

        <AppBar
          style={{zIndex: '0'}}
          title={title}
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
          <MenuItem onClick={this.handleClose}><Link to='/me'>{user.name}</Link></MenuItem>
          <MenuItem onClick={this.handleClose}><Link to='/week'>Teach</Link></MenuItem>
          <MenuItem onClick={this.handleClose}><Link to='/logout'>Logout</Link></MenuItem>

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
