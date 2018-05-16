import React from 'react';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';



const TechnicianReqOptionButtons = (props) => {

  const isDone = props.req.isDone;
  const type = props.req.type;


  console.log(props);

  if (type === 'lesson') {
    return (
      <div style={{display: 'flex', flexDirection: 'row', bottom:'0', justifyContent: 'flex-end', alignItems: 'flex-end'}}>
      <RaisedButton
        style={{marginLeft: '10px'}}
        primary={true}
        type='submit'
        onClick={props.handlePostNewReq}
        value='Save'>
        SAVE
      </RaisedButton>
      <FlatButton
        style={{marginLeft: '10px'}}
        disabled={props.isEditing}
        primary={true}
        onClick={props.handleModalClose}>
        CLOSE
      </FlatButton>
      </div>
    )
  } else {
    return(
      <div style={{display: 'flex', flexDirection: 'row', bottom:'0', justifyContent: 'flex-end', alignItems: 'flex-end'}}>
        {!props.req.isDone &&
        <RaisedButton
          style={{marginLeft: '10px'}}
          primary={true}
          disabled={isDone}
          name='isEditing'
          onClick={props.handleEditClick}>
          {props.isEditing ? 'DISCARD' : 'EDIT'}
        </RaisedButton>
      }

          <FlatButton
            style={{marginLeft: '10px'}}
            disabled={props.isEditing}
            primary={true}
            onClick={props.handleModalClose}>
            CLOSE
          </FlatButton>
        </div>

      )

  }


};

export default TechnicianReqOptionButtons;
