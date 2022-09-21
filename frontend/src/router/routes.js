const routes = [
  {
    name: "home",
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/EventsList.vue") },
      {
        name: "new-event",
        path: "events",
        component: () => import("pages/ManageEvent.vue"),
      },
      {
        name: "edit-event",
        path: "events/:eventId",
        props: true,
        component: () => import("pages/ManageEvent.vue"),
      },
      {
        name: "participants-list",
        path: "events/:eventId/participants",
        props: true,
        component: () => import("pages/ParticipantsList.vue"),
      },
      {
        name: "login",
        path: "login",
        component: () => import("pages/UserLogin.vue"),
      },
      {
        name: "signup",
        path: "signup",
        component: () => import("pages/UserSignup.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
