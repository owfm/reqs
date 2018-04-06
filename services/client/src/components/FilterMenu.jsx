import React, {Component} from 'react';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentFilterList from 'material-ui/svg-icons/content/filter-list';
import NavigationClose from 'material-ui/svg-icons/navigation/close';
import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';
import Toggle from 'material-ui/Toggle';


export default class FilterMenu extends Component {
  constructor(props){
    super(props);

    this.state = {
      openMenu: false,
      filters: {...props.filters}
    }
  }

  handleOpenMenu = () => {
    this.setState({
      openMenu: true,
    });
  }

  handleOnRequestChange = (value) => {
    this.setState({
      openMenu: value,
    });
  }

  render() {

    const SiteFilterToggles = this.props.school.sites.map(site => {

      const siteName = site.name;

      try {
        const filters = {...this.props.filters};
        const toggled = filters.sites[siteName];
        return(
          <ListItem
            key={siteName}
            rightToggle={<Toggle toggled={toggled} name={siteName} onToggle={this.props.handleFilterToggle}/>}
            primaryText={site.name}
          />
        )
      }
      catch (err) {
        console.error(err);
      }
    }
  )


  return (
    <div>
      <IconMenu
        style={{position: 'fixed', bottom: '70px', right: '70px'}}
        iconButtonElement={<FloatingActionButton style={{position: 'fixed', right:'20px', bottom: '20px'}}>{this.state.openMenu ? <NavigationClose/> : <ContentFilterList />}</FloatingActionButton>}
        open={this.state.openMenu}
        onRequestChange={this.handleOnRequestChange}
        >
          <List>
            <Subheader>Filter Requisitions</Subheader>
            <ListItem
              rightToggle={<Toggle toggled={this.props.filters.isDone} name="isDone" onToggle={this.props.handleFilterToggle}/>}
              secondaryText="Completed"
            />
            <ListItem
              rightToggle={<Toggle toggled={this.props.filters.hasIssue} name="hasIssue" onToggle={this.props.handleFilterToggle}/>}
              secondaryText="Problems"
            />
            <Divider/>
            <Subheader>Sites</Subheader>
            {SiteFilterToggles}

          </List>
        </IconMenu>
      </div>
    );
  }
}
