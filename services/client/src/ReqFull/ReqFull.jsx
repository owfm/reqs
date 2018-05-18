import React from 'react';
import { postReqEdit, postNewReq } from '../utils/Helpers';
import { ReqFullForm, ReqHeader, ReqIssueInfo } from '/';

import './ReqFull.css';

class ReqFull extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      req: {...this.props.session},
      valid: false,
      isEditing: false,
    }
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handlePostNewReq = this.handlePostNewReq.bind(this);
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleEditReq = this.handleEditReq.bind(this);
    this.handlePostNewReq = this.handlePostNewReq.bind(this);
    this.goBack = this.goBack.bind(this);
  }

  goBack(){
    this.props.history.goBack();
  }

  handlePostNewReq (e) {
    e.preventDefault();
    const data = {
      'lesson_id': this.props.session.id,
      'title': this.state.req.title,
      'equipment': this.state.req.equipment,
      'notes': this.state.req.notes,
      'currentWbDate': this.props.currentWbDate
    }

    postNewReq(data)
    .then((res) => {
      this.props.emitSnackbar(res.data.message);
      this.props.updateStateWithNewOrEditedReq(res.data.data);
    })
    .catch((err) => this.props.emitSnackbar(err))
  }

  handleEditClick (e) {
    e.preventDefault();

    const isEditing = this.state.isEditing;

    if (isEditing){
      // discard changes, revert back to props.
      this.setState ({
        req: {title: this.props.session.title,
              equipment: this.props.session.equipment,
              notes: this.props.session.notes}
            })
        isEditing: false
    }
  }

  handleEditReq(e) {
    e.preventDefault();
    postReqEdit(this.props.session, this.state.req)
    .then((res) => {
      this.setState({
        isEditing: false,
      });
      this.props.handleModalClose();
      this.props.emitSnackbar(res.data.message)
      this.props.updateStateWithNewOrEditedReq(res.data.data);
    })
    .catch((err) => console.error(err))
  }

  handleInputChange(e) {
    const target = e.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    var req = {...this.state.req}
    req[name] = value;

    this.setState({
      req
    })

  }


  render() {

    if (this.props.session) {

      const hasIssue = this.props.session.hasIssue;
      const valid = this.state.valid;

      return(

        <div>

        <button onClick={this.goBack}>Back</button>

        <ReqHeader req={this.props.session}/>

        <ReqFullForm
          handlePostNewReq={this.handlePostNewReq}
          handleModalClose={this.props.handleModalClose}
          handlePostNewReq={this.handlePostNewReq}
          handleEditReq={this.handleEditReq}
          valid={valid}
          handleInputChange={this.handleInputChange}
          req={this.state.req}
          handleEditClick={this.handleEditClick}
          roleCode={this.props.roleCode}
        />

        {hasIssue && <ReqIssueInfo req={this.props.session}/>}

      </div>
    )} else {
      return (
        <div>Loading...</div>
      )
    }
  }
}



export { ReqFull };
