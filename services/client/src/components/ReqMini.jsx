import React from 'react';
import './ReqMini.css';


export class ReqMini extends React.Component {

  constructor(props) {
    super(props);

    this.state = ({
      shadow: 1
    })

    this.handleCardClick = this.handleCardClick.bind(this);
  }

  handleCardClick () {
    this.props.handleModalOpen();
    this.props.handleSetModalObject(this.props.session.id, this.props.session.type);
  }

  render() {

    const reqDone = this.props.session.isDone;
    const hasIssue = this.props.session.hasIssue;

    const statusClass = this.props.session.type === 'lesson' ? 'lesson' : reqDone ? 'done' : hasIssue ? 'issue' : 'pending'


    return (
      <div onClick={this.handleCardClick} className={`req-small ${statusClass}`}>
        <h1>{this.props.session.classgroup.name}</h1>
        <h3>({this.props.session.room.name})</h3>
        <div></div>
        <div className='req-mini-info-box'>
          <div><strong>{this.props.session.title}</strong></div>
          <br/>
          <div>{this.props.session.equipment || ''}</div>
          <br/>

          <div>{this.props.session.notes || ''}</div>
        </div>

      </div>
    )

  }


    };

    export default ReqMini;
