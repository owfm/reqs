import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';


import './ReqFull.css';

const ReqFull = (props) => {

  const { session, handleInputChange, handleSubmit, role } = props;

  return(


    <div>

      <TextField
        label="Lesson Title (required)"
        value={session.title}
        name='title'
        onChange={handleInputChange}
        multiline
        autoFocus
        fullWidth
      />

      <br />

      <TextField
        label="Equipment"
        value={session.equipment}
        onChange={handleInputChange}
        name='equipment'
        multiline
        fullWidth
      />
      <br />

      <TextField
        label="Notes"
        value={session.notes}
        name='notes'
        onChange={handleInputChange}
        multiline
        fullWidth
      />

      {!session.isDone && role !== 'Technician' &&
      <Button
        disabled={!session.title}
        variant="raised"
        color="primary"
        onClick={handleSubmit}
        >
          {session.type === 'lesson' ? 'Post!' : 'Update!'}
        </Button>
      }


    </div>
  )
}



export { ReqFull };
