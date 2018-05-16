import React from 'react';

import { connect } from 'react-redux';



class ReqFullContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {

  }

  render() {

    const { items } = this.props.reqs;
    const { id } = this.props.match.params;

    const req = items.find(req => req.id == id);
    console.log(req);

    return (
      <div>{req.title}</div>
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
