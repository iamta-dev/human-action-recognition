<template>
  <v-sheet id="scrolling-techniques-7" class="overflow-y-auto" max-height="875">
    <!-- background-color: red; -->
    <v-container style="margin-top: 64px; height: 1500px">
      <div class="profile" style="margin: 60px">
        <v-row justify="space-around">
          <v-card width="800">
            <v-img height="300px" :src="require('../assets/kws2.jpg')">
              <v-app-bar flat color="rgba(0, 0, 0, 0)">
                <v-avatar size="50">
                  <img alt="user" :src="require('../assets/logo-kws.jpg')" />
                </v-avatar>

                <v-toolbar-title class="title white--text pl-4">
                  KWS SCHOOL
                </v-toolbar-title>

                <v-spacer></v-spacer>

                <v-btn color="white" icon>
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </v-app-bar>

              <v-card-title class="white--text mt-16">
                <v-avatar size="100">
                  <img alt="user" :src="require('../assets/teacher.png')" />
                </v-avatar>
                <h2 class="ml-5">{{ this.$session.get("userName") }}</h2>
              </v-card-title>
            </v-img>

            <v-card-title>
              <h3>{{ classRoom.className }}</h3>
            </v-card-title>
            <v-card-subtitle class="d-flex justify-start">
              <h4>{{ classRoom.classLevel }}</h4>
            </v-card-subtitle>

            <v-list-item>
              <v-icon class="ml-2">fas fa-map-marker-alt</v-icon>
              <p class="ml-5 mt-4">{{ classRoom.roomName }}</p>
            </v-list-item>

            <v-list-item>
              <v-icon class="ml-1">fas fa-clock</v-icon>
              <p class="ml-5 mt-4">
                {{ classRoom.time }}
              </p>
            </v-list-item>

            <v-list-item>
              <v-icon>fas fa-users</v-icon>
              <p class="ml-5 mt-4">
                จำนวนนักเรียน {{ classRoom.numPerson }} คน
              </p>
            </v-list-item>

            <v-list-item>
              <v-icon>fas fa-school</v-icon>
              <p class="ml-5 mt-4">{{ classRoom.school }}</p>
            </v-list-item>

            <v-card-text class="text--primary">
              <div>{{ classRoom.school }}</div>
              <div>Nam Chuet, Kra Buri District, Ranong 85110</div>
            </v-card-text>
          </v-card>
        </v-row>
      </div>
    </v-container>
  </v-sheet>
</template>

<script>
import http from "../http-common";
export default {
  name: "Prefile",
  data() {
    return {
      viewClassRoom: [],
      classRoom: {
        className: "NULL",
        time: "NULL",
        roomName: "NULL",
        numPerson: "NULL",
        classLevel: "NULL",
        school: "NULL",
      },
    };
  },
  methods: {
    /* eslint-disable no-console */
    getClassRoom() {
      http
        .get("/classRoom/")
        .then((response) => {
          this.viewClassRoom = response.data;
          console.log(this.viewClassRoom);
          this.classRoom.className = this.viewClassRoom[0].className;
          this.classRoom.time = this.viewClassRoom[0].time;
          this.classRoom.roomName = this.viewClassRoom[0].roomName;
          this.classRoom.numPerson = this.viewClassRoom[0].numPerson;
          this.classRoom.classLevel = this.viewClassRoom[0].classLevel;
          this.classRoom.school = this.viewClassRoom[0].school;
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  beforeCreate() {
    if (!this.$session.exists()) {
      this.$router.push("/");
    }
  },
  mounted() {
    this.getClassRoom();
  },
};
</script>
