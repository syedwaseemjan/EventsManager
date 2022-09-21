<template>
  <q-page>
    <div class="q-pa-md row flex-center">
      <q-table
        v-model:pagination="pagination"
        title="Participants Usernames"
        row-key="name"
        :rows="rows"
        :columns="columns"
        :loading="loading"
        style="width: 30vw"
        @request="onRequest"
      >
        <template #body-cell-username="props">
          <q-td :props="props">
            {{ props.row }}
          </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { eventsAPI } from "../api";

export default {
  name: "ParticipantsList",
  props: {
    eventId: {
      type: String,
      default: null,
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

  mounted() {
    this.loadParticipants();
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
};
</script>
