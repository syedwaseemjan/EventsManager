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
            v-model="form.password1"
            label="Password *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type your password'
            ]"
          />

          <q-input
            filled
            type="password"
            v-model="form.password2"
            label="Repeat password *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Re-enter your password'
            ]"
          />

          <div>
            <q-btn label="Signup" type="submit" color="primary"/>
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
  name: 'UserSignup',

  data () {
    return {
      form: {
        email: '',
        password1: '',
        password2: ''
      }
    }
  },

  computed: {
    ...mapStores(eventStore)
  },

  methods: {
    onSubmit () {
      this.eventStore.signup(this.form).catch(error => {
        let errors = error.response.data;
        errors = JSON.stringify(errors)
        alert(errors)
      })
    }
  }
}
</script>