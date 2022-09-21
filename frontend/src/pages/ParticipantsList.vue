<template>
  <q-page>
    <div class="q-pa-md row flex-center">
      <q-table
        title="Participants Usernames"
        row-key="name"
        :rows="rows"
        :columns="columns"
        v-model:pagination="pagination"
        :loading="loading"
        @request="onRequest"
        style="width: 30vw"
      >
        <template v-slot:body-cell-username="props">
          <q-td :props="props">
            {{ props.row }}
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
  name: "ParticipantsList",
  props: {
    eventId: {
      type: String,
    },
  },
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
        { name: "username", label: "", field: "username", align: "center" },
      ],
      rows: [],
    };
  },

  methods: {
    loadParticipants(params) {
      eventsAPI.getEventParticipants(this.eventId, params).then(({ data }) => {
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
      this.loadParticipants(params);
    },
  },

  mounted() {
    this.loadParticipants();
  },
};
</script>
