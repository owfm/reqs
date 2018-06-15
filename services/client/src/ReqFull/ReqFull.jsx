import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';

import ReqIssueInfo from './ReqIssueInfo';

import './ReqFull.css';

const styles = theme => ({
  root: theme.mixins.gutters({
    paddingTop: 16,
    paddingLeft: 16,
    paddingRight: 16,
    paddingBottom: 16,
    margin: theme.spacing.unit * 3,
  }),
  inputs: theme.mixins.gutters({
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2,
  }),
});


const ReqFull = (props) => {
  const {
    session,
    handleInputChange,
    handleSubmit,
    role,
    classes,
  }
    = props;

  const {
    week, day, period, room, classgroup, isDone, hasIssue,
  } = session;
  const title = `${week || ''}${day}${period} ${room.name}${classgroup.name}`;

  return (

    <Paper className={classes.root} elevation={4}>
      <Grid
        container
        spacing={16}
        className={classes.demo}
        alignItems="stretch"
        direction="column"
        justify="center"
      >
        <Grid item>
          <Typography variant="title">
            {classgroup.name}
          </Typography>
          <Typography variant="subheading" gutterBottom>
            {room.name}
          </Typography>
        </Grid>

        <Grid item>

          <TextField
            label="Lesson Title (required)"
            value={session.title}
            name="title"
            onChange={handleInputChange}
            multiline
            autoFocus
            fullWidth
          />
        </Grid>

        <Grid item>

          <TextField
            label="Equipment"
            value={session.equipment}
            onChange={handleInputChange}
            name="equipment"
            multiline
            fullWidth
          />
        </Grid>
        <Grid item>

          <TextField
            label="Notes"
            value={session.notes}
            name="notes"
            onChange={handleInputChange}
            multiline
            fullWidth
          />
        </Grid>

        {!session.isDone && role !== 'Technician' &&
        <Grid item>
          <Button
            disabled={!session.title}
            variant="raised"
            color="primary"
            onClick={handleSubmit}
          >
            {session.type === 'lesson' ? 'Post!' : 'Update!'}
          </Button>
        </Grid>

      }
        {session.hasIssue &&
          <Grid item>
            <ReqIssueInfo session={session} />
          </Grid>
        }

      </Grid>


    </Paper>

  );
};

ReqFull.propTypes = {
  handleInputChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  role: PropTypes.string.isRequired,
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ReqFull);
