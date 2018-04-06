import React from 'react';
import { Card, CardHeader, CardText } from 'material-ui/Card';
import Toggle from 'material-ui/Toggle';


const styles = {
  block: {
    maxWidth: 250,
  },
  toggle: {
    marginBottom: 16,
  }
};

class FilterSites extends React.Component {
  constructor(props){
    super(props);

    const sites = {};

    for (let site in props.school.sites) {
      sites[props.school.sites[site].name] = false;
    }

    this.state = {
      all: true,
      sites
    }
  };


render() {



  const siteToggles = this.props.school.sites.map(
    site => {

    const siteName = site.name;

    try {
      const filters = {...this.props.filters};
      const toggled = filters.sites[siteName];

      return(
        <Toggle
          toggled={toggled}
          key={site.name}
          name={site.name}
          label={site.name}
          labelPosition="right"
          style={styles.toggle}
          defaultToggled={true}
          onToggle={this.props.handleFilterToggle}
        />
      )
    }
    catch (err) {
      console.error(err);
    }

        }
  );


  return(
    <div style={{display:'flex'}}>
      {siteToggles}
    </div>


  )

}
}

export default FilterSites;
