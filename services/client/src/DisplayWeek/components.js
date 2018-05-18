import styled from 'styled-components';

export const MainGrid = styled.div`
padding: 20px;
display: grid;
grid-template-rows: auto repeat(${props=>props.periods.length}, auto);
grid-gap: 10px;
grid-template-columns: auto repeat(5, 1fr);
`
export const SessionGrid = styled.div`
  display: grid;
  grid-gap: 5px;
`
