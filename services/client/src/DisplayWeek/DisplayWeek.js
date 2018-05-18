import React from 'react';
import moment from 'moment';
import { ReqMini } from '../_components';
import uuidv4 from 'uuid/v4';
import { appConstants } from '../_constants'
import { MainGrid, SessionGrid } from './components';


export const DisplayWeek = (props) => {

  const { periods, sessions } = props;
  const { days } = appConstants;

  const sessionGridContents = [];

  periods.forEach((period) => {
    sessionGridContents.push(<div key={`period${period}`} style={{'alignSelf': 'center', 'justifySelf': 'center', 'fontWeight': 'bold'}}>{period}</div>);

    days.forEach(day => {
      sessionGridContents.push(
        <SessionGrid key={uuidv4()}>
          {sessions
            .filter(session=>session.period===period && session.day===day)
            .map(session=><ReqMini session={session} key={uuidv4()}/>)
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
