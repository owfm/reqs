import React from 'react';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import AppBar from 'material-ui/AppBar';
import { UserCode } from '../utils/Constants';
import Logout from './Logout'



export default class Navigation extends React.Component {

  constructor(props) {
    super(props);
    this.state = {open: false};
  }

  handleToggle = () => this.setState({open: !this.state.open});
  handleClose = () => this.setState({open: false});

  render() {

    const title = `${this.props.user.name} (${UserCode[this.props.user.role_code]})`

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
          <MenuItem onClick={this.handleClose}>{this.props.user.name}</MenuItem>
          <MenuItem onClick={this.handleClose}>Menu Item 2</MenuItem>
          <MenuItem onClick={this.props.logoutUser}>Logout</MenuItem>

        </Drawer>
      </div>
    );
  }
}
