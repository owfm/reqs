import React from 'react';
import { Days } from '../utils/Constants';
import ReqMini from './ReqMini';
import Loading from './Loading';
import moment from 'moment';
export class WeekGrid extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      periods: [1,2,3,4,5,6]
    }

    this.getGridStyle = this.getGridStyle.bind(this);
  };

  getGridStyle = () => {
    return ({

      display: 'grid',
      gridColumnGap: '10px',
      justifyItems: 'center',
      gridTemplateColumns: '1 repeat(5, 3fr)',
      gridTemplateRows: `1 repeat(${this.state.periods.length})`,
      flexDirection: 'rows'
    })
  }

  render() {

    const dayRow = [];

    const daysDate = getDatesOfWeekdays(this.props.currentWbDate);

    for (let day in Days) {
      dayRow.push(<div style={{gridColumn: `${parseInt(day, 10)+2}`, gridRow: '1'}}>{Days[day]}<br/>{daysDate[day]}</div>)
    }

    const periodCol = [];

    for (var period in this.state.periods) {
      periodCol.push(
        <div style={{gridRow: `${parseInt(period, 10)+2}`, gridColumn: '1', alignContent: 'center'}}>
          <span>
            Period {this.state.periods[period]}
          </span>
        </div>
      )
    };

    if (!this.props.school || !this.props.sessions) {
      return(
        <Loading />
      )
    }

    const reqCards = [];

    for (let day in Days) {
      for (let period in this.state.periods) {
        reqCards.push(
          <div style={
            {display: 'flex',
            flexDirection: 'column',
            gridColumn: `${parseInt(day, 10)+2}`,
            gridRow: `${parseInt(period, 10)+2}`}
          }>

          {this.props.sessions
            .filter(req => req.day === Days[day] && req.period === this.state.periods[period] )
            .map(req =>
              <div style={{marginBottom: '10px'}}>

              <ReqMini
                emitSnackbar={this.props.emitSnackbar}
                key={req.id}
                req={req}
                handleSetModalObject={this.props.handleSetModalObject}
                handleModalOpen={this.props.handleModalOpen}
                handleSetModalType={this.props.handleSetModalType}
                role_code={this.props.role_code}
              />
            </div>
              )}
            </div>
          )
        }
      }

      const gridStyle = this.getGridStyle();

      return(

          <div style={gridStyle}>
            {periodCol}
            {dayRow}
            {reqCards}
          </div>
      )

    }
  }

const getDatesOfWeekdays = (currentWbDate) => {
  const daysDate = [];
  daysDate.push(moment(currentWbDate, 'DD-MM-YY').format('DD MMM'));
  daysDate.push(moment(currentWbDate, 'DD-MM-YY').add(1, 'days').format('DD MMM'));
  daysDate.push(moment(currentWbDate, 'DD-MM-YY').add(2, 'days').format('DD MMM'));
  daysDate.push(moment(currentWbDate, 'DD-MM-YY').add(3, 'days').format('DD MMM'));
  daysDate.push(moment(currentWbDate, 'DD-MM-YY').add(4, 'days').format('DD MMM'));
  return daysDate;

}
