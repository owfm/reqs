import React from 'react';
import {List, ListItem} from 'material-ui/List';
import Card from 'material-ui/Card';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';
import Checkbox from 'material-ui/Checkbox';
import Toggle from 'material-ui/Toggle';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import TimePicker from 'material-ui/TimePicker';


const styles = {
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
};

class AdminPreferences extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      periods: 6,
      periodStartTimes: [],
      reminderEmails: false
    }
  }

handleChange = (event, index, periods) => this.setState({periods});

handleChangeTimePicker = (event) => {

}

  render() {

    const periodStartTimes = [];

    for (let i = 0; i < this.state.periods; i++) {
      periodStartTimes.push(
        <TimePicker
          format="24hr"
          hintText={`Period ${i+1} start time`}
          minuteStep={5}
          autoOk={true}
          // value={this.state.value12}
          onChange={this.handleChangeTimePicker}
        />
      )
    }


    return(


    <div style={styles.root}>
      <Card>

        <List>
          <Subheader>School Info</Subheader>
          <ListItem
            primaryText="How many periods in the school day?"
            >
            <SelectField
              name={'periods'}
              value={this.state.periods}
              onChange={this.handleChange}
              >
                <MenuItem value={4} primaryText="4" />
                <MenuItem value={5} primaryText="5" />
                <MenuItem value={6} primaryText="6" />
                <MenuItem value={7} primaryText="7" />
                <MenuItem value={8} primaryText="8" />
                <MenuItem value={9} primaryText="9" />
                <MenuItem value={10} primaryText="10" />
              </SelectField>
          </ListItem>
          <ListItem>
            {periodStartTimes}
          </ListItem>




        </List>
        <Divider />
      </Card>
      <Card>

        <List>
          <ListItem
            primaryText="When calls and notifications arrive"
            secondaryText="Always interrupt"
          />
        </List>
        <Divider />
        <List>
          <Subheader>Notifications</Subheader>
          <ListItem primaryText="Send staff reminder emails" rightToggle={<Toggle />} />
          <ListItem primaryText="Staff reminder day" rightToggle={<Toggle />} />
        </List>
        <Divider />
        <List>
          <Subheader>Hangout Notifications</Subheader>
          <ListItem primaryText="Notifications" leftCheckbox={<Checkbox />} />
          <ListItem primaryText="Sounds" leftCheckbox={<Checkbox />} />
          <ListItem primaryText="Video sounds" leftCheckbox={<Checkbox />} />
        </List>
      </Card>
    </div>
  )
  }

};

export default AdminPreferences;
