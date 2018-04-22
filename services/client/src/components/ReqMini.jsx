import React from 'react';
import './ReqMini.css';
import Truncate from 'react-truncate';
import ActionBuild from 'material-ui/svg-icons/action/build';
import ActionDescription from 'material-ui/svg-icons/action/description';




export class ReqMini extends React.Component {

  constructor(props) {
    super(props);

    this.handleCardClick = this.handleCardClick.bind(this);
  }

  handleCardClick () {
    this.props.handleModalOpen();
    this.props.handleSetModalObject(this.props.session.id, this.props.session.type);
  }

  render() {

    const reqDone = this.props.session.isDone;
    const hasIssue = this.props.session.hasIssue;

    const equipmentSet = this.props.session.equipment !== "";
    const notesSet = this.props.session.notes !== "";

    const statusClass = this.props.session.type === 'lesson' ? 'lesson' : reqDone ? 'done' : hasIssue ? 'issue' : 'pending'


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

export default ReqMini;
