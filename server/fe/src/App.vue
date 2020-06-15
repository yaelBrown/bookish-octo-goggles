<template>
  <div id="app">
    <h1>Yael</h1>
    <Graph/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Graph from './components/Graph.vue'

export default {
  name: 'App',
  components: {
    Graph
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  margin-top: 60px;
}

body{
  background-color: #111111;
}

</style>
