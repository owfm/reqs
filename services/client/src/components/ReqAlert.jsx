import React from 'react';
import Chip from 'material-ui/Chip';

const styles = {
  chip: {
    margin: 4,
  },
  wrapper: {
    display: 'flex',
    flexWrap: 'wrap',
  },
};

const ReqAlert = (props) => {
  return(

  <Chip
    backgroundColor={props.type === 'Done' ? '#4ef442' : '#f45041'}
    style={styles.chip}
  >
    {props.type}
  </Chip>
)
}

export default ReqAlert;
