import React from 'react';
import moment from 'moment';
import Card from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import AvSkipNext from 'material-ui/svg-icons/av/skip-next';
import AvSkipPrevious from 'material-ui/svg-icons/av/skip-previous';

const styles = {
  button: {
    margin: '10px'
  }
}

const DateSelect = (props) => {

    const date = moment(props.currentWbStamp, 'DD-MM-YY').format('ddd DD/MM')

    const inTerm = Number.isInteger(props.weekNumber);

    return(
        <Card>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>

              <RaisedButton
                secondary={true}
                onClick={() => props.handleWeekChange(-7)}
                label="PREV WEEK"
                labelPosition="after"
                primary={true}
                icon={<AvSkipPrevious />}
                style={styles.button}
              />
              <div>

                <strong>{date}</strong> ({inTerm && 'Week'} {props.weekNumber})
              </div>
              <RaisedButton
                secondary={true}
                onClick={() => props.handleWeekChange(+7)}
                label="NEXT WEEK"
                labelPosition="before"
                primary={true}
                icon={<AvSkipNext />}
                style={styles.button}
                />

          </div>
        </Card>
    )
}

export default DateSelect;
