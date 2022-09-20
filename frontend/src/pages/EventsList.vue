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
      />
    </div>
  </q-page>
</template>

<script>

import { eventsAPI } from '../api';

export default {
  data () {
    return {
      loading: false,
      pagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 0
      },
      columns: [
        { name: 'action', label: '', field: 'action', align: 'center' },
        { name: 'title', align: 'left', label: 'Title', field: 'title' },
        { name: 'description', align: 'left', label: 'Description', field: 'description' },
        { name: 'date', label: 'Date', field: 'date', align: 'center' },
        { name: 'total_participants', align: 'left', label: 'Total Participants', field: 'total_participants', align: 'center'},
        { name: 'creator_username', align: 'left', label: 'Creator', field: 'creator_username'},
      ],
      rows: []
    }
  },

  methods: {
    loadEvents(params) {
      eventsAPI.loadEvents(params).then(({ data }) => {
        this.rows = data.results;
        this.pagination.rowsNumber = data.count;
        if (params) {
          this.pagination.rowsPerPage = params.page_size
          this.pagination.page = params.page
        }
      });
    },
    onRequest(props) {
      const params = {
        page_size: props.pagination.rowsPerPage,
        page: props.pagination.page,
      };
      this.loadEvents(params)
    }
  },

  mounted() {
    this.loadEvents()
  }
}
</script>
