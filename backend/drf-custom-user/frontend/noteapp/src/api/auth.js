import axios from "axios";

const API_URL = "http://127.0.0.1:8000/account/";

export const register = (email, password, first_name, last_name) => {
  return axios.post(`${API_URL}register`, {
    email,
    password,
    first_name,
    last_name,
  });
};

export const login = (email, password) => {
  return axios.post(`${API_URL}login`, {
    email,
    password,
  });
};
