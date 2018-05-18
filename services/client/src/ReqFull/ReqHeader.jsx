import React from 'react';
import { DoneChip, IssueChip } from '../_components';

const styles = {
  headerDiv: {
    justifyContent: 'center',
    padding: '5px',
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'nowrap',
    justifyItems: 'space-between',
    alignItems: 'middle',
    background:'palevioletred'
  },
  header: {
    color: 'white',
    fontSize: '22px',
    margin: '0',
    fontWeight: '500'
  }
}

const ReqHeader = (props) => {
  const title = `${props.req.week || ''}${props.req.day}${props.req.period} ${props.req.room.name}${props.req.classgroup.name}`

  const isDone = props.req.isDone;
  const hasIssue = props.req.hasIssue;

  return (
<div>
    <div style={styles.headerDiv}>
        <h1 style={styles.header}>{title}</h1>
    </div>
  <div>

        {isDone && <DoneChip style={{margin: '0px', padding: '0px'}}/>}
        {hasIssue && <IssueChip style={{margin: '0px', padding: '0px'}}/>}
      </div>
</div>
  )

};

export { ReqHeader };
