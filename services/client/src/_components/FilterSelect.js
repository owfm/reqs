import React from 'react';

import { connect } from 'react-redux';
import { filterActions } from '../_actions';

const FilterSelect = (props) => {

  const siteList = props.sites.map(
    site => <li><a onClick={()=>props.dispatch(filterActions.setSiteFilter(site))}>{site}</a></li>
  )

  const filteredSitesList = props.sitesFilter.map(
    site => <li> <a onClick={()=>props.dispatch(filterActions.clearSiteFilter(site))}>{site}</a></li>
  )

  const filteredStatus = <li><a onClick={()=>props.dispatch(filterActions.clearStatusFilter())}>{props.statusFilter}</a></li>


  return (
    <div>
      Site Filters:
    <ul>
      {siteList}
    </ul>
    <br />
    Status Filters:
    <ul>
      <li><a onClick={()=> props.dispatch(filterActions.setStatusFilter('isDone'))}>Completed</a></li>
      <li><a onClick={()=> props.dispatch(filterActions.setStatusFilter('hasIssue'))}>Has Problem</a></li>
      <li><a onClick={()=> props.dispatch(filterActions.setStatusFilter('active'))}>Active</a></li>

    </ul>

    <br />

    Active Filters (click to remove):
    <ul>
      {filteredSitesList}
      {filteredStatus}
    </ul>


    <br/>




    <ul>
      <li><a onClick={()=>props.dispatch(filterActions.clearAllSiteFilters())}>Clear All Sites</a></li>
      <li><a onClick={()=>props.dispatch(filterActions.clearAllFilters())}>Clear Filters</a></li>

    </ul>


  </div>
  )

}


function mapStateToProps(state) {

  const { school, filters } = state;
  const { sites, status } = filters;

  return {
    sites: school.sites.map(s => s.name),
    sitesFilter: sites,
    statusFilter: status
  };
}

const connectedFilterSelect = connect(mapStateToProps)(FilterSelect);
export { connectedFilterSelect as FilterSelect };
