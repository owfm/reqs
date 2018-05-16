import React from 'react';
import { Redirect } from 'react-router';

import './ReqMini.css';
import Truncate from 'react-truncate';
import ActionBuild from 'material-ui/svg-icons/action/build';
import ActionDescription from 'material-ui/svg-icons/action/description';

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

    const { session } = this.props;
    const { isDone, hasIssue, type } = session;
    const { id } = session;
    const equipmentSet = session.equipment !== "";
    const notesSet = session.notes !== "";

    const statusClass = type === 'lesson' ? 'lesson' : isDone ? 'done' : hasIssue ? 'issue' : 'pending'



    if (this.state.redirect && type === 'requisition') {
      return <Redirect push to={`requisition/${id}`} />
    }

    if (this.state.redirect && type === 'lesson') {
      return <Redirect push to={`submit/${id}`} />
    }

    return (
      <div onClick={this.handleCardClick} className={`req-small`}>
        <div className={`status-bar ${statusClass}`}></div>
        <h1>{this.props.session.classgroup.name}</h1>
        <h3>({this.props.session.room.name})</h3>
        <div></div>
        {this.props.session.type === 'lesson' && <div className={'add-req-label'}>+ add req</div>}
        <div className='req-mini-info-box'>
          <div><strong>{this.props.session.title}</strong></div>
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
