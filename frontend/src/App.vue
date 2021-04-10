<template>
  <div id="app">
    <v-app>
      <v-card class="overflow-hidden">
        <v-app-bar
          absolute
          color="primary lighten-1 white--text"
          elevate-on-scroll
          scroll-target="#scrolling-techniques-7"
        >
          <v-btn icon>
            <v-icon color="white"> fas fa-bars </v-icon>
          </v-btn>

          <v-toolbar-title>HappySchool</v-toolbar-title>

          <v-spacer></v-spacer>

          <div id="nav">
            <router-link to="/">Home</router-link> |
            <router-link to="/DataProcessing">DataProcessing</router-link> |
            <!-- <router-link to="/Video">Video</router-link> | -->
            <router-link to="/Profile">Profile</router-link>
          </div>

          <v-btn icon>
            <v-icon color="white"> fas fa-search </v-icon>
          </v-btn>

          <v-btn icon @click="logOut">
            <v-icon color="white"> fas fa-door-open </v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon color="white"> fas fa-ellipsis-v </v-icon>
          </v-btn>
        </v-app-bar>
        <v-main>
          <router-view />
        </v-main>
      </v-card>

      <!-- footer bar -->
      <v-footer color="primary lighten-1" padless>
        <v-row justify="center" no-gutters>
          <v-btn
            v-for="link in footerLinks"
            :key="link"
            color="white"
            text
            rounded
            class="my-2"
          >
            {{ link }}
          </v-btn>
          <v-col
            class="primary lighten-1 py-4 text-center white--text"
            cols="12"
          >
            <strong>HappySchool, Inc.</strong> &#169;
            {{ new Date().getFullYear() }} - <strong>Privacy</strong>
          </v-col>
        </v-row>
      </v-footer>
    </v-app>
  </div>
</template>


<script>
export default {
  data: () => ({
    footerLinks: ["Home", "About Us", "Team", "Services", "Blog", "Contact Us"],
  }),
  created() {},
  methods: {
    logOut() {
      this.$session.destroy();
      this.$router.push("/");
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #22272c;
    &.router-link-exact-active {
      color: #ffffff;
    }
  }
}
</style>


