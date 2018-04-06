import React from 'react';
import Chip from 'material-ui/Chip'


const FilterChips = (props) => {


  if (allFiltersAreTrue(props.filters)) {
    return null;
  }


  const siteChips = [];


  for (let site in props.filters.sites) {
    if (props.filters.sites[site] === true) {
      siteChips.push(
        <Chip
          onRequestDelete={() => props.handleRemoveFilter(site)}>
          {site}
        </Chip>)
      }
  }


  return (
    <div style={{display:'flex', flexWrap:'wrap', justifyContent:'space-between '}}>
      <div style={{display:'flex'}}>
      {props.filters.isDone && <Chip onRequestDelete={() => props.handleRemoveFilter('isDone')}>Done</Chip>}
      {props.filters.hasIssue && <Chip onRequestDelete={() => props.handleRemoveFilter('hasIssue')}>Issues</Chip>}
      {siteChips}
      </div>
      <div onClick={() => props.handleRemoveFilter('ALL')}>X Remove All Filters</div>
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
