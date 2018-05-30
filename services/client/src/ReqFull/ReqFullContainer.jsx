import React from 'react';
import { Redirect, withRouter } from 'react-router';
import { connect } from 'react-redux';

import { reqActions, alertActions } from '../_actions';

import { ReqFull } from './';

class ReqFullContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {




    }

  render() {

    const { dispatch, loading, error, session, history } = this.props;

    if (loading) {
      return(<div>Twats...</div>);
    }

    if (error) {
      dispatch(alertActions.flash(error))
      return <Redirect push to='/week' />
    }

    if (!session) {
      dispatch(alertActions.flash("Not found!"))
      return <Redirect push to='/week' />
    }

    return (
      <ReqFull history={history} session={session} />
    )
  }
}


function mapStateToProps(state, ownProps) {

    const { type, id, currentWbStamp } = ownProps.match.params;
    const { reqs, lessons } = state;
    const { loading, error } = reqs;

    const session = type === 'lesson' ?
      lessons.items.find(s => s.id == id) :
      reqs[currentWbStamp].items.find(s => s.id == id);

    console.log('\n\n\n\n\n\n\n');
    console.log(session);


    return {
      session,
      loading
    };
}

const connectedReqFullContainer = withRouter(connect(mapStateToProps)(ReqFullContainer));
export { connectedReqFullContainer as ReqFullContainer };
