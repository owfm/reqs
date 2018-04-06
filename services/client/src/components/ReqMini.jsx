import React from 'react';
import { Card, CardHeader, CardText } from 'material-ui';
import { IssueChip, DoneChip, UserChip, GeneralChip } from './Chips';
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
    const type = this.props.session.type;
    const title = `${this.props.session.week || ''}${this.props.session.day}${this.props.session.period} ${this.props.session.room.name}${this.props.session.classgroup.name}`


    return (
      <div onClick={this.handleCardClick} class='req-small'>
        <div class='req-small-header'>
          <div class='req-small-time-info'>
            <p>{this.props.session.week}{this.props.session.day}{this.props.session.period} {this.props.session.time}</p>
          </div>
        <h1>{this.props.session.title}</h1>
        <h1>{this.props.session.room.name}</h1>
        {reqDone && <h1>DONE</h1>}
        </div>
        <div class='req-small-info'>
          <p>{this.props.session.teacher.staff_code} {this.props.session.classgroup.name}</p>
        </div>
      </div>
    )

  }


    };

    export default ReqMini;
