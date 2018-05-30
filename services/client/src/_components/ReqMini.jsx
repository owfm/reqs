import React from 'react';
import { Redirect } from 'react-router';

import './ReqMini.css';
import Truncate from 'react-truncate';
import ActionBuild from 'material-ui/svg-icons/action/build';
import ActionDescription from 'material-ui/svg-icons/action/description';
import moment from 'moment';

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

    const { session, currentWbStamp } = this.props;
    const { isDone, hasIssue, type } = session;
    const { id } = session;

    if (this.state.redirect) {
      return <Redirect push to={`${currentWbStamp}/${type}/${id}`} />
    }

    const equipmentSet = session.equipment !== "";
    const notesSet = session.notes !== "";

    const statusClass = type === 'lesson' ? 'lesson' : isDone ? 'done' : hasIssue ? 'issue' : 'pending'


    return (
      <div onClick={this.handleCardClick} className={`req-small`}>
        <div className={`status-bar ${statusClass}`}></div>
        <h1>{this.props.session.classgroup.name}</h1>
        <h3>({this.props.session.room.name})</h3>
        {this.props.session.type === 'lesson' && <div className={'add-req-label'}>+ add req</div>}
        <div className='req-mini-info-box'>
          <div>{this.props.session.type === 'requisition' && moment(this.props.session.time).fromNow()}</div>
          <div><strong>{this.props.session.title}</strong></div>
          <div>{this.props.time}</div>
          <br/>
          {equipmentSet &&
            <Truncate lines={2} ellipsis={<span>... </span>}>
            {this.props.session.equipment}
          </Truncate>
        }
        {notesSet && <Truncate lines={2} ellipsis={<span>... </span>}>
        {this.props.session.notes}
      </Truncate>}
    </div>

  </div>
)

  }





};

export { ReqMini };
