<template>
  <q-page>
    <div class="row flex-center">
      <div class="q-pa-md" style="min-width: 400px">
        <q-form
          @submit="onSubmit"
          class="q-gutter-md"
        >
          <q-input
            filled
            type="email"
            v-model="form.email"
            label="Email *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type your email']"
          />

          <q-input
            filled
            type="password"
            v-model="form.password"
            label="Password *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type your password'
            ]"
          />

          <div>
            <q-btn label="Login" type="submit" color="primary"/>
          </div>
        </q-form>
      </div>
    </div>
  </q-page>
</template>


<script>

import { eventStore } from 'stores/event';
import { mapStores } from 'pinia'

export default {
  name: 'UserLogin',

  data () {
    return {
      form: {
        email: '',
        password: ''
      }
    }
  },

  computed: {
    ...mapStores(eventStore)
  },

  methods: {
    onSubmit () {
      this.eventStore.login(this.form).catch(error => {
        let errors = error.response.data;
        errors = JSON.stringify(errors)
        alert(errors)
      })
    }
  }
}
</script>