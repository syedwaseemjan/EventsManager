<template>
  <q-layout view="hHh lpR fFf">
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
import { eventStore } from 'stores/event';
import { mapStores, mapState } from 'pinia'

export default defineComponent({
  name: 'MainLayout',

  data () {
    return {
    }
  },

  computed: {
    ...mapStores(eventStore),
    ...mapState(eventStore, {
      isUserAuthenticated: "isUserAuthenticated"
    }),
    headerLinks (){
      let links = []
      if (this.isUserAuthenticated) {
        links.push(...[
          {label: "Home", url: '/'},
          {label: "New Event", url: '/new-event'},
          {label: "Logout", url: '/logout'},
        ])
      } else {
        links.push(...[
          {label: "Home", url: '/'},
          {label: "Login", url: '/login'},
          {label: "Signup", url: '/signup'},
        ])
      }
      return links;
    }

  },

  methods: {
    navigationPreprocessor (event, tabName) {
      if (tabName == "Logout") {
        event.preventDefault()
        this.eventStore.logout()
      }
    }
  }
})
</script>
