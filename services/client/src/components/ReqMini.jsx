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

    return (
      <div onClick={this.handleCardClick} className='req-small'>
        <div className='req-small-header'>
          <div className='req-small-time-info'>
            <p>{this.props.session.week}{this.props.session.day}{this.props.session.period} {this.props.session.time}</p>
          </div>
        <h1>{this.props.session.title}</h1>
        <h1>{this.props.session.room.name}</h1>
        {reqDone && <h1 style={{fontWeight:'600', color:'#34b21e'}}>DONE</h1>}
        {hasIssue && <h1 stlye={{fontWeight: '600', color: '#b2251d'}}>ISSUE</h1>}

        </div>
        <div className='req-small-info'>
          <p>{this.props.session.teacher.staff_code} {this.props.session.classgroup.name}</p>
        </div>
      </div>
    )

  }


    };

    export default ReqMini;
