import React from 'react';
import { Redirect } from 'react-router';

import './ReqMini.css';

import Truncate from 'react-truncate';
import ActionBuild from 'material-ui/svg-icons/action/build';
import ActionDescription from 'material-ui/svg-icons/action/description';
import moment from 'moment';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import { withStyles } from '@material-ui/core/styles';


const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
  },
});


class ReqMini extends React.Component {

  constructor(props){
    super(props);

    this.state = {
      redirect: false
    }
  }

  handleCardClick = () => {
    this.setState({
      redirect: true
    })
  }

  render() {

    const { session, currentWbStamp, classes } = this.props;
    const { isDone, hasIssue, type } = session;
    const { id } = session;

    if (this.state.redirect) {
      return <Redirect push to={`${currentWbStamp}/${type}/${id}`} />
    }

    const equipmentSet = session.equipment !== "";
    const notesSet = session.notes !== "";

    const statusClass = type === 'lesson' ? 'lesson' : isDone ? 'done' : hasIssue ? 'issue' : 'pending'


    return (
      <Paper
        onClick={this.handleCardClick}>
      {/* <div onClick={this.handleCardClick} className={`req-small`}> */}
        <div className={`status-bar ${statusClass}`}></div>
        <Typography variant={"title"}>
          {session.classgroup.name}
        </Typography>
        <Typography variant={"subheading"}>
          {session.room.name}
        </Typography>

        {session.type === 'lesson' &&
          <div className={'add-req-label'}>
            <Button
              variant="fab"
              mini color="secondary"
              aria-label="add"
              className={classes.button}>
              <AddIcon />
          </Button>

          </div>
        }
        <div className='req-mini-info-box'>
          <div>{session.type === 'requisition' && moment(session.time).fromNow()}</div>
          <div><strong>{session.title}</strong></div>
          <div>{this.props.time}</div>
          <br/>
          {equipmentSet &&
            <Truncate lines={2} ellipsis={<span>... </span>}>
            {session.equipment}
          </Truncate>
        }
        {notesSet && <Truncate lines={2} ellipsis={<span>... </span>}>
        {session.notes}
      </Truncate>}
    </div>
  {/* </div> */}
  </Paper>
)

  }





};

export default withStyles(styles)(ReqMini);
