<template>
  <div>
    <reactive-bar-chart :chart-data="chartData"></reactive-bar-chart>
  </div>
</template>

<script>
import http from "../http-common";
import ReactiveBarChart from "./ReactiveBarChart2.js";
export default {
  name: "ChartLongAll",
  components: {
    ReactiveBarChart,
  },
  data() {
    return {
      chartData: {
        labels: [
          "reading",
          "writing",
          "raiseHand",
          "sleeping",
          "standing",
          "siting",
        ],
        datasets: [
          {
            label: "ทุกช่วงเวลา",
            backgroundColor: [
              "Red",
              "Blue",
              "Yellow",
              "Green",
              "Purple",
              "Orange",
            ],
            data: [0, 0, 0, 0, 0, 0],
            // data: newArray
          },
        ],
      },
      dateNow: "",
      viewHumanAction: [],
      lastID: 0,
      countData: {
        reading: 0,
        writing: 0,
        raiseHand: 0,
        sleeping: 0,
        standing: 0,
        siting: 0,
      },
    };
  },
  methods: {
    generateData() {
      this.getHumanActionUpdate();
      this.chartData = {
        labels: [
          "reading",
          "writing",
          "raiseHand",
          "sleeping",
          "standing",
          "siting",
        ],
        datasets: [
          {
            label: "ทุกช่วงเวลา",
            backgroundColor: [
              "Red",
              "Blue",
              "Yellow",
              "Green",
              "Purple",
              "Orange",
            ],
            data: [
              this.countData.reading,
              this.countData.writing,
              this.countData.raiseHand,
              this.countData.sleeping,
              this.countData.standing,
              this.countData.siting,
            ],
            // data: newArray
          },
        ],
      };
    },
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
      http
        .get("/human-action/")
        .then((response) => {
          this.viewHumanAction = response.data.reverse();
          this.countDataHumanAction();
          // console.log("GET - HumanAction");
        })
        .catch((e) => {
          console.log(e);
        });
    },
    countDataHumanAction() {
      this.countData.reading = 0;
      this.countData.writing = 0;
      this.countData.raiseHand = 0;
      this.countData.sleeping = 0;
      this.countData.standing = 0;
      this.countData.siting = 0;
      for (let i in this.viewHumanAction) {
        switch (this.viewHumanAction[i].action) {
          case "reading":
            this.countData.reading += 1;
            break;
          case "writing":
            this.countData.writing += 1;
            break;
          case "raiseHand":
            this.countData.raiseHand += 1;
            break;
          case "sleeping":
            this.countData.sleeping += 1;
            break;
          case "standing":
            this.countData.standing += 1;
            break;
          case "siting":
            this.countData.siting += 1;
            break;
        }
      }
    },
  },
  created(){
    setInterval(this.generateData, 4000);
  },
  mounted() {
    this.getHumanActionAll();
  },
};
</script>

