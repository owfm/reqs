import React from 'react';
import { Redirect } from 'react-router';

import { reqActions, alertActions } from '../_actions';
import { connect } from 'react-redux';

class ReqFullContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {

    const { dispatch } = this.props;
    const { items } = this.props.reqs;
    const { id } = this.props.match.params;

    try {
      const req = items.find(req => req.id == id);
    } catch (err) {
      dispatch(reqActions.getReq(id));
      // console.log(err)
    }

  }

  render() {

    const { reqs, dispatch } = this.props;
    const { id } = this.props.match.params;

    if (reqs.loading) {
      return(<div>Loading...</div>);
    }

    if (reqs.error) {
      dispatch(alertActions.flash(reqs.error))
      return <Redirect push to='/week' />
    }

    // const req = reqs.items.find(req => req.id == id);



    return (
      null
      // <div>{req.title}</div>
    )
  }
}


function mapStateToProps(state) {
    const { reqs } = state;
    return {
      reqs
    };
}

const connectedReqFullContainer = connect(mapStateToProps)(ReqFullContainer);
export { connectedReqFullContainer as ReqFullContainer };
