import React from 'react';
import Loading from './Loading';
import { postReqEdit } from '../utils/Helpers';
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
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleEditReq = this.handleEditReq.bind(this);
    this.handlePostNewReq = this.handlePostNewReq.bind(this);
  }

  handlePostNewReq (e) {

    // TODO: write a helper function to map the updated lesson state object
    // into a req object to be sumbitted. This needs to take account of the
    // dates and times of the current page and ensure it is correctly
    // mapped to the correct week.

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
