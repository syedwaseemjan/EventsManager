<template>
  <q-page>
    <div class="q-pa-md">
      <q-table
        title="Events"
        row-key="name"
        :rows="rows"
        :columns="columns"
        v-model:pagination="pagination"
        :loading="loading"
        @request="onRequest"
      >
        <template v-slot:body-cell-action="props">
          <q-td :props="props">
            <div v-if="user != null" class="q-gutter-sm">
              <q-btn
                v-if="props.row.creator == user.pk"
                color="secondary"
                label="Edit"
                size="sm"
                @click="editEvent(props.row)"
              />
              <q-btn
                v-else-if="props.row.is_user_participant == false"
                color="primary"
                label="Join"
                size="sm"
                @click="join(props.row)"
              />
              <q-btn
                v-else-if="props.row.is_user_participant == true"
                color="red"
                label="Withdraw"
                size="sm"
                @click="withdraw(props.row)"
              />
            </div>
          </q-td>
        </template>
        <template v-slot:body-cell-total_participants="props">
          <q-td :props="props">
            <q-btn
              title="Click to load participants list"
              color="deep-orange"
              :label="props.value"
              size="sm"
              @click="loadParticipants(props.row)"
            />
          </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { eventStore } from "stores/event";
import { mapStores, mapState } from "pinia";
import { eventsAPI } from "../api";

export default {
  name: "EventsList",
  data() {
    return {
      loading: false,
      pagination: {
        sortBy: "desc",
        descending: false,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 0,
      },
      columns: [
        { name: "action", label: "", field: "action", align: "center" },
        { name: "title", align: "left", label: "Title", field: "title" },
        {
          name: "description",
          align: "left",
          label: "Description",
          field: "description",
        },
        { name: "date", label: "Date", field: "date", align: "center" },
        {
          name: "total_participants",
          label: "Total Participants",
          field: "total_participants",
          align: "center",
        },
        {
          name: "creator_username",
          align: "left",
          label: "Creator",
          field: "creator_username",
        },
      ],
      rows: [],
    };
  },

  computed: {
    ...mapStores(eventStore),
    ...mapState(eventStore, {
      user: "user",
    }),
  },

  methods: {
    loadEvents(params) {
      eventsAPI.loadEvents(params).then(({ data }) => {
        this.rows = data.results;
        this.pagination.rowsNumber = data.count;
        if (params) {
          this.pagination.rowsPerPage = params.page_size;
          this.pagination.page = params.page;
        }
      });
    },
    onRequest(props) {
      const params = {
        page_size: props.pagination.rowsPerPage,
        page: props.pagination.page,
      };
      this.loadEvents(params);
    },
    editEvent(event) {
      this.$router.push({
        name: "edit-event",
        params: {
          eventId: event.event_id,
        },
      });
    },
    join(event) {
      eventsAPI.signUpForEvent(event.event_id).then(() => {
        event.total_participants += 1;
        event.is_user_participant = true;
      });
    },
    withdraw(event) {
      eventsAPI.withdrawFromEvent(event.event_id).then(() => {
        event.total_participants -= 1;
        event.is_user_participant = false;
      });
    },
    loadParticipants(event) {
      this.$router.push({
        name: "participants-list",
        params: {
          eventId: event.event_id,
        },
      });
    },
  },

  mounted() {
    this.loadEvents();
  },
};
</script>
