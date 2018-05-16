import React from 'react';
import styled from 'styled-components';
import moment from 'moment';
import { ReqMini } from '../_components';

import { appConstants } from '../_constants'

const MainGrid = styled.div`
padding: 20px;
display: grid;
grid-template-rows: auto repeat(${props=>props.periods.length}, auto);
grid-gap: 10px;
grid-template-columns: auto repeat(5, 1fr);
`
const SessionGrid = styled.div`
  display: grid;
  grid-gap: 5px;
`


export const DisplayWeek = (props) => {

  const { periods, reqs } = props;
  const { days } = appConstants;

  const sessionGridContents = [];

  periods.forEach((period) => {
    sessionGridContents.push(<div style={{'alignSelf': 'center', 'justifySelf': 'center', 'fontWeight': 'bold'}}>{period}</div>);

    days.forEach(day => {
      sessionGridContents.push(
        <SessionGrid>
          {props.reqs.items
            .filter(req=>req.period===period && req.day===day)
            .map(req=><ReqMini session={req} key={`${req.id}${req.type}`}/>)
          }
        </SessionGrid>
      )
    })
  });


  const dayHeaders = days.map(day =>
      <div style={{'justifySelf': 'center', 'fontWeight': 'bold'}} key={`d${day}`}>{day}</div>
    )



  return (

    <MainGrid periods={props.periods}>
      <div></div>
      {dayHeaders}
      {sessionGridContents}
    </MainGrid>

  )
};
