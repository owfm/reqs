import React from 'react';
// import './WeekGridUsingGridUsingGrid.css';
import ReqMini from './ReqMini';
import styled from 'styled-components';
const Days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];


const MainGrid = styled.div`
  padding: 20px;
  display: grid;
  grid-template-columns: 1fr repeat(5, 5fr);
  grid-template-rows: 1fr repeat(${props=>props.periods}, 5fr);
  grid-gap: 10px;
`

const SessionGrid = styled.div`
  display: grid;
`


const GetDayHeaders = () => {

  // const periodsArray = Array(periods).fill().map((x,i)=>i+1);

  return (
    Days.map(day =>
      <div style={{'justifySelf': 'center', 'fontWeight': 'bold'}} key={`d${day}`}>{day}</div>
    )
  );
}

const GetSessionGridContents = (props) => {

  const elements = [];

  for (let period = 1; period <= props.periods; period++) {

    elements.push(<div style={{'alignSelf': 'center', 'justifySelf': 'center', 'fontWeight': 'bold'}}>{period}</div>);

    Days.forEach(day => {

      elements.push(<SessionGrid>
        {props.sessions
          .filter(session=>session.period===period && session.day===day)
          .map(session=><ReqMini
                  session={session}
                  emitSnackbar={props.emitSnackbar}
                  key={`${session.id}${session.type}`}
                  handleSetModalObject={props.handleSetModalObject}
                  handleModalOpen={props.handleModalOpen}
                  handleSetModalType={props.handleSetModalType}
                  role_code={props.role_code}
          />)
        }
      </SessionGrid>)
    })
  }

  return elements;
}

const WeekGrid = (props) => {

  const dayHeaders = GetDayHeaders();
  const sessionGridContents = GetSessionGridContents(props);

  return (
    <MainGrid periods={8}>
      <div></div>
      {dayHeaders}
      {sessionGridContents}
    </MainGrid>

  )
}

export default WeekGrid;
