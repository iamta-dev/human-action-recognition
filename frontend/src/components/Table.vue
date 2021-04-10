<template>
  <div align="center" justify="center">
    <v-card width="1000">
      <v-card-title>
        <label style="margin-bottom: 30px; margin-left: 20px"
          >Human Action Recognition</label
        >
        <v-spacer></v-spacer>
        <!-- append-icon="fas fa-search" -->
        <v-text-field
          v-model="field_search"
          label="Search by ID"
          solo
          rounded
        ></v-text-field>
        <v-btn
          icon
          style="position: relative; right: 50px; bottom: 15px; margin: 0"
          @click="getHumanActionByID"
        >
          <v-icon id="search_btn_enroll001" size="24px">fas fa-search</v-icon>
        </v-btn>
      </v-card-title>

      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">id</th>
              <th class="text-left">classId</th>
              <th class="text-left">dateTime</th>
              <th class="text-left">face</th>
              <th class="text-left">face_acc</th>
              <th class="text-left">action</th>
              <th class="text-left">action_acc</th>
              <th class="text-left">position</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in viewHumanAction" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.classId }}</td>
              <td>{{ item.dateTime }}</td>
              <td>{{ item.face }}</td>
              <td>{{ item.face_acc }}</td>
              <td>{{ item.action }}</td>
              <td>{{ item.action_acc }}</td>
              <td>{{ item.position }}</td>
            </tr>
            <tr v-if="viewHumanAction.length < 1">
              <td colspan="7" class="text-center">
                <h5>No data found</h5>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          color="rgb(24,103,193)"
          style="margin-right: 20px"
          @click="getHumanActionAll"
          >View all information</v-btn
        >

        <Label
          id="ass001"
          v-if="viewHumanAction.length < 1"
          style="margin-right: 20px"
          >No data found</Label
        >
        <Label
          id="ass002"
          v-if="viewHumanAction.length > 0"
          style="margin-right: 20px"
          >Found information</Label
        >
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import http from "../http-common";
export default {
  name: "Table",
  data() {
    return {
      snackbar: false,
      text: "",
      popup: {
        RowDetail: false,
      },
      view: {
        data: false,
        loading: false,
      },
      field_search: "",
      viewHumanAction: [],
      lastID: 0,
    };
  },
  methods: {
    /* eslint-disable no-console */
    getHumanActionUpdate() {
      http
        .get("/human-action/lastID/")
        .then((response) => {
          if (this.lastID < response.data.id) {
            this.getHumanActionAll();
            this.lastID = response.data.id;
            // console.log("Update HumanAction");
          } else {
            // console.log("NOT Update HumanAction");
          }
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getHumanActionAll() {
      this.view.data = false;
      this.view.loading = true;

      http
        .get("/human-action/")
        .then((response) => {
          this.viewHumanAction = response.data.reverse();
          // console.log("GET - HumanAction");

          this.view.loading = false;
          this.view.data = true;
        })
        .catch((e) => {
          console.log(e);

          this.view.loading = false;
          this.view.data = true;
        });
    },
    getHumanActionByID() {
      this.view.data = false;
      this.view.loading = true;

      http
        .get("/human-action/" + this.field_search.trim() + "/")
        .then((response) => {
          if (response.data != null) {
            this.viewHumanAction = [response.data];
            console.log(this.viewHumanAction.action);
            console.log("field_search = " + this.field_search);
          }

          // console.log("GET - HumanAction");

          this.view.loading = false;
          this.view.data = true;
        })
        .catch((e) => {
          console.log(e);
          this.viewHumanAction = [];
          this.view.loading = false;
          this.view.data = true;
        });
    },
  },
  created() {
    setInterval(() => this.getHumanActionUpdate(), 4000);
  },
  mounted() {
    this.getHumanActionAll();
  },
};
</script>