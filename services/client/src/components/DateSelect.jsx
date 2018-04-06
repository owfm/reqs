import React from 'react';
import moment from 'moment';
import DatePicker from 'material-ui/DatePicker';
import Card from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import FontIcon from 'material-ui/FontIcon';
import Avatar from 'material-ui/Avatar';
import AvSkipNext from 'material-ui/svg-icons/av/skip-next';
import AvSkipPrevious from 'material-ui/svg-icons/av/skip-previous';

const styles = {
  button: {
    margin: '10px'
  }
}

const DateSelect = (props) => {

    const date = moment(props.currentWbDate, 'DD-MM-YY').format('ddd DD/MM')

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
                <strong>
                  {date}
                </strong>
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
