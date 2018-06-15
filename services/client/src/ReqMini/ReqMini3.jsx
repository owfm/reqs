import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import moment from 'moment';
import { appConstants } from '../_constants';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import classnames from 'classnames';
import Button from '@material-ui/core/Button'
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Collapse from '@material-ui/core/Collapse';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import red from '@material-ui/core/colors/red';
import blue from '@material-ui/core/colors/blue';
import green from '@material-ui/core/colors/green';
import CheckCircle from '@material-ui/icons/CheckCircle';
import Warning from '@material-ui/icons/Warning';

import ShareIcon from '@material-ui/icons/Share';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import MoreVertIcon from '@material-ui/icons/MoreVert';

import { reqActions } from '../_actions';

const styles = theme => ({
  card: {
    // maxWidth: 400,
  },
  media: {
    height: 0,
    // paddingTop: '56.25%', // 16:9
  },
  actions: {
    display: 'flex',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  avatarProblem: {
    backgroundColor: red[500],
  },
  avatarActive: {
    backgroundColor: blue[500],
  },
  avatarDone: {
    backgroundColor: green[500],
  },

});

class ReqMini extends React.Component {
  state = { expanded: false };

  handleExpandClick = () => {
    this.setState({ expanded: !this.state.expanded });
  };

  handleDoneToggle = () => {
    const { session, dispatch, currentWbStamp } = this.props;
    dispatch(reqActions.postReqUpdate({
      currentWbStamp,
      id: session.id,
      isDone: !session.isDone
    }))
  }

  render() {
    const { classes, session, userRole, currentWbStamp } = this.props;

    return (
      <div>
        <Card className={classes.card}>
          <CardHeader
            avatar={
              <Avatar
                aria-label="Recipe"
                className={
                  session.hasIssue ?
                  classes.avatarProblem :
                  session.isDone ?
                  classes.avatarDone :
                  classes.avatarActive
                }>
                {session.room.site.name.match(/\b\w/g).join('')}
              </Avatar>
            }
            action={
              <IconButton>
                <MoreVertIcon />
              </IconButton>
            }
            title={`${session.classgroup.name} ${session.room.name}`}
            subheader={session.type === 'requisition' && moment(session.time).fromNow()}
          />

          <CardContent>
            {session.type === 'requisition' ?
            <Typography variant="title">
              {session.title}
            </Typography> :
            <Button
              component={Link}
              to={`/week/${currentWbStamp}/lesson/${session.id}`}
              variant="contained"
              size="medium"
              color="primary"
              className={classes.button}>
                      Post
                    </Button>                    }
            <Typography component="p">




            </Typography>

          </CardContent>
          {session.type === 'requisition' &&
          <div>

          <CardActions className={classes.actions} disableActionSpacing>

            {userRole === 'Technician' &&
            <div>

            <IconButton
              aria-label="Mark as Done">
              <CheckCircle
                color={session.isDone ? 'primary' : 'disabled'}
                onClick={this.handleDoneToggle}
              />
            </IconButton>


            <IconButton aria-label="Problem?">
              <Warning />
            </IconButton>
          </div>

          }

            <IconButton
              className={classnames(classes.expand, {
                [classes.expandOpen]: this.state.expanded,
              })}
              onClick={this.handleExpandClick}
              aria-expanded={this.state.expanded}
              aria-label="Show more"
            >
              <ExpandMoreIcon />
            </IconButton>
          </CardActions>

          <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
            <CardContent>
              <Typography paragraph variant="body2">
                Equipment:
              </Typography>
              <Typography paragraph>
                {session.equipment || 'No equipment specified.'}
              </Typography>
              <Typography paragraph variant="body2">
                Notes:
              </Typography>

              <Typography paragraph>
                {session.notes || 'No notes specified.'}
              </Typography>

            </CardContent>
          </Collapse>
        </div>

        }
        </Card>
      </div>
    );
  }
}

ReqMini.propTypes = {
  classes: PropTypes.object.isRequired,
};

function mapStateToProps(state, ownProps) {
  const { authentication } = state;
  const { user } = authentication;
  const { role_code } = user;
  const { currentWbStamp } = ownProps.match.params;


  return {
    userRole: appConstants.UserCode[role_code],
    currentWbStamp
  };
}
const reqMiniWithStyles = withStyles(styles)(ReqMini)
export default connect(mapStateToProps)(reqMiniWithStyles);
