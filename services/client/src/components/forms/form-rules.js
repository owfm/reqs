export const registerFormRules = [
  {
    id: 1,
    field: 'name',
    name: 'Name must be greater than 5 characters.',
    valid: false
  },
  {
    id: 2,
    field: 'email',
    name: 'Email must be greater than 5 characters.',
    valid: false
  },
  {
    id: 3,
    field: 'email',
    name: 'Email must be a valid email address.',
    valid: false
  },
  {
    id: 4,
    field: 'password',
    name: 'Password must be greater than 10 characters.',
    valid: false
},
// {
//   id: 5,
//   field: 'staff_code',
//   name: 'Staff code must 3 or more characters.',
//   valid: false
// },
{
  id: 6,
  field: 'school_name',
  name: 'School name is required.',
  valid: false
},
{
   id: 7,
   name: 'Email must be unique.',
   valid: false
}
]

export const loginFormRules = [
  {
    id: 1,
    field: 'email',
    name: 'Email is required.',
    valid: false
  },
  {
    id: 2,
    field: 'password',
    name: 'Password is required.',
    valid: false
  }
];
