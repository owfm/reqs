import React from 'react';
import Loading from './Loading';
import { postReqEdit, postNewReq } from '../utils/Helpers';
import ReqFullForm from './ReqFullForm';
import ReqIssueInfo from './ReqIssueInfo';
import { ReqHeader } from './ReqHeader';
import './ReqFull.css';

class ReqFull extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      req: {...this.props.req},

      isEditing: false,
    }
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handlePostNewReq = this.handlePostNewReq.bind(this);
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleEditReq = this.handleEditReq.bind(this);
    this.handlePostNewReq = this.handlePostNewReq.bind(this);
  }

  handlePostNewReq (e) {
    e.preventDefault();
    const data = {
      'lesson_id': this.props.req.id,
      'title': this.state.req.title,
      'equipment': this.state.req.equipment,
      'notes': this.state.req.notes,
      'currentWbDate': this.props.currentWbDate
    }

    postNewReq(data)
    .then((res) => {
      this.props.emitSnackbar(res.data.message);
      this.props.updateStateWithNewOrEditedReq(res.data.data);
      this.props.handleModalClose();
    })
    .catch((err) => this.props.emitSnackbar(err))
  }

  handleEditClick (e) {
    e.preventDefault();

    const isEditing = this.state.isEditing;

    if (isEditing){
      // discard changes, revert back to props.
      this.setState ({
        req: {title: this.props.req.title,
              equipment: this.props.req.equipment,
              notes: this.props.req.notes}
            })
        isEditing: false;
    }
    this.setState({
      isEditing: !isEditing
    })
  }

  // TODO: ON SAVE EDITED REQ, UPDATE STATE OBJECT WITH NEW VERSION

  handleEditReq(e) {
    e.preventDefault();
    postReqEdit(this.props.req, this.state.req)
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

    if (this.props.req) {

      const isEditing = this.state.isEditing;
      const hasIssue = this.props.req.hasIssue;

      return(

        <div>

        <ReqHeader req={this.props.req}/>

        <ReqFullForm
          handlePostNewReq={this.handlePostNewReq}
          handleModalClose={this.props.handleModalClose}
          handlePostNewReq={this.handlePostNewReq}
          handleEditReq={this.handleEditReq}
          isEditing={isEditing}
          handleInputChange={this.handleInputChange}
          req={this.state.req}
          handleEditClick={this.handleEditClick}
          roleCode={this.props.roleCode}
        />

        {hasIssue && <ReqIssueInfo req={this.props.req}/>}

      </div>
    )} else {
      return (
        <Loading />
      )
    }
  }
}



export default ReqFull;
