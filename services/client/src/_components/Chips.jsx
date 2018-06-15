import React from 'react';
import { red500, red900, green500, green900 } from 'material-ui/styles/colors';
import Avatar from 'material-ui/Avatar';
import Chip from 'material-ui/Chip';
import FontIcon from 'material-ui/FontIcon';

const styles = {
  chip: {
    margin: '10px',
    flexBasis: 'content',
    fontWeight: 'bold',
  },
  chipDone: {
    margin: '10px',
    flexBasis: 'content',
    fontWeight: 'bold',
  },

  chipContainer: {
    display: 'flex',
    flexWrap: 'nowrap',
  },
};

export const DoneChip = () =>

  (<Chip
    backgroundColor={green500}
    style={styles.chipDone}
  >
    <Avatar
      backgroundColor={green900}
      color="rgba(229,234,212, 1.0)"
      icon={<FontIcon className="material-icons">check</FontIcon>}
    />
    Done
   </Chip>
  );


export const IssueChip = () => (
  <Chip
    backgroundColor={red500}
    style={styles.chipDone}
  >
    <Avatar
      backgroundColor={red900}
      color="rgba(229,234,212, 1.0)"
      icon={<FontIcon className="material-icons">error</FontIcon>}
    />
        Issue
  </Chip>
);


export const UserChip = props => (

  <Chip
    style={styles.chip}
    onClick={() => props.user.email}
  >
    <Avatar
      icon={<FontIcon className="material-icons">email</FontIcon>}
    />
    {props.user.staff_code}
  </Chip>
);

export const GeneralChip = props => (
  <Chip style={styles.chip}>
    {props.children}
  </Chip>

);
