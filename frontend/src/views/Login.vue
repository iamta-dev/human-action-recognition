<template>
  <v-sheet id="scrolling-techniques-7" class="overflow-y-auto" max-height="875">
    <!-- background-color: red; -->
    <v-container style="margin-top: 64px; height: 811px">
      <div
        class="login d-flex justify-center align-center"
        style="height: 100%"
      >
        <v-card style="background-color: #f2f3f4" width="600">
          <v-card-title>
            <span class="display-1 font-weight-light">LOGIN AS TEACHER</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-spacer></v-spacer>
                <v-col cols="8">
                  <v-text-field
                    id="usernameStu1"
                    :rules="[(v) => !!v || 'You didn\'t enter a username .']"
                    v-model="LoginTeacher.username"
                    class="headline font-weight-light"
                    label="Username"
                    required
                  ></v-text-field>
                  <span
                    v-if="LoginTeacher.errorUsername"
                    style="margin: auto; color: red"
                    >You didn't enter a username .</span
                  >
                </v-col>
                <v-spacer></v-spacer>
              </v-row>
              <v-row>
                <v-spacer></v-spacer>
                <v-col cols="8">
                  <v-text-field
                    id="passwordStu1"
                    :rules="[(v) => !!v || 'You didn\'t enter a password .']"
                    v-model="LoginTeacher.password"
                    class="headline font-weight-light"
                    label="Password"
                    type="password"
                    required
                  ></v-text-field>
                  <span
                    v-if="LoginTeacher.errorPassword"
                    style="margin: auto; color: red"
                    >You didn't enter a password .</span
                  >
                </v-col>
                <v-spacer></v-spacer>
              </v-row>
              <v-row>
                <v-spacer></v-spacer>
                <v-btn
                  id="bin-login-stu"
                  class="headline font-weight-light"
                  color="info"
                  width="200"
                  height="40"
                  @click="getLogin"
                  >LOGIN</v-btn
                >
                <v-spacer></v-spacer>
              </v-row>
            </v-container>
            <v-row style="margin: 200">
              <v-spacer></v-spacer>
              <v-btn
                id="showloginAsEmp"
                class="subtitle-2 font-weight-light"
                text
                color="info"
                >Log in as an Student</v-btn
              >
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </v-sheet>
</template>

<script>
import http from "../http-common";
export default {
  name: "Login",
  data() {
    return {
      LoginTeacher: {
        errorUsername: false,
        errorpassword: false,
        username: "",
        password: "",
      },
    };
  },
  methods: {
    /* eslint-disable no-console */
    getLogin() {
      if (
        this.LoginTeacher.username != "" &&
        this.LoginTeacher.password != ""
      ) {
        http
          .get("/teracher/")
          .then((response) => {
            console.log(response.data);
            if (
              response.data[0].username == this.LoginTeacher.username &&
              response.data[0].password == this.LoginTeacher.password
            ) {
              this.$session.start();
              this.$session.set("userName", response.data[0].name);
              this.$router.push("/Profile");
            }
          })
          .catch((e) => {
            console.log(e);
          });
      }
    },
  },
  mounted() {
    // this.getClassRoom();
  },
};
</script>
