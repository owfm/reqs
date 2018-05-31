import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';


import './ReqFull.css';

const ReqFull = (props) => (

  <div>

  <TextField
    label="Lesson Title (required)"
    value={props.session.title}
    name='title'
    onChange={props.handleInputChange}
    multiline
    autoFocus
    fullWidth
  />

  <br />

  <TextField
    label="Equipment"
    value={props.session.equipment}
    onChange={props.handleInputChange}
    name='equipment'
    multiline
    fullWidth
  />
  <br />

  <TextField
    label="Notes"
    value={props.session.notes}
    name='notes'
    onChange={props.handleInputChange}
    multiline
    fullWidth
  />

  {!props.session.isDone &&
    <Button
      disabled={!props.session.title}
      variant="raised"
      color="primary"
      onClick={props.handleSubmit}
      >
          {props.session.type === 'lesson' ? 'Post!' : 'Update!'}
    </Button>
  }


</div>
)


export { ReqFull };
