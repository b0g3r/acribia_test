<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <v-text-field v-model="host" solo></v-text-field>
        <v-select v-model="deep" :items="[1,2,3]"></v-select>
        <v-btn
          @click="checkHost"
          :disabled="check"
        >Кнопка</v-btn>
        <v-progress-linear
          v-model="progress"
        ></v-progress-linear>
        <v-card>
          <v-card-title>
            Найденные хосты
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :items="hosts"
            :headers="[{text: 'Хост', sortable: false, value: 'host'}]"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.host }}</td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="warning">
              Your search for "{{ search }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      host: 'vuetifyjs.com',
      deep: 1,
      hosts: [],
      search: '',
      check: false,
      counter: {
        full: 1,
        current: 0
      }
    }
  },
  created() {
    this.$options.sockets.onmessage = (data) => this.callback(JSON.parse(data.data))
  },
  methods: {
    checkHost() {
      this.check = true
      this.hosts = []
      this.counter.full = 1
      this.counter.current = 0
      this.$socket.sendObj({host: this.host, deep: this.deep})
    },
    callback(msg) {
      if (msg.action === 'check_start') {
        this.counter.full = msg.data.count
      } else if (msg.action === 'new_host') {
        this.hosts.unshift(msg.data)
        this.counter.current = msg.data.count
      } else if (msg.action === 'progress') {
        this.counter.current = msg.data.count
      } else if (msg.action === 'check_over') {
        this.check = false
      }
    }
  },
  computed: {
    progress() {
      return (this.counter.current / this.counter.full) * 100
    },
  },
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
}
</style>
