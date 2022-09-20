<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="text-white shadow-2 rounded-borders">
        Events App
        <q-space />
        <q-tabs shrink
          v-for="headerLink in headerLinks"
          :key="headerLink.label">
          <q-route-tab :to="headerLink.url" exact replace :label="headerLink.label" @click="navigationPreprocessor($event, headerLink.label)" />
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'MainLayout',

  data () {
    return {
      headerLinks: [
        {label: "Home", url: '/'},
        {label: "New Event", url: '/new-event'},
        {label: "Logout", url: '/logout'},
        {label: "Login", url: '/login'},
        {label: "Signup", url: '/signup'},
      ]
    }
  },

  methods: {
    navigationPreprocessor (event, tabName) {
      if (tabName == "Logout") {
        event.preventDefault()
        this.$router.push({ path: '/' })
      }
    }
  }
})
</script>
