<template>
<!-- TODO -->
</template>

<script>
export default {
  name: "RoomDevicesTable",
  props: {
    id: String
  },
  data() {
    return {
      loading: false,
      headers: [
        {
          text: "ID",
          align: "start",
          sortable: false,
          value: "name"
        },
        { text: "Type", value: "type" },
        { text: "Действия", value: "actions", sortable: false }
      ],
      data: []
    };
  },
  computed: {
  },
  methods: {},
  components: {},
  created() {}
};
</script>

<style scoped>
</style>
