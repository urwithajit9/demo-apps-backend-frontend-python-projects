import axios from "axios";

const API_URL = "http://127.0.0.1:8000/notes/";

export const createNote = (user, title, content, accessToken) => {
  return axios.post(
    API_URL,
    { user, title, content },
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
};

export const getNotes = (accessToken) => {
  return axios.get(API_URL, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
};
