<template>
  <div class="app">
    <AppHeader />
    <div class="app-body">
      <Sidebar :nav-items="nav" />
      <main class="main">
        <breadcrumb :list="list" class="mb-0" />
        <div class="container-fluid">
          <nuxt />
        </div>
      </main>
      <AppAside />
    </div>
    <AppFooter />
  </div>
</template>

<script>
import nav from './menu'
import {
  Header as AppHeader,
  Sidebar,
  Aside as AppAside,
  Footer as AppFooter,
  Breadcrumb
} from '~/components/'

export default {
  name: 'Full',
  components: {
    AppHeader,
    Sidebar,
    AppAside,
    AppFooter,
    Breadcrumb
  },
  data() {
    return {
      nav: nav.items
    }
  },
  computed: {
    name() {
      return this.$route.name
    },
    list() {
      return this.$route.matched
    }
  }
}
</script>
