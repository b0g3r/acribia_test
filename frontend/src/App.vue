<template>
  <v-app>
    <v-content>
      <HelloWorld/>
    </v-content>
    <v-footer fixed app>
      <span>b0g3r & acribia &copy; 2018</span>
    </v-footer>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>
