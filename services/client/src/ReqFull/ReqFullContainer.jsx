import React from 'react';
import PropTypes from 'prop-types';
import { Redirect, withRouter } from 'react-router';
import { connect } from 'react-redux';

import { appConstants } from '../_constants';
import { reqActions, alertActions } from '../_actions';

import ReqFull from './ReqFull';

class ReqFullContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      session: {
        ...props.session,
      },
    };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(e) {
    const { role } = this.props;

    if (role === 'Technician') {
      return null;
    }

    if (this.props.session.isDone) {
      this.props.dispatch(alertActions.flash(`Sorry! Already marked 'done' by ${this.props.session.done_by.name}.`));
      return null;
    }


    const { target } = e;
    const { name } = target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const session = { ...this.state.session };
    session[name] = value;

    if (value.length > appConstants.maxReqPostLength) {
      return null;
    }

    this.setState({
      session,
    });
  }

  handleSubmit() {
    const { currentWbStamp, id } = this.props.match.params;
    const {
      title, equipment, notes, type,
    } = this.state.session;
    const { dispatch } = this.props;

    type === 'lesson' ?
      dispatch(reqActions.postNewReq({
        currentWbStamp, lesson_id: id, title, equipment, notes,
      })) :
      dispatch(reqActions.postReqUpdate({
        currentWbStamp, id, title, equipment, notes,
      }));
  }

  render() {
    const {
      dispatch, loading, error, role,
    } = this.props;
    const { session } = this.state;


    if (loading) {
      return (<div>Loading...</div>);
    }

    if (error) {
      dispatch(alertActions.flash(error));
      return <Redirect push to="/week" />;
    }

    if (!session) {
      dispatch(alertActions.flash('Not found!'));
      return <Redirect push to="/week" />;
    }

    return (
      <div>
        <ReqFull
          session={session}
          role={role}
          handleInputChange={this.handleInputChange}
          handleSubmit={this.handleSubmit}
        />

      </div>
    );
  }
}


function mapStateToProps(state, ownProps) {
  const { type, id, currentWbStamp } = ownProps.match.params;
  const { reqs, lessons, authentication } = state;
  const { user } = authentication;
  const { loading, error } = reqs;

  const session = type === 'lesson' ?
    lessons.items.find(s => s.id == id) :
    reqs[currentWbStamp].items.find(s => s.id == id);

  return {
    session,
    loading,
    error,
    role: appConstants.UserCode[user.role_code],
  };
}

export default withRouter(connect(mapStateToProps)(ReqFullContainer));

ReqFullContainer.propTypes = {
  role: PropTypes.string.isRequired,
  dispatch: PropTypes.func.isRequired,
  currentWbStamp: PropTypes.number.isRequired,

};
