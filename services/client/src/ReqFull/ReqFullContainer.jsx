import React from 'react';
import { Redirect } from 'react-router';
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

    const { dispatch, history, reqs, lessons } = this.props;
    const { id, type } = this.props.match.params;

    const session = type === 'requisition' ?
      reqs.items.find((req) => req.id == id) :
      lessons.items.find((lesson) => lesson.id == id);

    if (reqs.loading) {
      return(<div>Twats...</div>);
    }

    if (reqs.error) {
      dispatch(alertActions.flash(reqs.error))
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


function mapStateToProps(state) {
    const { reqs, lessons, filters } = state;
    const { currentWbStamp } = filters;
    return {
      reqs: reqs[currentWbStamp],
      lessons
    };
}

const connectedReqFullContainer = connect(mapStateToProps)(ReqFullContainer);
export { connectedReqFullContainer as ReqFullContainer };
