import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import moment from 'moment';


import { filterActions } from '../_actions';

class HomePage extends React.Component {
    componentDidMount() {

    }

    render() {
        const { user, wbStamp } = this.props;
        return (
            <div className="col-md-6 col-md-offset-3">
                <h1>Hi {user.name}!</h1>

                <p>
                    <Link to="/logout">Logout</Link>
                    <br/>
                    <Link to={`/week/${wbStamp}`}>Teach</Link>

                </p>
            </div>
        );
    }
}

function mapStateToProps(state) {
    const { authentication } = state;
    const { user } = authentication;

    const now = moment();

    return {
        user,
        wbStamp: filterActions.getWbStampFromDate(now)
    };
}

const connectedHomePage = connect(mapStateToProps)(HomePage);
export { connectedHomePage as HomePage };
