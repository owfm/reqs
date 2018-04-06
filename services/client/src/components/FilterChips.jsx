import React from 'react';
import Chip from 'material-ui/Chip'
import './FilterChips.css';

const FilterChips = (props) => {


  if (allFiltersAreTrue(props.filters)) {
    return null;
  }


  const siteChips = [];


  for (let site in props.filters.sites) {
    if (props.filters.sites[site] === true) {
      siteChips.push(
        <div className='chip'>
          <Chip
            onClick={() => props.handleRemoveFilter('ALL')}
            onRequestDelete={() => props.handleRemoveFilter(site)}>
            {site}
          </Chip>
      </div>
    )
      }
  }


  return (
    <div className="filter-chip-wrapper">
      <div className="filter-chips">
      {props.filters.isDone && <div className='chip'><Chip onClick={() => props.handleRemoveFilter('isDone')} onRequestDelete={() => props.handleRemoveFilter('isDone')}>Done</Chip></div>}
      {props.filters.hasIssue && <div className='chip'><Chip onClick={() => props.handleRemoveFilter('hasIssue')} onRequestDelete={() => props.handleRemoveFilter('hasIssue')}>Issues</Chip></div>}
      {siteChips}
      </div>
      <div className='chip'>
        <Chip onRequestDelete={() => props.handleRemoveFilter('ALL')}>Remove All Filters</Chip>
      </div>
    </div>
  )

}

export default FilterChips;

const allFiltersAreTrue = (filters) => {
  for (let filter in filters) {
    if (filter !== 'sites') {
      if (!filters[filter]) return false;
    }
  }

  for (let site in filters.sites) {
    if (!filters.sites[site]) return false;
  }
  return true;
}
