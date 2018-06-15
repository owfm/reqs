import React from 'react';
import { connect } from 'react-redux';

import { filterActions } from '../_actions';

import uuidv4 from 'uuid/v4';

import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Divider from '@material-ui/core/Divider';

import FilterListIcon from '@material-ui/icons/FilterList';

class FilterSelect extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      anchorEl: null,
    };
  }

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  }

  handleClose = () => {
    this.setState({ anchorEl: null });
  }

  handleSiteFilterToggle(site) {
    const { sitesFilter, dispatch } = this.props;

    sitesFilter.includes(site) ?
      dispatch(filterActions.clearSiteFilter(site)) :
      dispatch(filterActions.setSiteFilter(site));
  }


  render() {
    const { anchorEl } = this.state;

    const siteList = this.props.sites.map(site =>
      (<MenuItem
        key={uuidv4()}
        onClick={() => this.handleSiteFilterToggle(site)}
        selected={this.props.sitesFilter.includes(site)}

      >
        {site}
       </MenuItem>));

    return (
      <div>

        <Button
          style={{ position: 'fixed', bottom: '15px', right: '15px' }}
          aria-owns={anchorEl ? 'filter-menu' : null}
          aria-haspopup="true"
          variant="fab"
          color="primary"
          aria-label="add"
          onClick={this.handleClick}
        >
          <FilterListIcon />
        </Button>

        <Menu
          id="fade-menu"
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={this.handleClose}
        >
          {siteList}
          <Divider />
          <MenuItem
            onClick={() => this.props.dispatch(filterActions.setStatusFilter('isDone'))}
            selected={this.props.statusFilter === 'isDone'}
          >

              Completed
          </MenuItem>
          <MenuItem
            onClick={() => this.props.dispatch(filterActions.setStatusFilter('hasIssue'))}
            selected={this.props.statusFilter === 'hasIssue'}
          >Problems
          </MenuItem>
          <MenuItem
            onClick={() => this.props.dispatch(filterActions.setStatusFilter('active'))}
            selected={this.props.statusFilter === 'active'}
          >Active
          </MenuItem>

          <Divider />
          <MenuItem
            onClick={() => this.props.dispatch(filterActions.clearAllSiteFilters())}
          >Clear Site Filters
          </MenuItem>

          <MenuItem
            onClick={() => this.props.dispatch(filterActions.clearStatusFilter())}
          >Clear Status Filters
          </MenuItem>

          <MenuItem
            onClick={() => this.props.dispatch(filterActions.clearAllFilters())}
          >Clear All Filters
          </MenuItem>

        </Menu>


      </div>
    );
  }
}


function mapStateToProps(state) {
  const { school, filters } = state;
  const { sites, status } = filters;

  return {
    sites: school.sites.map(s => s.name),
    sitesFilter: sites,
    statusFilter: status,
  };
}

// const StyledFilterSelect = withStyles(styles)(FilterSelect);
const connectedFilterSelect = connect(mapStateToProps)(FilterSelect);
export { connectedFilterSelect as FilterSelect };
