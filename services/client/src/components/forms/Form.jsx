import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import { Card } from 'material-ui/Card';

import { registerFormRules, loginFormRules } from './form-rules.js';
import FormErrors from './FormErrors.jsx';
import TextField from 'material-ui/TextField';


class Form extends Component {
  constructor (props) {
    super(props);
    this.state = {
      formData: {
        name: '',
        email: '',
        school_name: '',
        staff_code: '',
        password: ''
      },
      registerFormRules: registerFormRules,
      loginFormRules: loginFormRules,
      valid: false,
    };
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
  };
  componentDidMount() {
    this.clearForm();
  };


  componentWillReceiveProps(nextProps) {
    if (this.props.formType !== nextProps.formType) {
      this.clearForm();
      this.resetRules();
    };
  };
  clearForm() {
    this.setState({
      formData: {name: '', email: '', password: '', staff_code: '', school_name: ''}
    });
  };

  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
    this.validateForm();
  };

  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = this.props.formType
    let data;
    if (formType === 'login') {
      data = {
        email: this.state.formData.email,
        password: this.state.formData.password
      };
    };
    if (formType === 'register') {
      data = {
        name: this.state.formData.name,
        email: this.state.formData.email,
        password: this.state.formData.password,
        staff_code: this.state.formData.staff_code,
        school_name: this.state.formData.school_name
      };
    };
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;

    axios.post(url, data)
    .then((res) => {
      this.props.emitSnackbar(res.data.message);
      this.clearForm();
      this.props.loginUser(res.data.user, res.data.auth_token);
    })
    .catch((err) => {
      if (formType === 'login') {
        console.error(err);
        this.props.emitSnackbar('User does not exist.', 'danger');
      };
      if (formType === 'register') {
        this.props.emitSnackbar('That user already exists.', 'danger');
      };
    });
  };
  allTrue() {
    let formRules = registerFormRules;
    if (this.props.formType === 'login') {
      formRules = loginFormRules;
    }
    for (const rule of formRules) {
      if (!rule.valid) return false;
    }
    return true;
  };
  resetRules() {
    if (this.props.formType === 'login') {
      const formRules = this.state.loginFormRules;
      for (const rule of formRules) {
        rule.valid = false;
      }
      this.setState({loginFormRules: formRules})
    }
    if (this.props.formType === 'register') {
      const formRules = this.state.registerFormRules;
      for (const rule of formRules) {
        rule.valid = false;
      }
      this.setState({registerFormRules: formRules})
    }
    this.setState({valid: false});
  };

  validateEmail(email) {
    // eslint-disable-next-line
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  };


  validateForm() {
    // define self as this
    const self = this;
    // get form data
    const formData = this.state.formData;
    // reset all rules
    self.resetRules()
    // validate register form
    if (self.props.formType === 'register') {
      const formRules = self.state.registerFormRules;
      if (formData.name.length > 5) formRules[0].valid = true;
      if (formData.email.length > 5) formRules[1].valid = true;
      if (this.validateEmail(formData.email)) formRules[2].valid = true;
      if (formData.password.length > 10) formRules[3].valid = true;
      // if (formData.staff_code.length > 2) formRules[4].valid = true;
      if (formData.school_name.length > 0) formRules[4].valid = true;
      if (this.state.emailAvailable && !this.state.checkingEmail) formRules[5].valid = true;
      self.setState({registerFormRules: formRules})
      if (self.allTrue()) self.setState({valid: true});
    }
    // validate login form
    if (self.props.formType === 'login') {
      const formRules = self.state.loginFormRules;
      if (formData.email.length > 0) formRules[0].valid = true;
      if (formData.password.length > 0) formRules[1].valid = true;
      self.setState({registerFormRules: formRules})
      if (self.allTrue()) self.setState({valid: true});
    }
  };
  render() {
    if (this.props.isAuthenticated) {
      return <Redirect to='/' />;
    };
    let formRules = this.state.loginFormRules;
    if (this.props.formType === 'register') {
      formRules = this.state.registerFormRules;
    }

    return (

    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: '60%'}}>

        <Card style={{padding: '20px'}}>


          <h1 style={{'textTransform':'capitalize'}}>{this.props.formType}</h1>
          <FormErrors
            formType={this.props.formType}
            formRules={formRules}
          />
          <form onSubmit={(e) => this.handleUserFormSubmit(e)}>

          {this.props.formType === 'register' &&
            <TextField
            name="name"
            hintText="Please enter your name"
            floatingLabelText="Name"
            floatingLabelFixed={true}
            value={this.state.formData.name}
            onChange={this.handleFormChange}
          />

          }

          <TextField
              name="email"
              type="email"
              placeholder="Enter an email address"
              required
              value={this.state.formData.email}
              onChange={this.handleFormChange}
            />

            <br/>

            <TextField
                  name="password"
                  hintText="Password Field"
                  floatingLabelText="Password"
                  type="password"
                  value={this.state.formData.password}
                  onChange={this.handleFormChange}
                />
              <br />
          {this.props.formType === 'register' &&
          <div className="form-group">
            <TextField
              name="school_name"
              type="text"
              placeholder="Enter the name of the school to register"
              required
              value={this.state.formData.school_name}
              onChange={this.handleFormChange}
            />
          </div>}
          {this.props.formType === 'register' &&
          <div className='form-group'>
            <TextField
              name="school_code"
              type="text"
              placeholder="Enter your teacher code."
              required
              value={this.state.formData.school_code}
              onChange={this.handleFormChange}
            />
          </div>
        }

        <input
          type="submit"
          className="btn btn-primary btn-lg btn-block"
          value="Submit"
          disabled={!this.state.valid}
        />
      </form>
    </Card>
      </div>
    </div>
    )
  };
};

export default Form;
