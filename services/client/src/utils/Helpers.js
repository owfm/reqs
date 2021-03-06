import axios from 'axios';

export const getUser = () => axios.get(
  `${process.env.REACT_APP_USERS_SERVICE_URL}/users/me`,
  {
    headers:
      { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
  },
);

export const getSchool = () => axios.get(
  `${process.env.REACT_APP_USERS_SERVICE_URL}/schools`,
  {
    headers:
      { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
  },
);

export const postNewReq = (data) => {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;

  const res = axios.post(url, data, {
    headers:
    { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
  });

  return res;
};

export const getWeekNumber = date => axios.get(
  `${process.env.REACT_APP_USERS_SERVICE_URL}/schools/check?date=${date}`,
  {
    headers:
      { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
  },
);


export const getReqs = (older = null) => {
  let url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs`;
  if (older) {
    url = url.concat(`?older=${older}`);
  }

  return axios.get(
    url,
    {
      headers:
      { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
    },
  );
};

export const postReqEdit = (oldReq, newReq) => {
  const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/reqs/${oldReq.id}`;

  const patch = [];

  for (const key in newReq) {
    if (key === 'title' || key === 'equipment' || key === 'notes') { patch.push({ op: 'replace', path: `/${key}`, value: `${newReq[key]}` }); }
  }

  return axios.patch(url, patch, {
    headers:
    { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` },
  });
};
