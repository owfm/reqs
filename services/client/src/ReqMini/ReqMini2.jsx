import React from 'react';
import { Redirect } from 'react-router';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const styles = {
  card: {
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    marginBottom: 16,
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
};

class SimpleCard extends React.Component {

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

  render(){

    const { redirect } = this.state;

    const { session, currentWbStamp } = this.props;

    const { isDone, hasIssue, type, id } = session;

    if (redirect) {
      return <Redirect push to={`${currentWbStamp}/${type}/${id}`} />
    }

    const { classes } = this.props;
    const bull = <span className={classes.bullet}>•</span>;

    return (
      <div>
        <Card className={classes.card}>
          <CardContent>
            <Typography variant="headline" component="h2">
              {session.classgroup.name}
            </Typography>
            <Typography className={classes.pos} color="textSecondary">
              {session.room.name}
            </Typography>
            <Typography component="p">
              
            </Typography>
          </CardContent>
          <CardActions>
            <Button
              onClick={this.handleCardClick}
              size="small">Open</Button>
            </CardActions>
          </Card>
        </div>
      );
    }
  }

  SimpleCard.propTypes = {
    classes: PropTypes.object.isRequired,
  };

  export default withStyles(styles)(SimpleCard);
