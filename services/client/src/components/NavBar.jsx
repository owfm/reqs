import React from 'react';
import { BrowserRouter as Link } from "react-router-dom";
import { NavItem, Navbar } from 'react-materialize';

const NavBar = (props) => (
  <Navbar>
    <NavItem>{props.name}</NavItem>
    <NavItem to='/'>Home</NavItem>
    <NavItem to='/teach'>Teach</NavItem>
    {props.isAuthenticated ? <Link to='/logout'>Logout</Link> : <Link to='/login'>Login</Link>}
    {/* {props.user.role_code} */}
</Navbar>
)

export default NavBar;
