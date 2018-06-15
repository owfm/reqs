import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const styles = {
  card: {
    maxWidth: 345,
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
};

function ReqIssueCard(props) {
  const { classes, session } = props;
  return (
    <div>
      <Card className={classes.card}>
        <CardMedia
          className={classes.media}
          image="https://st3.depositphotos.com/1109793/14092/v/450/depositphotos_140923348-stock-illustration-doctor-holding-broken-bone-x.jpg"
          title="A sad looking scientist."
        />
        <CardContent>
          <Typography gutterBottom variant="headline" component="h2">
            Problem
          </Typography>
          <Typography gutterBottom variant="subheading">
            This req has been marked as problematic by {session.issue_technician.name}.
          </Typography>

          <Typography component="p">
            {session.issue_text}
          </Typography>
        </CardContent>
        <CardActions>
          <Button
            size="small"
            color="primary"
            variant="outlined"
            >
            Email
          </Button>

        </CardActions>
      </Card>
    </div>
  );
}

ReqIssueCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ReqIssueCard);
