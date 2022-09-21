import { defineStore } from "pinia";
import { usersAPI } from "../api";

export const eventStore = defineStore("event", {
  state: () => ({
    token: localStorage.getItem("token"),
    user: JSON.parse(localStorage.getItem("user")),
    returnUrl: null,
  }),

  getters: {
    isUserAuthenticated() {
      return this.token != null;
    },
  },

  actions: {
    login(form) {
      return usersAPI.login(form.email, form.password).then((response) => {
        this.token = response.data.key;
        localStorage.setItem("token", this.token);
        this.getUserDetails();
        this.router.push(this.returnUrl || "/");
      });
    },
    signup(form) {
      return usersAPI
        .signup(form.email, form.password1, form.password2)
        .then((response) => {
          this.token = response.data.key;
          localStorage.setItem("token", this.token);
          this.getUserDetails();
          this.router.push(this.returnUrl || "/");
        });
    },

    logout() {
      return usersAPI.logout().then(() => {
        this.token = null;
        this.user = null;
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        this.router.push("/");
      });
    },

    getUserDetails() {
      return usersAPI.getUserDetails().then((response) => {
        this.user = response.data;
        localStorage.setItem("user", JSON.stringify(response.data));
      });
    },
  },
});
