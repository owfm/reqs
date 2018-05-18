import React from 'react';
import { appConstants } from '../_constants';
import {
  TeacherReqOptionButtons,
  TechnicianReqOptionButtons
} from './';

import styled from 'styled-components';

const ReqInput = styled.textarea`
  outline: none;
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
  font-size: 18px;
  font-weight: 600;
`

const ReqFullForm = (props) => {

  const { roleCode, isEditing } = props;
  const { type } = props.req;
  const { UserCode } = appConstants;

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
          req={props.req}
          handleEditReq={props.handleEditReq}
          handlePostNewReq={props.handlePostNewReq}
          handleEditClick={props.handleEditClick}
          isEditing={props.isEditing}
          valid={props.valid}
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



export { ReqFullForm };
