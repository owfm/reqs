import React from 'react';
import { Card, CardHeader, CardText } from 'material-ui/Card';

export const SchoolInfo = (props) => {

return (
  <Card style={{margin: '10px', flexBasis: 'content'}}>
    <CardHeader
      title={props.school.name}
    />
    <CardText>
      Week: {props.weekNumber}

    </CardText>
  </Card>
)

}
