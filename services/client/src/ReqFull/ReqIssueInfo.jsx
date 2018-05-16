import React from 'react';
import FontIcon from 'material-ui/FontIcon';


const ReqIssueInfo = (props) => {
  return (
    <div>
      <h4>This req has a problem</h4>
      <br/>
      <p>
        {props.req.issue_text}
      </p>
      <p>
        Issue assigned by {props.req.issue_technician.name}. <a href={'mailto:' + props.req.issue_technician.email}><FontIcon className="material-icons">email</FontIcon></a>
      </p>
    </div>
  )
}

export default ReqIssueInfo;
