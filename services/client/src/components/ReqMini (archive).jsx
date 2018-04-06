import React from 'react';
import { Card, CardHeader, CardText } from 'material-ui';
import { IssueChip, DoneChip, UserChip, GeneralChip } from './Chips';

const styles = {
  chipContainer: {
    display: 'flex',
    flexWrap: 'wrap'
  },
  lessonCard: {
    borderRadius: '15px',
    border: '1px solid black'
  },

  reqCard: {
    borderRadius: '0'
  }
}

export class ReqMini extends React.Component {

  constructor(props) {
    super(props);

    this.state = ({
      shadow: 1
    })

    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
    this.handleCardClick = this.handleCardClick.bind(this);
  }

  onMouseOver() {
    this.setState({
      shadow: 3
    })
  }

  onMouseOut() {
    this.setState({
      shadow: 1
    })
  }

  handleCardClick () {
    this.props.handleModalOpen();
    this.props.handleSetModalObject(this.props.req.id, this.props.req.type);
  }

  render() {

    const reqDone = this.props.req.isDone;
    const hasIssue = this.props.req.hasIssue;
    const type = this.props.req.type;
    const title = `${this.props.req.week || ''}${this.props.req.day}${this.props.req.period} ${this.props.req.room.name}${this.props.req.classgroup.name}`


    return (
      <div>
        <Card
          style={type === 'lesson' ? styles.lessonCard : styles.reqCard}
          onClick={this.handleCardClick}
          onMouseOver={this.onMouseOver}
          onMouseOut={this.onMouseOut}
          zDepth={this.state.shadow}
            >
          <CardHeader>{title}</CardHeader>
          <CardText>{this.props.req.title}</CardText>


          <div style={styles.chipContainer}>

            <UserChip user={this.props.req.teacher}/>
            <GeneralChip>
              {this.props.req.room.site.name}
            </GeneralChip>

            {reqDone && <DoneChip />}

            {hasIssue && <IssueChip />}

          </div>

        </Card>
      </div>

    )

  }


    };

    export default ReqMini;
