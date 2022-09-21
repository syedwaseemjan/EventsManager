<template>
  <q-page>
    <div class="row flex-center">
      <div class="q-pa-md" style="min-width: 400px">
        <q-form class="q-gutter-md" @submit="onSubmit">
          <q-input
            v-model="form.title"
            filled
            type="text"
            label="Event Title *"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type event title',
            ]"
          />

          <q-input
            v-model="form.description"
            filled
            type="textarea"
            label="Event Description *"
            lazy-rules
            :rules="[
              (val) =>
                (val && val.length > 0) || 'Please type event desciption',
            ]"
          />

          <div class="row">
            <q-input
              v-model="form.date"
              filled
              type="date"
              hint="Event Date *"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type event date',
              ]"
              class="q-mr-md"
              @change="dateChanged"
            />

            <q-input
              v-model="form.time"
              filled
              type="time"
              hint="Event Time *"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type event time',
              ]"
              @change="timeChanged"
            />
          </div>
          <div>
            <q-btn type="submit" color="primary">
              {{ eventId ? "Update" : "Create" }} Event
            </q-btn>
          </div>
        </q-form>
      </div>
    </div>
  </q-page>
</template>

<script>
import { eventStore } from "stores/event";
import { mapStores } from "pinia";
import { eventsAPI } from "../api";

export default {
  name: "ManageEvent",
  props: {
    eventId: {
      type: String,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      form: {
        title: "",
        description: "",
        date: "",
        time: "",
        datetime: "",
      },
    };
  },

  computed: {
    ...mapStores(eventStore),
  },

  mounted() {
    this.loadEvent();
  },

  methods: {
    loadEvent() {
      if (this.eventId == null) {
        return;
      }
      eventsAPI
        .getEvent(this.eventId)
        .then((response) => {
          const data = response.data;
          let datetime = new Date(data.date);
          let time = datetime.toLocaleTimeString();
          let date = datetime.toISOString().split("T")[0];
          this.form = {
            title: data.title,
            description: data.description,
            date: date,
            time: time,
            datetime: datetime,
          };
        })
        .catch((error) => {
          if (error.response) {
            let errors = error.response.data;
            errors = JSON.stringify(errors);
            alert(errors);
          } else {
            console.error(error);
          }
        });
    },
    dateChanged(date) {
      if (this.form.time) {
        const timeString = this.form.time + ":00";
        this.form.datetime = new Date(date + " " + timeString);
      }
    },
    timeChanged(time) {
      if (this.form.date) {
        const timeString = time + ":00";
        this.form.datetime = new Date(this.form.date + " " + timeString);
      }
    },
    onSubmit() {
      const payload = {
        title: this.form.title,
        description: this.form.description,
        date: this.form.datetime,
      };
      let eventPromise = null;
      if (this.eventId != null) {
        eventPromise = this.updateEvent(payload);
      } else {
        eventPromise = this.createEvent(payload);
      }

      eventPromise
        .then(() => {
          this.$router.push({ name: "home" });
        })
        .catch((error) => {
          if (error.response) {
            let errors = error.response.data;
            errors = JSON.stringify(errors);
            alert(errors);
          } else {
            console.error(error);
          }
        });
    },
    createEvent(payload) {
      return eventsAPI.createEvent(payload);
    },
    updateEvent(payload) {
      return eventsAPI.updateEvent(this.eventId, payload);
    },
  },
};
</script>
