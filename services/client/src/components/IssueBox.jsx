import React from 'react';

const IssueBox = (props) => {

      return (
         <div className="issuebox">
         <h4>Marked problematic by {props.issue_technician.name}:</h4>
         <input
            type='text'
            disabled='true'
            value={props.issue_text} />
         </div>
      )

};

export default IssueBox;
