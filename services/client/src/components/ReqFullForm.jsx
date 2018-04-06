import React from 'react';
import { Input } from 'react-materialize';
import { UserCode } from '../utils/Constants';
import TeacherReqOptionButtons from './TeacherReqOptionButtons';
import TechnicianReqOptionButtons from './TechnicianReqOptionButtons';

import styled from 'styled-components';

const ReqInput = styled.textarea`
  flex: 1 1;
  padding: 5px;
  margin: 10px 0;
  border-radius: 2px;
  border: ${props=> props.disabled ? 'none' : '1px solid palevioletred'};
  background: ${props=> props.disabled ? 'white' : 'white'};
  color: ${props=> props.disabled ? 'black' : 'black'};
  `
const ReqInputLabel = styled.h4`
  color: palevioletred;
  font-size: 14px;
  font-weight: 400;
`

const ReactFullForm = (props) => {

  const roleCode = props.roleCode;
  const type = props.req.type;
  const isEditing = props.isEditing;

  return (

    <form>
      <div className='reqFullTitleBar'>
        <ReqInputLabel>Lesson Title</ReqInputLabel>

        <ReqInput
          disabled={type === 'requisition' ? !isEditing : false}
          name='title'
          type="text"
          onChange={props.handleInputChange}
          value={props.req.title} />

          <ReqInputLabel>Equipment</ReqInputLabel>

          <ReqInput
            disabled={type === 'requisition' ? !isEditing : false}
            name='equipment'
            type="textarea"
            onChange={props.handleInputChange}
            value={props.req.equipment}
          />
          <ReqInputLabel>Notes</ReqInputLabel>

          <ReqInput
            disabled={type === 'requisition' ? !isEditing : false}
            name='notes'
            type="textarea"
            onChange={props.handleInputChange}
            value={props.req.notes} />
          </div>

        {UserCode[roleCode] === 'Teacher' &&
        <TeacherReqOptionButtons
          handlePostNewReq={props.handlePostNewReq}
          req={props.req}
          handleEditReq={props.handleEditReq}
          handlePostNewReq={props.handlePostNewReq}
          handleEditClick={props.handleEditClick}
          isEditing={props.isEditing}
          handleModalClose={props.handleModalClose}
        />
        }

        {UserCode[roleCode] === 'Technician' &&
        <TechnicianReqOptionButtons
          req={props.req}
          handleModalClose={props.handleModalClose}
        />
        }

      </form>
  )

};

export default ReactFullForm;
