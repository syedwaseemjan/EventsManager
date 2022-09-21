import axios from "axios";

const ajax = axios.create({
  baseURL:
    process.env.VUE_APP_BASE_URL !== undefined
      ? process.env.VUE_APP_API_URL
      : "http://0.0.0.0:7000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

ajax.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const usersAPI = {
  login(email, password) {
    return ajax.post("/login/", { email, password });
  },
  logout() {
    return ajax.post("/logout/", {});
  },
  signup(email, password1, password2) {
    return ajax.post("/registration/", { email, password1, password2 });
  },
  getUserDetails() {
    return ajax.get("/user/");
  },
};

const eventsAPI = {
  createEvent(payload) {
    return ajax.post("/events/", payload);
  },
  getEvent(eventID) {
    return ajax.get(`/events/${eventID}/`);
  },
  loadEvents(params) {
    return ajax.get("/events/", { params: { ...params } });
  },
  updateEvent(eventID, payload) {
    return ajax.put(`/events/${eventID}/`, payload);
  },
  getEventParticipants(eventID, params) {
    return ajax.get(`/events/${eventID}/participants/`, {
      params: { ...params },
    });
  },
  signUpForEvent(eventID) {
    return ajax.post(`/events/${eventID}/signup_for_event/`);
  },
  withdrawFromEvent(eventID) {
    return ajax.delete(`/events/${eventID}/withdraw_from_event/`);
  },
};

export { ajax, usersAPI, eventsAPI };
