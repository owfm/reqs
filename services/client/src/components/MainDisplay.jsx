import React from 'react';
import WeekGrid from './WeekGrid';
import FilterReqs from './FilterReqs';
import FilterSites from './FilterSites';
import DateSelect from './DateSelect';
import { SchoolInfo } from './SchoolInfo';
import Paper from 'material-ui/Paper';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import FilterMenu from './FilterMenu';
import FilterChips from './FilterChips';


function MainDisplay(props) {

      return (
        <div>
          <FilterChips
            handleRemoveFilter={props.handleRemoveFilter}
            filters={props.filters}/>
          {/* <Paper
            zDepth={3}
            style={{display: 'flex', flexDirection: 'row', flexWrap: 'wrap', marginBottom: '50px'}}>

            <div style={{display: 'flex', justifyContent: 'center', zIndex: '0'}}>
            <FilterReqs
              filters={props.filters}
              school={props.school}
              handleFilterToggle={props.handleFilterToggle}/>
            </div>
            <div style={{zIndex: '0'}}>
            <FilterSites
              filters={props.filters}
              style={{zIndex: '0'}}
              school={props.school}
              handleFilterToggle={props.handleFilterToggle}
            />
            </div>
          </Paper> */}


            <div style={{zIndex: '0'}}>
            <SchoolInfo
              school={props.school}
              weekNumber={props.weekNumber}
            />
            <DateSelect
              currentWbDate={props.currentWbDate}
              handleWeekChange={props.handleWeekChange}
              />

          </div>

          <WeekGrid
            currentWbDate={props.currentWbDate}
            emitSnackbar={props.emitSnackbar}
            handleSetModalObject={props.handleSetModalObject}
            handleModalOpen={props.handleModalOpen}
            handleSetModalType={props.handleSetModalType}
            role={props.user.role_code}
            sessions={props.sessions}
            school={props.school}
            periods={6}
            />

            <FilterMenu
              school={props.school}
              filters={props.filters}
              handleFilterToggle={props.handleFilterToggle}
            />
        </div>
      )
}

export default MainDisplay;
