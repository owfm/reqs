import React from 'react';
import WeekGrid from './WeekGrid';

import DateSelect from './DateSelect';
import { SchoolInfo } from './SchoolInfo';
import FilterMenu from './FilterMenu';
import FilterChips from './FilterChips';


function MainDisplay(props) {

      return (
        <div>
          <FilterChips
            handleRemoveFilter={props.handleRemoveFilter}
            filters={props.filters}/>

            <div style={{zIndex: '0'}}>
            {/* <SchoolInfo
              school={props.school}
            /> */}
            <DateSelect
              weekNumber={props.weekNumber}
              currentWbStamp={props.currentWbStamp}
              handleWeekChange={props.handleWeekChange}
              />

          </div>

          <WeekGrid
            currentWbStamp={props.currentWbStamp}
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
