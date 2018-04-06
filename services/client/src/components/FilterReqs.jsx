import React from 'react';
import { Card, CardHeader, CardText } from 'material-ui/Card';
import Toggle from 'material-ui/Toggle';


const styles = {
  block: {
    maxWidth: 250,
  },
  toggle: {
    marginBottom: 16,
  },
  thumbOff: {
    backgroundColor: '#ffcccc',
  },
  trackOff: {
    backgroundColor: '#ff9d9d',
  },
  thumbSwitched: {
    backgroundColor: 'red',
  },
  trackSwitched: {
    backgroundColor: '#ff9d9d',
  },
  labelStyle: {
    color: 'red',
  },
};

const FilterReqs = (props) => {
return(
  <div style={{display: 'flex', flexDirection: 'row'}}>
    <Toggle
      name="isDone"
      label="Show Done"
      labelPosition="right"
      style={styles.toggle}
      defaultToggled={true}
      onToggle={props.handleFilterToggle}
    />
    <Toggle
      name="hasIssue"
      label="Show Reqs with Issues"
      labelPosition="right"
      style={styles.toggle}
      defaultToggled={true}
      onToggle={props.handleFilterToggle}
    />
  </div>
)
}

export default FilterReqs;
