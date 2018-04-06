import React from 'react';
import Toggle from 'material-ui/Toggle';



export const TechnicianReqOptionButtons = (props) => (

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


<div style={{display: 'flex', flexDirection: 'row', bottom:'0', justifyContent: 'flex-end', alignItems: 'flex-end'}}>


  <Toggle
    defaultToggled={props.req.isDone}
    disabled={props.req.hasIssue}
    label="Mark as Done"
    style={styles.toggle}
  />

  <Toggle
    defaultToggled={props.req.hasIssue}
    disabled={props.req.isDone}
    label="Mark with Issue"
    style={styles.toggle}
  />

  <FlatButton
    disabled={props.isEditing}
    primary={true}
    onClick={props.handleModalClose}>
    CLOSE
  </FlatButton>
</div>

)
