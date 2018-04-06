import React from 'react';
import './WeekGrid.css';
import ReqMini from './ReqMini';

const Days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

const GetPeriodHeaders = (periods) => {

  const periodsArray = Array(periods).fill().map((x,i)=>i+1);

  return (
    periodsArray.map(period =>
      <div className="periodhead">{period}</div>
    )
  );

}

const GetDayRows = (props) => {

  const periodsArray = Array(props.periods).fill().map((x,i)=>i+1);

  const DayRows = [];

  for (let day in Days) {
    DayRows.push(
      <div className='grid-row'>
        <div className='day-col'>{Days[day]}</div>
        {periodsArray.map(period => {
          return <div className='period'>
            {props.sessions
                .filter(session => session.day === Days[day] && session.period === period)
                .map(session => <ReqMini
                                    session={session}
                                    emitSnackbar={props.emitSnackbar}
                                    key={session.id}
                                    handleSetModalObject={props.handleSetModalObject}
                                    handleModalOpen={props.handleModalOpen}
                                    handleSetModalType={props.handleSetModalType}
                                    role_code={props.role_code}
                                  />)}
          </div>
        })}
      </div>
    )
  }

  return DayRows;

}

const WeekGrid = (props) => {


  const periodHeaders = GetPeriodHeaders(props.periods);
  const dayRows = GetDayRows(props);

  return (
    <div className='week-grid-wrapper'>

      <div className='period-row'>
        <div className='day-col'></div>
          {periodHeaders}
      </div>
      {dayRows}

    </div>
  )
}

export default WeekGrid;
