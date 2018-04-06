import React from 'react';
import CircularProgress from 'material-ui/CircularProgress';

const styles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },

  center: {
    marginTop: '50px'
  }
}

const Loading = () => (
  <div style={styles.container}>
    <div style={styles.center}>
      <CircularProgress size={50} thickness={8} />
    </div>

  </div>


)

export default Loading;
